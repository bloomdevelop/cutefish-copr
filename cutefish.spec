# Nightly snapshot of the Cutefish desktop environment, built from the 18
# github.com/cutefishos repositories in one source package.  See README.md.
#
# One source package, one build per night: the components are built in
# dependency order and installed into subpackages.  Skia and PDFium are fetched
# by the components' own scripts during %build (Copr allows network access).

%global version 0.1.0

# Rewritten by scripts/make-nightly-srpm.sh before rpmbuild -bs.
%global nightly_date 19700101
%global nightly_run 0

# debuginfo for Skia + PDFium is several GB per nightly build.
%global debug_package %{nil}

# %build installs every component as it goes, because the next component needs
# the previous one's headers and libraries.  %{buildroot} cannot be used for
# that: rpmbuild deletes it right before %install.  Stage the tree elsewhere
# and copy it into %{buildroot} from %install.
%global stage %{_builddir}/%{name}-%{version}-stage

Name:           cutefish
Version:        %{version}
Release:        1.%{nightly_date}.%{nightly_run}%{?dist}
Summary:        Cutefish desktop environment (nightly snapshot)
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND BSD-3-Clause
URL:            https://github.com/cutefishos
Source0:        cutefish-toolkit-%{version}.tar.gz
Source1:        cutefish-framework-%{version}.tar.gz
Source2:        cutefish-qt-plugins-%{version}.tar.gz
Source3:        cutefish-icons-%{version}.tar.gz
Source4:        cutefish-core-%{version}.tar.gz
Source5:        cutefish-dm-%{version}.tar.gz
Source6:        cutefish-filemanager-%{version}.tar.gz
Source7:        cutefish-terminal-%{version}.tar.gz
Source8:        xdg-desktop-portal-cutefish-%{version}.tar.gz
Source9:        cutefish-settings-%{version}.tar.gz
Source10:       cutefish-system-monitor-%{version}.tar.gz
Source11:       cutefish-text-editor-%{version}.tar.gz
Source12:       cutefish-video-player-%{version}.tar.gz
Source13:       cutefish-calendar-%{version}.tar.gz
Source14:       cutefish-calculator-%{version}.tar.gz
Source15:       cutefish-preview-%{version}.tar.gz
Source16:       cutefish-compositor-%{version}.tar.gz
Source17:       cutefish-wallpapers-%{version}.tar.gz
# Fedora PAM stacks: upstream cutefish-dm ships Debian common-* includes.
Source18:       cutefish-dm.pam
Source19:       cutefish-dm-greeter.pam
Source20:       cutefish-dm.tmpfiles.conf
# Auth/password substack so pam_oo7 runs after password-auth's
# "sufficient" pam_unix, as gdm-password does; without it the login
# keyring never unlocks and GOA finds no credentials.
Source21:       cutefish-dm-auth-substack
# Local fixes that are not upstream yet.
Patch0:         0001-cutefish-core-session-target.patch
Patch1:         0002-cutefish-qt-plugins-qt6.11.patch
Patch2:         0003-cutefish-qt-plugins-menu-bar.patch
Patch3:         0004-cutefish-toolkit-fontconfig-freetype.patch

# Keep in sync with scripts/fetch-sources.sh and the Source list above.

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  ninja-build
BuildRequires:  git-core
BuildRequires:  curl
BuildRequires:  unzip
BuildRequires:  python3
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  gettext
BuildRequires:  systemd-rpm-macros
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  systemd-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libicu-devel
BuildRequires:  expat-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  zlib-ng-compat-devel
BuildRequires:  libwebp-devel
BuildRequires:  libtiff-devel
BuildRequires:  libheif-devel
BuildRequires:  libjxl-devel
BuildRequires:  pipewire-devel
BuildRequires:  lcms2-devel
BuildRequires:  openjpeg-devel
BuildRequires:  highway-devel
BuildRequires:  abseil-cpp-devel
BuildRequires:  ffmpeg-free-devel
BuildRequires:  libva-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdrm-devel
BuildRequires:  libinput-devel
BuildRequires:  libseat-devel
BuildRequires:  libxcb-devel
BuildRequires:  libarchive-devel
BuildRequires:  fuse3-devel
BuildRequires:  libmtp-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libssh-devel
BuildRequires:  libzip-devel
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  lzfse-devel
BuildRequires:  libXcursor-devel
BuildRequires:  pcre2-devel
BuildRequires:  pam-devel
BuildRequires:  libxcrypt-devel
BuildRequires:  mpv-devel
BuildRequires:  libcurl-devel
BuildRequires:  libical-devel
BuildRequires:  gtest-devel
BuildRequires:  librsvg2-devel
BuildRequires:  gtk-update-icon-cache

%description
Cutefish is a desktop environment built with Qt 6 and Wayland.  This source
package builds the complete environment from the current upstream branches:
the compositor, toolkit and framework libraries, the display manager, and the
core applications.

This is a nightly snapshot, rebuilt from upstream HEAD every day.

%package toolkit
Summary:        Cutefish toolkit library
License:        BSD-3-Clause AND LGPL-3.0-or-later
Requires:       fontconfig
%description toolkit
Base C++ library of the Cutefish desktop (files, JSON, D-Bus, platform
integration), with Skia linked in for rendering.

%package framework
Summary:        Cutefish client libraries and PDF support
License:        LGPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       fontconfig
%description framework
D-Bus client libraries for accounts, appearance, audio, Bluetooth, display,
NetworkManager, PackageKit, power profiles, timedate and UPower, plus file
utilities and PDF rendering.

%package qt-plugins
Summary:        Cutefish Qt 6 platform theme and image format plugins
License:        LGPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description qt-plugins
Qt 6 platform theme and image format plugins used by the Cutefish
applications.

%package icons
Summary:        Cutefish icon theme
License:        GPL-3.0-or-later
Requires:       hicolor-icon-theme
%description icons
The Cutefish icon theme.

%package core
Summary:        Cutefish session manager and services
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
Requires:       %{name}-compositor = %{version}-%{release}
Requires:       accountsservice
Requires:       polkit
Requires:       dbus
Requires:       fontconfig
Requires:       rsms-inter-fonts
Recommends:     oo7-daemon
Requires(post):  systemd
Requires(preun): systemd
Requires(postun): systemd
%description core
The Cutefish wayland session, the user services it starts, plus the
applications-folder, locales, privacy and polkit agent services.

%package dm
Summary:        Cutefish display manager
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-compositor = %{version}-%{release}
Requires:       pam
Requires:       pam_oo7
Requires:       systemd
Requires(post):  policycoreutils-python-utils
Requires(post):  policycoreutils
Requires(post):  systemd
Requires(pre):   shadow-utils
Requires(preun): systemd
Requires(postun): systemd
%description dm
The Cutefish login screen.  It runs the compositor in greeter mode as the
unprivileged cutefish-greeter user.

%package filemanager
Summary:        Cutefish file manager
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
Recommends:     udisks2
Recommends:     gvfs
%description filemanager
The Cutefish file manager, its daemon, mount service and preview service.

%package terminal
Summary:        Cutefish terminal emulator
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description terminal
The Cutefish terminal emulator.

%package -n xdg-desktop-portal-cutefish
Summary:        Cutefish backend for xdg-desktop-portal
License:        LGPL-3.0-or-later
Requires:       cutefish-toolkit = %{version}-%{release}
Requires:       cutefish-framework = %{version}-%{release}
Requires:       xdg-desktop-portal
%description -n xdg-desktop-portal-cutefish
The Cutefish implementation of the xdg-desktop-portal interfaces (screenshot,
screen cast, file chooser, wallpaper, settings).

%package settings
Summary:        Cutefish settings application
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description settings
The Cutefish control center.

%package system-monitor
Summary:        Cutefish system monitor
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description system-monitor
The Cutefish system monitor.

%package text-editor
Summary:        Cutefish text editor
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description text-editor
The Cutefish text editor.

%package video-player
Summary:        Cutefish video player
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
Requires:       mpv-libs
%description video-player
The Cutefish video player, using mpv for playback.

%package calendar
Summary:        Cutefish calendar
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description calendar
The Cutefish calendar and its reminder service.

%package calculator
Summary:        Cutefish calculator
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description calculator
The Cutefish calculator.

%package preview
Summary:        Cutefish preview application
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
%description preview
The Cutefish document and image preview application.

%package compositor
Summary:        Cutefish Wayland compositor
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
Requires:       pam
Requires:       systemd
Requires:       xorg-x11-server-Xwayland
%description compositor
The Cutefish Wayland compositor and window manager, with its lock screen
authentication helper.

%package wallpapers
Summary:        Cutefish wallpapers and avatars
License:        GPL-3.0-or-later
%description wallpapers
The default Cutefish wallpapers and account avatars.

%package l10n
Summary:        Translations for the Cutefish desktop
License:        GPL-3.0-or-later AND LGPL-3.0-or-later
%description l10n
Translations for all Cutefish components.

%package desktop
Summary:        Complete Cutefish desktop environment
License:        GPL-3.0-or-later
Requires:       %{name}-toolkit = %{version}-%{release}
Requires:       %{name}-framework = %{version}-%{release}
Requires:       %{name}-qt-plugins = %{version}-%{release}
Requires:       %{name}-icons = %{version}-%{release}
Requires:       %{name}-core = %{version}-%{release}
Requires:       %{name}-dm = %{version}-%{release}
Requires:       %{name}-filemanager = %{version}-%{release}
Requires:       %{name}-terminal = %{version}-%{release}
Requires:       xdg-desktop-portal-cutefish = %{version}-%{release}
Requires:       %{name}-settings = %{version}-%{release}
Requires:       %{name}-system-monitor = %{version}-%{release}
Requires:       %{name}-text-editor = %{version}-%{release}
Requires:       %{name}-video-player = %{version}-%{release}
Requires:       %{name}-calendar = %{version}-%{release}
Requires:       %{name}-calculator = %{version}-%{release}
Requires:       %{name}-preview = %{version}-%{release}
Requires:       %{name}-compositor = %{version}-%{release}
Requires:       %{name}-wallpapers = %{version}-%{release}
Requires:       %{name}-l10n = %{version}-%{release}
Requires:       xdg-desktop-portal
Requires:       xdg-desktop-portal-gtk
Requires:       xdg-user-dirs
Requires:       pipewire
Requires:       pipewire-pulseaudio
Requires:       wireplumber
Requires:       NetworkManager
Requires:       bluez
Requires:       upower
Requires:       udisks2
Requires:       fuse3
Requires:       adwaita-icon-theme
%description desktop
Meta package that installs the complete Cutefish desktop environment and the
runtime services it expects on Fedora.

%prep
%setup -q -c -T -n %{name}-%{version}

for tarball in %{_sourcedir}/*-%{version}.tar.gz; do
    tar -xzf "$tarball"
done

patch -p1 -d cutefish-toolkit-%{version} \
    < %{_sourcedir}/0004-cutefish-toolkit-fontconfig-freetype.patch
patch -p1 -d cutefish-core-%{version} \
    < %{_sourcedir}/0001-cutefish-core-session-target.patch
patch -p1 -d cutefish-qt-plugins-%{version} \
    < %{_sourcedir}/0002-cutefish-qt-plugins-qt6.11.patch
patch -p1 -d cutefish-qt-plugins-%{version} \
    < %{_sourcedir}/0003-cutefish-qt-plugins-menu-bar.patch

# Upstream ships Debian PAM stacks; use the Fedora ones instead.
cp %{SOURCE18} cutefish-dm-%{version}/data/cutefish-dm.pam
cp %{SOURCE19} cutefish-dm-%{version}/data/cutefish-dm-greeter.pam

%build
# The components find each other through the staging tree until %install.
rm -rf %{stage}
build_one() {
    local src=$1
    shift
    cmake -S "$src" -B "build/$src" \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DCMAKE_INSTALL_LIBDIR=%{_lib} \
        -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir} \
        -DCMAKE_PREFIX_PATH="%{stage}%{_prefix};%{stage}%{_libdir}" \
        -DCMAKE_C_FLAGS="%{optflags}" \
        -DCMAKE_CXX_FLAGS="%{optflags}" \
        -DBUILD_TESTING=OFF "$@"
    cmake --build "build/$src" --parallel %{_smp_build_ncpus}
    DESTDIR=%{stage} cmake --install "build/$src"
}

# Skia and PDFium are not vendored; their pinned revisions are fetched here.
(cd cutefish-toolkit-%{version} && ./scripts/fetch-skia.sh)
(cd cutefish-framework-%{version} && ./scripts/fetch-pdfium.sh)

build_one cutefish-toolkit-%{version}
build_one cutefish-framework-%{version}
build_one cutefish-qt-plugins-%{version}
build_one cutefish-icons-%{version}
build_one cutefish-core-%{version}
build_one cutefish-dm-%{version}
build_one cutefish-filemanager-%{version}
build_one cutefish-terminal-%{version}
build_one xdg-desktop-portal-cutefish-%{version}
build_one cutefish-settings-%{version}
build_one cutefish-system-monitor-%{version}
build_one cutefish-text-editor-%{version}
build_one cutefish-video-player-%{version}
build_one cutefish-calendar-%{version}
build_one cutefish-calculator-%{version}
build_one cutefish-preview-%{version}
build_one cutefish-compositor-%{version} \
    -DCUTEFISH_PAM_CONFIG=%{_builddir}/%{name}-%{version}/cutefish-compositor-%{version}/data/cutefish-auth-fedora
build_one cutefish-wallpapers-%{version}

%install
# Everything was installed into %{stage} by %build; rpmbuild emptied
# %{buildroot} before this section, so it has to be filled from there.
cp -a %{stage}/. %{buildroot}/

install -d %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 644 %{SOURCE20} \
    %{buildroot}%{_prefix}/lib/tmpfiles.d/cutefish-dm.conf

# The PAM substack has no upstream equivalent, so unlike the two stacks
# replaced inside the source tree it is installed directly.
install -m 644 %{SOURCE21} \
    %{buildroot}%{_sysconfdir}/pam.d/cutefish-dm-auth-substack

# Each component installs its own gettext domain (cutefish-toolkit,
# cutefish-core, ...), so match all of them instead of just `cutefish`.
%find_lang %{name} --all-name

%pre dm
getent group cutefish-greeter >/dev/null || groupadd -r cutefish-greeter
getent passwd cutefish-greeter >/dev/null || \
    useradd -r -g cutefish-greeter -d /var/lib/cutefish-greeter \
        -s /sbin/nologin -c 'Cutefish greeter' -m cutefish-greeter

%post core
# The systemd macros take the complete unit list on one line: RPM ends a macro
# invocation at the newline, so shell line continuations would turn the
# remaining units into stray commands in the scriptlet.
%systemd_post cutefish-applications-folder.service cutefish-locales.service cutefish-privacy.service

%preun core
%systemd_preun cutefish-applications-folder.service cutefish-locales.service cutefish-privacy.service

%postun core
%systemd_postun_with_restart cutefish-applications-folder.service cutefish-locales.service cutefish-privacy.service

%post dm
install -d -m 700 -o cutefish-greeter -g cutefish-greeter \
    /var/lib/cutefish-greeter
systemd-tmpfiles --create %{_prefix}/lib/tmpfiles.d/cutefish-dm.conf >/dev/null 2>&1 || :
%systemd_post cutefish-dm.service
# Give the DM the SELinux domain Fedora uses for display managers, as GDM,
# LightDM and SDDM have.  Without it pam_selinux cannot transition the
# greeter into the user's session domain.
if command -v selinuxenabled >/dev/null 2>&1 && selinuxenabled; then
    fcontext() {
        semanage fcontext -a -t "$2" "$1" 2>/dev/null ||
            semanage fcontext -m -t "$2" "$1" 2>/dev/null || :
    }
    fcontext '/usr/bin/cutefish-dm' 'xdm_exec_t'
    fcontext '/run/cutefish-dm(/.*)?' 'xdm_var_run_t'
    fcontext '/var/lib/cutefish-dm(/.*)?' 'xdm_var_lib_t'
    fcontext '/var/lib/cutefish-greeter(/.*)?' 'xdm_var_lib_t'
    restorecon -R /usr/bin/cutefish-dm /var/lib/cutefish-dm \
        /var/lib/cutefish-greeter 2>/dev/null || :
fi

%preun dm
%systemd_preun cutefish-dm.service

%postun dm
%systemd_postun_with_restart cutefish-dm.service

%files
%license cutefish-toolkit-%{version}/LICENSE

%files toolkit
%license cutefish-toolkit-%{version}/LICENSE
%{_libdir}/libcutefish-toolkit*
# The toolkit installs two public header trees: the UI headers under
# /usr/include/cutefish-toolkit and, since the upstream rename, the base
# library's headers under /usr/include/cutefish-toolkit-base.
%{_includedir}/cutefish-toolkit/
%{_includedir}/cutefish-toolkit-base/
%{_libdir}/cmake/CutefishToolkit/

%files framework
%license cutefish-framework-%{version}/LICENSE
%{_libdir}/libcutefish-*-client.so*
%{_libdir}/libcutefish-files*.so*
%{_libdir}/libcutefish-pdf.so*
%{_includedir}/cutefish/
%{_libdir}/cmake/CutefishClients/
%{_libdir}/cmake/CutefishFiles/
%{_libdir}/cmake/CutefishPdf/

%files qt-plugins
%license cutefish-qt-plugins-%{version}/LICENSE
%{_libdir}/libcutefish-qt-scrolling*.so
%{_libdir}/qt6/plugins/platformthemes/libcutefishplatformtheme.so
%{_libdir}/qt6/plugins/imageformats/libqsvg-rsvg.so
%{_libdir}/qt6/plugins/imageformats/libqheif.so
%{_libdir}/qt6/plugins/imageformats/libqjxl.so

%files icons
%license cutefish-icons-%{version}/LICENSE
%{_datadir}/icons/Cutefish/

%files core
%license cutefish-core-%{version}/LICENSE
%{_bindir}/cutefish-appruntime
%{_bindir}/cutefish-polkit-agent
%{_bindir}/cutefish-services
%{_bindir}/cutefish-session
%{_bindir}/cutefish-wayland-session
%{_libexecdir}/cutefish-applications-folder
%{_libexecdir}/cutefish-locales
%{_libexecdir}/cutefish-privacy
%{_libexecdir}/cutefish-screenrecorder
%{_prefix}/lib/modules-load.d/cutefish-ddc.conf
%{_prefix}/lib/udev/rules.d/60-cutefish-ddc.rules
%{_prefix}/lib/udev/rules.d/60-cutefish-privacy.rules
%{_prefix}/lib/systemd/system/cutefish-applications-folder.service
%{_prefix}/lib/systemd/system/cutefish-locales.service
%{_prefix}/lib/systemd/system/cutefish-privacy.service
%{_prefix}/lib/systemd/user/cutefish-session.target
%{_prefix}/lib/systemd/user/xdg-document-portal.service.d/cutefish-session.conf
%{_datadir}/applications/cutefish-mimeapps.list
%{_datadir}/cutefish-services/
%{_datadir}/dbus-1/system.d/org.cutefish.ApplicationsFolder.conf
%{_datadir}/dbus-1/system.d/org.cutefish.Locales.conf
%{_datadir}/dbus-1/system.d/org.cutefish.Privacy.conf
%{_datadir}/dbus-1/system-services/org.cutefish.ApplicationsFolder.service
%{_datadir}/dbus-1/system-services/org.cutefish.Locales.service
%{_datadir}/dbus-1/system-services/org.cutefish.Privacy.service
%{_datadir}/polkit-1/actions/org.cutefish.applications-folder.policy
%{_datadir}/polkit-1/actions/org.cutefish.locales.policy
%{_datadir}/polkit-1/actions/org.cutefish.privacy.policy
%{_datadir}/wayland-sessions/cutefish-wayland.desktop
%config(noreplace) %{_sysconfdir}/fonts/conf.d/56-cutefish-sans.conf

%files dm
%license cutefish-dm-%{version}/LICENSE
%{_bindir}/cutefish-dm
%{_libexecdir}/cutefish-dm-helper
%{_libexecdir}/cutefish-dm-session
%{_prefix}/lib/systemd/system/cutefish-dm.service
%{_prefix}/lib/systemd/user/*/cutefish-dm.conf
%{_prefix}/lib/tmpfiles.d/cutefish-dm.conf
%{_datadir}/dbus-1/system.d/org.cutefish.DisplayManager.conf
%config(noreplace) %{_sysconfdir}/pam.d/cutefish-dm
%config(noreplace) %{_sysconfdir}/pam.d/cutefish-dm-auth-substack
%config(noreplace) %{_sysconfdir}/pam.d/cutefish-dm-greeter

%files filemanager
%license cutefish-filemanager-%{version}/LICENSE
%{_bindir}/cutefish-filemanager
%{_libexecdir}/cutefish-filemanager-daemon
%{_libexecdir}/cutefish-mountd
%{_datadir}/applications/cutefish-filemanager.desktop
%{_datadir}/dbus-1/services/org.cutefish.FileManager1.service
%{_datadir}/dbus-1/services/org.cutefish.FileOperations.service
%{_datadir}/dbus-1/services/org.cutefish.FilePreview.service
%{_datadir}/dbus-1/services/org.cutefish.Mounts1.service
%{_datadir}/polkit-1/rules.d/60-cutefish-filemanager.rules

%files terminal
%license cutefish-terminal-%{version}/LICENSE
%{_bindir}/cutefish-terminal
%{_datadir}/applications/cutefish-terminal.desktop
%{_datadir}/cutefish-terminal/

%files -n xdg-desktop-portal-cutefish
%license xdg-desktop-portal-cutefish-%{version}/LICENSE
%{_libexecdir}/xdg-desktop-portal-cutefish
%{_prefix}/lib/systemd/user/xdg-desktop-portal-cutefish.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.cutefish.service
%{_datadir}/xdg-desktop-portal/cutefish-portals.conf
%{_datadir}/xdg-desktop-portal/portals/cutefish.portal

%files settings
%license cutefish-settings-%{version}/LICENSE
%{_bindir}/cutefish-settings
%{_datadir}/applications/cutefish-settings.desktop
%{_datadir}/cutefish-settings/
%{_datadir}/polkit-1/rules.d/60-cutefish-datetime.rules
%{_datadir}/polkit-1/rules.d/60-cutefish-device-name.rules

%files system-monitor
%license cutefish-system-monitor-%{version}/LICENSE
%{_bindir}/cutefish-system-monitor
%{_datadir}/applications/cutefish-system-monitor.desktop

%files text-editor
%license cutefish-text-editor-%{version}/LICENSE
%{_bindir}/cutefish-text-editor
%{_datadir}/applications/cutefish-text-editor.desktop

%files video-player
%license cutefish-video-player-%{version}/LICENSE
%{_bindir}/cutefish-video-player
%{_datadir}/applications/cutefish-video-player.desktop

%files calendar
%license cutefish-calendar-%{version}/LICENSE
%{_bindir}/cutefish-calendar
%{_bindir}/cutefish-calendar-reminders
%{_datadir}/applications/cutefish-calendar.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/cutefish-calendar-reminders.desktop

%files calculator
%license cutefish-calculator-%{version}/LICENSE
%{_bindir}/cutefish-calculator
%{_datadir}/applications/cutefish-calculator.desktop

%files preview
%license cutefish-preview-%{version}/LICENSE
%{_bindir}/cutefish-preview
%{_datadir}/applications/cutefish-preview.desktop

%files compositor
# The upstream install already drops LICENSE and the protocol XML files into
# the licenses directory under /usr/share, so an extra license macro line
# would list the same file twice.
%{_bindir}/cutefish-compositor
%{_bindir}/cutefish-displayctl
%{_bindir}/cutefish-screenshot
%{_libexecdir}/cutefish-auth-helper
%{_datadir}/applications/cutefish-screenshot.desktop
%{_datadir}/cutefish-compositor/
%{_datadir}/licenses/cutefish-compositor/
%config(noreplace) %{_sysconfdir}/pam.d/cutefish-auth

%files wallpapers
%license cutefish-wallpapers-%{version}/LICENSE
%{_datadir}/backgrounds/cutefishos/
%{_datadir}/cutefish/avatars/

%files l10n -f %{name}.lang

%files desktop

%changelog
* Tue Nov 17 2026 Bloom Perez <valenplayer3000+code@gmail.com> - 0.1.0-1
- Nightly snapshot of the Cutefish desktop environment, packaged from the
  current upstream branches of the github.com/cutefishos repositories.
