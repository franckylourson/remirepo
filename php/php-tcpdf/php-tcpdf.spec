%global dl_version 6_0_012
%global real_name  tcpdf

Name:           php-tcpdf
Summary:        PHP class for generating PDF documents
Version:        6.0.012
Release:        1%{?dist}

Source0:        http://downloads.sourceforge.net/%{real_name}/%{real_name}_%{dl_version}.zip
URL:            http://www.tcpdf.org
License:        LGPLv3+
Group:          Development/Libraries

Patch0:         php-tcpdf_badpath.patch
Patch1:         php-tcpdf_cachepath.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php >= 5.2
Requires:       php-openssl
#imagick is optionnal (and conflicts with gmagick)
#Requires:       php-pecl(imagick)
Requires:       php-spl
Requires:       php-bcmath
Requires:       php-curl
Requires:       php-date
Requires:       php-gd
Requires:       php-hash
Requires:       php-mbstring
Requires:       php-mcrypt
Requires:       php-pcre
Requires:       php-tidy
Requires:       php-xml


%description
PHP class for generating PDF documents.

* no external libraries are required for the basic functions;
* all standard page formats, custom page formats, custom margins and units
  of measure;
* UTF-8 Unicode and Right-To-Left languages;
* TrueTypeUnicode, OpenTypeUnicode, TrueType, OpenType, Type1 and CID-0 fonts;
* font subsetting;
* methods to publish some XHTML + CSS code, Javascript and Forms;
* images, graphic (geometric figures) and transformation methods;
* supports JPEG, PNG and SVG images natively, all images supported by GD 
  (GD, GD2, GD2PART, GIF, JPEG, PNG, BMP, XBM, XPM) and all images supported
  via ImagMagick (http: www.imagemagick.org/www/formats.html)
* 1D and 2D barcodes: CODE 39, ANSI MH10.8M-1983, USD-3, 3 of 9, CODE 93,
  USS-93, Standard 2 of 5, Interleaved 2 of 5, CODE 128 A/B/C, 2 and 5 Digits
  UPC-Based Extention, EAN 8, EAN 13, UPC-A, UPC-E, MSI, POSTNET, PLANET,
  RMS4CC (Royal Mail 4-state Customer Code), CBC (Customer Bar Code),
  KIX (Klant index - Customer index), Intelligent Mail Barcode, Onecode,
  USPS-B-3200, CODABAR, CODE 11, PHARMACODE, PHARMACODE TWO-TRACKS,
  Datamatrix ECC200, QR-Code, PDF417;
* ICC Color Profiles, Grayscale, RGB, CMYK, Spot Colors and Transparencies;
* automatic page header and footer management;
* document encryption up to 256 bit and digital signature certifications;
* transactions to UNDO commands;
* PDF annotations, including links, text and file attachments;
* text rendering modes (fill, stroke and clipping);
* multiple columns mode;
* no-write page regions;
* bookmarks and table of content;
* text hyphenation;
* text stretching and spacing (tracking/kerning);
* automatic page break, line break and text alignments including justification;
* automatic page numbering and page groups;
* move and delete pages;
* page compression (requires php-zlib extension);
* XOBject templates;
* PDF/A-1b (ISO 19005-1:2005) support.

By default, TCPDF uses the GD library which is know as slower than ImageMagick
solution. You can optionally install php-pecl(imagick); TCPDF will use it.


%prep
%setup -qn %{real_name}
%patch0 -p1
%patch1 -p1
: globally fix permissions, always broken...
chmod 755 `find ./ -type d`
chmod 644 `find ./ -type f`
: remove composer
rm -f composer.json
: langs are not config...
mv config/lang .
: move certs in examples
mv config/cert examples/
: some files in config are relevant for examples only
mv images examples/
mkdir examples/cache
mv cache/* examples/cache/
: change examples include paths
sed -i examples/*.php examples/barcodes/*.php \
    -e "s|../config/cert/|./cert/|" \
    -e "s|../config/lang|%{_datadir}/php/%{real_name}/lang|g" \
    -e "s|../%{real_name}.php|%{real_name}.php|" \
    -e "s|../config/tcpdf_config_alt.php|%{_sysconfdir}/%{name}/%{real_name}_config_alt.php|" \
    -e "s|../cache/|./cache/|" \
    -e "s|../images/|./images/|" \
    -e "s|dirname(__FILE__).'/../../|'|"
: wrong end-of-line encoding
sed -i 's/\r//' \
    lang/bul.php \
    examples/images/bug.eps \
    examples/images/tiger.ai \
    examples/images/pelican.ai
pushd examples
: non UTF8 files
iconv -f iso8859-1 -t utf-8 example_030.php > example_030.php.conv && mv -f example_030.php.conv example_030.php
popd


%build
: empty build section, nothing required


%install
rm -rf $RPM_BUILD_ROOT
# install
install -d $RPM_BUILD_ROOT%{_datadir}/php/%{name}
cp -a *.php $RPM_BUILD_ROOT%{_datadir}/php/%{name}/
cp -a include $RPM_BUILD_ROOT%{_datadir}/php/%{name}/
cp -a fonts $RPM_BUILD_ROOT%{_datadir}/php/%{name}/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -s ../../../..%{_sysconfdir}/%{name} $RPM_BUILD_ROOT%{_datadir}/php/%{name}/config
install -d $RPM_BUILD_ROOT%{_localstatedir}/cache/%{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.TXT README.TXT CHANGELOG.TXT doc/* examples
%{_datadir}/php/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%dir %attr(-,apache,apache) %{_localstatedir}/cache/%{name}


%changelog
* Thu May 09 2013 Johan Cwiklinski <johan AT x-tnd DOt be> - 6.0.012-1.trashy
- Initial packaging