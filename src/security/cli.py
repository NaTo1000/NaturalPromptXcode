"""CLI commands for security operations (SHA256 and GPG)."""

import argparse
import sys
from pathlib import Path

from .sha256 import (
    compute_sha256, verify_sha256, write_sha256_file, SHA256Error
)
from .gpg import (
    verify_gpg_signature, sign_with_gpg, GPGError
)


def add_security_commands(subparsers):
    """
    Add security-related subcommands to the argument parser.
    
    Args:
        subparsers: Subparser from argparse.ArgumentParser.add_subparsers()
    """
    
    # SHA256 compute command
    sha256_compute = subparsers.add_parser(
        'compute-sha256',
        help='Compute SHA256 checksum of a file'
    )
    sha256_compute.add_argument(
        'file',
        type=str,
        help='Path to file to hash'
    )
    sha256_compute.add_argument(
        '--output',
        type=str,
        help='Path for .sha256 file (default: <file>.sha256)'
    )
    sha256_compute.set_defaults(func=_handle_compute_sha256)
    
    # SHA256 verify command
    sha256_verify = subparsers.add_parser(
        'verify-sha256',
        help='Verify SHA256 checksum of a file'
    )
    sha256_verify.add_argument(
        'file',
        type=str,
        help='Path to file to verify'
    )
    group = sha256_verify.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--hash',
        type=str,
        help='Expected SHA256 hash'
    )
    group.add_argument(
        '--checksum-file',
        type=str,
        help='Path to .sha256 file with expected hash'
    )
    sha256_verify.set_defaults(func=_handle_verify_sha256)
    
    # GPG verify command
    gpg_verify = subparsers.add_parser(
        'verify-gpg',
        help='Verify GPG signature of a file'
    )
    gpg_verify.add_argument(
        'file',
        type=str,
        help='Path to file to verify'
    )
    gpg_verify.add_argument(
        'signature',
        type=str,
        help='Path to signature file (.asc or .sig)'
    )
    gpg_verify.add_argument(
        '--public-key',
        type=str,
        help='Path to public key file to import'
    )
    gpg_verify.set_defaults(func=_handle_verify_gpg)
    
    # GPG sign command
    gpg_sign = subparsers.add_parser(
        'sign-gpg',
        help='Sign a file with GPG'
    )
    gpg_sign.add_argument(
        'file',
        type=str,
        help='Path to file to sign'
    )
    gpg_sign.add_argument(
        '--output',
        type=str,
        help='Path for signature file (default: <file>.asc)'
    )
    gpg_sign.add_argument(
        '--key-id',
        type=str,
        help='GPG key ID to use for signing'
    )
    gpg_sign.add_argument(
        '--passphrase',
        type=str,
        help='Passphrase for the private key'
    )
    gpg_sign.set_defaults(func=_handle_sign_gpg)


def _handle_compute_sha256(args):
    """Handle compute-sha256 command."""
    try:
        file_path = Path(args.file)
        
        if args.output:
            output_path = write_sha256_file(file_path, args.output)
            checksum = compute_sha256(file_path)
            print(f"SHA256: {checksum}")
            print(f"Checksum file: {output_path}")
        else:
            checksum = compute_sha256(file_path)
            print(checksum)
        
        return 0
    
    except SHA256Error as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _handle_verify_sha256(args):
    """Handle verify-sha256 command."""
    try:
        file_path = Path(args.file)
        
        if args.hash:
            valid = verify_sha256(file_path, expected_hash=args.hash)
        else:
            valid = verify_sha256(file_path, checksum_file=args.checksum_file)
        
        if valid:
            print(f"✓ Verification successful: {file_path}")
            return 0
        else:
            print(f"✗ Verification failed: {file_path}", file=sys.stderr)
            return 1
    
    except SHA256Error as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _handle_verify_gpg(args):
    """Handle verify-gpg command."""
    try:
        file_path = Path(args.file)
        signature_path = Path(args.signature)
        public_key_path = Path(args.public_key) if args.public_key else None
        
        valid = verify_gpg_signature(
            file_path, 
            signature_path, 
            public_key_path
        )
        
        if valid:
            print(f"✓ GPG signature valid: {file_path}")
            return 0
        else:
            print(f"✗ GPG signature invalid: {file_path}", file=sys.stderr)
            return 1
    
    except GPGError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _handle_sign_gpg(args):
    """Handle sign-gpg command."""
    try:
        file_path = Path(args.file)
        output_path = Path(args.output) if args.output else None
        
        signature_path = sign_with_gpg(
            file_path,
            output_path=output_path,
            key_id=args.key_id,
            passphrase=args.passphrase
        )
        
        print(f"✓ Signed successfully")
        print(f"  File: {file_path}")
        print(f"  Signature: {signature_path}")
        return 0
    
    except GPGError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
