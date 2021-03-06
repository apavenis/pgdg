Name:		pgdg-redhat
Version:	8.2
Release:	6
Summary:	PostgreSQL 8.2.X PGDG RPMs for RHEL - Yum Repository Configuration
Group:		System Environment/Base 
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-82-redhat.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	redhat-release

%description
This package contains yum configuration for RHEL, and also the GPG
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
* Mon Sep 26 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 8.2-6
- Use https://yum.postgresql.org as the new repo URL..

* Tue Mar 02 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 8.2-5
- Bump up version for the new repo URL.

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@gunduz.org> - 8.2-4
- Rebuilt

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@gunduz.org> - 8.2-3
- Enable srpms

* Tue Mar 11 2008 Devrim GUNDUZ <devrim@gunduz.org> - 8.2-2
- Enable gpgcheck

* Mon Oct 8 2007 Devrim GUNDUZ <devrim@gunduz.org> - 8.2-1
- Initial packaging for PostgreSQL Global Development Group RPMs
