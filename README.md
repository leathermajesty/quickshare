# 🚀 QuickShare

QuickShare is a lightweight Python utility that allows you to quickly share a single file over your local network using Python's built-in HTTP server.

It was created to simplify transferring files from a host machine to a virtual machine during Hack The Box (HTB), TryHackMe (THM), CTFs, and penetration testing labs.

Instead of manually starting an HTTP server and typing download URLs, QuickShare automates the entire process.

---

## Features

* 📂 Lists all files in the current directory
* 🔢 Select a file using its number
* 📦 Shares only the selected file
* 🌐 Automatically detects your local IP address
* 📋 Copies the download command to your clipboard
* ⬇️ Stops automatically after the first successful download
* 🧹 Cleans up temporary files automatically
* 🐍 Built using only Python's standard library (no third-party packages)

---

## Supported Platforms

* ✅ macOS
* ✅ Linux
* ✅ Windows

Each platform has its own script:

```text
macos.py
linux.py
windows.py
```

---

## Usage

### macOS

```bash
python3 macos.py
```

### Linux

```bash
python3 linux.py
```

### Windows

```powershell
python windows.py
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

Simply paste the copied command into your VM and press **Enter**.

After the download finishes, the server automatically stops.

---

## Typical Use Cases

* Hack The Box
* TryHackMe
* Capture The Flag (CTFs)
* Penetration Testing
* Local file transfers
* Sharing payloads, VPN files, scripts, or tools

---

## Requirements

* Python 3.8+
* No external Python libraries

Platform-specific clipboard utilities:

### macOS

* `pbcopy` (built in)

### Linux

* `xclip` or `xsel`

### Windows

* `clip` (built in)

---

## Project Structure

```text
quickshare/
├── macos.py
├── linux.py
├── windows.py
├── README.md
├── FUNCTION.md
└── LICENSE
```

---

## License

This project is licensed under the MIT License.

---

## Contributing

Bug reports, feature requests, and pull requests are welcome.

If QuickShare saves you a few minutes every HTB or THM session, consider giving the repository a ⭐.

