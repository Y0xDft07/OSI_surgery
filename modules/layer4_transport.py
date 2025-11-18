import subprocess
import socket
from rich.console import Console

console = Console()

def run(target, report):
    console.print("[bold blue]Memulai Layer 4: Transport Layer...[/]")
    report.write("[ Layer 4: Transport Layer ]\n")

    try:
        # Resolusi target → IP
        ip = socket.gethostbyname(target)
        console.print(f"- Target berhasil diubah menjadi IP: {ip}")
        report.write(f"- Target berhasil diubah menjadi IP: {ip}\n")

        # ==============================
        # 1. TCP SYN Ping (Port 80)
        # ==============================
        console.print("\n[cyan]Menjalankan TCP SYN Ping pada port 80...[/]")
        result_tcp = subprocess.run(
            ['hping3', '-S', '-p', '80', '-c', '1', ip],
            capture_output=True, text=True
        )
        console.print("[green]Hasil TCP SYN Ping (port 80):[/]")
        console.print(result_tcp.stdout)
        report.write("- TCP SYN Ping (port 80):\n" + result_tcp.stdout + "\n")

        # ==============================
        # 2. UDP Ping (Port 53)
        # ==============================
        console.print("\n[cyan]Menjalankan UDP Ping pada port 53...[/]")
        result_udp = subprocess.run(
            ['hping3', '--udp', '-p', '53', '-c', '1', ip],
            capture_output=True, text=True
        )
        console.print("[green]Hasil UDP Ping (port 53):[/]")
        console.print(result_udp.stdout)
        report.write("- UDP Ping (port 53):\n" + result_udp.stdout + "\n")

        # ====================================================
        # 🔥 FITUR ADVANCED SECURITY UNTUK LAYER 4
        # ====================================================

        # 3. Port Scan (Fast)
        console.print("\n[bold magenta]Melakukan pemindaian port cepat (Fast Scan)...[/]")
        report.write("[ Fast Port Scan ]\n")

        common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 8080]
        for port in common_ports:
            scan = subprocess.run(
                ['hping3', '-S', '-p', str(port), '-c', '1', ip],
                capture_output=True, text=True
            )

            if "flags=SA" in scan.stdout:
                console.print(f"[green]• Port {port} terbuka[/]")
                report.write(f"Port {port} terbuka\n")
            else:
                console.print(f"[red]• Port {port} tertutup / difilter[/]")
                report.write(f"Port {port} tertutup / difilter\n")

        # 4. Stealth Scan (FIN Scan)
        console.print("\n[bold magenta]Melakukan Stealth Scan (FIN Scan)...[/]")
        fin_scan = subprocess.run(
            ['hping3', '-F', '-p', '80', '-c', '1', ip],
            capture_output=True, text=True
        )
        console.print(fin_scan.stdout)
        report.write("[ FIN Scan ]\n" + fin_scan.stdout + "\n")

        # 5. XMAS Scan
        console.print("\n[bold magenta]Melakukan XMAS Scan (Stealth mode)...[/]")
        xmas_scan = subprocess.run(
            ['hping3', '-F', '-P', '-U', '-p', '80', '-c', '1', ip],
            capture_output=True, text=True
        )
        console.print(xmas_scan.stdout)
        report.write("[ XMAS Scan ]\n" + xmas_scan.stdout + "\n")

        # 6. Deteksi Firewall (Drop/Reject)
        console.print("\n[bold magenta]Mendeteksi keberadaan firewall...[/]")
        fw_test = subprocess.run(
            ['hping3', '-S', '-p', '80', '--flood', '-c', '3', ip],
            capture_output=True, text=True
        )
        console.print(fw_test.stdout)
        report.write("[ Firewall Detection ]\n" + fw_test.stdout + "\n")

        # 7. RTT (Latency) Measurement
        console.print("\n[bold magenta]Mengukur waktu respon (RTT/Latency)...[/]")
        rtt = subprocess.run(
            ['hping3', '-S', '-p', '80', '-c', '5', ip],
            capture_output=True, text=True
        )
        console.print(rtt.stdout)
        report.write("[ RTT Measurement ]\n" + rtt.stdout + "\n")

    except Exception as e:
        error_msg = f"Kesalahan pada Layer 4: {e}"
        console.print(f"[bold red]{error_msg}[/]")
        report.write(error_msg + "\n")

    console.print("")
    report.write("\n")
