#!/usr/bin/env python3

# ZipKrack Combined Tool
# Mode 1 = Wordlist
# Mode 2 = Brute Force (add_unzip.py merged)

import zipfile
import itertools
import string
import threading
from queue import Queue
import time
import os
import sys
import argparse

Tool_Name = "ZipKrack"
Version = "2.0"

# ----------------------------
# SHARED STATE FOR BRUTE FORCE
# ----------------------------
found = False
password = None
lock = threading.Lock()

def try_password(zip_path, pwd):
    global found, password
    if found:
        return
    try:
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
            if not names:
                return
            zf.read(names[0], pwd=pwd.encode('utf-8'))
        with lock:
            if not found:
                found = True
                password = pwd
                print(f"\n[+] PASSWORD FOUND: {pwd}")
    except:
        return

def worker(zip_path, queue):
    while not found:
        try:
            pwd = queue.get(timeout=1)
        except:
            continue
        if pwd is None:
            queue.task_done()
            break
        try_password(zip_path, pwd)
        print(f"\r[*] Trying: {pwd}", end="", flush=True)
        queue.task_done()

def generate_passwords(chars, min_len, max_len):
    for L in range(min_len, max_len + 1):
        for combo in itertools.product(chars, repeat=L):
            yield ''.join(combo)

def choose_charset(c):
    if c == "1": return string.digits
    if c == "2": return string.ascii_lowercase
    if c == "3": return string.ascii_uppercase
    if c == "4": return string.ascii_letters
    if c == "5": return string.ascii_letters + string.digits
    if c == "6": return string.ascii_letters + string.digits + string.punctuation
    return string.digits

def estimate_space(n, mn, mx):
    total = 0
    for L in range(mn, mx + 1):
        total += n ** L
    return total

# ----------------------------
# WORDLIST CRACKER
# ----------------------------

def wordlist_mode(zip_path, wl_path):
    try:
        zipf = zipfile.ZipFile(zip_path, "r")
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    try:
        wordlist = open(wl_path, "r", encoding="utf-8", errors="replace")
    except:
        print("[ERROR] Cannot open wordlist")
        zipf.close()
        return

    members = [m for m in zipf.infolist() if not m.is_dir()]
    if not members:
        print("[ERROR] ZIP contains no files.")
        return

    test_member = members[0].filename

    attempts = 0
    start = time.time()
    found_pwd = None

    for pwd in wordlist:
        pwd = pwd.strip()
        if pwd == "":
            continue

        sys.stdout.write("\rTrying: " + pwd)
        sys.stdout.flush()

        try:
            with zipf.open(test_member, pwd=pwd.encode()) as f:
                f.read(1)   # Force password validation
            found_pwd = pwd
            break
        except:
            pass

        attempts += 1

    zipf.close()
    wordlist.close()
    print()

    if found_pwd:
        print(f"[✔] Found password: {found_pwd}")
    else:
        print("[×] No password found in list.")

    zipf.close()
    wordlist.close()
    print()

    if found_pwd:
        print(f"[✔] Found password: {found_pwd}")
    else:
        print("[×] No password found in list.")

# ----------------------------
# BRUTE FORCE MODE
# ----------------------------

def brute_force_mode(zip_path):
    global found, password
    found = False
    password = None

    print("\nChoose charset")
    print("1 = Numbers (0-9)")
    print("2 = Lowercase (a-z)")
    print("3 = Uppercase (A-Z)")
    print("4 = Letters (a-zA-Z)")
    print("5 = Alphanumeric")
    print("6 = Full printable")

    cs = choose_charset(input("Choice: ").strip())

    try:
        mn = int(input("Min length: "))
        mx = int(input("Max length: "))
    except:
        print("Invalid length")
        return

    total = estimate_space(len(cs), mn, mx)
    print(f"Total combinations: {total}")

    threads = int(input("Threads (4-12 recommended): ") or 8)

    q = Queue(maxsize=50000)
    gen = generate_passwords(cs, mn, mx)

    for _ in range(threads):
        t = threading.Thread(target=worker, args=(zip_path, q))
        t.daemon = True
        t.start()

    try:
        for pwd in gen:
            if found:
                break
            q.put(pwd)
    except KeyboardInterrupt:
        print("\nStopped by user.")

    for _ in range(threads):
        q.put(None)

    if found:
        print(f"\n[✔] Password: {password}")
    else:
        print("\n[×] Not found.")

# ----------------------------
# MAIN MENU
# ----------------------------

def main():
    print("==== ZipKrack v2.0 ====")
    zip_path = input("Zip path: ").strip()

    if not os.path.isfile(zip_path):
        print("Invalid zip path")
        return

    print("\nSelect Mode:")
    print("1 = Wordlist Attack")
    print("2 = Brute Force")

    mode = input("Choice: ").strip()

    if mode == "1":
        wl = input("Wordlist path: ").strip()
        wordlist_mode(zip_path, wl)

    elif mode == "2":
        brute_force_mode(zip_path)

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()