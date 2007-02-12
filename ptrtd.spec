# TODO: unify preun/postun
Summary:	Portable Transport-layer Relay Translator daemon
Summary(pl.UTF-8):   Przenośny demon TRT (Transport-layer Relay Translator)
Name:		ptrtd
Version:	0.5.2
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://v6web.litech.org/ptrtd/dist/%{name}-%{version}.tar.gz
# Source0-md5:	bfe026445fdc4fe509a9c70ec4551744
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://v6web.litech.org/ptrtd/
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The portable Transport Relay Translator daemon (pTRTd) is a method of
allowing IPv6 hosts to communicate with IPv4 hosts. It is a TRT as
specified by RFC 3142, similar to the Faith package implemented by the
KAME project. However, unlike Faith, it doesn't depend on special
support in the kernel IPv6 stack, and thus should be fairly easy to
port to most Unix-like operating systems.

%description -l pl.UTF-8
Przenośny demon Transport Relay Translator (pTRTd) to metoda
umożliwienia hostom IPv6 komunikowania się z hostami IPv4. Jest to TRT
zgodne z RFC 3142, podobne do pakietu Faith zaimplementowanego przez
projekt KAME. Jednak, w przeciwieństwie do Faikt, nie polega na
specjalnym wsparciu w stosie IPv6 w jądrze, przez co powinien być dość
łatwy w portowaniu na większość uniksowych systemów operacyjnych.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/rc.d/init.d,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ptrtd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ptrtd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ptrtd

%preun
if [ "$1" = "0 "]; then
	/etc/rc.d/init.d/ptrtd stop >&2
	/sbin/chkconfig --del ptrtd
fi

%postun
if [ "$1" -ge "1" ]; then
	/etc/rc.d/init.d/ptrtd condrestart >&2
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ptrtd
