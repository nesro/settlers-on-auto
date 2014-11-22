from sikuli import *
import datetime

def log(message):
    print "[" + str(datetime.datetime.now()) + "] " + message

def move(xstep, ystep):
    log("move called with xstep=%s and ystep=%s" % (xstep, ystep))
    dragDrop(getCenter().offset(xstep,ystep),getCenter())

#pause. increase the time, if you have time :)
def p():
    time.sleep(1)

def close_windows():
    return
    b=exists("1415351580086.png")
    if b:
        click(b)
    return
    a=exists("1415351289651.png")
    if a:
        click(a)
    c=exists("1415351761625.png")
    if c:
        click(c)
        
def reset():
    App.focus('chrome')
    click("1413909539900.png")
    p()
    mouseMove(getCenter())
    p()
    type('0')
    p()
    close_windows()
    p()
    type('0')
    p()
    type('0')
    type('0')
    mouseMove(getCenter())
    click(getCenter())
    click(getCenter())
    click(getCenter())
    log('reset')

def refill_wheat():
    wheat_img=Pattern("1413912521932.png").similar(0.45)
    if not exists(wheat_img):
        log("there is no wheat lol")
        return
    
    findAll(wheat_img)
    for mm in list(getLastMatches()):
        print "found: ",  mm
        click("1413836688442.png")
        click("1413836702986.png")
        click("1413836716854.png")
        click(mm)
        p()
        close_windows()
        p()
        while exists("1413912251773.png"):
            time.sleep(2)
        log("a wheat has been probably built :D");
    return

#-----------------------------------------------------------------
def refill(search_for, building_level, building):
    if not exists(search_for):
        log("there is no such pattern")
        return
    
    findAll(search_for)
    for mm in list(getLastMatches()):
        print "found: ",  mm
        click("1413836688442.png")
        click(building_level)
        click(building)
        p()
        click(mm)
        p()
        close_windows()
        p()
        while exists("1413912251773.png"):
            time.sleep(2)
        
        log("again");
#---------------------------------------------------------------------


def move_to_wheats(deposit):
    if deposit == 6:
        type('6')
        time.sleep(1)
        move(-250,-175)
        time.sleep(1)
        move(-250,-175)
        time.sleep(1)
    elif deposit == 4:
        type('4')
        time.sleep(1)
        move(150,150)
    elif deposit == 2:
        type('2')
        move(-250,-175)
        time.sleep(1)
        move(-250,-250)
    elif deposit == 7:
        type('7')

def move_to_wells(deposit):
    if deposit == 1:
        type('1')
        p()
        move(0,-100)
        p()
    elif deposit == 8:
        type('8')
        p()
        move(-250,250)
        p()
    elif deposit == 6:
        type('6')




def event_items_click_on(image):
    click(image)
    sleep(0.1)
    click(image)
    sleep(0.1)
    click(image)

def find_event_items():
    event_items_click_on(Pattern("1414517001491.png").similar(0.50))
    event_items_click_on(Pattern("1414517548437.png").similar(0.50))

#find_event_items()

building_advanced="1413836702986.png"
well="1414886312505.png"
well_empty=Pattern("1414886339882.png").similar(0.40)

if 1:
    reset()
    if 0:
        for w in [1,8,6]:
            move_to_wells(w)
            refill(well_empty, building_advanced,well)
    p()
    for w in [4,6,2,7]:
        move_to_wheats(w)
        refill_wheat()