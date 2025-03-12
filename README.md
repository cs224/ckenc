# ckenc

A demonstration project for post-quantum file encryption using CRYSTALS-Kyber ([FIPS203](https://www.sectigo.com/resource-library/who-are-nists-post-quantum-algorithm-winners) / ML-KEM) + AES, with a
Click-based command line interface.


## Requirements

- Python 3.9+
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

With [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer):

```bash
# Generate keys
poetry run ckenc genkey

echo "testsecret" | poetry run ckenc encrypt kyber_public.bin - - | poetry run ckenc decrypt kyber_secret.bin - -

# Encrypt a file
poetry run ckenc encrypt kyber_public.bin test-secret.txt  test-secret.txt.enc

# Decrypt
poetry run ckenc decrypt kyber_secret.bin test-secret.txt.enc test-secret.dec.txt
```

Or with [uv](https://docs.astral.sh/uv/getting-started/installation/)/[uvx](https://docs.astral.sh/uv/guides/tools/):
```bash
uvx gh:cs224/ckenc genkey
uvx --from git+https://github.com/cs224/ckenc ckenc genkey
echo "testsecret" | uvx --from git+https://github.com/cs224/ckenc ckenc encrypt kyber_public.bin - - | uvx --from git+https://github.com/cs224/ckenc ckenc decrypt kyber_secret.bin - -
```

