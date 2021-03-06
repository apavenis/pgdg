Name:		pgdg-oraclelinux90
Version:	9.0
Release:	6
Summary:	PostgreSQL 9.0.X PGDG RPMs for Oracle Linux - Yum Repository Configuration
Group:		System Environment/Base
License:	BSD
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/RPM-GPG-KEY-PGDG-90
Source2:	pgdg-90-oraclelinux.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	oraclelinux-release

%description
This package contains yum configuration for Oracle Linux, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
rm -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-90

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
rm -rf %{buildroot}

%post
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-90

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Wed Oct 21 2015 Devrim Gündüz <devrim@gunduz.org> - 9.0-6
- Point the download URL in repo file to new location.

* Tue Apr 29 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0-5
- Initial support for Oracle Linux

* Fri Sep 23 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0-4
- Use yum.postgresql.org as the new repo URL.
- Change the package name, and add PostgreSQL major version number.
  This will let us install the repo RPMs easier. Also, rename RPM key,
  so that --import won't throw any errors.
- Own %%{_sysconfdir}/pki/rpm-gpg
- Trim changelog

* Mon Jan 10 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0-3
- Use full path for rpm command. Noted while testing 9.0 live CD.

* Tue Mar 02 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0-2
- Bump up version for the new repo URL.

* Fri Jan 22 2010 Devrim GUNDUZ <devrim@gunduz.org> - 9.0-1
- 8.5 is now 9.0
