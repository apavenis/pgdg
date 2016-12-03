%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname	pgtap

Summary:	Unit testing for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.97.0
Release:	1%{?dist}
Group:		Applications/Databases
License:	PostgreSQL
URL:		http://pgxn.org/dist/pgtap/
Source0:	http://api.pgxn.org/dist/pgtap/%{version}/pgtap-%{version}.zip
Patch0:		%{sname}-makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-server, perl-Test-Harness >= 3.0

BuildArch:	noarch

%description
pgTAP is a unit testing framework for PostgreSQL written in PL/pgSQL and
PL/SQL. It includes a comprehensive collection of TAP-emitting assertion
functions, as well as the ability to integrate with other TAP-emitting
test frameworks. It can also be used in the xUnit testing style.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 TAPSCHEMA=pgtap %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
%{__make} install USE_PGXS=1 DESTDIR=%{buildroot} %{?_smp_mflags}

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/pgtap.mmd
%{pginstdir}/share/extension/pgtap-*.sql
%{pginstdir}/share/extension/pgtap.control

%changelog
* Sat Dec 3 2016 Devrim Gündüz <devrim@gunduz.org> 0.97.0-1
- Update to 0.97.0

* Fri Mar 27 2015 Devrim Gündüz <devrim@gunduz.org> 0.95.0-1
- Update to 0.95.0

* Wed Jul 2 2014 Devrim Gündüz <devrim@gunduz.org> 0.94.0-1
- Update to 0.94.0

* Fri Apr 1 2011 Devrim Gündüz <devrim@gunduz.org> 0.25.0-1
- Update to 0.25.0

* Fri Oct 8 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-3
- Use alternatives method for binaries.
- Use %%{?_smp_mflags} macro for make.

* Thu Oct 7 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-2
- Update spec for 9.0 layout.
- TODO: Use alternatives.

* Tue Jun 15 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-1
- Update to 0.24

* Mon Dec 28 2009 Devrim Gündüz <devrim@gunduz.org> 0.23-1
- Update to 0.23

* Wed Aug 19 2009 Darrell Fuhriman <darrell@projectdx.com> 0.22-1
- initial RPM

