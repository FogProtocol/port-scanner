import sys
import json
from scanner import PortScanner, COMMON_PORTS

def print_banner():
    print("\n" + "=" * 65)
    print("        NMAP-LITE PORT SCANNER & BANNER GRABBER TOOL        ")
    print("=" * 65)

def main():
    while True:
        print_banner()
        print("1. Fast Scan Common Ports (Top 14 Services)")
        print("2. Custom Port Range Scan (e.g. 1 - 1024)")
        print("3. Single Target Full Audit (Ports 1 - 65535)")
        print("4. Exit")
        print("-" * 65)

        choice = input("Select an option (1-4): ").strip()

        if choice in ["1", "2", "3"]:
            target = input("\nEnter Target Hostname or IP (e.g., 127.0.0.1 or scanme.nmap.org): ").strip()
            if not target:
                target = "127.0.0.1"

            if choice == "1":
                scanner = PortScanner(target, timeout=1.0, threads=20)
                print(f"\n[*] Scanning common top ports for {target}...")
                open_ports = []
                for p in sorted(COMMON_PORTS.keys()):
                    res = scanner.scan_port(p)
                    if res:
                        open_ports.append(res)
                        print(f"  [+] Port {res['port']:<5}/TCP | Service: {res['service']:<12} | Banner: {res['banner']}")
                
                print(f"\n[+] Scan finished. Found {len(open_ports)} open port(s).")

            elif choice == "2":
                try:
                    start_p = int(input("Enter Start Port (default 1): ") or 1)
                    end_p = int(input("Enter End Port (default 1024): ") or 1024)
                except ValueError:
                    print("[!] Invalid port number.")
                    continue
                
                scanner = PortScanner(target, timeout=1.0, threads=100)
                summary = scanner.run_scan(start_p, end_p)
                
                if summary.get("error"):
                    print(f"[!] Error: {summary['error']}")
                else:
                    print(f"\n[+] Finished in {summary['scan_duration_sec']}s. Found {summary['total_open_ports']} open port(s).")
                    
                    export = input("\nSave scan results to JSON file? (y/N): ").strip().lower()
                    if export == 'y':
                        filename = f"scan_{target.replace('.', '_')}.json"
                        with open(filename, 'w') as f:
                            json.dump(summary, f, indent=4)
                        print(f"[+] Saved results to '{filename}'.")

            elif choice == "3":
                print("\n[!] Full port scan (1-65535) will take longer...")
                scanner = PortScanner(target, timeout=0.8, threads=200)
                summary = scanner.run_scan(1, 65535)
                print(f"\n[+] Finished in {summary['scan_duration_sec']}s. Found {summary['total_open_ports']} open port(s).")

        elif choice == "4":
            print("Exiting Port Scanner. Goodbye!")
            sys.exit(0)

        else:
            print("[!] Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
