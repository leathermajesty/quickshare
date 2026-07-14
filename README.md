# 🚀 QuickShare

QuickShare is a lightweight Python utility that lets you quickly share a **single file** from your **macOS host** to a **virtual machine** over your local network.

It was built while solving **Hack The Box (HTB)**, **TryHackMe (THM)**, and **CTF** labs where transferring files from the host machine to the VM is a repetitive task.

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
* 📦 Shares only the selected file
* 🌐 Automatically detects your Mac's local IPv4 address (`en0`)
* 📋 Copies the ready-to-use `wget` command to your clipboard
* ⬇️ Automatically stops after the first successful download
* 🧹 Cleans up temporary files automatically
* 🐍 Built using only Python's standard library (no external dependencies)

---

## Requirements

* macOS
* Python 3.8 or later

No third-party Python packages are required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/leathermajesty/quickshare.git
cd quickshare
```

---

## Usage

Run the script:

```bash
python3 macos.py
```

Select the file you want to share, then switch to your VM and paste the copied command.

---

## Demo

https://github.com/user-attachments/assets/85bd655c-8d34-49c4-a642-2c7b551f0284

---

## Example

```text
$ python3 macos.py

Available Files:

[1] macos.py
[2] .DS_Store
[3] README.md

Select file number: 1

Sharing: macos.py

Download command (also copied to clipboard):

wget http://12.10.10.47:1234/macos.py

Waiting for one download...
```

On your VM, simply paste the copied command and press **Enter**:

```bash
wget http://12.10.10.47:1234/macos.py
```

Once the download is complete, QuickShare automatically stops the HTTP server and removes the temporary directory.
---

## Typical Use Cases

* Hack The Box
* TryHackMe
* Capture The Flag (CTFs)
* Sharing VPN configuration files
* Transferring payloads and enumeration scripts
* Moving tools from macOS to a Linux VM

---

## License

This project is licensed under the MIT License.

---

If QuickShare makes your HTB or THM workflow a little faster, consider giving the repository a ⭐.
