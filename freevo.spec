%define	name 	freevo
%define version 1.9.0
%define release %mkrel 2

%define 	_cachedir /var/cache
%define         py_ver 	  %(python -c 'import sys; print sys.version[:3]')

# Set default freevo parameters
%define display  x11

Summary:        Open-source digital video jukebox 
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
URL:            http://freevo.sourceforge.net/
Source0: 	http://belnet.dl.sourceforge.net/sourceforge/freevo/%{name}-%{version}.tar.gz
Source11:	freevo-mail-0.6.tgz 
Source1: 	redhat-boot_config
Source2:	local_conf.py
Source4:	firebird.py
Source7:	freevo_tvgrab
Source8:	mute
Source9:	unmute
Patch0:		%{name}-build.patch
Patch5: 	%{name}-webserver.patch
Patch6: 	%{name}-boot.patch
Patch7: 	%{name}-volume.patch
License: 	GPLv2+
Group: 		Video
Buildarch:	noarch
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires: 	docbook-utils
BuildRequires:  wget
%py_requires
BuildRequires:  pygame >= 1.5
BuildRequires:  python-twisted >= 1.1.0
BuildRequires:  python-imaging >= 1.1.4
BuildRequires:  python-kaa-base
BuildRequires:	python-kaa-metadata
BuildRequires:	python-kaa-imlib2
BuildRequires:  python-pyxml
BuildRequires:  python-devel
BuildRequires:	python-beautifulsoup >= 3.0.3
BuildRequires:  python-numeric
Requires:	pygame >= 1.5
Requires:	python-twisted >= 1.1.0
Requires:	python-imaging >= 1.1.4
Requires:	python-kaa-base
Requires:	python-kaa-metadata
Requires:	python-kaa-imlib2
Requires:	python-beautifulsoup >= 3.0.3
Requires:	python-lirc >= 0.0.4
Requires:	mplayer, tvtime, xine-ui, xmltv, PyXML, libjpeg-progs, mencoder, cdparanoia, vorbis-tools, util-linux, python-numeric, lsdvd, python-osd, xmltv-grabbers
Requires(pre):  rpm-helper
Requires(post): rpm-helper 
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Freevo is a Linux application that turns a PC with a TV capture card
and/or TV-out into a standalone multimedia jukebox/VCR. It builds on
other applications such as xine, mplayer, tvtime and mencoder to play
and record video and audio.

Available rpmbuild rebuild options :
--without: use_sysapps

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q
%patch0 -p0
%patch5 -p0
%patch6 -p0
#%patch7 -p0

%build
find . -name CVS | xargs rm -rf
find . -name ".cvsignore" |xargs rm -f
find . -name "*.pyc" |xargs rm -f
find . -name "*.pyo" |xargs rm -f
find . -name "*.py" |xargs chmod 644

#./autogen.sh
#Building freevo
cd %{_builddir}/%{name}-%{version}/
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build 

#Building mail menu
#cd %{_builddir}/%{name}-%{version}/*mail*
#PYTHONPATH=../build/lib env CFLAGS="$RPM_OPT_FLAGS" python setup.py build


%install
rm -rf $RPM_BUILD_ROOT/%{name}-%{version}

mkdir -p %{buildroot}%{_sysconfdir}/freevo
# The following is needed to let RPM know that the files should be backed up
touch %{buildroot}%{_sysconfdir}/freevo/freevo.conf

# boot scripts
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_bindir}
install -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/freevo/boot_config

mkdir -p %{buildroot}%{_cachedir}/freevo
mkdir -p %{buildroot}%{_cachedir}/freevo/{thumbnails,audio}
mkdir -p %{buildroot}%{_cachedir}/xmltv/logos
chmod 777 %{buildroot}%{_cachedir}/{freevo,freevo/thumbnails,freevo/audio,xmltv,xmltv/logos}

mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}/etc/freevo
mkdir -p %{buildroot}%{_datadir}/%{name}/contrib
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
mkdir -p %{buildroot}/tmp/%{name}/Videos
mkdir -p %{buildroot}/etc/cron.weekly

python setup.py install %{?_without_compile_obj:--no-compile} --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

#cp -av contrib/examples contrib/fbcon contrib/xmltv %{buildroot}%{_prefix}/contrib
cp -av contrib/lirc/ %{buildroot}/%{_datadir}/%{name}/contrib/
install -m 755 freevo %{buildroot}%{_datadir}/%{name}
install -m 755 freevo_config.py %{buildroot}%{_datadir}/%{name}
install %SOURCE2 $RPM_BUILD_ROOT/%{_sysconfdir}/freevo/local_conf.py
install %SOURCE7 $RPM_BUILD_ROOT/etc/cron.weekly
install %SOURCE8 $RPM_BUILD_ROOT%{_datadir}/%{name}
install %SOURCE9 $RPM_BUILD_ROOT%{_datadir}/%{name}

#######################
#Installing Initscripts
#######################
#install -m 755 boot/freevo %{buildroot}%{_sysconfdir}/rc.d/init.d
#install -m 755 boot/freevo_dep %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 boot/recordserver %{buildroot}%{_initrddir}/freevo_recordserver
install -m 755 boot/webserver %{buildroot}%{_initrddir}/freevo_webserver
#install -m 755 boot/recordserver_init %{buildroot}%{_bindir}/freevo_recordserver_init
#install -m 755 boot/webserver_init %{buildroot}%{_bindir}/freevo_webserver_init

####################
# Installing Plugins
####################
# Mailer Plugin
#cd %{_builddir}/%{name}-%{version}/*mail*
#PYTHONPATH=../build/lib python setup.py install %{?_without_compile_obj:--no-compile} --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
#
install %SOURCE4 $RPM_BUILD_ROOT/%{py_sitedir}/freevo/plugins

###############
# Copying icons
###############
install -D -m 644 %{_builddir}/%{name}-%{version}/share/icons/misc/freevo_app.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -D -m 644 %{_builddir}/%{name}-%{version}/share/icons/misc/freevo_app.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -D -m 644 %{_builddir}/%{name}-%{version}/share/icons/misc/freevo_app.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

#####################
# Adding a menu entry
####################
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT/%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%name
Comment=%{summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;TV;Player;Recorder;
EOF

####################
# About locales... #
####################

find %buildroot/%_datadir/locale -name "*.po" -exec rm -f {} \;
%find_lang %name

####################
# Cleaning
####################
rm -rf $RPM_BUILD_ROOT/%{_datadir}/fxd/web*

%pre
%_pre_useradd %{name} %{_datadir}/%{name} /bin/bash

%post
rm -rf /var/log/freevo 2>/dev/null
%if %mdkversion < 200900
%{update_menus}
%endif

#Determining TV_NORM & CHANNEL_LIST from local clock
ZONE=`grep "ZONE" /etc/sysconfig/clock | sed -e "s/^ZONE\=\(.*\)\/\(.*\)/\1/g"`
CITY=`grep "ZONE" /etc/sysconfig/clock | sed -e "s/^ZONE\=\(.*\)\/\(.*\)/\2/g"`
TV_NORM="ntsc"
CHANNEL_LIST="us-cable"

if [ "${CITY}" = "Paris" ]; then
TV_NORM="secam"
CHANNEL_LIST="france"
else
        if [ "${ZONE}" = "Europe" ]; then
                TV_NORM="pal"
                CHANNEL_LIST="europe-west"
        fi
fi

#Determining current X configuration
RESOLUTION=`xdpyinfo 2>/dev/null | grep dimensions | awk '{ print $2 }'`
case $RESOLUTION in
	"1280x800")
		RESOLUTION="1024x768";
		;;
	"1280x720")
		RESOLUTION="1024x768";
		;;
	"1680x1050")
		RESOLUTION="1280x1024";
		;;
	"1400x1050")
		RESOLUTION="1280x1024";
		;;

	"1920x1200")
		RESOLUTION="1600x1200";
		;;
	"")	
		RESOLUTION="800x600";
		;;
esac

# Copy old local_conf.py to replace dummy file
cd %{_datadir}/%{name}
./freevo setup --geometry=$RESOLUTION --display=%{display} \
        --tv=${TV_NORM} --chanlist=${CHANNEL_LIST} \
	%{!?_without_use_sysapps:--sysfirst} 

if [ ! -f /etc/freevo/lircrc ]; then
	ln -sf %{_datadir}/%{name}/contrib/lirc/pinnacle_PCTV /etc/freevo/lircrc
fi;
%_post_service freevo_webserver
%_post_service freevo_recordserver


%preun
%_preun_service freevo_recordserver
%_preun_service freevo_webserver

%clean
rm -rf $RPM_BUILD_ROOT

%postun
%if %mdkversion < 200900
%{clean_menus}
%endif
%_postun_userdel %{name}

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING ChangeLog FAQ INSTALL README local_conf.py.example Docs/*
%{_datadir}/%{name}
%{_bindir}/freevo
%{_iconsdir}/freevo.png
%{_liconsdir}/freevo.png
%{_miconsdir}/freevo.png
%{_datadir}/applications/mandriva-%{name}.desktop
%config(noreplace) /etc/cron.weekly/*
# Hu, even those files are need, tmpwatch will delete it !!
#%attr(777,root,root) %dir /tmp/%{name}/Videos
#%attr(777,root,root) %dir /tmp/%{name}/
%attr(777,root,root) %dir %{_cachedir}/freevo
%attr(777,root,root) %dir %{_cachedir}/freevo/audio
%attr(777,root,root) %dir %{_cachedir}/freevo/thumbnails
%attr(777,root,root) %dir %{_cachedir}/xmltv
%attr(777,root,root) %dir %{_cachedir}/xmltv/logos
%dir %{_sysconfdir}/freevo
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/freevo/*
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/rc.d/init.d/*
%{py_sitedir}/freevo
%{py_sitedir}/*.egg-info
%{_defaultdocdir}/%{name}-%{version}
