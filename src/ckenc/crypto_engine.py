import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import oqs


def generate_kyber_keypair(kem_alg="Kyber512"):
    """Generate a Kyber keypair (public, secret) and return them as bytes."""
    kem = oqs.KeyEncapsulation(kem_alg)
    pub = kem.generate_keypair()
    sec = kem.export_secret_key()
    kem.free()
    return pub, sec


def encrypt_file(public_key: bytes, in_filename: str, out_filename: str, kem_alg="Kyber512"):
    """
    Encrypt the contents of 'in_filename' using the public_key (Kyber) + AES for
    bulk data encryption, writing the result to 'out_filename'.

    If in_filename is "-", read from stdin. If out_filename is "-", write to stdout.
    """
    # Prepare input
    if in_filename == "-":
        fin = sys.stdin.buffer
    else:
        fin = open(in_filename, "rb")

    # Prepare output
    if out_filename == "-":
        fout = sys.stdout.buffer
    else:
        fout = open(out_filename, "wb")

    # Create a KEM object with the given public key
    kem = oqs.KeyEncapsulation(kem_alg)

    # Encapsulate: generate ephemeral ciphertext (ct) + shared secret (ss)
    ct, ss = kem.encap_secret(public_key)

    # Derive an AES-256 key from the shared secret
    aes_key = ss[:32]
    iv = os.urandom(16)

    encryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv)).encryptor()

    # Write ephemeral ciphertext length, ciphertext, and IV
    fout.write(len(ct).to_bytes(2, byteorder='big'))
    fout.write(ct)
    fout.write(iv)

    # Encrypt the file data in chunks
    chunk_size = 4096
    while True:
        chunk = fin.read(chunk_size)
        if not chunk:
            break
        encrypted_chunk = encryptor.update(chunk)
        fout.write(encrypted_chunk)

    # Finalize encryption
    fout.write(encryptor.finalize())

    kem.free()

    # Close file handles (unless they were stdin/stdout)
    if in_filename != "-":
        fin.close()
    if out_filename != "-":
        fout.close()


def decrypt_file(secret_key: bytes, in_filename: str, out_filename: str, kem_alg="Kyber512"):
    """
    Decrypt 'in_filename' (which was produced by 'encrypt_file') using
    the secret_key (Kyber) to recover the symmetric key, then decrypt with AES.

    If in_filename is "-", read from stdin. If out_filename is "-", write to stdout.
    """
    # Prepare input
    if in_filename == "-":
        fin = sys.stdin.buffer
    else:
        fin = open(in_filename, "rb")

    # Prepare output
    if out_filename == "-":
        fout = sys.stdout.buffer
    else:
        fout = open(out_filename, "wb")

    # Read ephemeral ciphertext length, ciphertext, and IV
    ct_len = int.from_bytes(fin.read(2), byteorder='big')
    kyber_ct = fin.read(ct_len)
    iv = fin.read(16)

    # Initialize the KEM object with the secret key
    kem = oqs.KeyEncapsulation(kem_alg, secret_key=secret_key)

    # Decapsulate to recover the ephemeral shared secret
    ss = kem.decap_secret(kyber_ct)
    aes_key = ss[:32]

    decryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv)).decryptor()

    # Decrypt the file data in chunks
    chunk_size = 4096
    while True:
        chunk = fin.read(chunk_size)
        if not chunk:
            break
        decrypted_chunk = decryptor.update(chunk)
        fout.write(decrypted_chunk)

    # Finalize decryption
    fout.write(decryptor.finalize())

    kem.free()

    # Close handles
    if in_filename != "-":
        fin.close()
    if out_filename != "-":
        fout.close()
