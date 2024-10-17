%define name ivman
%define version 0.6.14
%define release %mkrel 8

Summary: A volume manager daemon
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Source1: ivman.init
Source2: ivman.xinit
Patch0: ivman-0.6.6-daemon.patch
Patch1: ivman-0.6.14-nodebug.patch
Patch2: ivman-0.6.14-fix-umount.patch
Patch3: ivman-0.6.14-manpage-system-service-not-needed.patch

License: QPL
Group: System/Base
Url: https://ivman.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: glib-devel
BuildRequires: hal-devel
BuildRequires: dbus-devel
BuildRequires: libxml2-devel
BuildRequires: glib2-devel
BuildRequires: pmount
BuildRequires: dbus-glib-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Suggests: pmount

%description
Ivman is a volume manager daemon. It detects added volumes such as DVDs, CDs, 
and USB sticks / hard drives, mounts them if necessary and also starts 
programs to handle the added media (such as an audio CD player, or a video DVD
player). It can also monitor properties of hardware and execute commands when 
these properties change to a predefined value.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .daemon
%patch1 -p1 -b .nodebug
%patch2 -p1 -b .umount
%patch3 -p1 -b .noinit

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -D -m755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -D -m755 %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/xinit.d/%{name}
%find_lang %{name}

%pre
%_pre_useradd ivman / /sbin/nologin
%_pre_groupadd daemon ivman

%post
%_post_service ivman

%preun
%_preun_service ivman

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_mandir}/man?/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_initrddir}/%{name}
%{_sysconfdir}/X11/xinit.d/%{name}
