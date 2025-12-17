ZIP Bruteforce Tool

A simple Python script to brute-force password-protected .zip files using either a wordlist or basic brute-force logic.
Built for learning, testing, and educational purposes only.

> ⚠️ Disclaimer: Use this tool only on ZIP files you own or have explicit permission to test.
Unauthorized use is illegal.




---

Features

Crack password-protected ZIP files

Supports wordlist-based attacks

Simple CLI usage

Lightweight & dependency-free (uses Python standard library)

Easy to modify and extend



---

Requirements

Python 3.x

A password-protected .zip file

(Optional) Wordlist file (.txt)



---

##Setup

Clone the repository:

git clone https://github.com/minecraftpe2509-cmd/zip-bruteforce

Move into the project directory:

cd zip-bruteforce


---

Usage

Run the script:

python brute_force.py

Follow the on-screen prompts to:

Select the ZIP file

Choose a wordlist (if applicable)

Start the brute-force process



---

Example

python brute_force.py

The script will attempt passwords until:

The correct password is found, or

The wordlist is exhausted



---

Notes

Speed depends on:

ZIP encryption strength

Password complexity

Size of the wordlist


This is not optimized for large-scale cracking — it’s meant for learning and small tests.



---

Project Structure

zip-bruteforce/
│
├── brute_force.py
├── README.md
└── wordlist.txt   # optional


---

Future Improvements (Planned)

Multi-threading

Charset-based brute force

Progress display (attempts/sec)

Better error handling



---

License

This project is released for educational purposes only.
You are responsible for how you use it.
