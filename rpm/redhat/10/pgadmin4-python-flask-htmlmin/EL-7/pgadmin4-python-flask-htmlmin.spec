%if 0%{?fedora} > 23
%{!?with_python3:%global with_python3 1}
%global __ospython3 %{_bindir}/python3
%{expand: %%global py3ver %(echo `%{__ospython3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%else
%{!?with_python3:%global with_python3 0}
%global __ospython2 %{_bindir}/python2
%{expand: %%global py2ver %(echo `%{__ospython2} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python2_sitelib %(%{__ospython2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%global sname	flask-htmlmin
%global mod_name	Flask-HTMLmin

%if 0%{?with_python3}
Name:		python3-%{sname}
%else
Name:		python-%{sname}
%endif

Version:	1.2
Release:	4%{?dist}
Summary:	Flask html response minifier
Group:		Development/Libraries
License:	BSD
URL:		https://github.com/hamidfzm/%{mod_name}/
Source0:	https://github.com/hamidfzm/%{mod_name}/archive/v%{version}.tar.gz
BuildArch:	noarch
%if 0%{?with_python3}
Requires:	python3-htmlmin
%else
Requires:	python-htmlmin
%endif

%if 0%{?with_python3}
%{?python_provide:%python_provide python3-%{sname}}
%else
%{?python_provide:%python_provide python-%{sname}}
%endif

%description
Minify flask text/html mime types responses. Just add MINIFY_PAGE = True to
your deployment config to minify html and text responses of your flask
application.

%prep
%setup -q -n %{mod_name}-%{version}

%if 0%{?with_python3}
%{__rm} -rf %{py3dir}
%{__cp} -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
%{__ospython3} setup.py build
%else
%{__ospython2} setup.py build
%endif

%install
%{__rm} -rf %{buildroot}

%if 0%{?with_python3}
%{__ospython3} setup.py install -O1 --skip-build --root %{buildroot}
%else
%{__ospython2} setup.py install --skip-build --root %{buildroot}
%endif

%files
%doc LICENSE README.md
%if 0%{?with_python3}
%{python3_sitelib}/Flask_HTMLmin*.egg-info/
%{python3_sitelib}/flask_htmlmin.py*
%{python3_sitelib}/__pycache__/flask_htmlmin.cpython-*.pyc
%else
%{python2_sitelib}/Flask_HTMLmin*.egg-info/
%{python2_sitelib}/flask_htmlmin.py*
%endif

%changelog
* Thu Apr 13 2017 Devrim Gündüz <devrim@gunduz.org> - 1.2-4
- Move the components under pgadmin web directory, per #2332.

* Fri Feb 17 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-3
- Another attempt to fix python3-htmlmin dependency on Fedora 24+

* Fri Feb 17 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-2
- Bump up package version for python-htmlmin dependency.

* Mon Feb 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Initial packaging for pgadmin4.
