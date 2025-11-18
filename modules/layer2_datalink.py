import socket
import subprocess
import requests

def run(target, report):
    print("\n\033[1;36m─── Layer 2: Data Link ───\033[0m")

    try:
        # Resolusi domain → IP
        print(f"[+] Mengonversi domain/IP target: {target} ...")
        target_ip = socket.gethostbyname(target)
        print(f"[✓] IP Target: {target_ip}")

        # ARP Scan pada target
        print(f"[+] Melakukan ARP scan pada {target_ip} (hanya bekerja dalam LAN)...")
        try:
            arp_result = subprocess.check_output(
                ["arp", "-n", target_ip],
                stderr=subprocess.DEVNULL
            ).decode()

            mac_address = "--"
            if target_ip in arp_result:
                mac_line = [l for l in arp_result.splitlines() if target_ip in l][0]
                mac_address = mac_line.split()[2]
                print(f"[✓] Alamat MAC ditemukan: {mac_address}")
            else:
                print("[!] Alamat MAC tidak ditemukan — target bukan satu jaringan LAN")
        except subprocess.CalledProcessError:
            mac_address = "--"
            print("[!] Perintah ARP gagal atau target tidak merespons")

        # Query ipinfo / Geo / ASN
        print(f"[+] Mengambil informasi ASN/Geo dari {target_ip} ...")
        asn, loc, hostname = "N/A", "N/A", "N/A"
        try:
            response = requests.get(
                f"https://https://ipinfo.io/{target_ip}/json",
                timeout=6
            )

            if response.ok:
                data = response.json()

                asn = data.get("org", "N/A")
                loc = f"{data.get('city','')}, {data.get('region','')}, {data.get('country','')}".strip(", ")
                hostname = data.get("hostname", "N/A")

                print(f"\n- ASN / Organisasi: {asn}")
                print(f"- Lokasi: {loc}")
                print(f"- Vendor MAC (perkiraan): {hostname}")

            else:
                print("[!] Gagal mendapatkan data dari layanan IP info.")
        except Exception as e:
            print(f"[!] Permintaan data IP info gagal: {e}")

        # --------------------------------------------
        # 🔥 ADVANCED LAYER 2 SECURITY SCAN
        # --------------------------------------------
        print("\n\033[1;35m[+] Menjalankan Advanced Security Scan (Layer 2)...\033[0m")
        report.write("\n--- Advanced Layer 2 Security Scan ---\n")

        # 1. ARP Scan seluruh LAN (jika user root)
        try:
            print("[+] Melakukan ARP Sweep seluruh LAN...")
            arp_sweep = subprocess.check_output(
                ["arp-scan", "--localnet"],
                stderr=subprocess.DEVNULL
            ).decode()

            print("[✓] ARP Sweep selesai — perangkat ditemukan:")
            print(arp_sweep)

            report.write("\n[ARP Sweep]\n")
            report.write(arp_sweep + "\n")

        except:
            print("[!] arp-scan tidak tersedia atau butuh sudo")
            report.write("[!] arp-scan tidak tersedia atau butuh sudo\n")

        # 2. Deteksi MAC spoofing umum
        spoof_risks = []

        if mac_address != "--":
            if mac_address.startswith(("00:00:00", "11:11:11", "22:22:22")):
                spoof_risks.append("Pola MAC mencurigakan — kemungkinan spoofing.")
            if mac_address[0:2].lower() in ["02"]:  # Locally administered bit
                spoof_risks.append("Alamat MAC menggunakan LAA — mungkin virtual/spoofed.")

        # 3. Deteksi Konflik IP (IP digunakan lebih dari 1 perangkat)
        print("[+] Mengecek kemungkinan konflik IP...")
        try:
            conflict = subprocess.check_output(
                ["arp", "-a"],
                stderr=subprocess.DEVNULL
            ).decode()

            hits = [l for l in conflict.splitlines() if target_ip in l]

            if len(hits) > 1:
                spoof_risks.append("Terdeteksi lebih dari satu MAC untuk IP ini — kemungkinan IP conflict atau ARP spoofing.")

        except:
            pass

        # Print hasil analisis risiko
        print("\n\033[1;33mAnalisis Risiko Layer 2:\033[0m")
        report.write("\n[Analisis Risiko Layer 2]\n")

        if spoof_risks:
            for r in spoof_risks:
                print(f"  • {r}")
                report.write("  • " + r + "\n")
        else:
            print("  • Tidak ada indikasi serangan Layer 2.")
            report.write("  • Tidak ada indikasi serangan Layer 2.\n")

        # Tulis semua hasil utama ke laporan
        report.write("\n--- Layer 2: Data Link ---\n")
        report.write(f"Target IP: {target_ip}\n")
        report.write(f"MAC Address: {mac_address}\n")
        report.write(f"ASN: {asn}\n")
        report.write(f"Lokasi: {loc}\n")
        report.write(f"MAC Vendor (perkiraan): {hostname}\n")

    except socket.gaierror:
        print(f"[!] Tidak dapat mengonversi domain: {target}")
        report.write(f"[!] Tidak dapat mengonversi domain: {target}\n")
    except Exception as e:
        print(f"[!] Kesalahan pada pemindaian Layer 2: {e}")
        report.write(f"[!] Kesalahan pada pemindaian Layer 2: {e}\n")
