%define		_modname	sasl
%define		_status		alpha
Summary:	%{_modname} - Cyrus SASL extension
Summary(pl.UTF-8):   %{_modname} - rozszerzenie Cyrus SASL
Name:		php-pecl-%{_modname}
Version:	0.1.0
Release:	7
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	8431731cc8a7921a2922af23a57a572f
Patch0:		%{name}-lib_fix.patch
Patch1:		%{name}-lib64_fix.patch
URL:		http://pecl.php.net/package/sasl/
BuildRequires:	cyrus-sasl-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SASL is the Simple Authentication and Security Layer (as defined by
RFC 2222). It provides a system for adding plugable authenticating
support to connection-based protocols. The SASL extension for PHP
makes the Cyrus SASL library functions available to PHP. It aims to
provide a 1-to-1 wrapper around the SASL library to provide the
greatest amount of implementation flexibility. To that end, it is
possible to build both a client-side and server-side SASL
implementation entirely in PHP.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
SASL to warstwa prostego uwierzytelnienia i bezpieczeństwa (Simple
Authentication and Security Layer) zdefiniowana w RFC 2222. Dostarcza
system do dodawania wtyczek obsługujących uwierzytelnianie do
protokołów opartych na połączeniach. Rozszerzenie SASL dla PHP
udostępnia w PHP funkcje biblioteki Cyrus SASL. Celem jest
dostarczenie obudowania 1-do-1 biblioteki SASL, aby udostępnić jak
największą elastyczność implementacji. W tym celu możliwe jest
zbudowanie zarówno klienckiej jak i serwerowej implementacji SASL
całkowicie w PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
# Ugly, could be done somehow prettier (one combined patch?)
%if "%{_lib}" == "lib64"
%patch1 -p1
%else
%patch0 -p1
%endif

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/docs/TODO
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
