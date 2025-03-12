import click
from pathlib import Path
from ckenc.crypto_engine import (
    generate_kyber_keypair,
    encrypt_file,
    decrypt_file
)

@click.group(help="ckenc: A sample post-quantum file encryption CLI (CRYSTALS-Kyber + AES).")
def main():
    pass

@main.command(help="Generate a new Kyber keypair and save to 'kyber_public.bin' and 'kyber_secret.bin'.")
def genkey():
    pub, sec = generate_kyber_keypair("Kyber512")
    with open("kyber_public.bin", "wb") as fpub:
        fpub.write(pub)
    with open("kyber_secret.bin", "wb") as fsec:
        fsec.write(sec)
    click.echo("Keypair generated: kyber_public.bin, kyber_secret.bin")

@main.command(help="Encrypt a file (or stdin if '-') using Kyber public key + AES.")
@click.argument("pubkey_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("plaintext_file", type=click.Path(dir_okay=False))
@click.argument("encrypted_file", type=click.Path(dir_okay=False))
def encrypt(pubkey_file, plaintext_file, encrypted_file):
    """If plaintext_file = '-', reads from stdin.
       If encrypted_file = '-', writes to stdout.
    """
    pubkey = Path(pubkey_file).read_bytes()
    encrypt_file(public_key=pubkey, in_filename=plaintext_file, out_filename=encrypted_file, kem_alg="Kyber512")
    if encrypted_file != '-':
        click.echo(f"Encrypted '{plaintext_file}' -> '{encrypted_file}'")

@main.command(help="Decrypt a file (or stdin if '-') using Kyber secret key + AES.")
@click.argument("secretkey_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("encrypted_file", type=click.Path(dir_okay=False))
@click.argument("decrypted_file", type=click.Path(dir_okay=False))
def decrypt(secretkey_file, encrypted_file, decrypted_file):
    """If encrypted_file = '-', reads from stdin.
       If decrypted_file = '-', writes to stdout.
    """
    seckey = Path(secretkey_file).read_bytes()
    decrypt_file(secret_key=seckey, in_filename=encrypted_file, out_filename=decrypted_file, kem_alg="Kyber512")
    if decrypted_file != '-':
        click.echo(f"Decrypted '{encrypted_file}' -> '{decrypted_file}'")
