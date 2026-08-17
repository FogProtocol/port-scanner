import socket
import concurrent.futures
import time

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt"
}

class PortScanner:
    def __init__(self, target, timeout=1.0, threads=100):
        self.target = target
        self.timeout = timeout
        self.threads = threads
        self.target_ip = self._resolve_target(target)

    def _resolve_target(self, target):
        """Resolves hostname to IPv4 address."""
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            return None

    def grab_banner(self, ip, port):
        """Attempts to grab service identification banner from an open port."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((ip, port))
            
            # Send HTTP HEAD request for web ports, or simple probe for others
            if port in [80, 8080]:
                s.send(b"HEAD / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
            elif port in [443, 8443]:
                s.send(b"\r\n")
            else:
                s.send(b"Help\r\n")

            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            s.close()
            # Clean single-line snippet of banner
            first_line = banner.split('\n')[0] if banner else "No banner returned"
            return first_line[:80]
        except Exception:
            return "No response / Sealed banner"

    def scan_port(self, port):
        """Performs TCP 3-Way Handshake connect attempt on a single port."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            result = s.connect_ex((self.target_ip, port))
            s.close()

            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown Service")
                banner = self.grab_banner(self.target_ip, port)
                return {
                    "port": port,
                    "state": "OPEN",
                    "service": service,
                    "banner": banner
                }
        except Exception:
            pass
        return None

    def run_scan(self, start_port=1, end_port=1024):
        """Executes multithreaded port scan across given range."""
        if not self.target_ip:
            return {"error": f"Could not resolve host '{self.target}'"}

        print(f"[*] Starting scan on {self.target} ({self.target_ip})")
        print(f"[*] Port Range: {start_port} - {end_port} | Threads: {self.threads} | Timeout: {self.timeout}s\n")

        open_ports = []
        start_time = time.time()

        ports_to_scan = range(start_port, end_port + 1)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            results = executor.map(self.scan_port, ports_to_scan)
            for res in results:
                if res:
                    open_ports.append(res)
                    print(f"  [+] Port {res['port']:<5}/TCP | State: {res['state']} | Service: {res['service']:<12} | Banner: {res['banner']}")

        elapsed = round(time.time() - start_time, 2)
        return {
            "target": self.target,
            "ip": self.target_ip,
            "scan_duration_sec": elapsed,
            "total_open_ports": len(open_ports),
            "open_ports": open_ports
        }
