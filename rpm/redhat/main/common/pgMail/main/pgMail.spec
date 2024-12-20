Summary:	Send email from inside a PostgreSQL Database
Name:		pgMail
Version:	1.5
Release:	1PGDG%{?dist}
License:	Apache
Source0:	https://github.com/captbrando/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/captbrando/%{name}

BuildArch:	noarch

%description
pgMail is simply a stored function written in TCL which takes 4
arguments of type 'text' (Who is it from, who is it to, subject, and
body of message), contacts the email server via TCL sockets, and
transmits your email (Now UTF-8 Compatible!).

Before you can use pgMail, you must install the TCL/u procedural
language. TCL/u is an UNRESTRICTED version of TCL that the database may
use in its stored functions.
** Take into account that you must prepare adequate security precautions
when adding the TCL/u language to your database! The author will not be
responsible for misconfigured servers allowing dangerous users to do bad things.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_datadir}/%{name}/
%{__install} -m 644 *.sql %{buildroot}%{_datadir}/%{name}/

%files
%defattr(644,root,root,755)
%doc README
%{_datadir}/%{name}/*.sql

%changelog
* Wed Dec 11 2024 Devrim Gündüz <devrim@gunduz.org> - 1.5-1PGDG
- Update to 1.5 per changes described at:
  https://github.com/captbrando/pgMail/releases/tag/v1.5

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4-2PGDG
- Add PGDG branding
- Spec file cleanup

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4-1.1
- Rebuild against PostgreSQL 11.0

* Thu Nov 16 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Initial packaging for PostgreSQL RPM Repository
