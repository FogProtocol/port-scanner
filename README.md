# ⚡ Nmap-Lite: Multithreaded TCP Port Scanner & Banner Grabber

A lightweight, high-performance Python network scanning tool built using low-level socket programming (`socket`) and multithreading (`concurrent.futures`). Performs TCP 3-Way Handshake connect scans and extracts service banners.

---

## ✨ Features

- **🌐 Hostname & IP Resolution**: Automatically resolves domain names (`scanme.nmap.org`) to IPv4 addresses.
- **🚀 Multithreaded TCP Connect Scanning**: Leverages `ThreadPoolExecutor` for concurrent socket probes across port ranges.
- **📡 Banner Grabbing**: Connects and sends targeted probes to retrieve HTTP server headers and service banners.
- **📊 JSON Exporting**: Save structured audit reports for target hosts.

---

## 🚀 Getting Started

### Running the Tool
```bash
python main.py
