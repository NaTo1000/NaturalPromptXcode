"""SHA256 checksum utilities for file verification."""

import hashlib
from pathlib import Path
from typing import Union


class SHA256Error(Exception):
    """Exception raised for SHA256-related errors."""
    pass


def compute_sha256(file_path: Union[str, Path], buffer_size: int = 65536) -> str:
    """
    Compute SHA256 checksum of a file.
    
    Args:
        file_path: Path to the file to hash
        buffer_size: Size of chunks to read (default: 64KB)
    
    Returns:
        Hexadecimal string representation of the SHA256 hash
    
    Raises:
        SHA256Error: If file cannot be read or hashed
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise SHA256Error(f"File not found: {file_path}")
    
    if not file_path.is_file():
        raise SHA256Error(f"Not a file: {file_path}")
    
    try:
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                sha256_hash.update(data)
        
        return sha256_hash.hexdigest()
    
    except Exception as e:
        raise SHA256Error(f"Failed to compute SHA256 for {file_path}: {e}")


def verify_sha256(file_path: Union[str, Path], 
                  expected_hash: str = None,
                  checksum_file: Union[str, Path] = None) -> bool:
    """
    Verify SHA256 checksum of a file.
    
    Args:
        file_path: Path to the file to verify
        expected_hash: Expected SHA256 hash (hexadecimal string)
        checksum_file: Path to .sha256 file containing the expected hash
    
    Returns:
        True if verification succeeds, False otherwise
    
    Raises:
        SHA256Error: If neither expected_hash nor checksum_file is provided,
                     or if files cannot be read
    
    Note:
        You must provide either expected_hash or checksum_file, not both.
    """
    file_path = Path(file_path)
    
    # Determine expected hash
    if expected_hash and checksum_file:
        raise SHA256Error("Provide either expected_hash or checksum_file, not both")
    
    if not expected_hash and not checksum_file:
        raise SHA256Error("Must provide either expected_hash or checksum_file")
    
    if checksum_file:
        checksum_file = Path(checksum_file)
        if not checksum_file.exists():
            raise SHA256Error(f"Checksum file not found: {checksum_file}")
        
        try:
            with open(checksum_file, 'r') as f:
                content = f.read().strip()
                # Support both "hash" and "hash filename" formats
                expected_hash = content.split()[0]
        except Exception as e:
            raise SHA256Error(f"Failed to read checksum file {checksum_file}: {e}")
    
    # Compute actual hash
    actual_hash = compute_sha256(file_path)
    
    # Compare (case-insensitive)
    return actual_hash.lower() == expected_hash.lower()


def write_sha256_file(file_path: Union[str, Path], 
                      output_path: Union[str, Path] = None) -> Path:
    """
    Compute SHA256 of a file and write it to a .sha256 file.
    
    Args:
        file_path: Path to the file to hash
        output_path: Path for the output .sha256 file (default: file_path + '.sha256')
    
    Returns:
        Path to the created .sha256 file
    
    Raises:
        SHA256Error: If file cannot be hashed or written
    """
    file_path = Path(file_path)
    
    if output_path is None:
        output_path = Path(str(file_path) + '.sha256')
    else:
        output_path = Path(output_path)
    
    checksum = compute_sha256(file_path)
    
    try:
        with open(output_path, 'w') as f:
            # Write in format: "hash filename"
            f.write(f"{checksum}  {file_path.name}\n")
        
        return output_path
    
    except Exception as e:
        raise SHA256Error(f"Failed to write checksum file {output_path}: {e}")
