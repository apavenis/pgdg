Name:		pgagroal
Version:	0.9.1
Release:	1%{dist}
Summary:	High-performance connection pool for PostgreSQL
License:	BSD
URL:		https://github.com/agroal/%{name}
Source0:	https://github.com/agroal/%{name}/archive/%{version}.tar.gz

BuildRequires:	gcc cmake make python3-docutils
BuildRequires:	libev libev-devel openssl openssl-devel
BuildRequires:	systemd systemd-devel chrpath
Requires:	libev openssl systemd

%description
pgagroal is a high-performance connection pool for PostgreSQL.

%prep
%setup -q

%build

%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
%{__make}

%install
%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__mkdir} -p %{buildroot}%{_libdir}
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/etc
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/images
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__mkdir} -p %{buildroot}%{_mandir}/man5
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}

%{__install} -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE
%{__install} -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/ARCHITECTURE.md %{buildroot}%{_docdir}/%{name}/ARCHITECTURE.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/CONFIGURATION.md %{buildroot}%{_docdir}/%{name}/CONFIGURATION.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/FAILOVER.md %{buildroot}%{_docdir}/%{name}/FAILOVER.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/GETTING_STARTED.md %{buildroot}%{_docdir}/%{name}/GETTING_STARTED.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/PERFORMANCE.md %{buildroot}%{_docdir}/%{name}/PERFORMANCE.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/PIPELINES.md %{buildroot}%{_docdir}/%{name}/PIPELINES.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/RPM.md %{buildroot}%{_docdir}/%{name}/RPM.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/SECURITY.md %{buildroot}%{_docdir}/%{name}/SECURITY.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-extended.png %{buildroot}%{_docdir}/%{name}/images/perf-extended.png
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-prepared.png %{buildroot}%{_docdir}/%{name}/images/perf-prepared.png
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-readonly.png %{buildroot}%{_docdir}/%{name}/images/perf-readonly.png
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/images/perf-simple.png %{buildroot}%{_docdir}/%{name}/images/perf-simple.png

%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}_hba.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}_hba.conf

%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}-admin.1 %{buildroot}%{_mandir}/man1/%{name}-admin.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}-cli.1 %{buildroot}%{_mandir}/man1/%{name}-cli.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}.conf.5 %{buildroot}%{_mandir}/man5/%{name}.conf.5
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}_databases.conf.5 %{buildroot}%{_mandir}/man5/%{name}_databases.conf.5
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}_hba.conf.5 %{buildroot}%{_mandir}/man5/%{name}_hba.conf.5

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name}-admin %{buildroot}%{_bindir}/%{name}-admin

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/libpgagroal.so.%{version} %{buildroot}%{_libdir}/libpgagroal.so.%{version}


# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.service %{buildroot}%{_unitdir}/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.socket %{buildroot}%{_unitdir}/
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{sname} 0755 root root -
EOF

chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}
chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}-cli
chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}-admin

cd %{buildroot}%{_libdir}/
%{__ln_s} -f libpgagroal.so.%{version} libpgagroal.so.0
%{__ln_s} -f libpgagroal.so.0 libpgagroal.so

%post
if [ $1 -eq 1 ] ; then
%systemd_post %{name}.service
fi

%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%license %{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/*.md
%{_docdir}/%{name}/SECURITY.md
%{_docdir}/%{name}/images/*.png
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-admin.1*
%{_mandir}/man1/%{name}-cli.1*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man5/%{name}_databases.conf.5*
%{_mandir}/man5/%{name}_hba.conf.5*
%config %{_sysconfdir}/%{name}/%{name}.conf
%config %{_sysconfdir}/%{name}/%{name}_hba.conf
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-admin
%{_libdir}/libpgagroal.so
%{_libdir}/libpgagroal.so.0
%{_libdir}/libpgagroal.so.%{version}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket

%changelog
* Tue Oct 14 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-1
- Update to 0.9.1

* Tue Sep 29 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-2
- Install systemd related files under their actual directory,
  and improve systemd support.
- Use macros more.

* Tue Sep 22 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-1
- Update to 0.9.0

* Wed Sep 2 2020 Devrim Gündüz <devrim@gunduz.org> - 0.8.2-1
- Update to 0.8.2

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-1
- Update to 0.8.1

* Tue Aug 4 2020 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-1
- Update to 0.8.0

* Tue Jul 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.3-1
- Update to 0.7.3

* Wed Jun 10 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-1
- Update to 0.7.1

* Wed May 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1
- Update to 0.7.0

* Fri May 1 2020 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1
- Update to 0.6.0

* Fri Apr 17 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1
- Update to 0.5.1

* Tue Mar 24 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1
- Initial packaging for PostgreSQL RPM repository, per upstream spec.
