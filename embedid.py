import json
import getpass
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rich.console import Console

VAULT_FILE = "keys.json.enc"
SALT_FILE = "vault.salt"

console = Console()

def _derive_key(password: str, salt: bytes) -> bytes:
    """Derives a cryptographic key from a password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

class EmbedID:
    """A simple vault for encrypting and decrypting API keys."""

    def __init__(self):
        self._keys = None
        self._password = None

    def _prompt_for_password(self):
        """Prompts the user for their master password."""
        if self._password:
            return
        self._password = getpass.getpass("[EmbedID] 🔑 Enter your master password to unlock the vault: ")

    def get_keys(self, exchange: str) -> tuple[str, str]:
        """
        Retrieves and decrypts API keys for a given exchange.
        Prompts for password if not already provided.
        """
        if not self._keys:
            self._prompt_for_password()
            if not os.path.exists(VAULT_FILE) or not os.path.exists(SALT_FILE):
                console.print("[bold red]Vault not found! Please run `python setup_vault.py` first.[/bold red]")
                raise FileNotFoundError("Vault files are missing.")

            with open(SALT_FILE, "rb") as f:
                salt = f.read()

            key = _derive_key(self._password, salt)
            fernet = Fernet(key)

            try:
                with open(VAULT_FILE, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                self._keys = json.loads(decrypted_data)
            except Exception:
                console.print("[bold red]Failed to decrypt vault. Incorrect password or corrupt vault.[/bold red]")
                raise ValueError("Decryption failed")

        api_key = self._keys.get(exchange, {}).get("key")
        api_secret = self._keys.get(exchange, {}).get("secret")

        if not api_key or not api_secret:
            raise ValueError(f"API keys for '{exchange}' not found in vault.")

        return api_key, api_secret
