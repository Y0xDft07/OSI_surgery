import os
import platform
import subprocess
import sys
import shutil

# ========== PYTHON PACKAGE INSTALLER ==========
def install_pip_package(package):
    print(f"[+] Installing Python package: {package}")
    subprocess.call([sys.executable, "-m", "pip", "install", package])

# ========== SYSTEM COMMAND RUNNER ==========
def run_cmd(cmd):
    print(f"[+] Executing: {cmd}")
    return subprocess.call(cmd, shell=True)

# ========== LINUX INSTALLER ==========
def install_linux_tools():
    print("\n=== Installing Linux Required Tools ===\n")
    tools = [
        "traceroute",
        "whois",
        "curl",
        "nmap",
        "hping3",
        "openssl",
        "dnsutils",
        "netcat-openbsd",
        "tcpdump",
        "iptables"
    ]

    run_cmd("sudo apt update -y")
    run_cmd("sudo apt upgrade -y")

    for tool in tools:
        run_cmd(f"sudo apt install -y {tool}")

# ========== WINDOWS INSTALLER ==========
def install_windows_tools():
    print("\n=== Installing Windows Required Tools ===\n")

    # Check if Chocolatey exists
    choco = shutil.which("choco")
    if not choco:
        print("[!] Chocolatey not found. Installing Chocolatey...")
        run_cmd('powershell -NoProfile -ExecutionPolicy Bypass -Command '
                "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))")

    tools = [
        "nmap",
        "curl",
        "openssl.light",
        "whois",
    ]

    for tool in tools:
        run_cmd(f"choco install {tool} -y")

    print("[+] For 'hping3' and 'traceroute', please install WSL (Linux subsystem).")

# ========== PYTHON DEPENDENCIES ==========
def install_python_requirements():
    print("\n=== Installing Python Packages ===\n")
    requirements = [
        "rich",
        "requests",
        "dnspython",
        "pyOpenSSL",
        "cryptography",
        "python-nmap",
        "shodan"
    ]
    for pkg in requirements:
        install_pip_package(pkg)

# ========== MAIN ==========
def main():
    print("\n=====================================")
    print("   SETUP ENVIRONMENT TOOL   ")
    print("=====================================\n")

    os_type = platform.system()

    # Install Python requirements
    install_python_requirements()

    # OS-specific tool installation
    if os_type == "Linux":
        print("[+] OS Detected: Linux")
        install_linux_tools()

    elif os_type == "Windows":
        print("[+] OS Detected: Windows")
        install_windows_tools()

    else:
        print("[!] Unsupported OS:", os_type)
        print("    Supported: Linux & Windows only.")
        sys.exit(1)

    print("\n=====================================")
    print("    SETUP COMPLETE — SIAP DIGUNAKAN  ")
    print("=====================================\n")

if __name__ == "__main__":
    main()
