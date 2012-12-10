#if 0 /*
#endif

#python modules
import os, popen2, fcntl, select, time
import pygame
import osd

#freevo modules
import config, menu, rc, plugin, skin, util

import event as em
from item import Item

from gui.AlertBox import AlertBox
from gui.RegionScroller import RegionScroller
from gui.ListBox import ListBox
from gui.AlertBox import PopupBox
from gui.GUIObject import Align

#get the sinfletons so we can add our menu and get skin info
skin = skin.get_singleton()
menuwidget = menu.get_singleton()

osd = osd.get_singleton()
class CommandMainMenuItem(Item):
    def actions(self):
        """
        return a list of actions for this item
        """
        items = [ ( self.RunCmd , 'Internet' ) ]
        return items
    def RunCmd(self, arg=None, menuw=None):
        popup_string=_("Starting Web Browser...")
        pop = PopupBox(text=popup_string)
        pop.show()
	osd.stopdisplay()
        os.system('mozilla-firebird') 
	osd.restartdisplay()
	osd.update()
	pop.destroy()
	osd.update()

class PluginInterface(plugin.MainMenuPlugin):
    """
    A quick plugin to spawn a web browser from the main menu. Currently runs mozilla
    firebird. You may wish to have a look at http://www.irvined.co.uk/kiosk.shtml where you
    can download browser.jar which will give you a very minimal web browser.

    To activate, put the following in local_conf.py

    plugin.active('firebird', level=45)
    """
    def items(self, parent):
        menu_items = skin.settings.mainmenu.items

        item = CommandMainMenuItem()
        item.name = _('Internet')
        item.parent = parent
        return [ item ]


