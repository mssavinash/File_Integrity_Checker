#!/usr/bin/env python3

import os
import sys
import hashlib
import json
from pathlib import Path
import argparse

# Hash store file location
HASH_STORE_DIR = Path.home() / ".logfile_integrity"
HASH_STORE_FILE = HASH_STORE_DIR / "hashes.json"

# Ensure the hash directory exists
HASH_STORE_DIR.mkdir(parents=True, exist_ok=True)

# Load stored hashes if available
def load_hashes():
    if HASH_STORE_FILE.exists():
        with open(HASH_STORE_FILE, "r") as f:
            return json.load(f)
    return {}

# Save hashes to file
def save_hashes(hashes):
    with open(HASH_STORE_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

# Calculate SHA-256 hash of a file
def calculate_hash(filepath):
    try:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[!] Error reading {filepath}: {e}")
        return None

# Initialize hashes for file or directory
def init_hashes(path):
    hashes = load_hashes()
    updated = False

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                hash_val = calculate_hash(full_path)
                if hash_val:
                    hashes[full_path] = hash_val
                    updated = True
    elif os.path.isfile(path):
        hash_val = calculate_hash(path)
        if hash_val:
            hashes[path] = hash_val
            updated = True
    else:
        print("[!] Invalid path.")
        return

    if updated:
        save_hashes(hashes)
        print("✅ Hashes stored successfully.")
    else:
        print("[!] No valid files found.")

# Check integrity of file or directory
def check_hashes(path):
    hashes = load_hashes()

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                verify_hash(full_path, hashes)
    elif os.path.isfile(path):
        verify_hash(path, hashes)
    else:
        print("[!] Invalid path.")

# Verify single file
def verify_hash(filepath, hashes):
    current_hash = calculate_hash(filepath)
    stored_hash = hashes.get(filepath)

    if not stored_hash:
        print(f"{filepath} → Status: Not initialized")
    elif current_hash != stored_hash:
        print(f"{filepath} → Status: ❌ Modified (Hash mismatch)")
    else:
        print(f"{filepath} → Status: ✅ Unmodified")

# Update hash for file or directory
def update_hashes(path):
    hashes = load_hashes()
    updated = False

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                update_hash(full_path, hashes)
                updated = True
    elif os.path.isfile(path):
        update_hash(path, hashes)
        updated = True
    else:
        print("[!] Invalid path.")
        return

    if updated:
        save_hashes(hashes)

# Update single file hash
def update_hash(filepath, hashes):
    hash_val = calculate_hash(filepath)
    if hash_val:
        hashes[filepath] = hash_val
        print(f"{filepath} → ✅ Hash updated successfully.")

# ------------------------
# Main CLI Entry
# ------------------------
def main():
    parser = argparse.ArgumentParser(description="🔐 File Integrity Checker using SHA-256")
    parser.add_argument("command", choices=["init", "check", "update"], help="Command to execute")
    parser.add_argument("path", help="Path to log file or directory")

    args = parser.parse_args()

    if args.command == "init":
        init_hashes(args.path)
    elif args.command == "check":
        check_hashes(args.path)
    elif args.command == "update":
        update_hashes(args.path)

if __name__ == "__main__":
    main()
