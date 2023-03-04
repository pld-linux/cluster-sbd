# NOTE: upstream name is "sbd" but is was already occupied, so using "cluster-" prefix
Summary:	Shared-storage based death
Summary(pl.UTF-8):	Uśmiercanie węzła poprzez współdzieloną przestrzeń dyskową
Name:		cluster-sbd
Version:	1.4.2
Release:	1
License:	GPL v2+
Group:		Daemons
#Source0Download: https://github.com/ClusterLabs/sbd/releases
Source0:	https://github.com/ClusterLabs/sbd/archive/v%{version}/sbd-%{version}.tar.gz
# Source0-md5:	035f9b05d11e4dfed44447e6dce56eb9
URL:		https://github.com/ClusterLabs/sbd/
BuildRequires:	autoconf >= 2.63
# for serial-tests
BuildRequires:	automake >= 1:1.13
BuildRequires:	corosync-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libaio-devel
BuildRequires:	libqb-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pacemaker-devel >= 1.1.8
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
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

%package devel
Summary:	SBD development package
Summary(pl.UTF-8):	Pakiet programistyczny SBD
Group:		Development/Libraries
# doesn't require base
BuildArch:	noarch

%description devel
SBD development package containing build information.

%description devel -l pl.UTF-8
Pakiet programistyczny SBD, zawierający informacje z czasu budowania.

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
%doc NEWS README.md
%attr(755,root,root) %{_sbindir}/sbd
%attr(755,root,root) %{_libdir}/stonith/plugins/external/sbd
%{_mandir}/man8/sbd.8*

%files devel
%defattr(644,root,root,755)
%{_npkgconfigdir}/sbd.pc
