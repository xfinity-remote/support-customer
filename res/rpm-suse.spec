Name:       xfinity
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/lib/xfinity/
mkdir -p %{buildroot}/usr/share/xfinity/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/rustdesk %{buildroot}/usr/bin/xfinity
install $HBB/libsciter-gtk.so %{buildroot}/usr/lib/xfinity/libsciter-gtk.so
install $HBB/res/rustdesk.service %{buildroot}/usr/share/xfinity/files/xfinity.service
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/xfinity.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/xfinity.svg
install $HBB/res/rustdesk.desktop %{buildroot}/usr/share/xfinity/files/xfinity.desktop
install $HBB/res/rustdesk-link.desktop %{buildroot}/usr/share/xfinity/files/xfinity-link.desktop

%files
/usr/bin/xfinity
/usr/lib/xfinity/libsciter-gtk.so
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
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
