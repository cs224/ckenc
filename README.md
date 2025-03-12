# ckenc

A demonstration project for file encryption using CRYSTALS-Kyber (KEM) + AES, with a
Click-based command line interface.

## Requirements

- Python 3.8+
- liboqs installed (if not pulling directly from GitHub).
- [liboqs-python](https://github.com/open-quantum-safe/liboqs-python).

## Installation

```bash
# Option 1: Using Poetry
poetry self add poetry-plugin-shell
poetry install

# Option 2: Using pip + setuptools
pip install .
```

## Usage

```bash
# Generate keys
poetry run ckenc genkey

echo "testsecret" | poetry run ckenc encrypt kyber_public.bin - - | poetry run ckenc decrypt kyber_secret.bin - -

# Encrypt a file
poetry run ckenc encrypt kyber_public.bin test-secret.txt  test-secret.txt.enc

# Decrypt
poetry run ckenc decrypt kyber_secret.bin test-secret.txt.enc test-secret.dec.txt
```