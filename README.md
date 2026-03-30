# nono Fedora COPR Package

Automated packaging of [nono](https://github.com/always-further/nono) for Fedora via COPR.

## Installation

```bash
# Enable the COPR repository
sudo dnf copr enable gschlager/nono

# Install nono
sudo dnf install nono

# Verify installation
nono --version
```

## About

This repository automatically monitors the [always-further/nono](https://github.com/always-further/nono) repository for new releases and builds updated RPM packages on Fedora COPR.

**nono** is a secure, kernel-enforced capability shell for running AI agents and any POSIX style process. It provides:

- No escape hatch - Once inside nono, there is no mechanism to bypass restrictions
- Agent agnostic - Works with any AI agent (Claude Code, OpenCode, etc.)
- OS-level enforcement - Kernel denies unauthorized operations
- Destructive command blocking - Blocks dangerous commands by default
- Secure credential injection - API keys and secrets are injected securely

## Automation

This repository uses GitHub Actions to:

1. Check for new releases daily at 9:00 UTC
2. Download the source tarball
3. Update the spec file version
4. Build an SRPM
5. Upload to COPR for building
6. Commit the updated spec file

## Setup Instructions

If you want to fork and maintain your own COPR builds:

### 1. Create COPR Account and API Token

1. Go to https://copr.fedorainfracloud.org/
2. Sign in with FAS account
3. Go to API → Generate new token
4. Copy the token information

### 2. Create COPR Project

```bash
# Install copr-cli
sudo dnf install copr-cli

# Configure (paste your API token)
mkdir -p ~/.config
nano ~/.config/copr  # paste token info

# Create the project
copr-cli create nono \
  --chroot fedora-39-x86_64 \
  --chroot fedora-40-x86_64 \
  --chroot fedora-41-x86_64 \
  --chroot fedora-rawhide-x86_64 \
  --description "Secure, kernel-enforced sandbox for AI agents" \
  --instructions "Install: sudo dnf copr enable YOUR-USERNAME/nono && sudo dnf install nono"
```

### 3. Fork This Repository

1. Fork this repository on GitHub
2. Go to Settings → Secrets and variables → Actions
3. Add these secrets:
   - `COPR_USERNAME`: Your COPR username
   - `COPR_LOGIN`: Your FAS login (from copr config)
   - `COPR_TOKEN`: Your API token (from copr config)

### 4. Test the Workflow

1. Go to Actions tab
2. Select "Monitor nono and Build on COPR"
3. Click "Run workflow"
4. Optionally specify a version to build (e.g., `v0.4.0`)

The workflow will:
- Download the source
- Build an SRPM
- Upload to your COPR project
- COPR will build for all enabled chroots

### 5. Check Build Status

Visit: `https://copr.fedorainfracloud.org/coprs/YOUR-USERNAME/nono/builds/`

## Manual Build

To build locally:

```bash
# Install dependencies
sudo dnf install rpm-build rpmdevtools

# Setup build tree
rpmdev-setuptree

# Download source
cd ~/rpmbuild/SOURCES
wget https://github.com/always-further/nono/archive/refs/tags/v0.4.0.tar.gz

# Copy spec file
cp nono.spec ~/rpmbuild/SPECS/

# Build
cd ~/rpmbuild/SPECS
rpmbuild -ba nono.spec

# Install locally
sudo dnf install ~/rpmbuild/RPMS/x86_64/nono-*.rpm
```

## Updating

The GitHub Actions workflow runs automatically daily. When a new version of nono is released, it will:

1. Detect the new version
2. Update the spec file
3. Build and upload to COPR
4. Commit the changes back to this repo

## Troubleshooting

### Build Fails

Check the COPR build logs at:
`https://copr.fedorainfracloud.org/coprs/YOUR-USERNAME/nono/builds/`

Common issues:
- Missing BuildRequires in spec file
- Rust version too old (requires 1.70+)
- Network issues during cargo build

### GitHub Actions Fails

1. Check the Actions tab for error logs
2. Verify your COPR secrets are correct
3. Ensure your COPR project exists and is enabled

## License

This packaging repository is licensed under Apache-2.0, matching the upstream nono project.

```
Copyright 2026 Gerhard Schlager

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Related Links

- [nono upstream](https://github.com/always-further/nono)
- [nono documentation](https://nono.sh)
- [Fedora COPR](https://copr.fedorainfracloud.org/)
- [COPR documentation](https://docs.pagure.org/copr.copr/)
