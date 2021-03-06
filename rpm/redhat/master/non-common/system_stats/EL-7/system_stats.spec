%global sname system_stats

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif

Summary:	A Postgres extension for exposing system metrics such as CPU, memory and disk information
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1%{dist}
License:	AGPLv3
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v1.0.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif

%description
system_stats is a Postgres extension that provides functions to access system
level statistics that can be used for monitoring. It supports Linux, macOS and
Windows.

Note that not all values are relevant on all operating systems. In such cases
NULL is returned for affected values.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%{__make} %{?_smp_mflags}

%install
%make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/include/server/extension/%{sname}/%{sname}.h

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/*%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*/*.bc
  %endif
 %endif
%endif

%changelog
* Thu Jun 25 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
