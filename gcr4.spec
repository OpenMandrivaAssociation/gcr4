%define url_ver %(echo %{version}|cut -d. -f1,2)
%define	Werror_cflags	%nil
%define _disable_rebuild_configure 1

%define major_gck   0
%define api_gck     1
%define major_gcr   1
%define api_gcr     3
%define libname		%mklibname gcr %{api_gcr} %{major_gcr}
%define libnamebase	%mklibname gcr-base %{api_gcr} %{major_gcr}
%define libnameui	%mklibname gcr-ui %{api_gcr} %{major_gcr}
%define libnamegck	%mklibname gck %{api_gck} %{major_gck}
%define girname		%mklibname gcr-gir %{major_gcr}
%define girnamegck	%mklibname gck-gir %{major_gck}
%define devname	%mklibname -d gcr 

Summary:	A library for bits of crypto UI and parsing
Name:		gcr
Version:	3.41.1
Release:	2
License:	GPLv2+ and LGPLv2+
Group:		Networking/Remote access
Url:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Source10:	%{name}.rpmlintrc

BuildRequires:  meson
BuildRequires:	intltool
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	libtasn1-tools
BuildRequires:	gnupg2
BuildRequires:  ssh-clients
BuildRequires:  pkgconfig(gi-docgen)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(p11-kit-1)
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	xsltproc
BuildRequires:	vala-devel
#Conflicts:	gnome-keyring < 3.3.1

%description
A library for bits of crypto UI and parsing etc.

This package also contains the gcr-viewer binary.

%package -n %{libname}
Group:	System/Libraries
Summary:	Library for integration with the gnome keyring system
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gnome-keyring < 2.29.4
Obsoletes:	%{_lib}gcr-3_0 < 3.1.4
Obsoletes:	%{_lib}gcr-3_1 < 3.1.91

%description -n %{libname}
This package contains shared libraries for Gnome keyring.

%package -n %{libnamegck}
Group:	System/Libraries
Summary:	Library for integration with the gnome keyring system

%description -n %{libnamegck}
This package contains shared libraries for Gnome keyring.

%package -n %{libnamebase}
Group:	System/Libraries
Summary:	Library for integration with the gnome keyring system

%description -n %{libnamebase}
This package contains shared libraries for Gnome keyring.

%package -n %{libnameui}
Group:	System/Libraries
Summary:	Library for integration with the gnome keyring system

%description -n %{libnameui}
This package contains shared libraries for Gnome keyring.

%package -n %{girname}
Summary:	GObject Introspection interface description for Gcr
Group:	System/Libraries

%description -n %{girname}
GObject Introspection interface description for Gcr.

%package -n %{girnamegck}
Summary:	GObject Introspection interface description for Gck
Group:	System/Libraries

%description -n %{girnamegck}
GObject Introspection interface description for Gck.

%package -n %{devname}
Group:	Development/C
Summary:	Development files and headers for %{name}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnamegck} = %{version}-%{release}
Requires:	%{libnamebase} = %{version}-%{release}
Requires:	%{libnameui} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Requires:	%{girnamegck} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	%{_lib}-gnome-keyring-devel < 2.29.4

%description -n %{devname}
Thi package contains the development files and headers for %{name}.

%prep
%autosetup -p1

%build

%meson

%meson_build

%install
%meson_install

#rm -f %{buildroot}/%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp*.xml

%find_lang %{name}

%files -f %{name}.lang
%doc README.md NEWS
%{_bindir}/gcr-viewer
%{_libexecdir}/gcr-prompter
%{_libexecdir}/gcr-ssh-askpass
%{_libexecdir}/gcr-ssh-agent
%{_datadir}/dbus-1/services/org.gnome.keyring.PrivatePrompter.service
%{_datadir}/dbus-1/services/org.gnome.keyring.SystemPrompter.service
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp*.convert
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp*.xml
%{_datadir}/applications/gcr-viewer.desktop
%{_datadir}/applications/gcr-prompter.desktop
%{_datadir}/mime/packages/gcr-crypto-types.xml
%{_datadir}/icons/hicolor/*/apps/gcr*.png
%{_userunitdir}/gcr-ssh-agent.service
%{_userunitdir}/gcr-ssh-agent.socket

%files -n %{libnamegck}
%{_libdir}/libgck-%{api_gck}.so.%{major_gck}*

%files -n %{girnamegck}
%{_libdir}/girepository-1.0/Gck-%{api_gck}.typelib

%files -n %{libnamebase}
%{_libdir}/libgcr-base-%{api_gcr}.so.%{major_gcr}*

%files -n %{libnameui}
%{_libdir}/libgcr-ui-%{api_gcr}.so.%{major_gcr}*

%files -n %{libname}
#%{_libdir}/libgcr-%{api_gcr}.so.%{major_gcr}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Gcr-%{api_gcr}.typelib
%{_libdir}/girepository-1.0/GcrUi-%{api_gcr}.typelib

%files -n %{devname}
%doc %{_datadir}/doc/gck*
%doc %{_datadir}/doc/gcr*
%{_libdir}/libgck-%{api_gck}.so
%{_libdir}/libgcr-ui-%{api_gcr}.so
%{_libdir}/libgcr-base-%{api_gcr}.so
%{_includedir}/gck-%{api_gck}
%{_includedir}/gcr-%{api_gcr}
%{_libdir}/pkgconfig/gck-%{api_gck}.pc
%{_libdir}/pkgconfig/gcr-%{api_gcr}.pc
%{_libdir}/pkgconfig/gcr-base-%{api_gcr}.pc
%{_libdir}/pkgconfig/gcr-ui-%{api_gcr}.pc
%{_datadir}/gir-1.0/Gck-%{api_gck}.gir
%{_datadir}/gir-1.0/Gcr-%{api_gcr}.gir
%{_datadir}/gir-1.0/GcrUi-%{api_gcr}.gir
%{_datadir}/vala/vapi/*

%post
/usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas

%postun
/usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas
