%global pgmajorversion 90

Summary:	Parallel Server for PostgreSQL
Name:		gridsql
Version:	2.0
Release:	0_2%{?dist}
License:	GPLv2
URL:		http://sourceforge.net/projects/gridsql/
Group:		Applications/Databases
Source0:	http://kent.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}-0.tar.gz
Source1:	http://kent.dl.sourceforge.net/sourceforge/%{name}/%{name}-client-%{version}-0.tar.gz
Source2:	http://kent.dl.sourceforge.net/sourceforge/%{name}/%{name}-agent-%{version}-0.tar.gz

Patch0:		%{name}_env.patch
Patch2:		%{name}-rpm.patch
Patch3:		%{name}-agent-rpm.patch
Patch4:		%{name}-client-rpm.patch
Patch6:		%{name}-config.patch
Patch7:		%{name}-agent-config.patch

Requires:	postgresql%{pgmajorversion}-server, postgresql%{pgmajorversion}-jdbc, java
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

%description
GridSQL is a shared-nothing clustered database system
that provides the heart of a Business Intelligence infrastructure.
It includes intelligence to maximize parallelization over multiple
servers, for querying large sets of data.

%package agent
Summary:	The agent programs needed for GridSQL
Group:		Applications/Databases
Requires:	gridsql = %{version}-%{release}

%description agent
Agent programs needed for GridSQL

%package client
Summary:	The client programs needed for GridSQL
Group:		Applications/Databases
Requires:	gridsql = %{version}-%{release}

%description client
Client programs needed for GridSQL

%package docs
Summary:	Documentation for GridSQL
Group:		Applications/Databases
Requires:	gridsql = %{version}-%{release}

%description docs
documentation for GridSQL

%prep
%setup -q -n %{name}-%{version} -c -a 2 -a 1
%patch0 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch6 -p0
%patch7 -p0

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_datadir}/java

# Install gridsql core files
pushd gridsql-2.0
install -m 755 bin/*.sh %{buildroot}%{_bindir}
install -m 755 bin/*.jar %{buildroot}%{_datadir}/java
install -m 755 config/* %{buildroot}%{_sysconfdir}/%{name}
install -m 755 lib/*.jar %{buildroot}%{_datadir}/java
install -m 644 release_notes.txt license.txt  %{buildroot}%{_docdir}/%{name}-%{version}/

install -m 755 docs/*.PDF %{buildroot}%{_docdir}/%{name}-%{version}

install -m 755 gridsql_env.sh %{buildroot}%{_bindir}

# Install gridsql agent files
cd ../gridsql-agent-2.0

install -m 755 bin/*.sh %{buildroot}%{_bindir}
install -m 755 config/* %{buildroot}%{_sysconfdir}/%{name}
install -m 755 lib/*.jar %{buildroot}%{_datadir}/java

# Install gridsql client files
cd ../gridsql-client-2.0

install -m 755 bin/*.sh %{buildroot}%{_bindir}
install -m 755 lib/*.jar %{buildroot}%{_datadir}/java

%clean
rm -rf %{buildroot}

%post
mkdir /var/log/gridsql

%files
%defattr(0755,root,root)
%{_bindir}/gs-agent.sh
%{_bindir}/gs-cmdline.sh
%{_bindir}/gs-createdb.sh
%{_bindir}/gs-createmddb.sh
%{_bindir}/gs-dbstart.sh
%{_bindir}/gs-dbstop.sh
%{_bindir}/gs-dropdb.sh
%{_bindir}/gridsql_env.sh
%{_bindir}/gs-execdb.sh
%{_bindir}/gs-impex.sh
%{_bindir}/gs-loader.sh
%{_bindir}/gs-server.sh
%{_bindir}/gs-shutdown.sh
%{_datadir}/java/edb-jdbc14.jar
%{_datadir}/java/jline-0_9_5.jar
%{_datadir}/java/log4j.jar
%{_datadir}/java/postgresql.jar
%{_datadir}/java/xdbengine.jar
%{_datadir}/java/xdbprotocol.jar
%{_datadir}/java/xdbserver.jar
%{_datadir}/java/xdbutil.jar

%doc %attr(0644,root,root) %{_docdir}/%{name}-%{version}/*.txt

%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/gridsql/gridsql.config

%files docs
%attr(0644,root,root) %{_docdir}/%{name}-%{version}/*.PDF

%files agent
%attr(0755,root,root) %{_bindir}/gs-agent.sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/gridsql/gridsql_agent.config

%files client
%attr(0755,root,root) %{_bindir}/gs-cmdline.sh

%changelog
* Mon Jan 10 2011 Devrim G??ND??Z <devrim@gunduz.org> - 2.0-0_2
- Apply explicit dependency for 9.0.

* Wed Mar 10 2010 Devrim G??ND??Z <devrim@gunduz.org> 2.0-0_1
- Update to 2.0.0

%changelog
* Tue May 12 2009 Devrim Gunduz <devrim@gunduz.org> 1.1-0beta
- Initial build
