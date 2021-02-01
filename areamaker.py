import string, random, pickle, sys

#TODO
#Implement gametest system where ObjectRPG.py can be called to run on the current areaset to quickly test it.
#This will bypass the main function by running a special function within ObjectRPG yet to be implemented.
#This funciton will create a base character and load the current areaset for testing.

areas = {}
enemies = ["Goblin", "Zombie", "Fast Zombie", "Imp", "Magic Goblin"]
items = ["potion", "key", "shiny ruby"]
events = []
global currentposition
currentposition = 1
global width
global height

class Area:
    def __init__(self, name):
        self.name = name
        self.idno = 0
        self.north = ["", 0]
        self.south = ["", 0]
        self.east = ["", 0]
        self.west = ["", 0]
        self.up = ["", 0]
        self.down = ["", 0]
        self.items = []
        self.sign = ""
        self.initswitch = True
        self.initmessage = ""
        self.message = ""
        self.enemy = False
        self.switches = {}
        self.variables = {}
        self.events = []

class Event:
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.commands = []
        self.description = ""
        self.preconditions = []
        self.states = []
        self.nextstatecond = []
        self.event = {}

class Precondition:
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.detail = ""
        self.value = 0

def createnewareaset():
    global areas
    areas = {}
    print("Please enter the name of the areaset.")
    areasetname = input(">")
    print("Please specify the dimensons of the area.")
    while True:
        width = input("Width? \n>")
        try:
            width = int(width)
            break
        except:
            print("Please enter an integer.")
    while True:
        height = input("Height? \n>")
        try:
            height = int(height)
            break
        except:
            print("Please enter an integer.")
    NewArea = Area(areasetname)
    NewArea.idno = 0
    print("Please enter an intro message if desired. Press Enter to skip.")
    message = input(">")
    NewArea.initmessage = message
    areas[0] = NewArea
    runareaset(areas, width, height, currentposition)



def printarea(position):
    currentposition = position
    #currentposition = int(currentposition)
    print(currentposition)
    print(areas[currentposition].idno)
    area = areas[currentposition]
    print("Name: {0}".format(area.name))
    print("ID: {0}".format(area.idno))
    if area.north[1] != 0:
        print("North: {0}: {1}".format(area.north[0], area.north[1]))
    if area.south[1] != 0:
        print("South: {0}: {1}".format(area.south[0], area.south[1]))
    if area.east[1] != 0:
        print("East: {0}: {1}".format(area.east[0], area.east[1]))
    if area.west[1] != 0:
        print("West: {0}: {1}".format(area.west[0], area.west[1]))
    if area.up[1] != 0:
        print("Up: {0}: {1}".format(area.up[0], area.up[1]))
    if area.down[1] != 0:
        print("Down: {0}: {1}".format(area.down[0], area.down[1]))
    print("Items: {0}".format(area.items))
    print("Sign: {0}".format(area.sign))
    print("Init message: {0}".format(area.initmessage))
    print("Message: {0}".format(area.message))
    print("Enemy: {0}".format(area.enemy))
    print("Switches: {0}".format(area.switches))
    print("Variables: {0}".format(area.variables))
    if area.events:
        eventnames = []
        for event in area.events:
            eventnames.append(event.name)        
        #    print("Events: {0}".format(event.name))
        print("Events: " + "".join("{}".format(eventnames)))


                       
def createarea():
    areaname = input("Area name?\n>")
    NewArea = Area(areaname)
    while True:
        areaid = input("Area ID?\n>")
        try:
            areaid = int(areaid)
            break
        except:
            print("Please enter an integer value")
    NewArea.idno = areaid
    print("Does this area connect to any other areas?")
    option = input("y or n?\n>")
    if option == "y":
        print("North?")
        option = input("y or n>\n>")
        if option == "y":
            while True:
                print("Please enter the ID of the area to the north.\n (negative numbers indicate a locked door)")
                option = input(">")
                #make sure this is an integer or lock
                try:
                    option = int(option)
                    print("ID: %i" % option)
                    break
                except:
                    print("Please enter an integer.\n")
            NewArea.north[0] = areaname
            NewArea.north[1] = option
            print("ID entered: %i" % NewArea.north)
        print("South?")
        option = input("y or n>\n>")
        if option == "y":
            while True:
                print("Please enter the ID of the area to the south.\n (negative numbers indicate a locked door)")
                option = input(">")
                #make sure this is an integer or lock
                try:
                    option = int(option)
                    print("ID: %i" % option)
                    break
                except:
                    print("Please enter an integer.\n")
            NewArea.south[0] = areaname
            NewArea.south[1] = option
            print("ID entered: %i" % NewArea.south)
        print("East?")
        option = input("y or n>\n>")
        if option == "y":
            while True:
                print("Please enter the ID of the area to the east.\n (negative numbers indicate a locked door)")
                option = input(">")
                #make sure this is an integer or lock
                try:
                    option = int(option)
                    print("ID: %i" % option)
                    break
                except:
                    print("Please enter an integer.\n")
            NewArea.east[0] = areaname
            NewArea.east[1] = option
            print("ID entered: %i" % NewArea.east)
        print("West?")
        option = input("y or n>\n>")
        if option == "y":
            while True:
                print("Please enter the ID of the area to the west.\n (negative numbers indicate a locked door)")
                option = input(">")
                #make sure this is an integer or lock
                try:
                    option = int(option)
                    print("ID: %i" % option)
                    break
                except:
                    print("Please enter an integer.\n")
            NewArea.west[0] = areaname
            NewArea.west[1] = option
            print("ID entered: %i" % NewArea.west)
    message = input("Initial message?\n>")
    NewArea.initmessage = message
    NewArea.initswitch = True
    message = input("Permament area message?\n>")
    NewArea.message = message
    enemyflag = input("Does this area contain enemies (y or n)?\n>")
    if enemyflag == "y":
        NewArea.enemy = True
    if not areas:
        areas[areaid] = NewArea
        #for i in range(1, len(areas)+1):
        #    print("Index: %i" % i)
        #    print(areas[i])
    else:
        #index = len(areas) + 1
        areas[areaid] = NewArea
        #for i in range(1, len(areas)+1):
        #    print("Index: %i" % i)
        #    print(areas[i].name)
    #areas.append(NewArea)
    #print("Which enemies?")
    #enemyIG = input(">")
    #if enemyIG in enemies:
    #    NewArea.enemy = 
    for area in areas:
        print(areas[area].name)
        print(areas[area].idno)
        print(areas[area].initmessage)
        print("Enemies: {0}".format(areas[area].enemy))

def showmap(areawidth, areaheight, position):
    width = int(areawidth)
    height = int(areaheight)
    currentposition = int(position)
    print("width: %i Height: %i " % (width, height))
    print("Map:",end="")
    #get column
    column = currentposition % width
    #get row
    row = int(currentposition / width)
    #print Coordinates
    #catch when in last column
    if column == 0:
        row -= 1
        print(" " + "%i, " % width + str(row + 1))
    else:
        print(" " + str(column) + ", " + str(row + 1))
    #setup temporary count
    count = row
    #print rows before current location
    while count > 0:
        print("[" + "".join("{}".format("-") for k in range(width)) + "]")
        count -= 1
    #print location
    if column == 0:
        print("[" + "".join("{}".format("-") for k in range(width-1)) + "%i" % currentposition + "]")
    else:
        before = column % width - 1
        after = width - before - 1
        print("[" + "".join("{}".format("-") for i in range(before)) + "%i" % currentposition + "".join("{}".format("-") for k in range(after)) + "]")
    #print rows after current location
    count = height - 1 - row
    while count > 0:
        print("[" + "".join("{}".format("-") for k in range(width)) + "]")
        count -= 1    

def edititems(currentarea, currentposition, areawidth, areaheight):
    area = currentarea
    position = currentposition
    width = areawidth
    height = areaheight
    while True:
        if not areas[position].items:
            print("There are no items here yet.")
        else:
            print("Current items in this area:")
            for item in areas[position].items:
                print(item)
        print("What do you want to do?")
        print("1.) Add new item")
        print("2.) Remove item")
        print("b.) Back")
        choice = input(">")
        if choice == "1":
            print("Current items in this area:")
            for item in areas[position].items:
                print(item)
            print("Please enter name of new item to add.")
            option = input(">")
            if option in items:
                areas[position].items.append(option)
                print("{} added.".format(option))
            else:
                print("{} is not a valid item.".format(option))
        if choice == "2":
            for item in areas[position].items:
                print(item)
            print("Remove which item?")
            choice = input(">")
            if choice in areas[position].items:
                areas[position].items.remove(choice)
                print("{} removed.".format(choice))
            else:
                print("{} is not a valid item in this area.".format(choice))
                edititems(area, position, width, height)
        if choice == "b" or "back":
            break
        else:
            print("Please enter a valid selection.")
            
        

def editcurrentarea(currentarea, currentposition, areawidth, areaheight):
    area = currentarea
    position = currentposition
    width = areawidth
    height = areaheight
    while True:
        if not areas:
            print("No areas to print yet!\n")
        else:
            print("Current Position: {0}".format(areas[position].idno))
            printarea(areas[position].idno)
        print("Current Position: {0}".format(position))
        showmap(width, height, position)
        print("What do you want to do?")
        print("1.) Change Area Name")
        print("2.) Change North destination")
        print("3.) Change South destination")
        print("4.) Change East destination")
        print("5.) Change West destination")
        print("6.) Change Up destination")
        print("7.) Change Down destination")
        print("8.) Edit Area Items")
        print("9.) Edit Area Sign")
        print("10.) Edit Initial Message")
        print("11.) Edit Message")
        print("12.) Edit Enemy Flag")
        print("13.) Edit Events")
        print("b.) Back")
        choice = input(">")
        if choice == "1":
            print("Current Name: {}".format(area.name))
            name = input("Please enter a new name for this area.\n>")
            areas[position].name = name
        elif choice == "2":
            if area.north[1] == 0:
                print("There is no destination set for North. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Is new destination in current area or new area?")
                        print("1.) Current Area")
                        print("2.) New Area")
                        choice = input(">")
                        if choice == "1":
                            while True:
                                print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                                choice = input(">")
                                if choice == "0":
                                    areas[position].north[0] = areas[0].name
                                    areas[position].north[1] = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].north[0] = areas[0].name
                                        areas[position].north[1] = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].north[0] = choice
                            while True:
                                print("Current position: {}".format(areas[position].idno))
                                print("Please enter destination position.")
                                option = input(">")
                                try:
                                    option = int(option)
                                    areas[position].north[1] = option
                                    break
                                except:
                                    print("Please enter a valid integer.")
                            break
                        else:
                            print("Please enter a valid selection.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current North Destination: {}".format(area.north))
                    print("Is new destination in current area or new area?")
                    print("1.) Current Area")
                    print("2.) New Area")
                    choice = input(">")
                    if choice == "1":
                        while True:
                            print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                            choice = input(">")
                            if choice == "0":
                                areas[position].north[0] = areas[0].name
                                areas[position].north[1] = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].north[0] = areas[0].name
                                    areas[position].north[1] = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].north[0] = choice
                        while True:
                            print("Current position: {}".format(areas[position].idno))
                            print("Please enter destination position.")
                            option = input(">")
                            try:
                                option = int(option)
                                areas[position].north[1] = option
                                break
                            except:
                                print("Please enter a valid integer.")
                        break
                    else:
                        print("Please enter a valid selection.")
        elif choice == "3":
            if area.south[1] == 0:
                print("There is no destination set for South. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Is new destination in current area or new area?")
                        print("1.) Current Area")
                        print("2.) New Area")
                        choice = input(">")
                        if choice == "1":
                            while True:
                                print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                                choice = input(">")
                                if choice == "0":
                                    areas[position].south[0] = areas[0].name
                                    areas[position].south[1] = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].south[0] = areas[0].name
                                        areas[position].south[1] = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].south[0] = choice
                            while True:
                                print("Current position: {}".format(areas[position].idno))
                                print("Please enter destination position.")
                                option = input(">")
                                try:
                                    option = int(option)
                                    areas[position].south[1] = option
                                    break
                                except:
                                    print("Please enter a valid integer.")
                            break
                        else:
                            print("Please enter a valid selection.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current South Destination: {}".format(area.south))
                    print("Is new destination in current area or new area?")
                    print("1.) Current Area")
                    print("2.) New Area")
                    choice = input(">")
                    if choice == "1":
                        while True:
                            print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                            choice = input(">")
                            if choice == "0":
                                areas[position].south[0] = areas[0].name
                                areas[position].south[1] = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].south[0] = areas[0].name
                                    areas[position].south[1] = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].south[0] = choice
                        while True:
                            print("Current position: {}".format(areas[position].idno))
                            print("Please enter destination position.")
                            option = input(">")
                            try:
                                option = int(option)
                                areas[position].south[1] = option
                                break
                            except:
                                print("Please enter a valid integer.")
                        break
                    else:
                        print("Please enter a valid selection.")
        elif choice == "4":
            if area.east[1] == 0:
                print("There is no destination set for East. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Is new destination in current area or new area?")
                        print("1.) Current Area")
                        print("2.) New Area")
                        choice = input(">")
                        if choice == "1":
                            while True:
                                print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                                choice = input(">")
                                if choice == "0":
                                    areas[position].east[0] = areas[0].name
                                    areas[position].east[1] = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].east[0] = areas[0].name
                                        areas[position].east[1] = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].east[0] = choice
                            while True:
                                print("Current position: {}".format(areas[position].idno))
                                print("Please enter destination position.")
                                option = input(">")
                                try:
                                    option = int(option)
                                    areas[position].east[1] = option
                                    break
                                except:
                                    print("Please enter a valid integer.")
                            break
                        else:
                            print("Please enter a valid selection.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current East Destination: {}".format(area.east))
                    print("Is new destination in current area or new area?")
                    print("1.) Current Area")
                    print("2.) New Area")
                    choice = input(">")
                    if choice == "1":
                        while True:
                            print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                            choice = input(">")
                            if choice == "0":
                                areas[position].east[0] = areas[0].name
                                areas[position].east[1] = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].east[0] = areas[0].name
                                    areas[position].east[1] = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].east[0] = choice
                        while True:
                            print("Current position: {}".format(areas[position].idno))
                            print("Please enter destination position.")
                            option = input(">")
                            try:
                                option = int(option)
                                areas[position].east[1] = option
                                break
                            except:
                                print("Please enter a valid integer.")
                        break
                    else:
                        print("Please enter a valid selection.")
        elif choice == "5":
            if area.west[1] == 0:
                print("There is no destination set for West. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Is new destination in current area or new area?")
                        print("1.) Current Area")
                        print("2.) New Area")
                        choice = input(">")
                        if choice == "1":
                            while True:
                                print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                                choice = input(">")
                                if choice == "0":
                                    areas[position].west[0] = areas[0].name
                                    areas[position].west[1] = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].west[0] = areas[0].name
                                        areas[position].west[1] = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].west[0] = choice
                            while True:
                                print("Current position: {}".format(areas[position].idno))
                                print("Please enter destination position.")
                                option = input(">")
                                try:
                                    option = int(option)
                                    areas[position].west[1] = option
                                    break
                                except:
                                    print("Please enter a valid integer.")
                            break
                        else:
                            print("Please enter a valid selection.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current West Destination: {}".format(area.west))
                    print("Is new destination in current area or new area?")
                    print("1.) Current Area")
                    print("2.) New Area")
                    choice = input(">")
                    if choice == "1":
                        while True:
                            print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                            choice = input(">")
                            if choice == "0":
                                areas[position].west[0] = areas[0].name
                                areas[position].west[1] = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].west[0] = areas[0].name
                                    areas[position].west[1] = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].west[0] = choice
                        while True:
                            print("Current position: {}".format(areas[position].idno))
                            print("Please enter destination position.")
                            option = input(">")
                            try:
                                option = int(option)
                                areas[position].west[1] = option
                                break
                            except:
                                print("Please enter a valid integer.")
                        break
                    else:
                        print("Please enter a valid selection.")
        elif choice == "6":
            if area.up[1] == 0:
                print("There is no destination set for Up. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Is new destination in current area or new area?")
                        print("1.) Current Area")
                        print("2.) New Area")
                        choice = input(">")
                        if choice == "1":
                            while True:
                                print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                                choice = input(">")
                                if choice == "0":
                                    areas[position].up[0] = areas[0].name
                                    areas[position].up[1] = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].up[0] = areas[0].name
                                        areas[position].up[1] = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].up[0] = choice
                            while True:
                                print("Current position: {}".format(areas[position].idno))
                                print("Please enter destination position.")
                                option = input(">")
                                try:
                                    option = int(option)
                                    areas[position].up[1] = option
                                    break
                                except:
                                    print("Please enter a valid integer.")
                            break
                        else:
                            print("Please enter a valid selection.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current Up Destination: {}".format(area.up))
                    print("Is new destination in current area or new area?")
                    print("1.) Current Area")
                    print("2.) New Area")
                    choice = input(">")
                    if choice == "1":
                        while True:
                            print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                            choice = input(">")
                            if choice == "0":
                                areas[position].up[0] = areas[0].name
                                areas[position].up[1] = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].up[0] = areas[0].name
                                    areas[position].up[1] = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].up[0] = choice
                        while True:
                            print("Current position: {}".format(areas[position].idno))
                            print("Please enter destination position.")
                            option = input(">")
                            try:
                                option = int(option)
                                areas[position].up[1] = option
                                break
                            except:
                                print("Please enter a valid integer.")
                        break
                    else:
                        print("Please enter a valid selection.")
        elif choice == "7":
            if area.down[1] == 0:
                print("There is no destination set for Down. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Is new destination in current area or new area?")
                        print("1.) Current Area")
                        print("2.) New Area")
                        choice = input(">")
                        if choice == "1":
                            while True:
                                print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                                choice = input(">")
                                if choice == "0":
                                    areas[position].down[0] = areas[0].name
                                    areas[position].down[1] = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].down[0] = areas[0].name
                                        areas[position].down[1] = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].down[0] = choice
                            while True:
                                print("Current position: {}".format(areas[position].idno))
                                print("Please enter destination position.")
                                option = input(">")
                                try:
                                    option = int(option)
                                    areas[position].down[1] = option
                                    break
                                except:
                                    print("Please enter a valid integer.")
                            break
                        else:
                            print("Please enter a valid selection.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current Down Destination: {}".format(area.down))
                    print("Is new destination in current area or new area?")
                    print("1.) Current Area")
                    print("2.) New Area")
                    choice = input(">")
                    if choice == "1":
                        while True:
                            print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                            choice = input(">")
                            if choice == "0":
                                areas[position].down[0] = areas[0].name
                                areas[position].down[1] = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].down[0] = areas[0].name
                                    areas[position].down[1] = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].down[0] = choice
                        while True:
                            print("Current position: {}".format(areas[position].idno))
                            print("Please enter destination position.")
                            option = input(">")
                            try:
                                option = int(option)
                                areas[position].down[1] = option
                                break
                            except:
                                print("Please enter a valid integer.")
                        break
                    else:
                        print("Please enter a valid selection.")
        elif choice == "8":
            edititems(area, position, width, height)
        elif choice == "9":
            print("Current Sign: {}".format(area.sign))
            sign = input("Please enter new text for the sign in this area.\n>")
            areas[position].sign = sign
        elif choice == "10":
            print("Current Inital Message: {}".format(area.initmessage))
            initmessage = input("Please enter a new initial message for this area.\n>")
            areas[position].initmessage = initmessage
            areas[position].initswitch = True
        elif choice == "11":
            print("Current Message: {}".format(area.message))
            message = input("Please enter new text for the message in this area.\n>")
            areas[position].message = message
        elif choice == "12":
            print("Current Enemy Flag: {}".format(area.enemy))
            flag = input("Will this area have enemies? (y or n?)")
            if flag == "y":
                areas[position].enemy = True
            elif flag == "n":
                areas[position].enemy = False
            else:
                print("Please enter 'y' or 'n'.")
        elif choice == "13":
            editevents(area, position, width, height)
        elif choice == "b" or choice == "back":
            #runareaset(areas, int(width), int(height), int(position))
            break
        else:
            print("Please enter a valid selection.")

def addaction(playeraction, currentarea):
    action = playeraction
    area = currentarea
    while True:
        print("Please choose what will happen when the {} command is used on this event.".format(action))
        print("1.) Respond with text only")
        print("2.) Item exchange")
        print("3.) Change party gold")
        print("4.) Set Switch")
        print("5.) Set Variable")
        print("6.) Set Choice")
        choice = input(">")
        if choice == "1":
            print("Please enter text response.")
            text = input(">")
            return ["text", text]
        elif choice == "2":
            while True:
                print("Give item or get item?")
                print("1.) Give item")
                print("2.) Get item")
                choice = input(">")
                if choice == "1":
                    itemexchange = "itemgive"
                    print("Please enter the item to give from the player to the event.")
                    itemname = input(">")
                    print("Item: {}".format(itemname))
                    print("Please enter a message how to refer to this event with the command.")
                    print("Example: If command is called 'give' this text might be 'give to who?")
                    message = input(">")
                    break
                elif choice == "2":
                    itemexchange = "itemget"
                    print("Please enter the item to get from the event.")
                    itemname = input(">")
                    print("Item: {}".format(itemname))
                    message = ""
                    break
                else:
                    print("Please enter a valid selection.")
            return itemexchange, itemname, message
        elif choice == "3":
            while True:
                print("Please enter the amnount of gold to add. \nUse a negative number to subtract gold.")
                changegold = input(">")
                try:
                    changegold = int(changegold)
                    break
                except:
                    print("Please enter an integer value.")
            return "goldexchange", changegold
        elif choice == "4":
            while True:
                print("Set global switch or local event switch?")
                print("1.) Global switch")
                print("2.) Local event switch")
                option = input(">")
                if option == "1":
                    print("Which switch?")
                    if areas[0].switches:
                        count = 1
                        print("{}.) Create new switch".format(count))
                        for switch in areas[0].switches:
                            count += 1
                            print("{}.) {}".format(count, switch))
                        select = input(">")
                        if select == "1":
                            print("Please enter a name for the new switch.")
                            name = input(">")
                            print("Please set the switch to True or False.")
                            print("1.) True")
                            print("2.) False")
                            value = input(">")
                            if value == "1":
                                pass
                            elif value == "2":
                                pass
                            
                            
                elif option == "2":
                    break
                else:
                    print("Please enter a valid selection.")
        elif choice == "5":
            while True:
                print("Set global variable or local event variable?")
                print("1.) Global variable")
                print("2.) Local event variable")
                option = input(">")
                if option == "1":
                    pass
                elif option == "2":
                    pass
                else:
                    print("Please enter a valid selection.")
        elif choice == "6":
            pass
        else:
            print("Please enter a valid selection.")
        
        

def editevents(currentarea, currentposition, areawidth, areaheight):
    area = currentarea
    position = currentposition
    width = areawidth
    height = areaheight
    while True:
        if not areas[position].events:
            print("There are no events here yet.")
        else:
            print("Current events in this area:")
            for event in areas[position].events:
                print(event.name)
        print("What do you want to do?")
        print("1.) Add new event")
        print("2.) Edit event")
        print("3.) Remove event")
        print("b.) Back")
        choice = input(">")
        if choice == "1":
            print("Current events in this area:")
            for event in areas[position].events:
                print(event.name)
            print("Please enter name of new event to add.")
            eventname = input(">")
            newevent = Event(eventname)
            print("What type of event is this?")
            print("NPC, lever, button, object, etc.")
            eventtype = input(">")
            newevent.type = eventtype
            while True:
                print("What command can be used to interact with this event?")
                command = input(">")
                if command == "go" or command == "east" or command == "west" or command == "north" or command == "south" or command == "up" or command == "south":
                    print("{} is a restricted command. Please enter a new command.".format(command))
                else:
                    newevent.commands.append(command)
                    i = len(newevent.commands)
                    #add actions
                    newevent.event[command] = []
                    while True:
                        action = addaction(command, area)
                        newevent.event[command].append(action)
                        print("Added {}".format(action))
                        try:
                            while True:
                                print("Add additional action? (y or n)")
                                option = input(">")
                                if option == "y" or option == "n":
                                    break
                                else:
                                    print("Please enter 'y' or 'n'.")
                            if option == "n":
                                raise
                        except:
                            break
                    try:
                        while True:
                            print("Add additional command? (y or n)")
                            option = input(">")
                            if option == "y" or option == "n":
                                break
                            else:
                                print("Please enter 'y' or 'n'.")
                        if option == "n":
                            raise
                    except:
                        break
            print("Please enter a description of this event that will appear when you enter the area.")
            description = input(">")
            newevent.description = description
            while True:
                while True:
                    print("Please enter preconditions for this event to appear.")
                    print("1.) None")
                    print("2.) Item held")
                    print("3.) Switch condition")
                    print("4.) Variable condition")
                    preconditions = input(">")
                    if preconditions == "1":
                        option = "n"
                        newevent.preconditions = "none"
                        break
                    elif preconditions == "2":
                        while True:
                            print("Which item should be held?")
                            for item in items:
                                print(item)
                            itemheld = input(">")
                            if itemheld in items:
                                newprecondition = Precondition(itemheld)
                                newprecondition.type = "item"
                                newprecondition.detail = itemheld
                                break
                            else:
                                print("Please enter a valid item.")
                        newevent.preconditions.append(newprecondition)
                        break
                    elif preconditions == "3":
                        pass
                    elif preconditions == "4":
                        pass
                    else:
                        print("Please enter a valid selection.")
                try:
                    while option != "n":
                        print("Add additional preconditions? (y or n)")
                        option = input(">")
                        if option == "y" or option == "n":
                            break
                        else:
                            print("Please enter 'y' or 'n'.")
                    if option == "n":
                        raise
                except:
                    break
            #add the event to the area
            areas[position].events.append(newevent)
            print("{} added.".format(newevent.name))
        elif choice == "2":
            print("Current events in this area:")
            for event in areas[position].events:
                print(event.name)
            print("Please enter name of new event to edit.")
            eventname = input(">")
            if eventname == event.name:
                pass
            else:
                print("{} is not a valid event in this area.".format(eventname))
        elif choice == "3":
            print("Current events in this area:")
            eventlist = []
            for event in areas[position].events:
                print(event.name)
                eventlist.append(event.name)
            print("Please enter name of new event to remove.")
            eventname = input(">")
            if eventname in eventlist:
                print("Removed {}".format(eventname))
                for event in areas[position].events:
                    if event.name == eventname:
                        areas[position].events.remove(event)
                        break
            else:
                print("{} is not a valid event in this area.".format(eventname))
        elif choice == "b" or "back":
            break
        else:
            print("Please enter a valid selection.")

def quickcreate(currentposition):
    position = currentposition
    NewArea = Area("New Area")
    NewArea.idno = position
    areas[position] = NewArea

def getnewposition():
    while True:
        position = input("Enter new position.\n>")
        try:
            position = int(position)
            try:
                if position > 0 and position <= width * height:
                    break
            except ValueError("Please enter a valid position (1-{})".format(width*height)):
                print("Please enter a valid position (1-{})".format(width*height))
            finally:
                break
        except Exception as ex:
            #print("Please enter an integer.")
            print("Please enter a valid position (1-{})\n".format(width*height))
        else:
            if position > 0 and position <= width * height:
                    break
            else:
                print("Please enter a valid position (1-{})".format(width*height))
                raise ValueError("Please enter a valid position (1-{})".format(width*height))
    return position
    

def runareaset(areaset, areawidth, areaheight, currentposition):
    width = areawidth
    height = areaheight
    position = currentposition
    areas = areaset
    while True:
        print("Current Position: {0}".format(position))
        showmap(width, height, position)
        print("What do you want to do?")
        print("1.) Create new area")
        print("2.) Print current area")
        print("3.) Edit current area")
        print("4.) Print all areas")
        print("5.) Set current position")
        print("6.) Save areas into area set")
        print("7.) Load existing area set")
        print("8.) Edit Intro Message")
        print("b.) back")
        print("Direction: north, south, east, west, up, down")
        choice = input(">")
        if choice == "1":
            createarea()
        elif choice == "2":
            if not areas:
                print("No areas to print yet!\n")
            else:
                print("Current Position: {0}".format(areas[position].idno))
                printarea(areas[position].idno)
        elif choice == "3":
            if not areas:
                print("Area does not exist!")
                print("Creating new area!")
                quickcreate(position)
                editcurrentarea(areas[position], position, width, height)
            else:
                try:
                    editcurrentarea(areas[position], position, width, height)
                except:
                    print("This area does not exist!")
                    print("Creating this new area!")
                    quickcreate(position)
                    editcurrentarea(areas[position], position, width, height)
        elif choice == "4":
            if not areas:
                print("No areas to print yet!\n")
            else:
                #count = 1
                for count in areas:
                    #currentposition = area.idno
                    currentposition = int(currentposition)
                    print("Current Position: {0}".format(areas[count].idno))
                    printarea(areas[count].idno)
                    #count += 1
                #count = 1
        elif choice == "5":
            while True:
                position = input("Enter new position.\n>")
                try:
                    position = int(position)
                    try:
                        if position > 0 and position <= width * height:
                            break
                    except ValueError("Please enter a valid position (1-{})".format(width*height)):
                        print("Please enter a valid position (1-{})".format(width*height))
                    finally:
                        break
                except Exception as ex:
                    #print("Please enter an integer.")
                    print("Please enter a valid position (1-{})\n".format(width*height))
                else:
                    if position > 0 and position <= width * height:
                            break
                    else:
                        print("Please enter a valid position (1-{})".format(width*height))
                        raise ValueError("Please enter a valid position (1-{})".format(width*height))
            currentposition = position
            print("cur pos: %i" % currentposition)
            #showmap(width, height, currentposition)
        elif choice == "6":
            print("Please suply a filename for this areaset.")
            filename = input(">")
            areas[0].name = filename
            saveareaset(filename, areas, width, height, position)            
        elif choice == "7":
            areas = {}
            print("Please enter the filename of the areaset you would like to load.")
            filename = input(">")
            areas, width, height, currentposition = loadareaset(filename)
            runareaset(areas, width, height, currentposition)
        elif choice == "8":
            print("Current intro message:")
            print(areas[0].message)
            print("Please enter a new intro message.")
            message = input(">")
            areas[0].message = message
        elif choice == "b" or choice == "back":
            break
        elif choice == "north":
            if not areas:
                print("No areas to move to yet!\n")
            else:
                if currentposition in areas:
                    if areas[currentposition].north[1] != 0:
                        try:
                            area = areas[currentposition]
                            print("North: {}".format(area.north[1]))
                            if area.north[1] < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].north[1]
                            else:
                                currentposition = areas[currentposition].north[1]
                            position = currentposition
                        except:
                            print("That area doesn't exist yet!")
                    else:
                        print("Connection to that area doesn't exist yet!")
                else:
                    print("This area does not exist yet!")
        elif choice == "south":
            if not areas:
                print("No areas to move to yet!\n")
            else:
                if currentposition in areas:
                    if areas[currentposition].south[1] != 0:
                        try:
                            area = areas[currentposition]
                            print("South: {}".format(area.south[1]))
                            if area.south[1] < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].south[1]
                            else:
                                currentposition = areas[currentposition].south[1]
                            position = currentposition
                        except:
                            print("That area doesn't exist yet!")
                    else:
                        print("Connection to that area doesn't exist yet!")
                else:
                    print("This area does not exist yet!")
        elif choice == "east":
            if not areas:
                print("No areas to move to yet!\n")
            else:
                if currentposition in areas:
                    if areas[currentposition].east[1] != 0:
                        try:
                            area = areas[currentposition]
                            print("East: {}".format(area.east[1]))
                            if area.east[1] < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].east[1]
                            else:
                                currentposition = areas[currentposition].east[1]
                            position = currentposition
                        except:
                            print("That area doesn't exist yet!")
                    else:
                        print("Connection to that area doesn't exist yet!")
                else:
                    print("This area does not exist yet!")
        elif choice == "west":
            if not areas:
                print("No areas to move to yet!\n")
            else:
                if currentposition in areas:
                    if areas[currentposition].west[1] != 0:
                        try:
                            area = areas[currentposition]
                            print("West: {}".format(area.west[1]))
                            if area.west[1] < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].west[1]
                            else:
                                currentposition = areas[currentposition].west[1]
                            position = currentposition
                        except:
                            print("That area doesn't exist yet!")
                    else:
                        print("Connection to that area doesn't exist yet!")
                else:
                    print("This area does not exist yet!")
        elif choice == "up":
            if not areas:
                print("No areas to move to yet!\n")
            else:
                if currentposition in areas:
                    if areas[currentposition].up[1] != 0:
                        try:
                            area = areas[currentposition]
                            print("Up: {}".format(area.up[1]))
                            currentposition = areas[currentposition].up[1]
                            position = currentposition
                        except:
                            print("That area doesn't exist yet!")
                    else:
                        print("Connection to that area doesn't exist yet!")
                else:
                    print("This area does not exist yet!")
        elif choice == "down":
            if not areas:
                print("No areas to move to yet!\n")
            else:
                if currentposition in areas:
                    if areas[currentposition].down[1] != 0:
                        try:
                            area = areas[currentposition]
                            print("Down: {}".format(area.down[1]))
                            currentposition = areas[currentposition].down[1]
                            position = currentposition
                        except:
                            print("That area doesn't exist yet!")
                    else:
                        print("Connection to that area doesn't exist yet!")
                else:
                    print("This area does not exist yet!")
        else:
            print("Please enter a valid selection.")

def loadareaset(filename):
    #create filename string
    newareas = str(filename) + ".pkl"
    print("Areas: ")
    print(newareas)
    try:
        fi = open(newareas, "rb")
    except IOError:
        print("Can't load", newareas)
        return {}, 1, 1, 1
    else:
        tempareas = pickle.load(fi)
        width = pickle.load(fi)
        height = pickle.load(fi)
        position = pickle.load(fi)
        print("New areas loaded successfully!")
        return  tempareas, width, height, position

def saveareaset(filename, areaset, areawidth, areaheight, currentposition):
    print(filename)
    print(areaset)
    #create filename string
    newareas = str(filename) + ".pkl"
    fi = open(newareas, "bw")
    pickle.dump(areaset,fi)
    pickle.dump(areawidth, fi)
    pickle.dump(areaheight, fi)
    pickle.dump(currentposition, fi)
    fi.close()
    print("Areas saved!")

#main loop
while True:
    print("Welcome to Area Maker!")
    print("What would you like to do?")
    print("1.) Create new area set")
    print("2.) Load area set")
    print("3.) Quit")
    choice = input(">")
    if choice == "1":
        createnewareaset()
    elif choice == "2":
        areas = {}
        print("Please enter the filename of the areaset you would like to load.")
        filename = input(">")
        areas, width, height, currentposition = loadareaset(filename)
        runareaset(areas, width, height, currentposition)
    elif choice == "3":
        sys.exit()
    else:
        print("Please enter a valid selection.")
