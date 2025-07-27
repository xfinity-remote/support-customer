Name:       xfinity
Version:    1.4.1
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     rustdesk <info@rustdesk.com>
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/xfinity" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/xfinity"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/rustdesk.service "%{buildroot}/usr/share/xfinity/files/xfinity.service"
install -Dm 644 $HBB/res/rustdesk.desktop "%{buildroot}/usr/share/xfinity/files/xfinity.desktop"
install -Dm 644 $HBB/res/rustdesk-link.desktop "%{buildroot}/usr/share/xfinity/files/xfinity-link.desktop"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/xfinity.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/xfinity.svg"

%files
/usr/share/xfinity/*
/usr/share/xfinity/files/xfinity.service
/usr/share/icons/hicolor/256x256/apps/xfinity.png
/usr/share/icons/hicolor/scalable/apps/xfinity.svg
/usr/share/xfinity/files/xfinity.desktop
/usr/share/xfinity/files/xfinity-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop xfinity || true
  ;;
esac

%post
cp /usr/share/xfinity/files/xfinity.service /etc/systemd/system/xfinity.service
cp /usr/share/xfinity/files/xfinity.desktop /usr/share/applications/
cp /usr/share/xfinity/files/xfinity-link.desktop /usr/share/applications/
ln -sf /usr/share/xfinity/xfinity /usr/bin/xfinity
systemctl daemon-reload
systemctl enable xfinity
systemctl start xfinity
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop xfinity || true
    systemctl disable xfinity || true
    rm /etc/systemd/system/xfinity.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/xfinity || true
    rmdir /usr/lib/xfinity || true
    rmdir /usr/local/xfinity || true
    rmdir /usr/share/xfinity || true
    rm /usr/share/applications/xfinity.desktop || true
    rm /usr/share/applications/xfinity-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/xfinity || true
    rmdir /usr/local/xfinity || true
  ;;
esac
