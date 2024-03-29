Name:               bino
Version:            1.6.8
Release:            7%{dist}
Summary:            Video Player with 3D and Multi-Display Video Support

Source:             https://bino3d.org/releases/%{name}-%{version}.tar.xz
Source1:            bino.desktop
#Patch:              ffmpeg4_fix.patch

URL:                http://bino.nongnu.org/
Group:              Applications/Multimedia
License:            GPLv2

BuildRequires:      pkgconfig(Qt5)
BuildRequires:      pkgconfig(glew) >= 1.5.0
BuildRequires:      pkgconfig(libavcodec) >= 0.8
BuildRequires:      pkgconfig(openal)
BuildRequires:      pkgconfig
BuildRequires:      autoconf
BuildRequires:      automake
BuildRequires:      gcc-c++
BuildRequires:      libtool
BuildRequires:      desktop-file-utils
BuildRequires:      texinfo
BuildRequires:      pkgconfig(libass)
BuildRequires:      pkgconfig(x11)
BuildRequires:      gettext-devel
BuildRequires:      libquadmath-devel
BuildRequires:      ffmpeg-devel
BuildRequires:      libsndfile
BuildRequires:      flac-libs

Requires:           hicolor-icon-theme

Requires(preun):    info
Requires(post):     info

%description
Bino is a video player with two special features:
* support for 3D videos, with a wide variety of input and output formats.
* support for multi display video, e.g. for Virtual Reality
  installations and other multi-projector setups.


%prep
%autosetup -n %{name}-%{version} -p1
mkdir m4
autoreconf -i

# fix removal of translations
pushd po
mv zh{_cn,_CN}.po
sed -i 's/_cn/_CN/' LINGUAS
popd

%build
%configure --disable-silent-rules --with-qt-version=5

%make_build


%install
%make_install

rm -rf "%{buildroot}%{_datadir}/doc"
rm -f %{buildroot}%{_infodir}/dir

desktop-file-install %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%find_lang "%{name}" || echo -n >"%{name}.lang"

%post
/usr/bin/update-desktop-database &> /dev/null || :
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}//bino.info.gz || :

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/bino.info.gz || :
fi

%postun
/usr/bin/update-desktop-database &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog README
%doc doc/*.html doc/*.jpg doc/*.png
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_infodir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_infodir}/*


%changelog

* Wed Jan 05 2022 David Va <davidva AT tuta DOT io> - 1.6.8-7
- Updated to 1.6.8

* Thu Sep 06 2018 David Va <davidva AT tuta DOT io> - 1.6.7-3
- Updated to 1.6.7

* Mon Jun 18 2018 David Va <davidva AT tutanota DOT com> - 1.6.6-3
- Rebuild for libass
- Updated to current commit

* Tue Jan 16 2018 David Va <davidva AT tutanota DOT com> - 1.6.6-2
- Updated to 1.6.6

* Wed Jun 07 2017 David Vásquez <davidva AT tutanota DOT com> - 1.6.5-2
- Initial build

