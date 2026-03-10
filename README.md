# Porthole: Advanced Network Discovery & Port Scanner

## Technical Requirements & Implementation
This script fulfills all requirements for the Porthole assignment, including:
* **Selective Scanning:** Port scanning is only performed on hosts identified as `(UP)`.
* **Flexible Input:** Support for single ports (`-p 80`), ranges (`-p 1-100`), and lists (`-p 80,443`).
* **Robust Networking:** Built using the standard Python `socket` library (TCP) with a 0.8s timeout to handle latency.
* **Extra Credit:** Integrated `socket.getservbyport` to identify service names for all open ports.

---

## Technical Logic
The scanner uses a two-stage discovery process:
1. **ICMP Check:** Pings the target to confirm availability.
2. **TCP Connection:** Attempts a connection to specified ports using `socket.connect_ex()`.



---

## Installation & Setup
1. Ensure Python 3.x is installed.
2. Clone the repository and navigate to the directory:
   ```bash
   cd porthole-assignment
   python3 ip_scanner.py 
