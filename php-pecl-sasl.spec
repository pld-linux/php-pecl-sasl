%define		_modname	sasl
%define		_status		alpha

Summary:	%{_modname} - Cyrus SASL Extension
Summary(pl):	%{_modname} - Rozszerzenie Cyrus SASL
Name:		php-pecl-%{_modname}
Version:	0.1.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	8431731cc8a7921a2922af23a57a572f
Patch0:		%{name}-lib_fix.patch
URL:		http://pecl.php.net/package/sasl/
BuildRequires:	cyrus-sasl-devel
BuildRequires:	libtool
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
SASL is the Simple Authentication and Security Layer (as defined by
RFC 2222). It provides a system for adding plugable authenticating
support to connection-based protocols. The SASL Extension for PHP
makes the Cyrus SASL library functions available to PHP. It aims to
provide a 1-to-1 wrapper around the SASL library to provide the
greatest amount of implementation flexibility. To that end, it is
possible to build both a client-side and server-side SASL
implementation entirely in PHP.

In PECL status of this extension is: %{_status}.

#%description -l pl
#
#To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
%patch0 -p1

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/docs/TODO
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
