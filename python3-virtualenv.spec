# TODO: finish doc and tests (BRs)
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# pytest tests

%define module	virtualenv
Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Name:		python3-virtualenv
Version:	20.29.3
Release:	1
License:	MIT
Group:		Development/Languages
#Source0Download: https://pypi.org/simple/virtualenv/
Source0:	https://files.pythonhosted.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
# Source0-md5:	828e9e88af0976c3230c4af5157e191b
Patch0:		multilib.patch
URL:		https://pypi.org/project/virtualenv/
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-hatchling
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-hatch_vcs
%if %{with tests}
# runtime dependencies
BuildRequires:	python3-distlib >= 0.3.1
BuildRequires:	python3-distlib < 1
BuildRequires:	python3-filelock >= 3.2
BuildRequires:	python3-filelock < 4
BuildRequires:	python3-platformdirs >= 2
BuildRequires:	python3-platformdirs < 3
BuildRequires:	python3-pytest
BuildRequires:	python3-six >= 1.9
BuildRequires:	python3-six < 2
# test-only dependencies
BuildRequires:	python-coverage >= 4
BuildRequires:	python-coverage-enable-subprocess >= 1
BuildRequires:	python-flaky >= 3
BuildRequires:	python-packaging >= 20.0
BuildRequires:	python-pytest >= 4
BuildRequires:	python-pytest-env >= 0.6.2
BuildRequires:	python-pytest-freezegun >= 0.4.1
BuildRequires:	python-pytest-mock >= 2
BuildRequires:	python-pytest-randomly >= 1
BuildRequires:	python-pytest-timeout >= 1
%endif
%if %{with doc}
BuildRequires:	python3-sphinx-argparse >= 0.2.5
BuildRequires:	python3-sphinx_rtd_theme >= 0.4.3
BuildRequires:	python3-proselint >= 0.10.2
BuildRequires:	python3-towncrier >= 21.3
BuildRequires:	sphinx-pdg >= 3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-distlib >= 0.3.1
Requires:	python3-filelock >= 3.2
Requires:	python3-modules >= 1:3.8
Requires:	python3-platformdirs >= 2
# for virtualenv-3 wrapper
Requires:	python3-setuptools
Requires:	python3-six >= 1.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtualenv is a tool to create isolated Python environments.
virtualenv is a successor to workingenv, and an extension of
virtual-python. It is written by Ian Bicking, and sponsored by the
Open Planning Project. It is licensed under an MIT-style permissive
license.

%description -l pl.UTF-8
virtualenv to narzędzie do tworzenia oddzielonych środowisk Pythona.
Jest to następca workignenv i rozszerzenie virtual-pythona. Jest
tworzone przez Iana Bickinga i sponsorowane przez Open Planning
Project. Zostało wydane na liberalnej licencji w stylu MIT.

%package -n virtualenv
Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Group:		Libraries/Python
Requires:	python3-virtualenv = %{version}-%{release}

%description -n virtualenv
virtualenv is a tool to create isolated Python environments.
virtualenv is a successor to workingenv, and an extension of
virtual-python. It is written by Ian Bicking, and sponsored by the
Open Planning Project. It is licensed under an MIT-style permissive
license.

%description -n virtualenv -l pl.UTF-8
virtualenv to narzędzie do tworzenia oddzielonych środowisk Pythona.
Jest to następca workignenv i rozszerzenie virtual-pythona. Jest
tworzone przez Iana Bickinga i sponsorowane przez Open Planning
Project. Zostało wydane na liberalnej licencji w stylu MIT.

%prep
%setup -q -n virtualenv-%{version}
%patch -P 0 -p1

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs text
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject
cp -p $RPM_BUILD_ROOT%{_bindir}/virtualenv{,-3}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md %{?with_doc:docs/_build/text/*.txt}
%attr(755,root,root) %{_bindir}/virtualenv-3
%{py3_sitescriptdir}/virtualenv
%{py3_sitescriptdir}/virtualenv-%{version}.dist-info

%files -n virtualenv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/virtualenv
