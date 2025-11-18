#!/usr/bin/env python3

import os
from rich import print
from rich.console import Console
from modules import (
    layer1_physical,
    layer2_datalink,
    layer3_network,
    layer4_transport,
    layer5_session,
    layer6_presentation,
    layer7_application
)

console = Console()

def print_banner():
    banner = r"""[bold blue]
       ____   _____ _____                                       
  / __ \ / ____|_   _|                                      
 | |  | | (___   | |    ___ _   _ _ __ __ _  ___ _ __ _   _ 
 | |  | |\___ \  | |   / __| | | | '__/ _` |/ _ \ '__| | | |
 | |__| |____) |_| |_  \__ \ |_| | | | (_| |  __/ |  | |_| |
  \____/|_____/|_____| |___/\__,_|_|  \__, |\___|_|   \__, |
                   ______              __/ |           __/ |
                  |______|            |___/           |___/ 
     [/]"""
    console.print(banner)

def main():
    print_banner()
    target = input("[bold green]Masukkan IP atau domain target:[/] ").strip()

    if not target:
        console.print("[bold red]Tidak ada target yang dimasukkan. Program dihentikan.[/]")
        return

    filename_safe_target = target.replace("https://", "").replace("http://", "").replace("/", "_")
    output_path = f"reports/{filename_safe_target}.txt"
    os.makedirs("reports", exist_ok=True)

    with open(output_path, 'w') as report:
        header = f"\n[+] Laporan OSI Breakdown untuk: {target}\n\n"
        report.write(header)
        console.print(f"\n[bold cyan]Memulai pemindaian OSI Layer pada:[/] {target}\n")

        console.print("[bold yellow]Layer 7: Aplikasi[/]")
        layer7_application.run(target, report)

        console.print("[bold yellow]Layer 6: Presentasi[/]")
        layer6_presentation.run(target, report)

        console.print("[bold yellow]Layer 5: Sesi[/]")
        layer5_session.run(target, report)

        console.print("[bold yellow]Layer 4: Transport[/]")
        layer4_transport.run(target, report)

        console.print("[bold yellow]Layer 3: Jaringan (Network)[/]")
        layer3_network.run(target, report)

        console.print("[bold yellow]Layer 2: Data Link[/]")
        layer2_datalink.run(target, report)

        console.print("[bold yellow]Layer 1: Fisik (Physical)[/]")
        layer1_physical.run(target, report)

    console.print(f"\n[bold green]✔ Selesai.[/]")
    console.print(f"[bold cyan]Laporan disimpan di:[/] {output_path}")

if __name__ == "__main__":
    main()
