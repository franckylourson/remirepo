%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_channel pear.symfony.com
%global pear_name %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')

Name:             php-symfony2-Routing
Version:          2.0.15
Release:          3%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/doc/current/components/routing.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php-common >= 5.3.2
Requires:         php-libxml
Requires:         php-pcre
Requires:         php-spl
Requires:         php-tokenizer
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# Optional requires
Requires:         php-pear(%{pear_channel}/Config) = %{version}
Requires:         php-pear(%{pear_channel}/Yaml) = %{version}

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
The Routing Component maps an HTTP request to a set of configuration variables.


%prep
%setup -q -c
# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml

# Fix package.xml for *.xsd file incorrectly being identified with role="doc"
# instead of role="php" (the *.xsd file is being referenced in code and is
# expected to be in the install directory instead of the doc directory)
# *** NOTE: This needs to be fixed upstream
sed -i \
    's#<file *md5sum="\([^"]\{1,\}\)" *name="\([^"]\{1,\}.xsd\)" *role="doc" */>#<file md5sum="\1" name="\2" role="php" />#' \
    %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Symfony/Component/%{pear_name}


%changelog
* Mon Jul 21 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.15-3
- backport for remi repository

* Tue Jun 12 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-3
- Fix package.xml for *.xsd file issue

* Mon Jun 11 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-2
- Added php-pear(%%{pear_channel}/Config) require
- Added php-pear(%%{pear_channel}/Yaml) require
- Removed ownership for directories already owned by required packages

* Wed May 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-1
- Updated to upstream version 2.0.15
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Updated %%prep section
- Removed cleaning buildroot from %%install section
- Removed documentation move from %%install section (fixed upstream)
- Removed %%clean section
- Updated %%doc in %%files section

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-3
- Moved documentation to correct location

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-2
- Removed BuildRoot
- Changed php require to php-common
- Added the following requires based on phpci results:
  php-libxml, php-pcre, php-spl, php-tokenizer
- Removed %%defattr from %%files section

* Fri May 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-1
- Updated to upstream version 2.0.14
- %%global instead of %%define
- Removed unnecessary cd from %%build section

* Wed May 2 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.13-1
- Updated to upstream version 2.0.13

* Sat Apr 21 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.12-1
- Initial package
