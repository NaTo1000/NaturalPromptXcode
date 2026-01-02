# 🔐 Security: SHA256 & GPG Signing

This document describes how to use SHA256 checksums and GPG signatures for verifying and signing artifacts in NaturalPromptXcode.

## Table of Contents

- [Overview](#overview)
- [SHA256 Checksums](#sha256-checksums)
- [GPG Signatures](#gpg-signatures)
- [GitHub Actions Integration](#github-actions-integration)
- [Verifying Releases](#verifying-releases)
- [Troubleshooting](#troubleshooting)

## Overview

NaturalPromptXcode supports two methods for ensuring artifact integrity:

1. **SHA256 Checksums**: Cryptographic hashes that detect file tampering or corruption
2. **GPG Signatures**: Digital signatures that verify authenticity and integrity

Both methods are integrated into the CLI and GitHub Actions workflows.

## SHA256 Checksums

### Computing SHA256

Compute the SHA256 checksum of a file:

```bash
# Output hash to console
python -m src.main compute-sha256 myfile.tar.gz

# Save hash to a .sha256 file
python -m src.main compute-sha256 myfile.tar.gz --output myfile.tar.gz.sha256
```

### Verifying SHA256

Verify a file against an expected checksum:

```bash
# Verify using hash string
python -m src.main verify-sha256 myfile.tar.gz --hash <expected-hash>

# Verify using .sha256 file
python -m src.main verify-sha256 myfile.tar.gz --checksum-file myfile.tar.gz.sha256
```

### SHA256 File Format

The `.sha256` files follow the standard format:

```
<hash>  <filename>
```

Example:
```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  myfile.tar.gz
```

## GPG Signatures

### Prerequisites

Install GnuPG on your system:

```bash
# macOS
brew install gnupg

# Ubuntu/Debian
sudo apt-get install gnupg

# Windows
# Download from https://www.gnupg.org/download/
```

### Generating GPG Keys

1. Generate a new GPG key pair:

```bash
gpg --full-generate-key
```

2. Follow the prompts:
   - Key type: RSA and RSA (default)
   - Key size: 4096 bits (recommended)
   - Expiration: Choose based on your needs
   - Name and email: Use your GitHub email for releases
   - Passphrase: Choose a strong passphrase

3. List your keys to get the Key ID:

```bash
gpg --list-secret-keys --keyid-format=long
```

Example output:
```
sec   rsa4096/ABC123DEF456 2024-01-01 [SC]
      ABCDEF0123456789ABCDEF0123456789ABCDEF01
uid                 [ultimate] Your Name <you@example.com>
```

The Key ID is `ABC123DEF456` or the full fingerprint.

### Signing Files

Sign a file with GPG:

```bash
# Sign with default key
python -m src.main sign-gpg myfile.tar.gz

# Sign with specific key
python -m src.main sign-gpg myfile.tar.gz --key-id ABC123DEF456

# Sign with passphrase (for automation)
python -m src.main sign-gpg myfile.tar.gz --key-id ABC123DEF456 --passphrase "yourpassphrase"

# Custom output path
python -m src.main sign-gpg myfile.tar.gz --output myfile.tar.gz.sig
```

This creates a detached signature file (`.asc` by default).

### Verifying Signatures

Verify a GPG signature:

```bash
# Verify using keys already in your keyring
python -m src.main verify-gpg myfile.tar.gz myfile.tar.gz.asc

# Import and verify with a specific public key
python -m src.main verify-gpg myfile.tar.gz myfile.tar.gz.asc --public-key pubkey.asc
```

### Exporting Keys

**Export your public key** (share this with users):

```bash
gpg --armor --export your@email.com > public-key.asc
```

**Export your private key** (keep this secret!):

```bash
gpg --armor --export-secret-keys your@email.com > private-key.asc
```

⚠️ **Never commit private keys to version control!**

## GitHub Actions Integration

### Setting Up Secrets

To enable automatic signing in GitHub Actions:

1. **Export your GPG private key**:

```bash
gpg --armor --export-secret-keys your@email.com
```

2. **Add secrets to your GitHub repository**:
   - Go to: Settings → Secrets and variables → Actions
   - Add the following secrets:

   | Secret Name | Description |
   |-------------|-------------|
   | `GPG_PRIVATE_KEY` | The full output from the export command (including `-----BEGIN/END-----` lines) |
   | `GPG_PASSPHRASE` | Your GPG key passphrase |
   | `GPG_KEY_ID` | (Optional) Your GPG key ID for selecting a specific key |

3. **Add your public key to the repository** (optional but recommended):

```bash
# Add to a docs/ directory so users can verify releases
gpg --armor --export your@email.com > docs/GPG_PUBLIC_KEY.asc
git add docs/GPG_PUBLIC_KEY.asc
git commit -m "Add GPG public key for release verification"
```

### Workflow Configuration

The `.github/workflows/release.yml` workflow automatically:

1. Builds distribution packages
2. Generates SHA256 checksums for all artifacts
3. Signs artifacts with GPG (if secrets are configured)
4. Verifies checksums and signatures
5. Uploads artifacts with signatures
6. Attaches artifacts to GitHub releases (for tags)

**Security Features:**

- Secrets are only used on trusted events (push to main/master, releases)
- PRs from forks cannot access secrets
- Graceful degradation if secrets are not configured
- Automatic verification before upload

### Triggering Releases

The workflow runs on:

- **Push to main/master**: Builds and signs artifacts
- **Tags matching `v*`**: Creates a GitHub release with signed artifacts
- **GitHub Releases**: Signs and uploads artifacts

Example:

```bash
# Create and push a release tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Verifying Releases

### Manual Verification

1. **Download release artifacts** from GitHub:
   - `naturalpromptxcode-x.y.z.tar.gz` (or `.whl`)
   - `naturalpromptxcode-x.y.z.tar.gz.sha256`
   - `naturalpromptxcode-x.y.z.tar.gz.asc`

2. **Import the project's public key** (if you haven't already):

```bash
# If public key is in the repository
gpg --import docs/GPG_PUBLIC_KEY.asc

# Or from a keyserver
gpg --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>
```

3. **Verify SHA256 checksum**:

```bash
python -m src.main verify-sha256 naturalpromptxcode-x.y.z.tar.gz \
  --checksum-file naturalpromptxcode-x.y.z.tar.gz.sha256

# Or using sha256sum directly
sha256sum -c naturalpromptxcode-x.y.z.tar.gz.sha256
```

4. **Verify GPG signature**:

```bash
python -m src.main verify-gpg naturalpromptxcode-x.y.z.tar.gz \
  naturalpromptxcode-x.y.z.tar.gz.asc

# Or using gpg directly
gpg --verify naturalpromptxcode-x.y.z.tar.gz.asc naturalpromptxcode-x.y.z.tar.gz
```

### Automated Verification Script

Create a verification script:

```bash
#!/bin/bash
# verify-release.sh

FILE=$1
CHECKSUM_FILE="${FILE}.sha256"
SIGNATURE_FILE="${FILE}.asc"

echo "Verifying $FILE..."

# Verify SHA256
if [ -f "$CHECKSUM_FILE" ]; then
  if sha256sum -c "$CHECKSUM_FILE"; then
    echo "✓ SHA256 checksum verified"
  else
    echo "✗ SHA256 verification failed"
    exit 1
  fi
else
  echo "⚠️  No checksum file found"
fi

# Verify GPG
if [ -f "$SIGNATURE_FILE" ]; then
  if gpg --verify "$SIGNATURE_FILE" "$FILE" 2>/dev/null; then
    echo "✓ GPG signature verified"
  else
    echo "✗ GPG signature verification failed"
    exit 1
  fi
else
  echo "⚠️  No signature file found"
fi

echo "✓ All verifications passed"
```

Usage:

```bash
chmod +x verify-release.sh
./verify-release.sh naturalpromptxcode-x.y.z.tar.gz
```

## Troubleshooting

### GPG: command not found

Install GnuPG:

```bash
# macOS
brew install gnupg

# Ubuntu/Debian
sudo apt-get install gnupg

# Windows
# Download from https://www.gnupg.org/download/
```

### GPG: signing failed: No secret key

You need to import your private key:

```bash
gpg --import private-key.asc
```

### GPG: signing failed: Inappropriate ioctl for device

Use the `--passphrase` option or set the passphrase mode:

```bash
export GPG_TTY=$(tty)
```

### Verification failed: No public key

Import the public key first:

```bash
gpg --import public-key.asc
```

### SHA256 mismatch

The file has been modified or corrupted. Do not use it. Download again from a trusted source.

### GitHub Actions: Secrets not available

Ensure:
1. Secrets are added to repository settings
2. Workflow has permission to access secrets
3. You're not running on a PR from a fork

## Best Practices

1. **Always verify downloads** before using them
2. **Keep private keys secure** - never commit them to repositories
3. **Use strong passphrases** for GPG keys
4. **Set key expiration dates** and rotate keys regularly
5. **Back up your keys** in a secure location
6. **Document your key fingerprint** in project documentation
7. **Use separate keys** for different projects (optional)
8. **Test verification** before distributing signed artifacts

## References

- [GnuPG Documentation](https://www.gnupg.org/documentation/)
- [GitHub Actions Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [SHA-256 on Wikipedia](https://en.wikipedia.org/wiki/SHA-2)
- [Digital Signature on Wikipedia](https://en.wikipedia.org/wiki/Digital_signature)
