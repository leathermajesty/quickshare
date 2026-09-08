# 🚀 QuickShare

QuickShare is a lightweight Python utility that lets you quickly share a **single file** from your **host machine** to a **virtual machine** or **Android device** over your local network.

It was built while solving **Hack The Box (HTB)**, **TryHackMe (THM)**, and **CTF** labs where transferring files from the host machine to the VM is a repetitive task.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/leathermajesty/quickshare.git
cd quickshare
```

That's it. No virtual environment or dependencies needed for basic usage.

**Optional:** Install `qrcode` to enable QR code generation for mobile downloads:

```bash
pip3 install qrcode
```

---

### Usage

Since QuickShare is fully cross-platform, you can run the exact same command on both macOS and Windows:

```bash
python3 src/quickshare.py
```

### Windows Users
If `python3` isn't recognized on your Windows machine, try using `python` instead:
```cmd
python src\quickshare.py
```

Select the file or directory you want to share. QuickShare will create a temporary HTTP server and generate a download command. 
If you choose a directory, it will automatically zip it before sharing!

---

## Demo

https://github.com/user-attachments/assets/85bd655c-8d34-49c4-a642-2c7b551f0284

---

## Why I Built This

During HTB and THM labs, I frequently needed to transfer files such as VPN configurations, enumeration scripts, payloads, and other tools to my VM.

My usual workflow was:

1. Start a Python HTTP server.
2. Find my local IP address.
3. Copy the IP.
4. Switch to the VM.
5. Type the download command.
6. Download the file.

Although the process only takes a minute, repeating it multiple times during every lab quickly becomes annoying.

**QuickShare** automates those repetitive steps so you can focus on solving the machine instead of setting up file transfers.

---

## Features

* 📂 Lists all files in the current directory
* 🔢 Select a file by number
* 📦 Shares only the selected file (served from a temporary directory for security)
* 🌐 Automatically detects local IPv4 address
* 📋 Generates a ready-to-use `wget` command
* 📋 Auto-copies the command to clipboard (macOS)
* 📱 Generates a QR code for easy mobile downloads *(optional, requires `qrcode`)*
* ⬇️ Automatically stops after the first successful download
* 🧹 Cleans up temporary files automatically
* 🐍 Zero dependencies for core functionality (Python standard library only)

---

## Requirements

* Python 3.8 or later
* [qrcode](https://pypi.org/project/qrcode/) *(optional — enables QR code display for mobile downloads)*

Supported platforms:

* ✅ macOS
* ✅ Windows

---

## Project Structure

```
quickshare/
├── src/
│   ├── macos.py          # macOS script
│   └── windows.py        # Windows script
├── assets/               # Demo videos and GIFs
├── .gitignore
├── requirements.txt      # Optional dependencies
└── README.md
```

---

## Example

```text
$ python3 src/quickshare.py

╭──────────────────────────────────────────╮
│                 QuickShare               │
│          Fast LAN File Sharing           │
╰──────────────────────────────────────────╯

Available Files & Directories
────────────────────────────────────────────
  [1] FILE requirements.txt               12.0 B
  [2] FILE README.md                      5.4 KB
  [3] DIR  assets                         10.2 KB
  [4] DIR  src                            21.1 KB
────────────────────────────────────────────

Select item: 4

✓ Ready to share

  Type      : Directory (ZIP)
  Name      : src.zip
  Size      : 6.0 KB
  IP        : 192.168.1.12
  Port      : 1234
  Share ID  : 4

VM / Linux
────────────────────────────────────────────
  wget http://192.168.1.12:1234/4
  ✓ Command copied to clipboard
```

On your VM, simply paste the copied command and press **Enter**:

```bash
wget http://192.168.1.12:1234/4
```

Thanks to the server's HTTP headers, `wget` will automatically save the file as `src.zip`!

> **Note:** If `qrcode` is not installed, the QR code section is skipped and you'll see a hint to install it.

---

## Typical Use Cases

* Hack The Box
* TryHackMe
* Capture The Flag (CTFs)
* Sharing VPN configuration files
* Transferring payloads and enumeration scripts
* Moving tools between host machines and Linux VMs
* Sharing files to Android devices on the same network

---

## License

This project is licensed under the MIT License.

---

If QuickShare makes your HTB or THM workflow a little faster, consider giving the repository a ⭐.