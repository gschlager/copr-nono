Name:           nono
Version:        0.4.0
Release:        1%{?dist}
Summary:        Secure, kernel-enforced sandbox for AI agents and MCP workloads

License:        Apache-2.0
URL:            https://github.com/always-further/nono
Source0:        https://github.com/always-further/nono/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust >= 1.70
BuildRequires:  cargo
BuildRequires:  dbus-devel
BuildRequires:  pkgconfig(dbus-1)

# Disable automatic dependency generation for Rust
%global __requires_exclude ^lib.*\\.so.*$
%global __provides_exclude_from ^%{_libdir}/.*$

# Disable debug package
%global debug_package %{nil}

%description
nono is a secure, kernel-enforced capability shell for running AI agents and 
any POSIX style process. Unlike policy-based sandboxes that intercept and 
filter operations, nono leverages OS security primitives (Landlock on Linux, 
Seatbelt on macOS) to create an environment where unauthorized operations are 
structurally impossible.

Features:
- No escape hatch - Once inside nono, there is no mechanism to bypass restrictions
- Agent agnostic - Works with any AI agent or process
- OS-level enforcement - Kernel denies unauthorized operations
- Destructive command blocking - Blocks dangerous commands by default
- Secure credential injection - API keys and secrets are injected securely

%prep
%autosetup -n %{name}-%{version}

%build
# Build with cargo in release mode
cargo build --release --locked

%install
# Install the binary
install -D -m 755 target/release/nono %{buildroot}%{_bindir}/nono

# Install documentation
install -D -m 644 README.md %{buildroot}%{_docdir}/%{name}/README.md

%check
# Run basic smoke test
%{buildroot}%{_bindir}/nono --version

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/nono
%{_docdir}/%{name}/README.md

%changelog
* Mon Mar 30 2026 Gerhard Schlager - 0.4.0-1
- Initial RPM package for nono
- Automated builds via COPR
