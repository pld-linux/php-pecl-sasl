%define		php_name	php%{?php_suffix}
%define		modname	sasl
%define		status		alpha
Summary:	%{modname} - Cyrus SASL extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie Cyrus SASL
Name:		%{php_name}-pecl-%{modname}
Version:	0.1.0
Release:	12
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	8431731cc8a7921a2922af23a57a572f
Patch0:		php-pecl-%{modname}-lib_fix.patch
Patch1:		php-pecl-%{modname}-lib64_fix.patch
URL:		http://pecl.php.net/package/sasl/
BuildRequires:	cyrus-sasl-devel
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-pear-%{modname}
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

In PECL status of this extension is: %{status}.

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

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
# Ugly, could be done somehow prettier (one combined patch?)
%if "%{_lib}" == "lib64"
%patch1 -p2
%else
%patch0 -p2
%endif

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc docs/TODO
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
