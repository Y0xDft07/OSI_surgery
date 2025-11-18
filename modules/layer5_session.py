import subprocess
import requests
from rich.console import Console

console = Console()

def run(target, report):
    console.print("[bold blue]Memulai Layer 5: Session Layer...[/]")
    report.write("[ Layer 5: Session Layer ]\n")

    try:
        # ========================================================
        # 1. NMAP TOP 1000 PORTS (Session Establishment Check)
        # ========================================================
        console.print("[cyan]- Menjalankan pemindaian Nmap (Top 1000 Ports)...[/]")
        result = subprocess.run(
            ['nmap', '-Pn', '--top-ports', '1000', target],
            capture_output=True, text=True
        )
        console.print("[green]Hasil pemindaian Nmap:[/]")
        console.print(result.stdout)
        report.write("- Nmap Top 1000 Ports:\n" + result.stdout + "\n")

        # ========================================================
        # 2. SESSION COOKIE ENUMERATION
        # ========================================================
        console.print("\n[cyan]- Mengambil cookie sesi dari target...[/]")
        url = f"http://{target}" if not target.startswith("http") else target
        
        try:
            r = requests.get(url, timeout=6)
            cookies = r.cookies

            if cookies:
                console.print("[green]Cookie sesi ditemukan:[/]")
                for cookie in cookies:
                    line = f"- Cookie sesi: {cookie.name} = {cookie.value}"
                    console.print(line)
                    report.write(line + "\n")
            else:
                console.print("[yellow]- Tidak ada cookie sesi ditemukan.")
                report.write("- Tidak ada cookie sesi ditemukan.\n")

        except Exception as e:
            console.print(f"[red]- Gagal mengambil cookie sesi: {e}")
            report.write(f"- Gagal mengambil cookie sesi: {e}\n")

        # ========================================================
        # 🔥 FITUR ADVANCED SECURITY
        # ========================================================

        console.print("\n[bold magenta]Menjalankan fitur keamanan lanjutan Layer 5...[/]")

        # --------------------------------------------------------
        # 3. SECURITY FLAG CHECK (HttpOnly / Secure / SameSite)
        # --------------------------------------------------------
        report.write("\n[ Session Cookie Security Flags ]\n")
        console.print("[cyan]Memeriksa atribut keamanan cookie...[/]")

        for cookie in cookies:
            secure_flag = "Secure" if cookie.secure else "Tidak Secure"
            http_only = "HttpOnly" if "httponly" in cookie._rest.keys() else "Tidak HttpOnly"
            same_site  = cookie._rest.get("samesite", "Tidak Ada")

            msg = (
                f"- {cookie.name}: Secure({secure_flag}), "
                f"HttpOnly({http_only}), SameSite({same_site})"
            )
            
            console.print(msg)
            report.write(msg + "\n")

        # --------------------------------------------------------
        # 4. SESSION FIXATION TEST
        # --------------------------------------------------------
        console.print("\n[cyan]Mengujicoba Session Fixation Attack...[/]")
        report.write("\n[ Session Fixation Test ]\n")

        fake_session = {"sessionid": "ATTACKER_FAKE_SESSION_12345"}

        fixation_test = requests.get(url, cookies=fake_session, timeout=6)

        if "ATTACKER_FAKE_SESSION_12345" in str(fixation_test.cookies):
            console.print("[red]‼ POTENSI Session Fixation: Target menerima session ID palsu[/]")
            report.write("POTENSI Session Fixation: Server menerima session ID palsu\n")
        else:
            console.print("[green]✓ Target MENOLAK session ID palsu (aman)[/]")
            report.write("Target menolak session ID palsu (aman)\n")

        # --------------------------------------------------------
        # 5. SESSION BRUTE-FORCE PROTECTION CHECK
        # --------------------------------------------------------
        console.print("\n[cyan]Mengujicoba respon brute-force session...[/]")
        report.write("\n[ Session Brute Force Detection ]\n")

        for i in range(3):
            test_cookie = {"sessionid": f"TESTSESSION_{i}"}
            brute_test = requests.get(url, cookies=test_cookie, timeout=6)
            
            report.write(f"Percobaan ke-{i}: Status {brute_test.status_code}\n")

        console.print("[green]✓ Pengujian brute-force sesi selesai.[/]")
        
    except Exception as e:
        error_msg = f"Kesalahan pada Layer 5: {e}"
        console.print(f"[bold red]{error_msg}[/]")
        report.write(error_msg + "\n")

    console.print("")
    report.write("\n")
