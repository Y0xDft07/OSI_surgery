import subprocess
import socket
from rich.console import Console

console = Console()

def run(target, report):
    console.print("[bold blue]Memulai Layer 1: Lapisan Fisik (Physical Layer)...[/]")
    report.write("[ Layer 1: Lapisan Fisik ]\n")

    try:
        # Resolusi IP target
        ip = socket.gethostbyname(target)

        # Informasi GeoIP / ISP
        geoip = subprocess.run(
            ['curl', '-s', f'https://ipinfo.io/{ip}'],
            capture_output=True,
            text=True
        )

        console.print("[bold green]- Informasi IP / ISP:[/]")
        console.print(geoip.stdout)
        report.write("- Informasi IP / ISP:\n" + geoip.stdout + "\n")

        # Penjelasan sifat Layer 1
        msg = (
            "- Inferensi: Media fisik (Fiber/Coax/Wi-Fi) tidak dapat dilihat langsung dari jarak jauh.\n"
            "- Asumsi: Jenis koneksi fisik bergantung pada ISP (fiber, seluler, kabel)."
        )
        console.print(msg)
        report.write(msg + "\n")

        # -------------------------------
        # 🔥 FITUR ADVANCED SECURITY SCAN
        # -------------------------------

        console.print("\n[bold yellow]Menjalankan Advanced Security Scan (Layer 1+)...[/]")
        report.write("\n[ Advanced Security Scan ]\n")

        # 1. Reverse DNS
        try:
            rev = socket.gethostbyaddr(ip)
            rev_dns = rev[0]
        except:
            rev_dns = "Tidak tersedia"

        console.print(f"- Reverse DNS: {rev_dns}")
        report.write(f"- Reverse DNS: {rev_dns}\n")

        # 2. AS Number / ASN Lookup
        asn_info = subprocess.run(
            ['curl', '-s', f'https://ipinfo.io/{ip}/org'],
            capture_output=True,
            text=True
        )

        console.print("- ASN / Organisasi Jaringan:")
        console.print(asn_info.stdout)
        report.write("- ASN / Organisasi Jaringan:\n" + asn_info.stdout + "\n")

        # 3. ICMP Latency Test (Ping 4x)
        console.print("[bold cyan]- Melakukan tes ping (latensi)...[/]")
        ping_test = subprocess.run(
            ['ping', '-c', '4', ip],
            capture_output=True,
            text=True
        )
        console.print(ping_test.stdout)
        report.write("- Tes Ping:\n" + ping_test.stdout + "\n")

        # 4. Basic Network Security Flags (indikasi risiko)
        risk_notes = []

        if "mobile" in geoip.stdout.lower():
            risk_notes.append("Koneksi seluler terdeteksi: NAT Carrier-grade sering digunakan, dapat mempengaruhi stabilitas.")
        if "vpn" in geoip.stdout.lower():
            risk_notes.append("Indikasi penggunaan VPN: Lokasi fisik tidak akurat.")
        if "hosting" in geoip.stdout.lower() or "data center" in geoip.stdout.lower():
            risk_notes.append("IP terindikasi berasal dari data center — kemungkinan server, bukan pengguna rumah.")

        console.print("[bold magenta]- Analisis Risiko Keamanan Dasar:[/]")
        report.write("- Analisis Risiko Keamanan Dasar:\n")

        if risk_notes:
            for r in risk_notes:
                console.print(f"  • {r}")
                report.write(f"  • {r}\n")
        else:
            console.print("  • Tidak ada indikasi risiko khusus dari IP ini.")
            report.write("  • Tidak ada indikasi risiko khusus dari IP ini.\n")

    except Exception as e:
        error_msg = f"Kesalahan pada Layer 1: {e}"
        console.print(f"[bold red]{error_msg}[/]")
        report.write(error_msg + "\n")

    console.print("")
    report.write("\n")
