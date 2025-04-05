# 🔐 Log File Integrity Checker

A simple and secure tool to **verify the integrity of application log files** to detect unauthorized tampering. This utility uses cryptographic hash functions (SHA-256) to track changes in log files and alert users of any suspicious modifications.

## 📌 Features

- ✅ Accepts a single file or an entire directory as input
- 🔐 Uses SHA-256 hashing to monitor file integrity
- 🧩 Stores and compares hashes securely
- 🚨 Alerts on file modification or tampering
- 🔄 Supports manual re-initialization and hash updates

## 📂 Use Cases

- Detect log tampering or unauthorized changes
- Ensure audit trail integrity
- File Integrity Monitoring (FIM) in security auditing

---

## 🛠 Installation

```bash
git clone https://github.com/your-username/log-file-integrity-checker.git
cd log-file-integrity-checker
chmod +x integrity-check.py
# Initialize hashes
./integrity-check.py init /var/log

# Check a specific log file
./integrity-check.py check /var/log/syslog

# Update the hash (if the file was modified and accepted)
./integrity-check.py update /var/log/syslog
```

All hashes are stored in ~/.logfile_integrity/hashes.json for safe keeping.
```
https://roadmap.sh/projects/file-integrity-checker
```
## Result
![image](https://github.com/user-attachments/assets/78251f95-5366-40fa-8d8a-1a08bd34f9dd)
