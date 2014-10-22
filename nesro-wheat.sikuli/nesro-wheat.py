from sikuli import *
import datetime

def log(message):
    print "[" + str(datetime.datetime.now()) + "] " + message

def move(xstep, ystep):
    log("move called with xstep=%s and ystep=%s" % (xstep, ystep))
    dragDrop(getCenter().offset(xstep,ystep),getCenter())

def reset():
    App.focus('chrome')
    click("1413909539900.png")
    time.sleep(1)
    type('0')
    type('0')
    type('0')
    mouseMove(getCenter())
    click(getCenter())
    click(getCenter())
    click(getCenter())
    log('reset')

def refill_wheat():
    wheat_img=Pattern("1413912521932.png").similar(0.40)
    findAll(wheat_img)
    for mm in list(getLastMatches()):
        print "found: ",  mm
        click("1413836688442.png")
        click("1413836702986.png")
        click("1413836716854.png")
        click(mm)
        time.sleep(2)
        while exists("1413912251773.png"):
            time.sleep(2)
        log("a wheat has been probably built :D");

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

reset()
for w in [4,6,2,7]:
    move_to_wheats(w)
    refill_wheat()