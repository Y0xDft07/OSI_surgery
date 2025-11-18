import subprocess
import socket
from rich.console import Console

console = Console()

def run(target, report):
    console.print("[bold blue]Memulai Layer 3: Jaringan (Network Layer)...[/]")
    report.write("[ Layer 3: Network Layer ]\n")

    try:
        # Resolusi domain → IP
        ip = socket.gethostbyname(target)
        console.print(f"- IP berhasil ditemukan: {ip}")
        report.write(f"- IP berhasil ditemukan: {ip}\n")

        # Traceroute (10 Hop)
        console.print("- Menjalankan traceroute (10 hop pertama)...")
        result = subprocess.run(['traceroute', '-m', '10', target], capture_output=True, text=True)

        console.print("[green]Hasil Traceroute:[/]")
        console.print(result.stdout)
        report.write("- Traceroute (10 hop pertama):\n" + result.stdout + "\n")

        # WHOIS (ASN, Netname, ISP)
        console.print("[cyan]Mengambil informasi WHOIS (ASN/ISP)...[/]")
        whois = subprocess.run(['whois', ip], capture_output=True, text=True)
        asn_lines = [
            line for line in whois.stdout.splitlines()
            if any(keyword in line.lower() for keyword in ['origin', 'netname', 'descr'])
        ]

        for line in asn_lines:
            console.print("  " + line)
            report.write("  " + line + "\n")

        # GeoIP Info dari ipinfo.io
        console.print("[yellow]Mengambil informasi lokasi (GeoIP)...[/]")
        geoip = subprocess.run(['curl', '-s', f'https://ipinfo.io/{ip}'], capture_output=True, text=True)
        console.print(geoip.stdout)
        report.write("- GeoIP Info:\n" + geoip.stdout + "\n")

        # ======================================================
        # 🤖 FITUR ADVANCED SECURITY
        # ======================================================

        # 1. Ping Sweep (cek host aktif/tidak)
        console.print("\n[bold magenta]Melakukan Ping Test (Apakah target hidup?)...[/]")
        ping = subprocess.run(['ping', '-c', '3', ip], capture_output=True, text=True)
        console.print(ping.stdout)
        report.write("\n[ Ping Test ]\n" + ping.stdout + "\n")

        # 2. Deteksi port umum (Top Ports)
        console.print("[bold magenta]Melakukan pemindaian port umum...[/]")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 8080]

        report.write("[ Port Scan ]\n")
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result_port = sock.connect_ex((ip, port))

            if result_port == 0:
                console.print(f"[green]• Port {port} terbuka[/]")
                report.write(f"Port {port} terbuka\n")
            sock.close()

        # 3. Deteksi Firewall
        console.print("[bold magenta]Mendeteksi kemungkinan Firewall...[/]")
        firewall_test = subprocess.run(['nmap', '-sA', ip], capture_output=True, text=True)
        console.print(firewall_test.stdout)
        report.write("\n[ Firewall Detection ]\n" + firewall_test.stdout + "\n")

    except Exception as e:
        error_msg = f"Terjadi kesalahan pada Layer 3: {e}"
        console.print(f"[bold red]{error_msg}[/]")
        report.write(error_msg + "\n")

    console.print("")
    report.write("\n")

