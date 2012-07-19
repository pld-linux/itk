Summary:	[incr Tk] - object-oriented extension of the Tcl/Tk language
Summary(pl.UTF-8):	[incr Tk] - obiektowo zorientowane rozszerzenie języka Tcl/Tk
%define snap	20111128
Name:		itk
Version:	3.4
Release:	0.%{snap}.2
License:	distributable
Group:		Development/Languages/Tcl
#Source0:	http://downloads.sourceforge.net/incrtcl/%{name}%{version}.tar.gz
# fossil clone http://core.tcl.tk/itk itk.fossil && mkdir itk && cd itk && fossil open ../itk.fossil itk-3-branch
Source0:	%{name}-3-%{snap}.tar.xz
# Source0-md5:	837ebeadb9f2e167431248186bf3f3e0
Patch0:		%{name}-soname.patch
Patch1:		%{name}-tclconfig.patch
URL:		http://incrtcl.sourceforge.net/itk/
BuildRequires:	autoconf >= 2.13
BuildRequires:	itcl-devel >= 3.4.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	tk-devel >= 8.4.6
BuildRequires:	xz
Requires:	itcl >= 3.4.1
Requires:	tk >= 8.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	%{_prefix}/lib

%description
[incr Tk] is a framework for building mega-widgets using the [incr
Tcl] object system. Mega-widgets are high-level widgets like a file
browser or a tab notebook that act like ordinary Tk widgets but are
constructed using Tk widgets as component parts, without having to
write C code. In effect, a mega-widget looks and acts exactly like a
Tk widget, but is considerably easier to implement.

%description -l pl.UTF-8
[incr Tk] to szkielet do tworzenia mega-widgetów przy użyciu systemu
obiektów [incr ZTcl]. Mega-widgety to widgety wyższego poziomu, takie
jak przeglądarka plików czy notatnik z zakładkami, zachowujące się jak
zwykłe widgety Tk, ale skonstruowane z części składowych będących
widgetami Tk bez potrzeby pisania kodu w C. W efekcie mega-widget
wygląda i zachowuje się dokładnie tak, jak widget Tk, ale jest
znacząco łatwiejszy w implementacji.

%package devel
Summary:	Header files for itk library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki itk
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	itcl-devel >= 3.4.1
Requires:	tk-devel >= 8.4.6

%description devel
Header files for itk library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki itk.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure \
	--libdir=%{_ulibdir}

%{__make} \
	CFLAGS_DEFAULT=

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_ulibdir}/itk%{version}/libitk* $RPM_BUILD_ROOT%{_libdir}

libfile=$(basename $RPM_BUILD_ROOT%{_libdir}/libitk%{version}.so.0.*)
ln -sf $libfile $RPM_BUILD_ROOT%{_libdir}/libitk%{version}.so.0
ln -sf $libfile $RPM_BUILD_ROOT%{_libdir}/libitk%{version}.so
ln -sf $libfile $RPM_BUILD_ROOT%{_libdir}/libitk.so

# some substs missing in configure, install missing in Makefile
%{__sed} -i -e "s,ITCL_VERSION='@ITCL_VERSION@',ITK_VERSION='%{version}'," \
	-e 's,@ITK_LIB_FILE@,libitk%{version}.so,' \
	-e 's,@ITK_BUILD_LIB_SPEC@,-litk%{version},' \
	-e 's,@ITK_LIB_SPEC@,-litk%{version},' \
	-e 's,@ITK_STUB_LIB_FILE@,,' \
	-e 's,@ITK_BUILD_STUB_LIB_SPEC@,,' \
	-e 's,@ITK_STUB_LIB_SPEC@,,' \
	-e 's,@ITK_SRC_DIR@,%{_ulibdir},' itkConfig.sh
install itkConfig.sh $RPM_BUILD_ROOT%{_ulibdir}

%{__sed} -i -e 's#%{_ulibdir}#%{_libdir}#' $RPM_BUILD_ROOT%{_ulibdir}/itk%{version}/pkgIndex.tcl

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libitk%{version}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libitk%{version}.so.0
%dir %{_ulibdir}/itk%{version}
%{_ulibdir}/itk%{version}/*.itk
%{_ulibdir}/itk%{version}/*.tcl
%{_ulibdir}/itk%{version}/tclIndex
%{_mandir}/mann/Archetype.n*
%{_mandir}/mann/Toplevel.n*
%{_mandir}/mann/Widget.n*
%{_mandir}/mann/itk.n*
%{_mandir}/mann/itkvars.n*
%{_mandir}/mann/usual.n*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libitk%{version}.so
%attr(755,root,root) %{_libdir}/libitk.so
%attr(755,root,root) %{_ulibdir}/itkConfig.sh
%{_includedir}/itk*.h
