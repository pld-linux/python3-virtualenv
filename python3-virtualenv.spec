#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (not in sdist)
%bcond_without	tests	# pytest tests

%define module	virtualenv
Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Name:		python3-virtualenv
Version:	20.29.3
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: https://pypi.org/simple/virtualenv/
Source0:	https://files.pythonhosted.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
# Source0-md5:	828e9e88af0976c3230c4af5157e191b
Patch0:		multilib.patch
URL:		https://pypi.org/project/virtualenv/
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-build
BuildRequires:	python3-hatch-vcs >= 0.3
BuildRequires:	python3-hatchling >= 1.17.1
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
# runtime dependencies
BuildRequires:	python3-distlib >= 0.3.7
BuildRequires:	python3-distlib < 1
BuildRequires:	python3-filelock >= 3.12.2
BuildRequires:	python3-filelock < 4
BuildRequires:	python3-platformdirs >= 3.9.1
BuildRequires:	python3-platformdirs < 5
# test-only dependencies
BuildRequires:	python3-flaky >= 3.7
BuildRequires:	python3-packaging >= 23.1
BuildRequires:	python3-pytest >= 7.4
BuildRequires:	python3-pytest-env >= 0.8.2
BuildRequires:	python3-pytest-mock >= 3.11.1
BuildRequires:	python3-pytest-randomly >= 3.12
BuildRequires:	python3-pytest-timeout >= 2.1
BuildRequires:	python3-setuptools >= 1:68
BuildRequires:	python3-time-machine >= 2.10
# coverage
#BuildRequires:	python3-covdefaults >= 2.3
#BuildRequires:	python3-coverage >= 7.2.7
#BuildRequires:	python3-coverage-enable-subprocess >= 1
%endif
%if %{with doc}
BuildRequires:	python3-furo >= 2023.7.26
BuildRequires:	python3-sphinx_argparse >= 0.4
BuildRequires:	python3-sphinxcontrib-towncrier >= 0.2.1a0
BuildRequires:	python3-proselint >= 0.13
BuildRequires:	python3-towncrier >= 23.6
BuildRequires:	sphinx-pdg >= 7.1.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.8
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
# disabled test cases (2*2 variants) use network to populate venv
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=flaky.flaky_pytest_plugin,pytest_mock.plugin,time_machine \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_can_build_c_extensions and not test_seed_link_via_app_data'
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
