import ssl
import socket
from urllib.parse import urlparse
from rich.console import Console

console = Console()

def run(target, report):
    console.print("[bold blue]Memulai Layer 6: Presentation Layer...[/]")
    report.write("[ Layer 6: Presentation Layer ]\n")

    try:
        # Pastikan URL memiliki skema
        if not target.startswith("http"):
            target = "https://" + target

        hostname = urlparse(target).hostname
        context = ssl.create_default_context()

        # ========================================================
        # 1. AMBIL DETAIL TLS DAN SERTIFIKAT
        # ========================================================
        console.print("[cyan]- Mengambil data TLS dan sertifikat SSL...[/]")

        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()

                tls_version = cipher[1]
                cipher_suite = cipher[0]

                console.print(f"- Versi TLS: {tls_version}")
                console.print(f"- Cipher Suite: {cipher_suite}")
                report.write(f"- Versi TLS: {tls_version}\n")
                report.write(f"- Cipher Suite: {cipher_suite}\n")

                console.print(f"- Subjek Sertifikat: {cert['subject']}")
                console.print(f"- Penerbit Sertifikat: {cert['issuer']}")
                console.print(f"- Berlaku Dari: {cert['notBefore']}")
                console.print(f"- Berlaku Hingga: {cert['notAfter']}")
                report.write(f"- Subjek Sertifikat: {cert['subject']}\n")
                report.write(f"- Penerbit Sertifikat: {cert['issuer']}\n")
                report.write(f"- Berlaku Dari: {cert['notBefore']}\n")
                report.write(f"- Berlaku Hingga: {cert['notAfter']}\n")

        # ========================================================
        # 🔥 FITUR ADVANCED SECURITY UNTUK LAYER 6
        # ========================================================

        console.print("\n[bold magenta]Menjalankan pemeriksaan keamanan lanjutan TLS...[/]")

        # --------------------------------------------------------
        # 2. DETEKSI VERSI TLS LEMAH
        # --------------------------------------------------------
        weak_tls = ["TLSv1", "TLSv1.1", "SSLv3", "SSLv2"]

        if tls_version in weak_tls:
            console.print("[red]‼ Peringatan: Versi TLS lemah terdeteksi![/]")
            report.write("‼ Peringatan: Versi TLS lemah terdeteksi!\n")
        else:
            console.print("[green]✓ Versi TLS aman[/]")
            report.write("Versi TLS aman\n")

        # --------------------------------------------------------
        # 3. DETEKSI CIPHER SUITE YANG RENTAN
        # --------------------------------------------------------
        weak_cipher_keywords = ["RC4", "3DES", "EXPORT", "NULL", "MD5"]

        if any(w in cipher_suite.upper() for w in weak_cipher_keywords):
            console.print("[red]‼ Peringatan: Cipher suite lemah terdeteksi![/]")
            report.write("‼ Peringatan: Cipher suite lemah terdeteksi!\n")
        else:
            console.print("[green]✓ Cipher suite aman[/]")
            report.write("Cipher suite aman\n")

        # --------------------------------------------------------
        # 4. CEK APABILA SERTIFIKAT SUDAH KADALUARSA
        # --------------------------------------------------------
        from datetime import datetime

        try:
            exp_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            now = datetime.utcnow()

            if exp_date < now:
                console.print("[red]‼ Sertifikat SSL SUDAH kadaluarsa![/]")
                report.write("‼ Sertifikat SSL SUDAH kadaluarsa!\n")
            else:
                console.print("[green]✓ Sertifikat SSL masih berlaku[/]")
                report.write("Sertifikat SSL masih berlaku\n")
        except Exception:
            console.print("[yellow]⚠ Tidak dapat memvalidasi tanggal sertifikat[/]")
            report.write("⚠ Tidak dapat memvalidasi tanggal sertifikat\n")

        # --------------------------------------------------------
        # 5. VALIDASI HSTS (HTTP Strict Transport Security)
        # --------------------------------------------------------
        import requests
        console.print("[cyan]- Mengecek dukungan HSTS...[/]")

        try:
            r = requests.get(f"https://{hostname}", timeout=5)
            hsts = r.headers.get("Strict-Transport-Security")

            if hsts:
                console.print("[green]✓ HSTS aktif[/]")
                report.write(f"HSTS aktif: {hsts}\n")
            else:
                console.print("[yellow]⚠ HSTS tidak aktif[/]")
                report.write("⚠ HSTS tidak aktif\n")

        except Exception as e:
            console.print(f"[yellow]⚠ Tidak dapat mengecek HSTS: {e}[/]")
            report.write(f"Tidak dapat mengecek HSTS: {e}\n")

        # --------------------------------------------------------
        # 6. CEK SERTIFIKAT SELF-SIGNED
        # --------------------------------------------------------
        issuer = cert.get("issuer")
        subject = cert.get("subject")

        if issuer == subject:
            console.print("[red]‼ Sertifikat SELF-SIGNED (tidak terpercaya)[/]")
            report.write("‼ Sertifikat SELF-SIGNED (tidak terpercaya)\n")
        else:
            console.print("[green]✓ Sertifikat bukan self-signed[/]")
            report.write("Sertifikat bukan self-signed\n")

        # --------------------------------------------------------
        # 7. CEK KESESUAIAN HOSTNAME
        # --------------------------------------------------------
        alt_names = []
        for entry in cert.get('subjectAltName', []):
            alt_names.append(entry[1])

        if hostname not in alt_names:
            console.print("[red]‼ Hostname TIDAK sesuai dengan sertifikat![/]")
            report.write("‼ Hostname TIDAK sesuai dengan sertifikat!\n")
        else:
            console.print("[green]✓ Hostname valid dengan sertifikat[/]")
            report.write("Hostname valid dengan sertifikat\n")

    except Exception as e:
        error_msg = f"Kesalahan pada Layer 6: {e}"
        console.print(f"[bold red]{error_msg}[/]")
        report.write(error_msg + "\n")

    console.print("")
    report.write("\n")

