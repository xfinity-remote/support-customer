Name:       xfinity
Version:    1.3.5
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://rustdesk.com
Vendor:     rustdesk <info@rustdesk.com>
Requires:   gtk3 libxcb libxdo libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/lib/xfinity" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/lib/xfinity"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/rustdesk.service "%{buildroot}/usr/share/xfinity/files/xfinity.service"
install -Dm 644 $HBB/res/rustdesk.desktop "%{buildroot}/usr/share/xfinity/files/xfinity.desktop"
install -Dm 644 $HBB/res/rustdesk-link.desktop "%{buildroot}/usr/share/xfinity/files/xfinity-link.desktop"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/xfinity.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/xfinity.svg"

%files
/usr/lib/xfinity/*
/usr/share/xfinity/files/xfinity.service
/usr/share/icons/hicolor/256x256/apps/xfinity.png
/usr/share/icons/hicolor/scalable/apps/xfinity.svg
/usr/share/xfinity/files/xfinity.desktop
/usr/share/xfinity/files/xfinity-link.desktop

%changelog
# let's skip this for now

# https://www.cnblogs.com/xingmuxin/p/8990255.html
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
cp /usr/share/xfinity/files/xfinity.service /etc/systemd/system/
cp /usr/share/xfinity/files/xfinity.desktop /usr/share/applications/
cp /usr/share/xfinity/files/xfinity-link.desktop /usr/share/applications/
ln -s /usr/lib/xfinity/xfinity /usr/bin/xfinity
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
    rm /usr/share/applications/xfinity.desktop || true
    rm /usr/share/applications/xfinity-link.desktop || true
    rm /usr/bin/xfinity || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
