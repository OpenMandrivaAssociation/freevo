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
cd $RPM_BUILD_DIR/%{name}-%{version}/
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build 

#Building mail menu
#cd $RPM_BUILD_DIR/%{name}-%{version}/*mail*
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
#cd $RPM_BUILD_DIR/%{name}-%{version}/*mail*
#PYTHONPATH=../build/lib python setup.py install %{?_without_compile_obj:--no-compile} --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
#
install %SOURCE4 $RPM_BUILD_ROOT/%{py_sitedir}/freevo/plugins

###############
# Copying icons
###############
install -D -m 644 $RPM_BUILD_DIR/%{name}-%{version}/share/icons/misc/freevo_app.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -D -m 644 $RPM_BUILD_DIR/%{name}-%{version}/share/icons/misc/freevo_app.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -D -m 644 $RPM_BUILD_DIR/%{name}-%{version}/share/icons/misc/freevo_app.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

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


%changelog
* Tue Nov 02 2010 Crispin Boylan <crisb@mandriva.org> 1.9.0-2mdv2011.0
+ Revision: 591981
- Rebuild

* Sun Aug 30 2009 Crispin Boylan <crisb@mandriva.org> 1.9.0-1mdv2010.0
+ Revision: 422461
- LSB-ify init scripts
- New release

* Mon Dec 29 2008 Crispin Boylan <crisb@mandriva.org> 1.8.3-1mdv2009.1
+ Revision: 321178
- BuildRequires numeric
- New release

* Sun Aug 31 2008 Crispin Boylan <crisb@mandriva.org> 1.8.2-1mdv2009.0
+ Revision: 277757
- New release

* Sun Aug 31 2008 Crispin Boylan <crisb@mandriva.org> 1.8.1-3mdv2009.0
+ Revision: 277756
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.8.1-2mdv2009.0
+ Revision: 266821
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Jun 02 2008 Crispin Boylan <crisb@mandriva.org> 1.8.1-1mdv2009.0
+ Revision: 214197
- New version

* Mon May 12 2008 Crispin Boylan <crisb@mandriva.org> 1.8.0-1mdv2009.0
+ Revision: 206442
- New version

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.7.6.1-2mdv2008.1
+ Revision: 170845
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Wed Feb 06 2008 Crispin Boylan <crisb@mandriva.org> 1.7.6.1-1mdv2008.1
+ Revision: 163297
- New release
- New release

* Fri Dec 28 2007 Crispin Boylan <crisb@mandriva.org> 1.7.5-1mdv2008.1
+ Revision: 138698
- New release

* Fri Dec 21 2007 Crispin Boylan <crisb@mandriva.org> 1.7.4-1mdv2008.1
+ Revision: 136714
- New version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 07 2007 Funda Wang <fwang@mandriva.org> 1.7.3-3mdv2008.1
+ Revision: 116177
- use %%py_requires
- drop old menus

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Fri Aug 24 2007 Erwan Velu <erwan@mandriva.org> 1.7.3-2mdv2008.0
+ Revision: 70747
- Oups, defaultdocdir was missing in the files section
- Fixing menu generation

* Sat Aug 11 2007 Crispin Boylan <crisb@mandriva.org> 1.7.3-1mdv2008.0
+ Revision: 61919
- New version, remove patch 12 (merged upstream)

* Fri Jun 01 2007 Crispin Boylan <crisb@mandriva.org> 1.7.2-1mdv2008.0
+ Revision: 33511
- New release

* Mon Apr 30 2007 Crispin Boylan <crisb@mandriva.org> 1.7.1-1mdv2008.0
+ Revision: 19406
- New release

* Tue Apr 17 2007 Crispin Boylan <crisb@mandriva.org> 1.7.0-2mdv2008.0
+ Revision: 13698
- Update local_conf.py file for latest version


* Tue Mar 13 2007 Crispin Boylan <crisb@mandriva.org> 1.7.0-1mdv2007.1
+ Revision: 143256
- Clean spec
- Remove merged patches 4,8 and sources 5,6
- Remove merged patches
- Remove merged weather and crystal plugins
- Disable freevo-mail (for now) as it doesnt work
- New version 1.7.0
- Requires kaa libraries
- Remove python-mm deps

* Wed Jan 03 2007 Crispin Boylan <crisb@mandriva.org> 1.6.2-1mdv2007.1
+ Revision: 103601
-Use py_sitedir instead of libdir
-XDG Menu
-Add python-devel to BuildRequires
-Add python-pyxml to BuildRequires
-Add patch12 to fix elementtree def
-New version
- Import freevo

* Wed Nov 16 2005 Erwan Velu <erwan@seanodes.com> 1.5.4-1mdk
- 1.5.4
- Adding 16/10 screen detection
- Fixing wrong path in freevo : removing stupid (drunked ?) patch12

* Tue Oct 04 2005 Erwan Velu <erwan@seanodes.com> 1.5.3-2mdk
- Adding dvb-t configuration
- Fixing wrong path which prevent webserver from starting
- Fixing rpm-helper requires
- Moving to noarch as there is no binary

* Mon Jan 24 2005 Erwan Velu <erwan@seanodes.com> 1.5.3-1mdk
- 1.5.3

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 1.5.2-2mdk
- Rebuild for new python

* Fri Nov 12 2004 Erwan Velu <erwan@seanodes.com> 1.5.2-1mdk
- 1.5.2

* Thu Sep 16 2004 Erwan Velu <erwan@mandrakesoft.com> 1.5.1-2mdk
- Missing dependencies on xmltv-grabbers

* Wed Sep 15 2004 Erwan Velu <erwan@mandrakesoft.com> 1.5.1-1mdk
- 1.5.1

* Sun Aug 15 2004 Erwan Velu <erwan@mandrakesoft.com> 1.5.0-1mdk
- 1.5.0
- Regenerating patch 1
- Remove patch 3 merged upstream
- Disabling patch 8, 9
- Adding python-numeric, lsdvd, python-osd requires
- Rework default freevo configuration
- Adding Weather Application
- New crystal theme

