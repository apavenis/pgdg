# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:

# Major Contributors:
# ---------------
# Tom Lane
# Devrim Gunduz
# Peter Eisentraut

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?upstreamserver:%define upstreamver	8.4-703}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	8.4.703
Release:	1PGDG%{?dist}
BuildArch:	noarch
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source3:	http://jdbc.postgresql.org/download/postgresql-%{upstreamver}.jdbc3.jar
Source4:	http://jdbc.postgresql.org/download/postgresql-%{upstreamver}.jdbc4.jar

BuildRoot:	%{_tmppath}/%{name}-%{upstreamver}-%{release}-root-%(%{__id_u} -n)

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_javadir}
install -m 755 %{SOURCE3} %{buildroot}%{_javadir}
install -m 755 %{SOURCE4} %{buildroot}%{_javadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_javadir}/postgresql-%{upstreamver}.jdbc3.jar
%{_javadir}/postgresql-%{upstreamver}.jdbc4.jar

%changelog
* Mon Sep 19 2011 Devrim G??ND??Z <devrim@gunduz.org> 0:8.4.703-1PGDG
- Update to build 703

* Mon Oct 4 2010 Devrim G??ND??Z <devrim@gunduz.org> 0:8.4.702-1PGDG
- Update to build 702

* Tue Jul 28 2009 Devrim Gunduz <devrim@gunduz.org> 0:8.4.701-1PGDG??  
- Update to build 701

* Mon Apr 6 2009 Devrim Gunduz <devrim@gunduz.org> 0:8.4dev.700-1PGDG
- Update to build 700 for 8.4 beta

* Wed Nov 19 2008 Devrim Gunduz <devrim@gunduz.org> 0:8.3.604-1PGDG
- Update to build 604

* Tue Mar 4 2008 Devrim Gunduz <devrim@gunduz.org> 0:8.3.603-1PGDG
- Use non-src versions for EL-4 and EL-5, they don't have build 
  environment from source.
