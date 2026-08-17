# ⚡ Port Scanner & Banner Grabber (Nmap-Lite)

A high-performance multithreaded TCP port scanner and service banner grabber built in Python using low-level socket programming.

---

## 🔍 What is Port Scanning & Banner Grabbing?

Port scanning is a fundamental networking technique used by security auditors and system administrators to discover open doors (ports) on a network host:

- 🚪 **Discover Open Services**: Identifies which ports (HTTP, SSH, FTP, MySQL) are actively accepting connections.
- 📡 **Banner Grabbing**: Probes open ports to extract service software signatures and version headers.
- 🛡️ **Network Auditing**: Detects unauthorized open ports or exposed legacy services.
- ⚡ **Multithreaded Performance**: Scans thousands of ports in seconds using concurrent worker threads.

---

## ⚙️ Scanning & Detection Logic

All probes rely on standard TCP/IP networking fundamentals:

| Check / Feature | Description |
| :--- | :--- |
| **TCP Connect Scan** | Performs full 3-way handshake (`SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`) via Python `socket`. |
| **Banner Grabbing** | Sends targeted HTTP/raw probes to retrieve server version headers on open ports. |
| **Multithreaded Engine** | Parallelized scanning using `concurrent.futures.ThreadPoolExecutor` for high speed. |
| **Service Mapping** | Maps open port numbers to standard protocols (FTP: 21, SSH: 22, HTTP: 80, HTTPS: 443, etc.). |
| **JSON Export** | Saves structured audit results and timestamps to `.json` files. |

---

## 📁 Project Structure

```text
port-scanner/
├── scanner.py       # Core TCP socket scanner & banner grabbing engine
├── main.py          # Interactive CLI menu interface & report exporter
├── .gitignore       # Excludes cache files and JSON audit exports
├── LICENSE          # MIT License
└── README.md        # Documentation file
