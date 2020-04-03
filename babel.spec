%{?scl:%scl_package babel}
%{!?scl:%global pkg_name %{name}}
%global python3_pkgversion %{nil}

%global srcname Babel
%global sum Library for internationalizing Python applications

# Bootstrap enabled permanently to disable tests due to missing dependencies
%bcond_without bootstrap

Name:           %{?scl_prefix}babel
Version:        2.7.0
Release:        11%{?dist}
Summary:        Tools for internationalizing Python applications

License:        BSD
URL:            http://babel.pocoo.org/
Source0:        https://files.pythonhosted.org/packages/source/B/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-devel
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-setuptools
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-rpm-macros
%if !%{with bootstrap}
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-pytz
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-pytest
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-freezegun
%endif

# build the documentation
BuildRequires:  make

%if !%{with bootstrap}
BuildRequires:  %{?scl_prefix}python%{python3_pkgversion}-sphinx
%endif

%description
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.


%package -n %{?scl_prefix}python%{python3_pkgversion}-babel
Summary:        %sum
Requires:       %{?scl_prefix}python%{python3_pkgversion}-setuptools
Requires:       %{?scl_prefix}python%{python3_pkgversion}-pytz

%description -n %{?scl_prefix}python%{python3_pkgversion}-babel
Babel is composed of two major parts:

* tools to build and work with gettext message catalogs

* a Python interface to the CLDR (Common Locale Data Repository),
  providing access to various locale display names, localized number
  and date formatting, etc.


%if !%{with bootstrap}
%package doc
Summary:        Documentation for Babel
Provides:       %{?scl_prefix}python-babel-doc = %{version}-%{release}
Provides:       %{?scl_prefix}python3-babel-doc = %{version}-%{release}

%description doc
Documentation for Babel
%endif


%prep
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%autosetup -n %{srcname}-%{version}
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%py3_build

BUILDDIR="$PWD/built-docs"
rm -rf "$BUILDDIR"

%if !%{with bootstrap}
pushd docs
make \
    SPHINXBUILD=sphinx-build-3 \
    BUILDDIR="$BUILDDIR" \
    html
popd
rm -f "$BUILDDIR/html/.buildinfo"
%endif
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%py3_install

mv %{buildroot}%{_bindir}/pybabel %{buildroot}%{_bindir}/pybabel-%{python3_version}
ln -s ./pybabel-%{python3_version} %{buildroot}%{_bindir}/pybabel-3
ln -s ./pybabel-3 %{buildroot}%{_bindir}/pybabel
%{?scl:EOF}


%check
%{?scl:scl enable %{scl} - << \EOF}
set -ex
export TZ=America/New_York
%if !%{with bootstrap}
%{__python3} -m pytest
%endif
%{?scl:EOF}


%files -n %{?scl_prefix}python%{python3_pkgversion}-babel
%doc CHANGES AUTHORS
%license LICENSE
%{python3_sitelib}/Babel-%{version}-py*.egg-info
%{python3_sitelib}/babel
%{_bindir}/pybabel-%{python3_version}
%{_bindir}/pybabel-3
%{_bindir}/pybabel

%if !%{with bootstrap}
%files doc
%doc built-docs/html/*
%endif


%changelog
* Mon Feb 03 2020 Tomas Orsava <torsava@redhat.com> - 2.7.0-11
- Import from the python38 module and modified for rh-python38 RHSCL
- Resolves: rhbz#1671025

* Fri Dec 13 2019 Tomas Orsava <torsava@redhat.com> - 2.7.0-10
- Exclude unsupported i686 arch

* Tue Dec 03 2019 Tomas Orsava <torsava@redhat.com> - 2.7.0-9
- Rename the pybabel executable to pybabel-3.8 and move it to the
  python38-babel package

* Wed Nov 20 2019 Lumír Balhar <lbalhar@redhat.com> - 2.7.0-8
- Adjusted for Python 3.8 module in RHEL 8

* Thu Oct 31 2019 Nils Philippsen <nils@tiptoe.de> - 2.7.0-7
- drop python2-babel only from F33 on as it is needed for trac (for the time
  being, #1737930)

* Thu Oct 31 2019 Nils Philippsen <nils@tiptoe.de> - 2.7.0-6
- drop python2-babel from F32 on

* Fri Sep 13 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-5
- Reduce Python 2 build dependencies on Fedora 32

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-3
- Bootstrap for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 27 2019 Felix Schwarz <fschwarz@fedoraproject.org> - 2.7.0-1
- update to upstream version 2.7.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-4
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-3
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Felix Schwarz <fschwarz@fedoraproject.org> - 2.6.0-2
- add setting to build without Python 2 support

* Fri Jun 29 2018 Felix Schwarz <fschwarz@fedoraproject.org> - 2.6.0-1
- update to upstream version 2.6.0

* Mon Jun 18 2018 Tomas Orsava <torsava@redhat.com> - 2.5.1-5
- Run tests in pytest (as declared in BuildRequires)

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-4
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-3
- Bootstrap for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Felix Schwarz <fschwarz@fedoraproject.org> - 2.5.1-1
- update to upstream version 2.5.1

* Fri Dec 15 2017 Iryna Shcherbina <ishcherb@redhat.com> - 2.3.4-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.4-4
- Finish bootstrapping for Python 3.6

* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.4-3
- Rebuild for Python 3.6
- Add "bootstrap" conditions

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Mon Apr 25 2016 Nils Philippsen <nils@redhat.com> - 2.3.4-1
- version 2.3.4
- always build Python3 subpackages
- remove obsolete packaging constructs
- update to current Python packaging guidelines
- build docs non-destructively
- tag license file as %%license
- use %%python_provide macro only if present
- update remove-pytz-version patch
- fix build dependencies
- set TZ in %%check

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov  6 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-10
- Also make sure that the babel package that has pybabel depends on the correct
  packages (python2 packages on F23 or less and python3 packages on F24 and
  greater.)

* Wed Nov  4 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-9
- Install the python3 version of pybabel on Fedora 24+ to match with Fedora's
  default python version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 17 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-7
- Remove pytz version requirement in egginfo as it confuses newer setuptools

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3-6
- Change python-setuptools-devel BR into python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 02 2014 Nils Philippsen <nils@redhat.com> - 1.3-3
- fix dependencies (#1083470)

* Sun Oct 06 2013 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3-2
- enable python3 subpackage

* Wed Oct 02 2013 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3-1
- update to Babel 1.3
- disabled %%check as it tries to download the CLDR

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.6-8
- split documentation off to a separate subpackage

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Nils Philippsen <nils@redhat.com> - 0.9.6-6
- run tests in %%check
- add pytz build requirement for tests

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.9.6-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug 01 2012 Felix Schwarz <felix.schwarz@oss.schwarz.eu> - 0.9.6-4
- disable building of non-functional python3 subpackage (#761583)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 07 2011 Nils Philippsen <nils@redhat.com> - 0.9.6-1
- version 0.9.6:
  * Backport r493-494: documentation typo fixes.
  * Make the CLDR import script work with Python 2.7.
  * Fix various typos.
  * Fixed Python 2.3 compatibility (ticket #146, #233).
  * Sort output of list-locales.
  * Make the POT-Creation-Date of the catalog being updated equal to
    POT-Creation-Date of the template used to update (ticket #148).
  * Use a more explicit error message if no option or argument (command) is
    passed to pybabel (ticket #81).
  * Keep the PO-Revision-Date if it is not the default value (ticket #148).
  * Make --no-wrap work by reworking --width's default and mimic xgettext's
    behaviour of always wrapping comments (ticket #145).
  * Fixed negative offset handling of Catalog._set_mime_headers (ticket #165).
  * Add --project and --version options for commandline (ticket #173).
  * Add a __ne__() method to the Local class.
  * Explicitly sort instead of using sorted() and don't assume ordering
    (Python 2.3 and Jython compatibility).
  * Removed ValueError raising for string formatting message checkers if the
    string does not contain any string formattings (ticket #150).
  * Fix Serbian plural forms (ticket #213).
  * Small speed improvement in format_date() (ticket #216).
  * Fix number formatting for locales where CLDR specifies alt or draft
    items (ticket #217)
  * Fix bad check in format_time (ticket #257, reported with patch and tests by
    jomae)
  * Fix so frontend.CommandLineInterface.run does not accumulate logging
    handlers (#227, reported with initial patch by dfraser)
  * Fix exception if environment contains an invalid locale setting (#200)
- install python2 rather than python3 executable (#710880)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-3
- Add python3 subpackage

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr  7 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.5-1
- This release contains a small number of bugfixes over the 0.9.4
- release.
-
- What's New:
- -----------
- * Fixed the case where messages containing square brackets would break
-  with an unpack error
- * Fuzzy matching regarding plurals should *NOT* be checked against
-  len(message.id) because this is always 2, instead, it's should be
-  checked against catalog.num_plurals (ticket #212).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 28 2009 Robert Scheck <robert@fedoraproject.org> - 0.9.4-4
- Added missing requires to python-setuptools for pkg_resources

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.4-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.4-1
- Update to 0.9.4

* Thu Jul 10 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.3-1
- Update to 0.9.3

* Sun Dec 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.1-1
- Update to 0.9.1

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-2
- BR python-setuptools-devel

* Mon Aug 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9-1
- Update to 0.9

* Mon Jul  2 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8.1-1
- Update to 0.8.1
- Remove upstreamed patch.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-3
- Replace patch with one that actually applies.

* Fri Jun 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-2
- Apply upstream patch to rename command line script to "pybabel" - BZ#246208

* Thu Jun 21 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.8-1
- First version for Fedora

