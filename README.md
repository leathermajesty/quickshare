# 🚀 QuickShare

QuickShare is a lightweight Python utility that lets you quickly share a **single file** from your **macOS host** to a **virtual machine** over your local network.

It was built to simplify file transfers during Hack The Box (HTB), TryHackMe (THM), and CTF labs. Instead of manually starting an HTTP server and typing download URLs every time, QuickShare automates the process.

---

## Features

* 📂 Lists all files in the current directory
* 🔢 Select a file by number
* 📦 Shares only the selected file
* 🌐 Automatically detects your Mac's local IPv4 address (`en0`)
* 📋 Copies the download command to your clipboard
* ⬇️ Automatically stops after the first successful download
* 🧹 Cleans up temporary files automatically
* 🐍 Uses only Python's standard library (no external dependencies)

---

## Requirements

* macOS
* Python 3.8 or later

No third-party Python packages are required.

---

## Usage

Clone the repository:

```bash
git clone https://github.com/leathermajesty/quickshare.git
cd quickshare
```

Run QuickShare:

```bash
python3 macos.py
```

---

## Example

```text
$ python3 macos.py

Available Files

[1] enterprise.ovpn
[2] linpeas.sh
[3] pspy64

Select file number: 2

Sharing: linpeas.sh

Download command (copied to clipboard):

wget http://192.168.1.12:1234/linpeas.sh

Waiting for one download...
```

Paste the copied command into your VM and press **Enter**.

After the download completes, QuickShare automatically shuts down the server.

---

## Typical Use Cases

* Hack The Box
* TryHackMe
* Capture The Flag (CTFs)
* Sharing VPN configuration files
* Transferring enumeration scripts and payloads
* Moving files from macOS to a Linux VM

---

## Project Structure

```text
quickshare/
├── macos.py
├── README.md
├── FUNCTION.md
└── LICENSE
```

---

## License

This project is licensed under the MIT License.

---

If QuickShare saves you time during your labs, consider giving the repository a ⭐.
