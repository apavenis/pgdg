%if 0%{?rhel} && 0%{?rhel} <= 6
%global systemd_enabled 0
%else
%global systemd_enabled 1
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
%global systemd_enabled 1
%endif
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Name:		pgbouncer
Version:	1.15.0
Release:	2%{?dist}
Summary:	Lightweight connection pooler for PostgreSQL
License:	MIT and BSD
URL:		https://www.pgbouncer.org/
Source0:	https://www.pgbouncer.org/downloads/files/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}.service
Source5:	%{name}.service.rhel7
Patch0:		%{name}-ini.patch
Patch1:		%{name}-mkauth-py3.patch

BuildRequires:	pgdg-srpm-macros
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libevent-devel
Requires:	libevent-devel
%endif
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
BuildRequires:	libevent2-devel >= 2.0
Requires:	libevent2 >= 2.0
Requires:	python-psycopg2
Requires:	initscripts
%else
BuildRequires:	libevent-devel >= 2.0
Requires:	libevent >= 2.0
Requires:	python3-psycopg2
%endif
BuildRequires:	openssl-devel pam-devel

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
BuildRequires:	c-ares-devel >= 1.11
Requires:	c-ares >= 1.11
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	c-ares-devel >= 1.11
Requires:	libcares2 >= 1.11
%endif

%if %{systemd_enabled}
BuildRequires:		systemd
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif
%else
Requires(post):		chkconfig
Requires(preun):	chkconfig
# This is for /sbin/service
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif
Requires:	/usr/sbin/useradd

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_min_requires
%endif
%endif

%description
pgbouncer is a lightweight connection pooler for PostgreSQL.
pgbouncer uses libevent for low-level socket handling.

%prep
%setup -q
%patch0 -p0
%if 0%{?rhel} && 0%{?rhel} <= 6
:
%else
%patch1 -p0
%endif


%build
sed -i.fedora \
 -e 's|-fomit-frame-pointer||' \
 -e '/BININSTALL/s|-s||' \
 configure

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
	%pgdg_set_ppc64le_compiler_flags
%endif
%endif

# Building with systemd flag tries to enable notify support which is not
# available on RHEL/CentOS 7, so use the flag on RHEL 8 and Fedora.
%configure \
	--datadir=%{_datadir} --disable-evdns \
%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1500
	--with-cares \
	--with-systemd \
%endif
	--with-pam

%{__make} %{?_smp_mflags} V=1

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Install sysconfig file
%{__install} -p -d %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -p -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/%{name}
%{__install} -p -m 700 etc/mkauth.py %{buildroot}%{_sysconfdir}/%{name}/

%if %{systemd_enabled}
%{__install} -d %{buildroot}%{_unitdir}
%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%{__install} -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}.service
%else
%{__install} -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.service
%endif

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{name} 0700 pgbouncer pgbouncer -
EOF

%else
%{__install} -p -d %{buildroot}%{_initrddir}
%{__install} -p -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif

# Create the directory for the pid files (defined in pgbouncer.ini)
%{__install} -d -m 755 %{buildroot}/var/run/%{name}

# Install logrotate file:
%{__install} -p -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# It seems we need to do this manually on SuSE:
%if 0%{?suse_version}
%{__mkdir} -p %{buildroot}%{_defaultdocdir}
%{__mv} %{buildroot}/usr/share/doc/%{name} %{buildroot}%{_defaultdocdir}/
%endif

%post
%if %{systemd_enabled}
%systemd_post %{name}.service
%else
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add %{name}
%endif
if [ ! -d %{_localstatedir}/log/pgbouncer ] ; then
%{__mkdir} -m 700 %{_localstatedir}/log/pgbouncer
fi
%{__chown} -R pgbouncer:pgbouncer %{_localstatedir}/log/pgbouncer
%{__chown} -R pgbouncer:pgbouncer %{_rundir}/%{name} >/dev/null 2>&1 || :

%pre
groupadd -r pgbouncer >/dev/null 2>&1 || :
useradd -m -g pgbouncer -r -s /bin/bash \
	-c "PgBouncer Server" pgbouncer >/dev/null 2>&1 || :

%preun
%if %{systemd_enabled}
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ] ; then
	/sbin/service pgbouncer condstop >/dev/null 2>&1
	chkconfig --del pgbouncer
fi
%endif

%postun
if [ $1 -eq 0 ]; then
%{__rm} -rf %{_rundir}/%{name}
fi
%if %{systemd_enabled}
%systemd_postun_with_restart %{name}.service
%else
if [ $1 -ge 1 ] ; then
	/sbin/service pgbouncer condrestart >/dev/null 2>&1 || :
fi
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%doc %{_defaultdocdir}/pgbouncer
%if %{systemd_enabled}
%license COPYRIGHT
%endif
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%if %{systemd_enabled}
%ghost %{_rundir}/%{name}
%{_tmpfilesdir}/%{name}.conf
%attr(644,root,root) %{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_sysconfdir}/%{name}/mkauth.py*
%attr(755,pgbouncer,pgbouncer) %dir /var/run/%{name}

%changelog
* Fri Feb 12 2021 Devrim G??nd??z <devrim@gunduz.org> - 1.15.0-2
- Fix SLES 15 dependency.

* Thu Aug 13 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.15.0-1
- Update to 1.15.0, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-115x

* Thu Aug 13 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.14.0-3
- Build with systemd support, per
  https://bugzilla.redhat.com/show_bug.cgi?id=1858814

* Fri Aug 7 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.14.0-2
- Fix RHEL 6 dependency, per PG bug 16573.

* Thu Jun 11 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.14.0-1
- Update to 1.14.0

* Wed Apr 29 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.13.0-1
- Update to 1.13.0
- Switch to pgdg-srpm-macros

* Wed Feb 26 2020 Devrim G??nd??z <devrim@gunduz.org> - 1.12.0-4
- Fix c-ares support. Per Peter:
  https://redmine.postgresql.org/issues/4808

* Thu Dec 19 2019 - John Harvey <john.harvey@crunchydata.com> 1.12.0-3
- Make sure that directory /var/run/pgbouncer is created with the RPM.
  This will ensure that pgbouncer.ini will work with its defaults.

* Thu Oct 17 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.12.0-2
- Use python3-psycopg2 as the dependency. instead of python-psycopg2.
  This will help us to solve conflict on Fedora 31 and onwards.
  All supported distros have this dependency anyway.

* Thu Oct 17 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.12.0-1
- Update to 1.12.0

* Tue Aug 27 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.11.0-1
- Update to 1.11.0

* Tue Jul 2 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.10.0-1
- Update to 1.10.0

* Thu Jun 27 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.9.0-3
- Change/Fix pgBouncer systemd configuration, per Peter:
  https://redmine.postgresql.org/issues/4398

* Fri Apr 12 2019 Devrim G??nd??z <devrim@gunduz.org> - 1.9.0-2
- Fix tmpfiles.d directory.

* Mon Oct 15 2018 Devrim G??nd??z <devrim@gunduz.org> - 1.9.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 21 2018 Devrim G??nd??z <devrim@gunduz.org> - 1.9.0-1
- Update to 1.9.0

* Fri Mar 2 2018 Devrim G??nd??z <devrim@gunduz.org> - 1.8.1-2
- Add python-psycopg2 as requires, for mkauth.py

* Wed Dec 20 2017 Devrim G??nd??z <devrim@gunduz.org> - 1.8.1-1
- Update to 1.8.1, and enable pam support.

* Tue Jul 18 2017 Devrim G??nd??z <devrim@gunduz.org> - 1.7.2-7
- Add libevent dependency, per Fahar Abbas (EDB QA testing)

* Wed Sep 28 2016 Devrim G??nd??z <devrim@gunduz.org> - 1.7.2-6
- Depend on libevent2 on RHEL 6, which is available as of
  RHEL 6.8. This change means we ask all users to upgrade to
  at least to RHEL 6.8. We require this for other packages already,
  so it should not be an issue. This also will eliminate the need
  for compat-libevent14 package that we ship in our repo. Fixes #1718.

* Tue Aug 9 2016 Devrim G??nd??z <devrim@gunduz.org> - 1.7.2-5
- Switch to c-ares. Per Omar Kilani. Fixes #1444

* Mon Jul 18 2016 Devrim G??nd??z <devrim@gunduz.org> - 1.7.2-4
- Don't remove /var/run/pgbouncer directory on upgrade. Per
  report from Eric Radman.
- Attempt to create the log directory only if does not exist.

* Thu Jul 7 2016 Devrim G??nd??z <devrim@gunduz.org> - 1.7.2-3
- Fix issues in systemd file, per report from Jehan-Guillaume,
  per #1339.

* Wed Mar 30 2016 Devrim G??nd??z <devrim@gunduz.org> - 1.7.2-2
- Fix Reload in systemd unit file, per #1042.
  Analysis and fix by Jehan-Guillaume de Rorthais.

* Tue Mar 15 2016 Devrim G??nd??z <devrim@gunduz.org> - 1.7.2-1
- Update to 1.7.2, per #1033.

* Mon Feb 22 2016 Devrim G??nd??z <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1, per #1011.
- Fix wrong log file name in sysconfig file, per #1008.
- Add openssl-devel as BR.
- Fix logrotate file, per #1009.

* Wed Dec 30 2015 Devrim G??nd??z <devrim@gunduz.org> - 1.7-1
- Update to 1.7

* Mon Sep 7 2015 Devrim G??nd??z <devrim@gunduz.org> - 1.6.1-1
- Update to 1.6.1
- Fix startup issues: The tmpfiles.d file was not created
  correctly, causing startup failures due to permissions.
- Fix systemd file: Use -q, not -v.

* Tue May 12 2015 Devrim G??nd??z <devrim@gunduz.org> - 1.5.5-2
- Fix service file, per Peter Eisentraut.
- Fix permissions of unit file and logrotate conf file. Per
  Peter Eisentraut.
- Fix logrotate configuration. Per Peter Eisentraut.
- Apply some spec file fixes so that we can use it on all
  platforms.

* Fri Apr 17 2015 Devrim G??nd??z <devrim@gunduz.org> - 1.5.5-1
- Update to 1.5.5
- Update to new URL
- Revert chown'ing /etc/pgbouncer to pgbouncer user, and keep
  it as root.
- Add systemd support, and convert the spec file to unified
  spec file for all platforms

* Mon May 19 2014 Devrim G??nd??z <devrim@gunduz.org> - 1.5.4-3
- Add logrotate file. It was already available in svn, but
  apparently I forgot to add it to spec file. Per an email from
  Jens Wilke.
- Change ownership of /etc/pgbouncer directory, to pgbouncer user.
  Per Jens Wilke.

* Mon Sep 16 2013 Devrim G??nd??z <devrim@gunduz.org> - 1.5.4-2
- Update init script, per #138, which fixes the following.
  Contributed by Peter:
 - various legacy code of unknown purpose
 - no LSB header
 - used the script name as NAME, making it impossible to copy
   the script and run two pgbouncers
 - didn't use provided functions like daemon and killproc
 - incorrect exit codes when starting already started service and
   stopping already stopped service (nonstandard condstop action
   was a partial workaround?)
 - restart didn't make use of pgbouncer -R option

* Mon Dec 10 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5.4-1
- Update to 1.5.4

* Wed Sep 12 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3, per changes described at:
  http://pgfoundry.org/forum/forum.php?forum_id=1981

* Tue Jul 31 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5.2-3
- Add mkauth.py among installed files.

* Thu Jun 21 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5.2-2
- Fix useradd line.

* Tue Jun 5 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2, per changes described at:
  http://pgfoundry.org/forum/forum.php?forum_id=1885

* Tue May 15 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Sun Apr 08 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5-2
-  Fix shell of pgbouncer user, to avoid startup errors.

* Fri Apr 6 2012 Devrim G??nd??z <devrim@gunduz.org> - 1.5-1
- Update to 1.5, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1920
- Trim changelog

* Fri Aug 12 2011 Devrim G??nd??z <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1863

* Mon Sep 13 2010 Devrim G??nd??z <devrim@gunduz.org> - 1.3.4-1
- Update to 1.3.4, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?prelease_id=1698
* Fri Aug 06 2010 Devrim G??nd??z <devrim@gunduz.org> - 1.3.3-2
- Sleep 2 seconds before getting pid during start(), like we do in PostgreSQL
  init script, to avoid false positive startup errors.

* Tue May 11 2010 Devrim G??nd??z <devrim@gunduz.org> - 1.3.3-1
- Update to 1.3.3, per pgrpms.org #25, for the fixes described at:
  http://pgfoundry.org/frs/shownotes.php?release_id=1645

* Tue Mar 16 2010 Devrim G??nd??z <devrim@gunduz.org> - 1.3.2-1
- Fix some issues in init script. Fixes pgrpms.org #9.
