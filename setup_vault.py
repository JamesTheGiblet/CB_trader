import os
import json
import getpass
from cryptography.fernet import Fernet
from rich.console import Console
from embedid import _derive_key, VAULT_FILE, SALT_FILE

console = Console()

def setup_vault():
    """A one-time setup script to create an encrypted vault for API keys."""
    console.print("[bold green]--- CB_Trader Secure Vault Setup ---[/bold green]")
    console.print("This script will encrypt your API keys in a local vault.")

    if os.path.exists(VAULT_FILE):
        overwrite = input(f"[yellow]'{VAULT_FILE}' already exists. Overwrite? (y/n): [/yellow]").lower()
        if overwrite != 'y':
            console.print("[red]Setup cancelled.[/red]")
            return

    # 1. Get API Keys
    coinbase_key = input("Enter your Coinbase API Key: ")
    coinbase_secret = getpass.getpass("Enter your Coinbase API Secret: ")
    gemini_key = input("Enter your Gemini API Key: ")
    gemini_secret = getpass.getpass("Enter your Gemini API Secret: ")

    keys_data = {
        "coinbase": {"key": coinbase_key, "secret": coinbase_secret},
        "gemini": {"key": gemini_key, "secret": gemini_secret}
    }

    # 2. Get Master Password
    while True:
        password = getpass.getpass("Enter a master password for the vault: ")
        password_confirm = getpass.getpass("Confirm master password: ")
        if password == password_confirm:
            break
        console.print("[red]Passwords do not match. Please try again.[/red]")

    # 3. Encrypt and Save
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    fernet = Fernet(key)

    encrypted_data = fernet.encrypt(json.dumps(keys_data).encode())

    with open(SALT_FILE, "wb") as f:
        f.write(salt)

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)

    console.print(f"\n[bold green]✓ Vault created successfully as '{VAULT_FILE}'.[/bold green]")
    console.print("[yellow]Important: Do not lose your master password. It cannot be recovered.[/yellow]")

if __name__ == "__main__":
    setup_vault()
