import requests
from bs4 import BeautifulSoup
import hashlib
from rich.console import Console

console = Console()

def hash_favicon(url):
    try:
        favicon = requests.get(url + "/favicon.ico", timeout=5)
        return hashlib.md5(favicon.content).hexdigest()
    except:
        return "N/A"

def run(target, report):
    console.print("[bold blue]Starting Layer 7: Application Layer...[/]")
    report.write("[ Layer 7: Application Layer ]\n")

    if not target.startswith("http"):
        target = "http://" + target

    try:
        r = requests.get(target, timeout=8)
        console.print(f"- Status Code: {r.status_code}")
        report.write(f"- Status Code: {r.status_code}\n")

        for key, value in r.headers.items():
            console.print(f"  {key}: {value}")
            report.write(f"  {key}: {value}\n")

        fav_hash = hash_favicon(target)
        console.print(f"- Favicon MD5 Hash: {fav_hash}")
        report.write(f"- Favicon MD5 Hash: {fav_hash}\n")

        soup = BeautifulSoup(r.text, 'html.parser')
        login_forms = soup.find_all('form')
        for form in login_forms:
            if form.find('input', {'type': 'password'}):
                found = f"- Found login form at action: {form.get('action')}"
                console.print(found)
                report.write(found + "\n")

        title = soup.title.string.strip() if soup.title else "No title"
        console.print(f"- Page Title: {title}")
        report.write(f"- Page Title: {title}\n")

    except Exception as e:
        error_msg = f"Error in Layer 7: {e}"
        console.print(f"[bold red]{error_msg}[/]")
        report.write(error_msg + "\n")

    console.print("")
    report.write("\n")


------------------------


import requests
from bs4 import BeautifulSoup
import hashlib
from rich.console import Console

console = Console()

def hash_favicon(url):
    try:
        favicon = requests.get(url + "/favicon.ico", timeout=5)
        return hashlib.md5(favicon.content).hexdigest()
    except:
        return "N/A"

def run(target, report):
    console.print("[bold blue]Memulai Layer 7: Application Layer...[/]")
    report.write("[ Layer 7: Application Layer ]\n")

    if not target.startswith("http"):
        target = "http://" + target

    try:
        # ======================================================
        # 1. HTTP STATUS dan HEADER
        # ======================================================
        console.print(f"[cyan]- Mengirim permintaan HTTP ke {target}...[/]")
        r = requests.get(target, timeout=8)

        console.print(f"[green]- Kode Status HTTP: {r.status_code}")
        report.write(f"- Kode Status HTTP: {r.status_code}\n")

        console.print("[cyan]- Header HTTP ditemukan:[/]")
        for key, value in r.headers.items():
            console.print(f"  {key}: {value}")
            report.write(f"  {key}: {value}\n")

        # ======================================================
        # 2. FAVICON HASHING (Fingerprinting Teknologi)
        # ======================================================
        fav_hash = hash_favicon(target)
        console.print(f"[yellow]- Favicon MD5 Hash: {fav_hash}")
        report.write(f"- Favicon MD5 Hash: {fav_hash}\n")

        # ======================================================
        # 3. MENCARI FORM LOGIN
        # ======================================================
        soup = BeautifulSoup(r.text, 'html.parser')
        login_forms = soup.find_all('form')

        console.print("[cyan]- Memeriksa formulir login...[/]")
        for form in login_forms:
            if form.find('input', {'type': 'password'}):
                found = f"- Form login ditemukan pada action: {form.get('action')}"
                console.print(found)
                report.write(found + "\n")

        # ======================================================
        # 4. JUDUL HALAMAN
        # ======================================================
        title = soup.title.string.strip() if soup.title else "Tidak ada judul"
        console.print(f"[green]- Judul Halaman: {title}")
        report.write(f"- Judul Halaman: {title}\n")

        # ======================================================
        # 🔥 FITUR ADVANCE SECURITY UNTUK LAYER 7
        # ======================================================
        console.print("\n[bold magenta]Menjalankan Fitur Keamanan Lanjutan Layer 7...[/]")

        # ------------------------------------------------------
        # 5. DETEKSI HEADER KEAMANAN
        # ------------------------------------------------------
        console.print("\n[cyan]- Memeriksa header keamanan...[/]")
        report.write("\n[ Security Headers Check ]\n")

        security_headers = {
            "Content-Security-Policy": "CSP melindungi dari XSS.",
            "X-Frame-Options": "Mencegah Clickjacking.",
            "X-XSS-Protection": "Mencegah serangan XSS.",
            "Strict-Transport-Security": "Memaksa HTTPS.",
            "X-Content-Type-Options": "Mencegah MIME sniffing.",
            "Referrer-Policy": "Mengontrol informasi referrer.",
            "Permissions-Policy": "Mengontrol akses API browser."
        }

        for header, desc in security_headers.items():
            if header in r.headers:
                msg = f"[OK] {header} aktif ✔"
                console.print(f"[green]{msg}")
                report.write(msg + "\n")
            else:
                msg = f"[!] {header} TIDAK ditemukan → Rawan"
                console.print(f"[red]{msg}")
                report.write(msg + "\n")

        # ------------------------------------------------------
        # 6. CARI POTENSI INPUT XSS
        # ------------------------------------------------------
        console.print("\n[cyan]- Memeriksa potensi input XSS...[/]")
        report.write("\n[ Possible XSS Inputs ]\n")

        inputs = soup.find_all("input")
        for i in inputs:
            name = i.get("name")
            itype = i.get("type", "text")
            msg = f"- Input ditemukan: name='{name}', type='{itype}'"
            console.print(msg)
            report.write(msg + "\n")

        # ------------------------------------------------------
        # 7. DETEKSI TEKNOLOGI (SERVER, FRAMEWORK, DLL)
        # ------------------------------------------------------
        console.print("\n[cyan]- Deteksi teknologi server...[/]")
        report.write("\n[ Technology Fingerprint ]\n")

        tech = []

        if "Server" in r.headers:
            tech.append(f"Server: {r.headers['Server']}")
        if "X-Powered-By" in r.headers:
            tech.append(f"X-Powered-By: {r.headers['X-Powered-By']}")

        if tech:
            for t in tech:
                console.print(f"[green]- {t}")
                report.write(f"- {t}\n")
        else:
            console.print("[yellow]- Tidak ada fingerprint teknologi ditemukan")
            report.write("Tidak ada fingerprint teknologi ditemukan\n")

        # ------------------------------------------------------
        # 8. CHECK FILE SENSITIVE (.env, backup, config)
        # ------------------------------------------------------
        console.print("\n[cyan]- Memeriksa file sensitif...[/]")
        report.write("\n[ Sensitive Files Check ]\n")

        sensitive_files = [
            "/.env", "/config.php", "/backup.zip", "/admin.php", "/phpinfo.php",
            "/server-status", "/.git/", "/.svn/"
        ]

        for path in sensitive_files:
            try:
                resp = requests.get(target + path, timeout=4)
                if resp.status_code == 200 and len(resp.text) > 5:
                    msg = f"[!] File sensitif ditemukan: {path}"
                    console.print(f"[red]{msg}")
                    report.write(msg + "\n")
            except:
                pass

        console.print("[green]✓ Pemeriksaan keamanan Layer 7 selesai.[/]\n")

    except Exception as e:
        error_msg = f"Kesalahan di Layer 7: {e}"
        console.print(f"[bold red]{error_msg}[/]")
        report.write(error_msg + "\n")

    console.print("")
    report.write("\n")
