Name:		pgdg-fedora
Version:	8.0
Release:	5
Summary:	PostgreSQL 8.0.X PGDG RPMs for Fedora - Yum Repository Configuration
Group:		System Environment/Base 
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-80-fedora.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	fedora-release

%description
This package contains yum configuration for Fedora, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T
#install -pm 644 %{SOURCE0} .
#install -pm 644 %{SOURCE1} .

%build

%install
rm -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
rm -rf %{buildroot}

%post
rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Tue Mar 02 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 8.0-5
- Bump up version for the new repo URL.

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@gunduz.org> - 8.0-4
- Rebuilt

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@gunduz.org> - 8.0-3
- Enable srpms

* Tue Mar 11 2008 Devrim GUNDUZ <devrim@gunduz.org> - 8.0-2
- Enable gpgcheck

* Mon Oct 8 2007 Devrim GUNDUZ <devrim@gunduz.org> - 8.0-1
- Initial packaging for PostgreSQL Global Development Group RPMs
