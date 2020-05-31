# NOTE: upstream name is "sbd" but is was already occupied, so using "cluster-" prefix
Summary:	Shared-storage based death
Summary(pl.UTF-8):	Uśmiercanie węzła poprzez współdzieloną przestrzeń dyskową
Name:		cluster-sbd
Version:	1.4.1
Release:	1
License:	GPL v2+
Group:		Daemons
#Source0Download: https://github.com/ClusterLabs/sbd/releases
Source0:	https://github.com/ClusterLabs/sbd/archive/v%{version}/sbd-%{version}.tar.gz
# Source0-md5:	506253d40490d49a8effc0f563bcd666
URL:		https://github.com/ClusterLabs/sbd/
BuildRequires:	autoconf >= 2.63
# for serial-tests
BuildRequires:	automake >= 1:1.13
BuildRequires:	corosync-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libaio-devel
BuildRequires:	libqb-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pacemaker-devel >= 1.1.8
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
Requires:	cluster-glue-stonith >= 1.0.9
Requires:	corosync-libs >= 2.0
Requires:	pacemaker-libs >= 1.1.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A highly reliable fencing or Shoot-the-other-node-in-the-head
(STONITH) mechanism that works by utilizing shared storage.

The component works with Pacemaker clusters. (Currently, it is only
tested on clusters using the "old" plugin to corosync, not yet the MCP
code).

%description -l pl.UTF-8
Wysoko wiarygodny mechanizm odgrodzenia lub "odstrzeliwania" (STONITH
- Shoot-the-other-node-in-the-head), działający dzięki wykorzystaniu
współdzielonej przestrzeni dyskowej.

Komponent działa z klastrami Pacemaker (aktualnie testowany był tylko
z klastrami wykorzystującymi "starą" wtyczkę corosync, nie kod MCP).

%prep
%setup -q -n sbd-%{version}

# see autogen.sh
echo 'm4_define([TESTS_OPTION], [serial-tests])' > tests-opt.m4

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd tests
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsbdtestbed.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README.md ROADMAP
%attr(755,root,root) %{_sbindir}/sbd
%attr(755,root,root) %{_libdir}/stonith/plugins/external/sbd
%{_mandir}/man8/sbd.8*
