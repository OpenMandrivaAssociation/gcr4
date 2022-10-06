%define url_ver %(echo %{version}|cut -d. -f1,2)
%define	Werror_cflags	%nil
%define _disable_rebuild_configure 1

%define major_gck   0
%define api_gck     2
%define major_gcr   0
%define api_gcr     4
%define libname		%mklibname gcr %{api_gcr} %{major_gcr}
%define libnamebase	%mklibname gcr-base %{api_gcr} %{major_gcr}
%define libnameui	%mklibname gcr-ui %{api_gcr} %{major_gcr}
%define libnamegck	%mklibname gck %{api_gck} %{major_gck}
%define girname		%mklibname gcr-gir %{major_gcr}
%define girnamegck	%mklibname gck-gir %{major_gck}
%define devname	%mklibname -d gcr 

Summary:	A library for bits of crypto UI and parsing
Name:		gcr4
Version:	3.92.0
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Networking/Remote access
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gcr/%{url_ver}/gcr-%{version}.tar.xz
# add MGA patch
Patch0:   0001-Make-gcr4-parellel-installable-with-gcr-3.41.x.patch

BuildRequires:  meson
BuildRequires:	intltool
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	libtasn1-tools
BuildRequires:	gnupg2
BuildRequires:  ssh-clients
BuildRequires:  pkgconfig(gi-docgen)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(p11-kit-1)
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	xsltproc
BuildRequires:	vala-devel
#Conflicts:	gnome-keyring < 3.3.1

Requires: %{libname} = %{version}-%{release}

%description
A library for bits of crypto UI and parsing etc.

This package also contains the gcr-viewer binary.

%package -n %{libname}
Group:	System/Libraries
Summary:	Library for integration with the gnome keyring system
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains shared libraries for Gnome keyring.

%package -n %{girname}
Summary:	GObject Introspection interface description for Gcr
Group:	System/Libraries

%description -n %{girname}
GObject Introspection interface description for Gcr.

%package -n %{devname}
Group:	Development/C
Summary:	Development files and headers for %{name}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{_lib}-gnome-keyring-devel < 2.29.4

%description -n %{devname}
Thi package contains the development files and headers for %{name}.

%prep
%autosetup -n gcr-%{version} -p1

%build

%meson

%meson_build

%install
%meson_install

%post
%systemd_user_post gcr4-ssh-agent.service

%preun
%systemd_user_preun gcr4-ssh-agent.service

%postun
%systemd_user_postun_with_restart gcr4-ssh-agent.service


#%find_lang gcr-%{api_gcr}

%files
%doc README.md NEWS
%{_bindir}/gcr-viewer-gtk4
%{_libexecdir}/gcr4-ssh-agent
%{_libexecdir}/gcr4-ssh-askpass
%{_userunitdir}/gcr4-ssh-agent.service
%{_userunitdir}/gcr4-ssh-agent.socket

%files -n %{libname}
%{_libdir}/libgck-%{api_gck}.so.%{major_gck}*
%{_libdir}/libgck-%{api_gck}.so.1.92.0
%{_libdir}/libgcr-%{api_gcr}.so.%{major_gck}*
%{_libdir}/libgcr-%{api_gcr}.so.%{version}

%files -n %{girname}
%{_libdir}/girepository-1.0/Gcr-%{api_gcr}.typelib
%{_libdir}/girepository-1.0/Gck-%{api_gck}.typelib

%files -n %{devname}
%doc %{_datadir}/doc/gck*
%doc %{_datadir}/doc/gcr*
%{_libdir}/libgck-%{api_gck}.so
%{_libdir}/libgcr-%{api_gcr}.so
%{_includedir}/gck-%{api_gck}
%{_includedir}/gcr-%{api_gcr}
%{_libdir}/pkgconfig/gck-%{api_gck}.pc
%{_libdir}/pkgconfig/gcr-%{api_gcr}.pc
%{_datadir}/gir-1.0/Gck-%{api_gck}.gir
%{_datadir}/gir-1.0/Gcr-%{api_gcr}.gir
%{_datadir}/vala/vapi/*
