#!/bin/sh
# Author: Brian Tomlinson
# Contact: darthlukan at gmail dot com

pkgname=lupdater
pkgver=1.2b
pkgrel=1
pkgdesc='Liquid Lemur Linux Update Notifier written in Python.'
arch=('any')
url='http://liquidlemur.com'
license=('GPLv2')
groups=('lemurapps')
depends=('python>=2.7, libnotify')
replaces=('lupdater')
source=(http://archrepo.liquidlemur.com/sources/any/$pkgname-$pkgver.tar.gz)
md5sums=('a4f1915222361b7becec4ef26121ae27')

build() {
    cd $srcdir/
    
    mkdir -p ${pkgdir}/usr/share/icons/
    cp -f lupdater.png ${pkgdir}/usr/share/icons/

    mkdir -p ${pkgdir}/usr/share/licenses/lupdater/
    cp -f LICENSE ${pkgdir}/usr/share/licenses/lupdater/

    mkdir -p ${pkgdir}/usr/share/doc/lupdater/
    cp -f README ${pkgdir}/usr/share/doc/lupdater/
    msg2 "README for lupdater is located in /usr/share/doc/lupdater"    

    mkdir -p ${pkgdir}/usr/share/applications/
    cp -f lupdater.desktop ${pkgdir}/usr/share/applications/

    mkdir -p ${pkgdir}/home/${SUDO_USER}/.config/autostart
    cp -f lupdater.desktop ${pkgdir}/home/${SUDO_USER}/.config/autostart/
    cp -f lupdaterapi.desktop ${pkgdir}/home/${SUDO_USER}/.config/autostart/
    msg2 "ludater.desktop has been placed in your ~/.config/autostart directory, lupdater will start automatically on next login."

    mkdir -p ${pkgdir}/usr/lib/python2.7/site-packages/
    cp -f lupdaterapi.py ${pkgdir}/usr/lib/python2.7/site-packages/
    chmod +x ${pkgdir}/usr/lib/python2.7/site-packages/lupdaterapi.py

    mkdir -p ${pkgdir}/usr/bin/
    cp -f lupdater.py ${pkgdir}/usr/bin/
    
    chmod +x ${pkgdir}/usr/bin/lupdater.py

    cd ${pkgdir}/usr/bin/
    ln -s lupdater.py lupdater

    msg2 "If you are not a Liquid Lemur Linux user, the following messages apply to you:"
    msg2 "You must now edit /etc/sudoers by adding (modulo)wheel ALL = NOPASSWD: /usr/bin/pacman -Syy for lupdater to work properly!"
    msg2 "Please read the README located in /usr/share/doc/lupdater for more information!"
}
