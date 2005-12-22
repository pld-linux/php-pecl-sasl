%define		_modname	sasl
%define		_status		alpha
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - Cyrus SASL extension
Summary(pl):	%{_modname} - rozszerzenie Cyrus SASL
Name:		php-pecl-%{_modname}
Version:	0.1.0
Release:	6
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	8431731cc8a7921a2922af23a57a572f
Patch0:		%{name}-lib_fix.patch
Patch1:		%{name}-lib64_fix.patch
URL:		http://pecl.php.net/package/sasl/
BuildRequires:	cyrus-sasl-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
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

%description -l pl
SASL to warstwa prostego uwierzytelnienia i bezpieczeñstwa (Simple
Authentication and Security Layer) zdefiniowana w RFC 2222. Dostarcza
system do dodawania wtyczek obs³uguj±cych uwierzytelnianie do
protoko³ów opartych na po³±czeniach. Rozszerzenie SASL dla PHP
udostêpnia w PHP funkcje biblioteki Cyrus SASL. Celem jest
dostarczenie obudowania 1-do-1 biblioteki SASL, aby udostêpniæ jak
najwiêksz± elastyczno¶æ implementacji. W tym celu mo¿liwe jest
zbudowanie zarówno klienckiej jak i serwerowej implementacji SASL
ca³kowicie w PHP.

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/docs/TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
