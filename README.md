# 🔍 TraceLink – Cross-Platform Digital Forensics Toolkit

**TraceLink** is a powerful digital forensics tool designed to analyze and extract key forensic data from multiple platforms, including **Android devices** and **Linux-based systems**. It provides a unified interface for managing forensic cases and viewing data retrieved from connected devices.

---

## 🚀 Features

### ✅ Android Forensics (via Android App)
- Extracts:
  - 📞 Call Logs
  - 💬 SMS History
  - 📱 Installed Applications
- Developed in **Android Studio**
- Sends data securely to backend server

### 🐧 Linux Forensics
- Collects:
  - 🖥 OS Version (`uname -a`)
  - 📜 Kernel Logs (`dmesg`)
  - 📦 Installed Apps (`apt list --installed`)
  - 👤 Last Logins (`last`)
  - 🌐 Network Connections (`netstat -tulnp`)
  - 📡 IP Configuration (`ifconfig`)
  - 🛣 Routing Table (`ip route`)
  - 💽 Partition Info (`lsblk`)

### 📁 Case Management
- Create investigation **cases**
- Add multiple devices (Android/Linux) to a case
- View device-specific forensic data in a clean UI

---

## 🧱 Tech Stack

| Layer     | Technology           |
|-----------|----------------------|
| Frontend  | React.js             |
| Backend   | Python + Flask       |
| Database  | SQLite               |
| Android   | Java/Kotlin (Android Studio) |
| Communication | REST API        |

---