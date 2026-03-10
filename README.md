
# Porthole

## 🚀 Features & Requirements
I’ve implemented all the core requirements for this assignment, plus some extra polish:

* **Smart Scanning:** To keep things fast, the script only scans ports on hosts that respond to a ping (UP hosts).
* **Flexible Port Input:** You can use `-p` for a single port (`80`), a range (`1-100`), or a specific list (`22,80,443`).
* **Error Handling:** I added a 0.8s timeout. This means if a port is "filtered" or a host is slow, the script won't hang forever.
* **✨ Extra Credit:** I added a service lookup feature! Instead of just seeing "Port 80," you'll see "Port 80 (OPEN - HTTP)."

---

## 🛠 How it Works (The Technical Stuff)
Under the hood, Porthole uses a **TCP Three-Way Handshake** logic to check for open ports. 



I chose to use `socket.connect_ex()` because it returns an error code (0 for success) instead of throwing a full exception. This makes the code much cleaner and more "human-readable."

---

## 💻 How to Run It
First, make sure you are in the project directory:
```bash
cd path/to/Porthole