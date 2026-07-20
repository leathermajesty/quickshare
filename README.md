# 🚀 QuickShare

QuickShare is a lightweight Python utility that lets you quickly share a **single file** from your **host machine** to a **virtual machine** over your local network.

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
* 🌐 Automatically detects local IPv4 address
* 📋 Generates a ready-to-use `wget` command
* ⬇️ Automatically stops after the first successful download
* 🧹 Cleans up temporary files automatically
* 🐍 Built using only Python's standard library (no external dependencies)

---

## Requirements

* Python 3.8 or later

No third-party Python packages are required.

Supported platforms:

* ✅ macOS
* ✅ Windows

---

## Installation

Clone the repository:

```bash
git clone https://github.com/leathermajesty/quickshare.git
cd quickshare
```

---

# Usage

## macOS

Run the script:

```bash
python3 macos.py
```

Select the file you want to share, then switch to your VM and paste the copied command.

---

## Windows

Run the script from Command Prompt:

```cmd
python windows.py
```

Select the file you want to share. QuickShare will create a temporary HTTP server and generate a download command.

Copy the generated command and run it inside your VM.

---

## Demo

https://github.com/user-attachments/assets/85bd655c-8d34-49c4-a642-2c7b551f0284

---

## Example

### macOS

```text
$ python3 macos.py

Available Files:

[1] macos.py
[2] .DS_Store
[3] README.md

Select file number: 1

Sharing: macos.py

Download command (also copied to clipboard):

wget http://192.168.1.12:1234/macos.py

Waiting for one download...
```

On your VM, simply paste the copied command and press **Enter**:

```bash
wget http://192.168.1.12:1234/macos.py
```

---

### Windows

```text
C:\QuickShare> python windows.py

Available Files:

[1] winpeas.exe
[2] payload.exe
[3] notes.txt

Select file number: 1

Sharing: winpeas.exe

Download command:

wget http://192.168.1.25:1234/winpeas.exe

Copy this command into your VM.

Waiting for one download...
```

Inside your VM, run:

```bash
wget http://192.168.1.25:1234/winpeas.exe
```

Once the download is complete, QuickShare automatically stops the HTTP server and removes the temporary directory.

---

## Typical Use Cases

* Hack The Box
* TryHackMe
* Capture The Flag (CTFs)
* Sharing VPN configuration files
* Transferring payloads and enumeration scripts
* Moving tools between host machines and Linux VMs

---

## License

This project is licensed under the MIT License.

---

If QuickShare makes your HTB or THM workflow a little faster, consider giving the repository a ⭐.