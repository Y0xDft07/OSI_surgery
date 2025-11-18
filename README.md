# OSI_surgery

### *contoh alat memindai jaringan lapisan OSI (Layer 1 hingga 7) sederhana** dari sebuah IP atau domain.

Setiap layer menjalankan modul rekonsis yang berbeda, dan hasilnya:

* Ditampilkan **langsung di terminal**, dan
* Disimpan ke dalam file laporan dengan timestamp di folder `/reports/`.

---

## Instalasi

```bash
# Clone repository
git clone https://github.com/YourUsername/OSI_surgery.git
cd OSI_surgery

## Cara Installasi dan Penggunaan

# Mode interaktif
python3 setup.py

# Untuk analisis Layer 2 (ARP/MAC) lebih dalam, gunakan root
sudo python3 osisurgery.py
```

---

## Struktur Project

```
OSI_surgery/
├── setup.py
├── osisurgery.py
├── modules/
│   ├── layer1_physical.py 
│   ├── layer2_datalink.py 
│   ├── layer3_network.py
│   ├── layer4_transport.py
│   ├── layer5_session.py
│   ├── layer6_presentation.py
│   └── layer7_application.py
└── reports/
    └── <report_timestamp>.txt
```

---

## Penjelasan Setiap Layer

### **Layer 7 — Application**

**File:** `modules/layer7_application.py`

**1. Pemeriksaan Header Keamanan Deteksi.**

* CSP
* HSTS
* XSS Protection
* Clickjacking protection
* Permissions Policy
* Referrer Policy

**2. Deteksi Input XSS.**

Mendata semua `<input>` untuk kemungkinan serangan XSS.

**3. Deteksi Teknologi Server Mengambil.**

* Server (Apache, Nginx, LiteSpeed, dll)
* X-Powered-By (PHP, ExpressJS, ASP.NET, dll)

**4. Sensitive File Checker.**

Mengecek apakah file sensitif dapat diakses:
* `.env`
* `phpinfo.php`
* `backup.zip`
* `.git/`
* `config.php`

**5. Favicon Hashing (WAF / CMS Fingerprint).**

Untuk identifikasi teknologi lewat hash MD5 favicon.

---

### **Layer 6 — Presentation**

**File:** `modules/layer6_presentation.py

**1. Deteksi TLS Lemah.**

* TLS 1.0, TLS 1.1 → tidak aman.

**2. Deteksi Cipher Lemah.**

* RC4
* 3DES
* NULL cipher
* Export-grade
* MD5-based

**3. Cek Sertifikat Kadaluarsa.**

Menampilkan apakah masih valid atau sudah expired.

**4. Validasi HSTS.**

Mengecek apakah server menggunakan **Strict-Transport-Security** (anti downgrade attack).

**5. Deteksi Self-Signed Certificate.**

Menentukan apakah sertifikat dapat dipercaya.

**6. Hostname Mismatch Detection.** 

Proteksi terhadap **MITM attack** dengan sertifikat salah domain.


---

### **Layer 5 — Session**

**File:** `modules/layer5_session.py`

**1. Cookie Security Flag Audit.**

Mengecek apakah cookie sesi:

* Secure
* HttpOnly
* SameSite (Lax / Strict / None)

👉 Penting untuk mencegah **session hijacking**.

**2. Session Fixation Attack Test.**

Mengirim session ID palsu:

* Jika diterima server → **rentan**
* Jika ditolak → **aman**

**3. Session Brute-Force Response Detection.**

Mengirim 3 session ID acak untuk memeriksa:

* Apakah server mudah menerima session random
* Apakah memblokir brute-force
* Apakah status code menunjukkan perlindungan

**4. Cookie Enumeration + Capturing.**

Menampilkan semua cookie sesi: 

* nama
* value
* atribut keamanan.

**5. HTTP Session Health Check.** 

Melihat apakah server:

* Mengelola sesi dengan benar
* Menggunakan cookie untuk autentikasi
* Menggunakan HTTPS untuk transport

---

### **Layer 4 — Transport**

**File:** `modules/layer4_transport.py`

**1. Fast Port Scanner (Hping3 SYN Scan).** 

Memindai port umum menggunakan paket SYN:

* 22 SSH
* 80 HTTP
* 443 HTTPS
* 3306 MySQL
* 8080 Web
* dll.

**2. FIN Scan (Stealth Mode).**

Teknik bypass firewall karena paket FIN sering diabaikan firewall.

**3. XMAS Scan.**

Paket dengan flag FIN, PSH, URG → untuk mendeteksi OS & port terbuka tersembunyi.

**4. Firewall Behavior Detection.**

Mendeteksi apakah firewall melakukan:

* DROP (diam)
* REJECT (balas ICMP)
* RESET (balas RST)

**5. RTT / Latency Measurement.** :
Mengukur delay jaringan berbasis TCP SYN.

---

### **Layer 3 — Network.**

**File:** `modules/layer3_network.py`

### 🚀 **Memetakan routing dan kepemilikan jaringan:**

* "Memulai Layer 3"
* IP berhasil ditemukan
* Resolusi DNS
* `traceroute` untuk peta hop
* WHOIS ASN (origin, netname, descr)
* GeoIP via `ipinfo.io`
* dan lainya

**🔥 A. Ping Test**

Menentukan apakah target hidup atau tidak.

```
ping -c 3 <IP>
```

**🔥 B. Port Scan (Top Port)**

Daftar port umum yang sering diserang:

* 22 SSH
* 80 HTTP
* 443 HTTPS
* 445 SMB
* 3306 MySQL

Port terbuka → potensi celah keamanan.

**🔥 C. Deteksi Firewall**
Menggunakan:

```
nmap -sA <IP>
```

Untuk melihat apakah ada filtering/Drop/Stealth mode.

---

### **Layer 2 — Data Link**

**File:** `modules/layer2_datalink.py`

#### **Mengumpulkan informasi jaringan lokal**:

* Deteksi vendor MAC otomatis
* ARP sweep full LAN (`arp-scan --localnet`)
* Deteksi duplikasi IP (ARP conflict)
* Deteksi spoofing MAC umum
* Indikasi risiko LAN (Medium/High)
* Reverse DNS per-IP (jika ada)

*Butuh `sudo` untuk melihat ARP secara penuh.*

---

### **Layer 1 — Physical**

**File:** `modules/layer1_physical.py`

**Reverse DNS Lookup** : 
Mengetahui hostname asli dari IP
**ASN & Network Organization Lookup** : 
Mengambil informasi AS Number dari IPinfo
**ICMP Latency / Ping Test** : 
Mengukur jarak jaringan & stabilitas
**Risk Notes Smart Detector** : 
Mendeteksi indikasi VPN, server, koneksi seluler

---

## Tips

* Direkomendasikan berjalan di **Kali Linux atau distro Debian-based**.
* Layer 4 & 5 dapat dinonaktifkan di `osisurgery.py` untuk pemindaian cepat.
* Jalankan sebagai **sudo** untuk akurasi Layer 2.
* Setiap pemindaian menghasilkan **report dengan timestamp** di `/reports/`.
* pengembangan lebih lanjut [tips dev](link)
* buku membahas mengenai dasar-dasar jaringan yang telah saya pelajari [](link)

---

## Disclaimer Etika

> Framework ini hanya untuk **riset keamanan yang sah** dan **tujuan edukasi**.
> Gunakan **hanya pada sistem yang Anda miliki atau yang telah memberi izin eksplisit**.
> Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini.


