%global __os_install_post %{nil}

# Python major version.
%{expand: %%global pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Fast data loader for PostgreSQL
Name:		pgloader
Version:	3.3.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgloader.io
Source0:	https://github.com/dimitri/%{name}/releases/download/v%{version}/%{name}-bundle-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python sbcl
Requires:	python-psycopg2

%description
pgloader imports data from different kind of sources and COPY it into
PostgreSQL.

The command language is described in the manual page and allows to describe
where to find the data source, its format, and to describe data processing
and transformation.

Supported source formats include SQL Server, CSV, fixed width flat files,
dBase3 files (DBF), and SQLite and MySQL databases. In most of those formats,
pgloader is able to auto-discover the schema and create the tables and the
indexes in PostgreSQL. In the MySQL case it's possible to edit CASTing rules
from the pgloader command directly.

%prep
%setup -q -n %{name}-bundle-%{version}
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
install -m 755 -d %{buildroot}/%{_bindir}
install -m 755 -d %{buildroot}/%{_docdir}/%{name}
install -m 755 -d %{buildroot}/%{_mandir}/man1
%{__mv} bin/%{name} %{buildroot}/%{_bindir}/%{name}
%{__mv} local-projects/%{name}-%{version}/docs/dist \
	local-projects/%{name}-%{version}/docs/howto \
	local-projects/%{name}-%{version}/docs/src \
	local-projects/%{name}-%{version}/docs/*.html \
	%{buildroot}/%{_docdir}/%{name}
%{__mv} local-projects/%{name}-%{version}/%{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1

%clean
%{__rm} -rf %{buildroot}

%files
%doc README.md
%doc %{_docdir}/%{name}/*
%{_mandir}/man1/%{name}.1
%{_bindir}/%{name}

%changelog
* Mon Aug 29 2016 Devrim Gunduz <devrim@gunduz.org> 3.3.1-1
- Update to 3.3.1 (bundle release)

* Tue Jul 28 2009 Devrim Gunduz <devrim@gunduz.org> 2.3.2-1
- Update to 2.3.2

* Sun Jun 15 2008 Devrim Gunduz <devrim@gunduz.org> 2.3.1-1
- Update to 2.3.1

* Wed Apr 9 2008 Devrim Gunduz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Various spec file fixes

* Fri Feb 1 2008 Devrim Gunduz <devrim@gunduz.org> 2.2.6-1
- Update to 2.2.6

* Sat Jan 19 2008 Devrim Gunduz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5

* Thu Jun 21 2007 Devrim Gunduz <devrim@gunduz.org> 2.2.0-1
- Initial packaging
