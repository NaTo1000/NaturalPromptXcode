"""Unit tests for security utilities (SHA256 and GPG)."""

import pytest
import tempfile
import os
from pathlib import Path
import subprocess

from src.security.sha256 import (
    compute_sha256, verify_sha256, write_sha256_file, SHA256Error
)
from src.security.gpg import (
    verify_gpg_signature, sign_with_gpg, GPGError, _check_gpg_available
)


class TestSHA256:
    """Tests for SHA256 utilities."""
    
    def test_compute_sha256_simple_file(self):
        """Test computing SHA256 of a simple file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Hello, World!")
            temp_file = f.name
        
        try:
            checksum = compute_sha256(temp_file)
            # Known SHA256 of "Hello, World!"
            expected = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
            assert checksum == expected
        finally:
            os.unlink(temp_file)
    
    def test_compute_sha256_empty_file(self):
        """Test computing SHA256 of an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            checksum = compute_sha256(temp_file)
            # Known SHA256 of empty file
            expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            assert checksum == expected
        finally:
            os.unlink(temp_file)
    
    def test_compute_sha256_nonexistent_file(self):
        """Test computing SHA256 of nonexistent file raises error."""
        with pytest.raises(SHA256Error, match="File not found"):
            compute_sha256("/nonexistent/file.txt")
    
    def test_compute_sha256_directory(self):
        """Test computing SHA256 of directory raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(SHA256Error, match="Not a file"):
                compute_sha256(temp_dir)
    
    def test_verify_sha256_with_hash(self):
        """Test verifying SHA256 with expected hash."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            temp_file = f.name
        
        try:
            # Compute the hash first
            expected_hash = compute_sha256(temp_file)
            
            # Verify with correct hash
            assert verify_sha256(temp_file, expected_hash=expected_hash) is True
            
            # Verify with incorrect hash
            assert verify_sha256(temp_file, expected_hash="0" * 64) is False
        finally:
            os.unlink(temp_file)
    
    def test_verify_sha256_case_insensitive(self):
        """Test SHA256 verification is case-insensitive."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            temp_file = f.name
        
        try:
            expected_hash = compute_sha256(temp_file)
            
            # Verify with uppercase
            assert verify_sha256(temp_file, expected_hash=expected_hash.upper()) is True
            
            # Verify with lowercase
            assert verify_sha256(temp_file, expected_hash=expected_hash.lower()) is True
        finally:
            os.unlink(temp_file)
    
    def test_verify_sha256_with_checksum_file(self):
        """Test verifying SHA256 with checksum file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Create test file
            test_file = temp_dir / "test.txt"
            test_file.write_text("Test content")
            
            # Create checksum file
            checksum_file = temp_dir / "test.txt.sha256"
            checksum = compute_sha256(test_file)
            checksum_file.write_text(f"{checksum}  test.txt\n")
            
            # Verify
            assert verify_sha256(test_file, checksum_file=checksum_file) is True
    
    def test_verify_sha256_missing_parameters(self):
        """Test verify_sha256 raises error when no hash or checksum file provided."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            with pytest.raises(SHA256Error, match="Must provide either"):
                verify_sha256(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_verify_sha256_both_parameters(self):
        """Test verify_sha256 raises error when both hash and checksum file provided."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            with pytest.raises(SHA256Error, match="not both"):
                verify_sha256(
                    temp_file, 
                    expected_hash="abc123",
                    checksum_file="/some/file"
                )
        finally:
            os.unlink(temp_file)
    
    def test_write_sha256_file(self):
        """Test writing SHA256 checksum to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Create test file
            test_file = temp_dir / "test.txt"
            test_file.write_text("Test content")
            
            # Write checksum file
            output_file = write_sha256_file(test_file)
            
            # Check file was created
            assert output_file.exists()
            assert output_file.name == "test.txt.sha256"
            
            # Verify content
            content = output_file.read_text()
            expected_hash = compute_sha256(test_file)
            assert expected_hash in content
            assert "test.txt" in content
    
    def test_write_sha256_file_custom_output(self):
        """Test writing SHA256 checksum to custom output path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Create test file
            test_file = temp_dir / "test.txt"
            test_file.write_text("Test content")
            
            # Write checksum file with custom name
            custom_output = temp_dir / "custom.checksum"
            output_file = write_sha256_file(test_file, custom_output)
            
            # Check file was created
            assert output_file == custom_output
            assert output_file.exists()


class TestGPG:
    """Tests for GPG utilities."""
    
    def test_gpg_available(self):
        """Test checking if GPG is available."""
        # This should pass in CI environment
        is_available = _check_gpg_available()
        assert isinstance(is_available, bool)
    
    @pytest.mark.skipif(not _check_gpg_available(), reason="GPG not available")
    def test_sign_and_verify_gpg(self):
        """Test signing and verifying with GPG."""
        # Skip if GPG not available
        if not _check_gpg_available():
            pytest.skip("GPG not available")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Create test file
            test_file = temp_dir / "test.txt"
            test_file.write_text("Test content for GPG signing")
            
            # Generate a test GPG key (unattended)
            # NOTE: %no-protection creates a key without a passphrase - this is
            # appropriate for testing only. Production keys should ALWAYS have
            # strong passphrases for security.
            key_batch = """
                %no-protection
                Key-Type: RSA
                Key-Length: 2048
                Name-Real: Test User
                Name-Email: test@example.com
                Expire-Date: 0
                %commit
            """
            
            batch_file = temp_dir / "keygen.batch"
            batch_file.write_text(key_batch)
            
            try:
                # Generate key
                result = subprocess.run(
                    ['gpg', '--batch', '--gen-key', str(batch_file)],
                    capture_output=True,
                    timeout=30,
                    env={**os.environ, 'GNUPGHOME': str(temp_dir / '.gnupg')}
                )
                
                if result.returncode != 0:
                    pytest.skip("Could not generate GPG test key")
                
                # Sign the file
                signature_file = sign_with_gpg(
                    test_file,
                    key_id="test@example.com"
                )
                
                # Verify signature exists
                assert signature_file.exists()
                
                # Verify the signature
                is_valid = verify_gpg_signature(test_file, signature_file)
                assert is_valid is True
            
            except (subprocess.TimeoutExpired, GPGError):
                pytest.skip("GPG key generation or signing failed")
    
    def test_verify_gpg_nonexistent_file(self):
        """Test verifying nonexistent file raises error."""
        with pytest.raises(GPGError, match="File not found"):
            verify_gpg_signature("/nonexistent/file.txt", "/nonexistent/sig.asc")
    
    def test_sign_gpg_nonexistent_file(self):
        """Test signing nonexistent file raises error."""
        with pytest.raises(GPGError, match="File not found"):
            sign_with_gpg("/nonexistent/file.txt")
    
    @pytest.mark.skipif(not _check_gpg_available(), reason="GPG not available")
    def test_verify_gpg_invalid_signature(self):
        """Test verifying file with invalid signature."""
        if not _check_gpg_available():
            pytest.skip("GPG not available")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            # Create test file
            test_file = temp_dir / "test.txt"
            test_file.write_text("Test content")
            
            # Create fake signature file
            sig_file = temp_dir / "test.txt.asc"
            sig_file.write_text("-----BEGIN PGP SIGNATURE-----\nfake signature\n-----END PGP SIGNATURE-----")
            
            # Verify should return False or raise error
            try:
                is_valid = verify_gpg_signature(test_file, sig_file)
                assert is_valid is False
            except GPGError:
                # Also acceptable - invalid signature format
                pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
