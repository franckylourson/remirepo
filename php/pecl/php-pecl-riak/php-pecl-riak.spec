# spec file for php-pecl-riak
#
# Copyright (c) 2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?php_inidir:  %{expand: %%global php_inidir  %{_sysconfdir}/php.d}}
%{!?__pecl:      %{expand: %%global __pecl      %{_bindir}/pecl}}

#############################
##       TODO              ##
##   bundled libs          ##
##   how to run test       ##
#############################


%global with_zts  0%{?__ztsphp:1}
%global pecl_name riak

Summary:        Riak database PHP extension
Name:           php-pecl-%{pecl_name}
Version:        0.6.0
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        ASL 2.0
Group:          Development/Languages
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel > 5.3
BuildRequires:  php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-json%{?_isa}

Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}

# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}

%description
Fast protocol buffers client for Riak database and session module.


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS
# Fix version
sed -e /PHP_RIAK_VERSION/s/0.1/%{version}/ -i php_riak.h

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_RIAK_VERSION/{s/.* "//;s/".*$//;p}' php_riak.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration

;riak.persistent.connections=20

;riak.persistent.timeout=5

; Keep sockets alive (recommended)
riak.socket.keep_alive=1

; Socket receive timeout [ms]
riak.socket.recv_timeout=10000

; Socket send timeout [ms]
riak.socket.send_timeout=10000

EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: Minimal load test for NTS extension
cd NTS
php --no-php-ini \
    --define extension=json.so \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}

# Need a running riak server + some configuration
#TEST_PHP_EXECUTABLE=%{_bindir}/php \
#TEST_PHP_ARGS="-n -d extension=json.so -d extension=$PWD/modules/%{pecl_name}.so" \
#NO_INTERACTION=1 \
#REPORT_EXIT_STATUS=1 \
#%{_bindir}/php -n run-tests.php

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=json.so \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc NTS/{LICENSE,README.md}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Oct 10 2013 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0 (beta)

* Thu Oct 03 2013 Remi Collet <remi@fedoraproject.org> - 0.5.4-1
- Update to 0.5.4 (beta)

* Wed Sep 25 2013 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- initial package, version 0.5.2 (beta)
