import string, random, pickle, sys

#TODO
#Update movement system so that each direction sets a tuple.
#Position 1 is the areaset name and position 2 is the position ID.
#Implement gametest system where ObjectRPG.py can be called to run on the current areaset to quickly test it.
#This will bypass the main function by running a special function within ObjectRPG yet to be implemented.
#This funciton will create a base character and load the current areaset for testing.

areas = {}
enemies = ["Goblin", "Zombie", "Fast Zombie", "Imp", "Magic Goblin"]
items = ["potion", "key"]
global currentposition
currentposition = 1
global width
global height

class Area:
    def __init__(self, name):
        self.name = name
        self.idno = 0
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0
        self.up = 0
        self.down = 0
        self.items = []
        self.sign = ""
        self.initswitch = True
        self.initmessage = ""
        self.message = ""
        self.enemy = False
        self.switches = [False]
        self.variables = [0]

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
    if area.north != 0:
        print("North: {0}".format(area.north))
    if area.south != 0:
        print("South: {0}".format(area.south))
    if area.east != 0:
        print("East: {0}".format(area.east))
    if area.west != 0:
        print("West: {0}".format(area.west))
    if area.up != 0:
        print("Up: {0}".format(area.up))
    if area.down != 0:
        print("Down: {0}".format(area.down))
    print("Items: {0}".format(area.items))
    print("Sign: {0}".format(area.sign))
    print("Init message: {0}".format(area.initmessage))
    print("Message: {0}".format(area.message))
    print("Enemy: {0}".format(area.enemy))


                       
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
            NewArea.north = option
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
            NewArea.south = option
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
            NewArea.east = option
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
            NewArea.west = option
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
        print("b.) Back")
        choice = input(">")
        if choice == "1":
            print("Current Name: {}".format(area.name))
            name = input("Please enter a new name for this area.\n>")
            areas[position].name = name
        elif choice == "2":
            if area.north == 0:
                print("There is no destination set for North. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                        choice = input(">")
                        if choice == "0":
                            areas[position].north = 0
                            break
                        else:
                            try:
                                choice = int(choice)
                                areas[position].north = choice
                                break
                            except:
                                print("Please enter a valid integer.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current North Destination: {}".format(area.north))
                    print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                    choice = input(">")
                    if choice == "0":
                        areas[position].north = 0
                        break
                    else:
                        try:
                            choice = int(choice)
                            areas[position].north = choice
                            break
                        except:
                            print("Please enter a valid integer.")
        elif choice == "3":
            if area.south == 0:
                print("There is no destination set for South. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                        choice = input(">")
                        if choice == "0":
                            areas[position].south = 0
                            break
                        else:
                            try:
                                choice = int(choice)
                                areas[position].south = choice
                                break
                            except:
                                print("Please enter a valid integer.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current South Destination: {}".format(area.south))
                    print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                    choice = input(">")
                    if choice == "0":
                        areas[position].south = 0
                        break
                    else:
                        try:
                            choice = int(choice)
                            areas[position].south = choice
                            break
                        except:
                            print("Please enter a valid integer.")
        elif choice == "4":
            if area.east == 0:
                print("There is no destination set for East. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                        choice = input(">")
                        if choice == "0":
                            areas[position].east = 0
                            break
                        else:
                            try:
                                choice = int(choice)
                                areas[position].east = choice
                                break
                            except:
                                print("Please enter a valid integer.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current East Destination: {}".format(area.east))
                    print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                    choice = input(">")
                    if choice == "0":
                        areas[position].east = 0
                        break
                    else:
                        try:
                            choice = int(choice)
                            areas[position].east = choice
                            break
                        except:
                            print("Please enter a valid integer.")
        elif choice == "5":
            if area.west == 0:
                print("There is no destination set for West. Set it? (y or n?)")
                option = input(">")
                if option == "y":
                    while True:
                        print("Please enter a new destination.\n (negative numbers indicate a locked door)")
                        choice = input(">")
                        if choice == "0":
                            areas[position].west = 0
                            break
                        else:
                            try:
                                choice = int(choice)
                                areas[position].west = choice
                                break
                            except:
                                print("Please enter a valid integer.")
                elif option == "n":
                    pass
                else:
                    print("Please enter 'y' or 'n'.")
            else:
                while True:
                    print("Current West Destination: {}".format(area.west))
                    print("Please enter a new destination. Set it to 0 to remove the destination.\n (negative numbers indicate a locked door)")
                    choice = input(">")
                    if choice == "0":
                        areas[position].west = 0
                        break
                    else:
                        try:
                            choice = int(choice)
                            areas[position].west = choice
                            break
                        except:
                            print("Please enter a valid integer.")
        elif choice == "6":
            if area.up == 0:
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
                                    areas[position].up = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].up = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].up = choice
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
                                areas[position].up = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].up = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].up = choice
                        break
                    else:
                        print("Please enter a valid selection.")
        elif choice == "7":
            if area.down == 0:
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
                                    areas[position].down = 0
                                    break
                                else:
                                    try:
                                        choice = int(choice)
                                        areas[position].down = choice
                                        break
                                    except:
                                        print("Please enter a valid integer.")
                            break
                        elif choice == "2":
                            print("Please enter name of areaset to set as destination.")
                            choice = input(">")
                            areas[position].down = choice
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
                                areas[position].down = 0
                                break
                            else:
                                try:
                                    choice = int(choice)
                                    areas[position].down = choice
                                    break
                                except:
                                    print("Please enter a valid integer.")
                        break
                    elif choice == "2":
                        print("Please enter name of areaset to set as destination.")
                        choice = input(">")
                        areas[position].down = choice
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
        elif choice == "b" or choice == "back":
            #runareaset(areas, int(width), int(height), int(position))
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
                    if areas[currentposition].north != 0:
                        try:
                            area = areas[currentposition]
                            print("North: {}".format(area.north))
                            if area.north < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].north
                            else:
                                currentposition = areas[currentposition].north
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
                    if areas[currentposition].south != 0:
                        try:
                            area = areas[currentposition]
                            print("South: {}".format(area.south))
                            if area.south < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].south
                            else:
                                currentposition = areas[currentposition].south
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
                    if areas[currentposition].east != 0:
                        try:
                            area = areas[currentposition]
                            print("East: {}".format(area.east))
                            if area.east < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].east
                            else:
                                currentposition = areas[currentposition].east
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
                    if areas[currentposition].west != 0:
                        try:
                            area = areas[currentposition]
                            print("West: {}".format(area.west + 1))
                            if area.west < 0:
                                print("Moving through locked door.")
                                currentposition = -1 * areas[currentposition].west
                            else:
                                currentposition = areas[currentposition].west
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
                    if areas[currentposition].up != 0:
                        try:
                            area = areas[currentposition]
                            print("Up: {}".format(area.up + 1))
                            currentposition = areas[currentposition].up
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
                    if areas[currentposition].down != 0:
                        try:
                            area = areas[currentposition]
                            print("Down: {}".format(area.down + 1))
                            currentposition = areas[currentposition].down
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
