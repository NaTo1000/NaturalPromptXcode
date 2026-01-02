"""GPG signature verification and signing utilities."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Union, Optional


class GPGError(Exception):
    """Exception raised for GPG-related errors."""
    pass


def _check_gpg_available() -> bool:
    """
    Check if GPG is available on the system.
    
    Returns:
        True if GPG is available, False otherwise
    """
    try:
        result = subprocess.run(
            ['gpg', '--version'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def verify_gpg_signature(file_path: Union[str, Path],
                        signature_path: Union[str, Path],
                        public_key_path: Optional[Union[str, Path]] = None) -> bool:
    """
    Verify GPG signature of a file.
    
    Args:
        file_path: Path to the file to verify
        signature_path: Path to the detached signature (.asc or .sig)
        public_key_path: Optional path to public key file to import first
    
    Returns:
        True if signature is valid, False otherwise
    
    Raises:
        GPGError: If GPG is not available or verification fails
    """
    if not _check_gpg_available():
        raise GPGError(
            "GPG is not available. Please install GnuPG:\n"
            "  - macOS: brew install gnupg\n"
            "  - Ubuntu/Debian: apt-get install gnupg\n"
            "  - Windows: https://www.gnupg.org/download/"
        )
    
    file_path = Path(file_path)
    signature_path = Path(signature_path)
    
    if not file_path.exists():
        raise GPGError(f"File not found: {file_path}")
    
    if not signature_path.exists():
        raise GPGError(f"Signature file not found: {signature_path}")
    
    # Import public key if provided
    if public_key_path:
        public_key_path = Path(public_key_path)
        if not public_key_path.exists():
            raise GPGError(f"Public key file not found: {public_key_path}")
        
        try:
            result = subprocess.run(
                ['gpg', '--import', str(public_key_path)],
                capture_output=True,
                timeout=10
            )
            if result.returncode != 0:
                # Import might "fail" if key already exists, which is okay
                pass
        except subprocess.TimeoutExpired:
            raise GPGError("GPG key import timed out")
        except Exception as e:
            raise GPGError(f"Failed to import public key: {e}")
    
    # Verify signature
    try:
        result = subprocess.run(
            ['gpg', '--verify', str(signature_path), str(file_path)],
            capture_output=True,
            timeout=10
        )
        
        # GPG returns 0 for valid signature
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        raise GPGError("GPG verification timed out")
    except Exception as e:
        raise GPGError(f"Failed to verify signature: {e}")


def sign_with_gpg(file_path: Union[str, Path],
                 output_path: Optional[Union[str, Path]] = None,
                 key_id: Optional[str] = None,
                 passphrase: Optional[str] = None,
                 private_key_data: Optional[str] = None) -> Path:
    """
    Sign a file with GPG, creating a detached signature.
    
    Args:
        file_path: Path to the file to sign
        output_path: Path for the signature file (default: file_path + '.asc')
        key_id: GPG key ID to use for signing (optional)
        passphrase: Passphrase for the private key (optional)
        private_key_data: Private key data to import (optional)
    
    Returns:
        Path to the created signature file
    
    Raises:
        GPGError: If GPG is not available or signing fails
    """
    if not _check_gpg_available():
        raise GPGError(
            "GPG is not available. Please install GnuPG:\n"
            "  - macOS: brew install gnupg\n"
            "  - Ubuntu/Debian: apt-get install gnupg\n"
            "  - Windows: https://www.gnupg.org/download/"
        )
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise GPGError(f"File not found: {file_path}")
    
    if output_path is None:
        output_path = Path(str(file_path) + '.asc')
    else:
        output_path = Path(output_path)
    
    # Import private key if provided
    if private_key_data:
        temp_key_file = None
        try:
            # Create temp file with secure permissions
            # Set restrictive umask before creating file to prevent race condition
            old_umask = os.umask(0o077)  # Ensures files are created with 0o600
            try:
                fd, temp_key_file = tempfile.mkstemp(suffix='.key', prefix='gpg_key_')
            finally:
                os.umask(old_umask)  # Restore original umask
            
            try:
                with os.fdopen(fd, 'w') as f:
                    f.write(private_key_data)
                
                result = subprocess.run(
                    ['gpg', '--batch', '--import', temp_key_file],
                    capture_output=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    # Import might "fail" if key already exists
                    pass
            
            finally:
                # Clean up temp file securely
                if temp_key_file and os.path.exists(temp_key_file):
                    os.unlink(temp_key_file)
        
        except subprocess.TimeoutExpired:
            raise GPGError("GPG key import timed out")
        except Exception as e:
            raise GPGError(f"Failed to import private key: {e}")
    
    # Build GPG command
    cmd = ['gpg', '--detach-sign', '--armor']
    
    if key_id:
        cmd.extend(['--local-user', key_id])
    
    # Use passphrase-fd for better security (doesn't expose in process list)
    passphrase_input = None
    if passphrase:
        cmd.extend(['--batch', '--yes', '--pinentry-mode', 'loopback', 
                   '--passphrase-fd', '0'])
        passphrase_input = passphrase.encode('utf-8')
    
    cmd.extend(['--output', str(output_path), str(file_path)])
    
    # Sign the file
    try:
        result = subprocess.run(
            cmd,
            input=passphrase_input,
            capture_output=True,
            timeout=30
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.decode('utf-8', errors='ignore')
            raise GPGError(f"GPG signing failed: {error_msg}")
        
        if not output_path.exists():
            raise GPGError(f"Signature file was not created: {output_path}")
        
        return output_path
    
    except subprocess.TimeoutExpired:
        raise GPGError("GPG signing timed out")
    except GPGError:
        raise
    except Exception as e:
        raise GPGError(f"Failed to sign file: {e}")
