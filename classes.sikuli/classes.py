from sikuli import *
import org.sikuli.script.FindFailed as FindFailed

import sys
import os.path
import datetime
import yaml

Settings.MoveMouseDelay = 0
Settings.ActionLogs = False
Settings.InfoLogs = True
Settings.DebugLogs = True

applications = {
    'Darwin'   : '/Applications/Google Chrome.app',
    'Mac OS X' : '/Applications/Google Chrome.app',
    'Linux'    : '/usr/bin/chromium-browser'
}

import java.lang.System
os_name = java.lang.System.getProperty('os.name')
app_path = applications[os_name]
browser = App(app_path)

def log(message):
    print "[" + str(datetime.datetime.now()) + "] " + message

arrow_up = Pattern("arrow_up.png")
arrow_down = Pattern("arrow_down.png")
button_ok = Pattern("button_ok.png")
button_close = Pattern("button_close.png")
button_accept  = Pattern("button_accept.png")
scroll_not_bottom = Pattern("scroll_not_bottom.png").similar(0.98)
current_sector = None

class BaseWindow(object):
    """An abstract for functionality shared between things that pop up windows"""
    # set by child elements
    # button          | button to open this window
    # dimensions      | size of window
    # offset          | between x/y of key and actual region
    # key             | letter used to open window
    # key_image       | unique element to identify this region's window
    # key_image_match | stores key_image match

    def __init__(self):
        self.key = None # key to open window
        self.button_region = None # stores button match
        self.window_region = None # window's whole region

        # this might be declared in a sub-class
        if not hasattr(self, 'id'):
            self.id = str(self.__class__.__name__).lower()
        if not hasattr(self, 'key_image'):
            self.key_image = Pattern("window_%(id)s_key.png" % {'id':self.id}).similar(0.85)
        if not hasattr(self, 'button'):
            self.button = Pattern("button_%(id)s.png" % {'id':self.id}).similar(0.60)
        self.get_button_region()

    def open(self):
        self.show_window()
        if not hasattr(self, 'key_image_match'):
            self.key_image_match = find(self.key_image)
            self.window_region = Region(
                self.key_image_match.getX() + self.offset['x'],
                self.key_image_match.getY() + self.offset['y'],
                self.dimensions['width'],
                self.dimensions['height']
            )
            self.get_sub_regions()

    # override this to have a custom window opening method, such as mayor's house
    def show_window(self):
        try:
            find(self.key_image) # screen context
        except FindFailed:
            self.button_region.click()

    def close(self):
        try:
            self.window_region.click(button_close)
        except FindFailed:
            log("close button not found, nothing to do!")

    def get_button_region(self):
        if self.button_region is None:
            self.button_region = find(self.button)

    def get_sub_regions(self):
        raise NotImplementedError # stub

class ProvisionHouse(BaseWindow):
    dimensions = { 'width':578, 'height':415 }
    offset = { 'x':0, 'y':0 }
    button = None

    tabs = {
        'buffs' : Pattern("provisionhouse_tab_buffs.png"),
        'resources' : Pattern("provisionhouse_tab_resources.png"),
        'deposits' : Pattern("provisionhouse_tab_deposits.png"),
        'event' : Pattern("provisionhouse_tab_event.png"),
    }

    products = {
        'fish_platter' : Pattern("product_fish_platter.png"),
        'solid_sandwich' : Pattern("product_solid_sandwich.png"),
        'fish_food' : Pattern("product_fish_food.png"),
        'deer_musk' : Pattern("product_deer_musk.png"),
        # '' : Pattern("product_.png"),
        # '' : Pattern("product_.png"),
        # '' : Pattern("product_.png"),
        # '' : Pattern("product_.png"),
        # '' : Pattern("product_.png"),
        'aunt_irma' : Pattern("product_aunt_irma.png")
    }

    def show_window(self):
        type("p")

    def get_button_region(self):
        pass

    def get_sub_regions(self):
        self.product_region = Region( # x,y,w,h
            self.window_region.getX() + 167,
            self.window_region.getY() + 107,
            158,
            276
        )
        self.queue_region = Region( # x,y,w,h
            self.window_region.getX() + 331,
            self.window_region.getY() + 93,
            225,
            289
        )
        self.tab_region = Region( # x,y,w,h
            self.window_region.getX() + 0,
            self.window_region.getY() + 388,
            578,
            26
        )

class StarMenu(BaseWindow):
    """The star menu.  Does almost everything."""
    dimensions = { 'width':388, 'height':255 }
    offset = { 'x':-70, 'y':26 }

    tabs = {
        'all' : Pattern("starmenu_tab_all.png"),
        'specialists' : Pattern("starmenu_tab_specialists.png"),
        'buffs' : Pattern("starmenu_tab_buffs.png"),
        'resources' : Pattern("starmenu_tab_resources.png"),
        'misc' : Pattern("starmenu_tab_misc.png"),
    }

    actors = {
        'explorers' : {
            'experienced_explorer' : Pattern("button_experienced_explorer.png").similar(0.90),
            'savage_scout' : Pattern("button_savage_scout.png").similar(0.90),
            'explorer' : Pattern("button_explorer.png").similar(0.90)
        },
        'geologists' : {
            'jolly_geologist' : Pattern("button_jolly_geologist.png").similar(0.90),
            'geologist' : Pattern("button_geologist.png").similar(0.90)
        }
    }

    resources = {
        'brew'            : Pattern("resource_brew.png").exact(),
        'balloons'        : Pattern("resource_balloons.png").exact(),
        'gold_ore'        : Pattern("resource_gold_ore.png").exact(),
        # 'coal'            : Pattern("resource_coal.png").exact(),
        'exotic_logs'     : Pattern("resource_exotic_wood.png").exact(),
        'gold_coins'      : Pattern("resource_gold_coins.png").exact(),
        'granite'         : Pattern("resource_granite.png").exact(),
        'guild_coins'     : Pattern("resource_guild_coins.png").exact(),
        'map_frags'       : Pattern("resource_map_fragments.png").exact(),
        'iron_swords'     : Pattern("resource_iron_swords.png").exact(),
        'longbows'        : Pattern("resource_longbows.png").exact(),
        'marble'          : Pattern("resource_marble.png").exact(),
        'copper_ore'      : Pattern("resource_copper_ore.png").exact(),
        'bows'            : Pattern("resource_bows.png").exact(),
        'hardwood_planks' : Pattern("resource_hardwood_planks.png").exact(),
        'pinewood_planks' : Pattern("resource_pinewood_planks.png").exact(),
        'titanium'        : Pattern("resource_titanium.png").exact(),
        'steel_swords'    : Pattern("resource_steel_swords.png").exact(),
        'steel'           : Pattern("resource_steel.png").exact(),
        'crossbows'       : Pattern("resource_crossbows.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        # '' : Pattern("resource_.png").exact(),
        'saltpeter'       : Pattern("resource_saltpeter.png").exact()
    }

    def get_sub_regions(self):
        self.resource_region = Region( # x,y,w,h
            self.window_region.getX() + 7,
            self.window_region.getY() + 10,
            338,
            212
        )
        self.scroll_region = Region( # x,y,w,h
            self.window_region.getX() + 346,
            self.window_region.getY() + 8,
            18,
            216
        )
        self.tab_region = Region( # x,y,w,h
            self.window_region.getX() + 1,
            self.window_region.getY() + 223,
            383,
            29
        )
        # self.resource_region.highlight(1)
        # self.scroll_region.highlight(1)
        # self.tab_region.highlight(1)

    def select_tab(self, tab):
        self.tab_region.click(self.tabs[tab])

    def deposit_resources(self):
        mh = MayorsHouse()
        mh.goToSector().center()

        log("depositing resources")
        self.open()
        self.select_tab('resources')
        while True:
            found = 0
            for key,resource in self.resources.iteritems():
                log("--checking %(key)s" % { 'key':key })
                while self.resource_region.exists(resource):
                    self.resource_region.click(resource)
                    time.sleep(0.3)
                    mh.deposit()
                    time.sleep(0.5)
                    found += 1
                    log("----deposited %(key)s" % { 'key':key })
                    self.open()
            if found is 0 and not self.scroll_region.exists(Pattern("window_starmenu_scrollbottom.png")):
                log("all done, break!")
                break
            else:
                self.scroll_region.wheel(WHEEL_DOWN, 1)
        self.close()

    def dispatch_explorers(self):
        self.open()
        self.select_tab('specialists')
        for actor_type,pattern in self.actors['explorers'].iteritems():
            log('looking for %(actor_type)s' % { 'actor_type':actor_type})
            try:
                matches = self.resource_region.findAll(pattern)
                while matches.hasNext():
                    log('found one!')
                    match = matches.next()
                    match.highlight(1)
                    Actor(actor_type,match).act()
                    self.open()
            except FindFailed:
                log('didn\'t find any %(actor_type)s!' % { 'actor_type':actor_type})
        self.close()

    def dispatch_geologists(self):
        self.open()
        self.select_tab('specialists')


class Mailbox(BaseWindow):
    """The mailbox class. Used for accepting mail"""
    dimensions = { 'width':586, 'height':395 }
    offset = { 'x':-271, 'y':0 }

    def get_sub_regions(self):
        self.subject_region = Region( # x,y,w,h
            self.window_region.getX() + 253,
            self.window_region.getY() + 56,
            181,
            152
        )
        self.content_region = Region( # x,y,w,h
            self.window_region.getX() + 9,
            self.window_region.getY() + 237,
            569,
            150
        )

    subjects = {
        'explorer_has' : Pattern("subject_explorer_has.png").similar(0.60),
        'quest_reward' : Pattern("subject_quest_reward.png").similar(0.60)
    }

    def get_mail(self):
        self.open()
        log("checking mail")
        while True:
            found = 0
            for key, subject in self.subjects.iteritems():
                log("--checking %(key)s" % { 'key':key })
                while self.subject_region.exists(subject):
                    self.subject_region.doubleClick(subject)
                    time.sleep(0.6)
                    self.content_region.click(button_accept)
                    time.sleep(0.4)
                    found += 1
                    log("----clicked on %(key)s" % { 'key':key })
            if found == 0:
                log("all done, break!")
                break
        self.close()

class Actor(BaseWindow):
    dimensions = { 'width':361, 'height':432 }
    offset = { 'x':5, 'y':-19 }

    def __init__(self, actor_type, match):
        self.id = actor_type
        self.type = actor_type

        self.button_region = match
        self.key_image = Pattern("window_agent_key.png").similar(0.85)

        handle = open(os.path.join(getBundlePath(),'explorers.yml'),'r')
        actions = yaml.safe_load(handle)
        handle.close()

        self.action_str = actions[self.type]['action']
        self.duration_str = actions[self.type]['duration']

        self.action = Pattern('actor_action_find_%(action)s.png' % { 'action' : self.action_str }).similar(0.96)
        self.duration = Pattern('actor_action_find_%(action)s_%(duration)s.png' % { 'action' : self.action_str, 'duration' : self.duration_str }).similar(0.96)

    def get_sub_regions(self):
        # this is the location of the name box for the initial window
        # but it is offset based on the size of the larger window
        # i'm lazy, sue me
        self.name_region = Region( # x,y,w,h
            self.window_region.getX() + 67,
            self.window_region.getY() + 27,
            235,
            19
        )
        self.action_region = Region( # x,y,w,h
            self.window_region.getX() + 13,
            self.window_region.getY() + 181,
            336,
            135
        )
        self.resolution_region = Region( # x,y,w,h
            self.window_region.getX() + 13,
            self.window_region.getY() + 356,
            336,
            65
        )

    def act(self):
        self.open()
        mouseMove(self.window_region.getTopLeft())
        self.choose_action()
        self.choose_duration()

    def choose_action(self):
        self.action_region.click(self.action)
        mouseMove(self.window_region.getTopLeft())

    def choose_duration(self):
        self.action_region.click(self.duration)
        self.resolution_region.click(button_ok)

class Location(object):
    """An abstract for functionality shared between clickable locations"""
    # sector

    def goToSector(self):
        global current_sector
        if self.sector != current_sector:
            type("0")
            sleep(0.5)
            type(self.sector)
            sleep(0.5)
            current_sector = self.sector

class Deposit(Location):
    """Deposits are meat, fish, etc."""
    pass

class Building(Location):
    """Buildings have a distinct appearance and can be found easily"""
    # key_image

    def center(self):
        if exists(self.key_image):
            dragDrop(getLastMatch(), getCenter())
        else:
            raise "Couldn't find my key image!"

    def deposit(self):
        mouseMove(getCenter().left(100))
        sleep(0.5)
        click(getCenter())

class MayorsHouse(Building):
    sector = "1"
    key_image = Pattern("building_mayors_house.png")

class Golem(BaseWindow):
    def open(self):
        sm = StarMenu()
        sm.open()
        sm.select_tab('buffs')
        while True:
            log("checking if any resources exist")
            # check if one of the key buffs is visible
            if sm.resource_region.exists(buff_marble):
                log("found marble buff!")
                sm.resource_region.click(buff_marble)
                break
            elif sm.resource_region.exists(buff_wheat):
                log("found wheat buff!")
                sm.resource_region.click(buff_wheat)
                break
            elif sm.resource_region.exists(buff_water):
                log("found water buff!")
                sm.resource_region.click(buff_water)
                break
            else:
                log("none existed, checking if at the bottom")
                if sm.scroll_region.exists(scroll_not_bottom):
                    log("not at the bottom, scrolling down")
                    for i in range(6):
                        sm.scroll_region.click(arrow_down)
                else:
                    log("at the bottom, none found, so sad!")
                    break


browser.focus()
Mailbox().get_mail()
# StarMenu().deposit_resources()
StarMenu().dispatch_explorers()

# buff_marble = Pattern("buff_marble.png").similar(0.98)
# buff_wheat = Pattern("buff_wheat.png").similar(0.98)
# buff_water = Pattern("buff_water.png").similar(0.98)



# if one of the buffs exists, click it
# else
# if we're at the bottom, raise exception
# otherwise, scroll down