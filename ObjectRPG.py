import sys
import os
import random
import math
import pickle
from os import path


#TODO
#Implement NPCs in areas that the player can interact with by talking to, buying and selling from, etc.
#Implement object system. NPCs are one object type. Others can be switches, levers, or other things to interact with.
#Objects will have a name, command to interact, array of states, each state will have conditions to move to the next state.
#States will be new instances of the event and the array of states will contain the names of these Events so that they can accessed.
#The content of the states can then be swapped with the original Event to effectively change the state.
#Conditions can be updating a switch or variable or combination of 2 inputs.
#Conditions are met via interacting using commands such as: give, talk, examine, etc.

#Implement spell system allowing multiple spells to choose from.
#Learned spells will be in an inventory on the character.
#Each character will have a list of spells that they will learn at specific levels. This might be defined on the class.

#Implement shop lists so that shops may be loaded with specific items only.

#Implement status effects
#Status effects will be the result of a chance from a weapon or a spell.
#Status effects are stored as an attribute of the weapon item or the spell itself.
#Stat modifications can be part of a class property that is dynamically added and then removed when it wears off.
#https://stackoverflow.com/questions/1325673/how-to-add-property-to-a-class-dynamically
#https://eev.ee/blog/2012/05/23/python-faq-descriptors/

#In battle, the battle action class sends the data of the spell used or physical attack
#Runbattleactionqueue will call a check to see if the equipped weapon or spell has a chance of status effect

#Implement summon and transformation type spells. This will either add an instance of the summon class character to the party, or replace the transforming character.
#If desired the stats of the summon or transformation could be retained and made to level up or they could be reset to a default value after each use.
#Implement control of enemies to temporarily add them to your party. If this wears off, they are returned to the enemy party. They could be AI controlled or player controlled.
#After battle they would be removed from the party. Or if desired, they could be captured and then used in future battles as desired.

#Implement specific enemy lists that are loaded from areasets.

#Implement scripted battles.
#Make use of the battle turn counter.
#Modify the combat action to add scipted elements.
#These will include a precondition and an action.
#have a universal game state set of flags.
#One for scripted battles being enabled, one for run being disabled in battle, and one for losing the scripted battle.
#For run being disable, when the run action is executed in battle, if the flag is set, running fails.
#For scripted battles, implement a win and a loss set of actions.
#When scripted battle loss flag is enabled, if the party dies, the dead() function needs to check for this flag and then run a function to
#execute scripted actions.
#If the player wins, the win() function needs to check for this flag and then run a function to execute scripted actions.

#Implement map updates.
#Update the initswitch on an area to be an array of two booleans.
#Use this to track if you have visited an area and if it is revealed by a map.
#Use this code: FF for unvisited. FT for visited. TF for map revealed. TT for both.
#Update the map function to iterate through each area ID from 1 to the product
#of the width x height and check if it has been displayed or has another status.
#Each area will have a specific map status that can be used to indicate something.
#There will be a corresponding symbol which can be configured to indicate something.
#An example would be using an 'X' to set a destination the player should visit.
#Areas that are not populated can be set to '.' and areas that are visited/visible on the map
#can be set to '-'.
#This will allow the map to show the shape of the areaset instead of a rectangle.

#Update direction code to implement items to resolve statuses.
#Position 0 is the areaset name
#Position 1 is the destination ID
#Position 2 is the message for how the path appears
#Position 3 is the status
#Position 4 is the status message
#Position 5 is the item that resolves the status. This will be an array in case multiple items resolve it.
#Position 6 is the resolution message

#Update direction handling to check for if direction exists, then status, then if areaset is current or new.

#Update direction code to replace all directions with a dictionary called direction.
#This would allow the creation of any direction as well as multiple paths in the same direction.

#Update direction status resolution items to be stored as lists with the structure:
#[itemname, consumableflag, setname]
#The consumable flag sets if the item is consumed upon use or not.
#The setname sets if the item is used alone to resolve the status or if it is part of a set.
#If the item is part of a set, all items with the same setname must be held in order to resolve the status.

#Update start1() and other functions so that it can be split so checking for running events is not done
#when returning from menus for simple non-movement actions.


weapons = {"Rusty Sword":20, "Dagger":15, "Wand":10, "Great Sword":40, "Battle Axe":50, "Iron Dagger":70, "Rod":50, "Staff":200}
armors = {"Leather Tunic":15, "Robe":10, "Chain Mail":50, "Plate Mail":100, "Magic Cloak":75, "Wizard Robe":200,"Shadow Cloak":150}
accs = {"Ring":75, "Magic Ring":125, "Mystic Ring":200, "Warrior Ring":100, "Iron Ring":100, "Quick Ring":50, "Agile Ring":100, "Lucky Ring":100, "Fortune Ring":200, "Ranger Ring":200}
potions = {"Potion":10}
spells = ["fireball"]
nothing = {"None"}
enemies = {1:{"name":"Goblin", "count":0}, 2:{"name":"Zombie","count":0}, 3:{"name":"Fast Zombie","count":0}, 4:{"name":"Imp","count":0}, 5:{"name":"Magic Goblin", "count":0}, 6:{"name":"Big Blob", "count":0}, 7:{"name":"Blob", "count":0}}
bosses = {1:{"name":"Boss Blob", "count":0}}
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
global areas
areas = {}
global width
global height
global filename
global battleturncounter
global scriptedbattles

currentparty = []
outofparty = []
battlepartymembers = []
enemyparty = []
defeatedenemyparty = []
battlemembers = []
sortedbattlemembers = []
newlyaddedbattlemembers = []
battleactionqueue = []
invtosell = []

#Scripted Battles: On, Run disabled, Loss enabled
#scriptedbattles = [False, False, False]

class GameData:
    def __init__(self, name):
        self.name = name
        self.filename = ""
        self.switches = {}
        self.variables = {}
        self.areas = {}
        self.weapons = {}
        self.armors = {}
        self.accs = {}
        self.potions = {}
        self.spells = {}
        self.items = {}
        self.nothing = {}
        self.enemies = {}
        self.bosses = {}
        self.currentparty = []
        self.outofparty = []
        self.battlepartymembers = []
        self.battlemembers = []
        self.sortedbattlemembers = []
        self.newlyaddedbattlemembers = []
        self.battleactionqueue = []
        self.invtosell = []
        self.scriptedbattles = [False, True, False]
        self.battlescripts = []
        self.battleturncounter = 0
GameDataIG = GameData("Current Game")

class Player:
    def __init__(self, name, charclass):
        self.name = name
        self.idno = 0
        self.level = 1
        self.mHP = 20
        self.hp = self.mHP
        self.hpgrowth = "med"
        self.mMP = 20
        self.mp = self.mMP
        self.mpgrowth = "med"
        self.base_attack = 10
        self.attackgrowth = "med"
        self.base_defense = 5
        self.defensegrowth = "med"
        self.base_wisdom = 8
        self.wisdomgrowth = "med"
        self.base_resistance = 5
        self.resistancegrowth = "med"
        self.base_agility = 5
        self.agilitygrowth = "med"
        self.base_luck = 2
        self.luckgrowth = "med"
        self.fireres = 0
        self.electricres = 0
        self.iceres = 0
        self.healres = 0
        self.status = []
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 1
        self.weapon = ["Rusty Sword"]
        self.curweapon = "None"
        self.armor = ["Leather Tunic"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.items = ["potion"]
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"
        self.battlecommands = []
        self.currentposition = 1

    @property
    def attack(self):
        attack = self.base_attack
        if self.curweapon == "Rusty Sword":
            attack += 5

        if self.curweapon == "Wand":
            attack += 3

        if self.curweapon == "Rod":
            attack += 5

        if self.curweapon == "Staff":
            attack += 10

        if self.curweapon == "Dagger":
            attack += 4

        if self.curweapon == "Iron Dagger":
            attack += 10

        if self.curweapon == "Great Sword":
            attack +=  15

        if self.curweapon == "Battle Axe":
            attack += 20

        if self.curacc == "Warrior Ring":
            attack += 5

        return attack

    @property
    def defense(self):
        defense = self.base_defense
        if self.curarmor == "Leather Tunic":
            defense += 5

        if self.curarmor == "Chain Mail":
            defense += 10

        if self.curarmor == "Plate Mail":
            defense += 15

        if self.curacc == "Iron Ring":
            defense += 5

        if self.curarmor == "Robe":
            defense += 1

        if self.curacc == "Magic Cloak":
            defense += 4

        if self.curacc == "Wizard Robe":
            defense += 10

        if self.curarmor == "Shadow Cloak":
            defense += 10

        return defense

    @property
    def wisdom(self):
        wisdom = self.base_wisdom
        if self.curweapon == "Wand":
            wisdom +=5

        if self.curweapon == "Rod":
            wisdom +=10

        if self.curweapon == "Staff":
            wisdom +=15
            
        if self.curacc == "Ring":
            wisdom += 5

        if self.curacc == "Magic Ring":
            wisdom += 10

        if self.curacc == "Mystic Ring":
            wisdom += 15

        return wisdom

    @property
    def resistance(self):
        resistance = self.base_resistance
        if self.curarmor == "Robe":
            resistance +=5
            
        if self.curacc == "Magic Cloak":
            resistance += 10

        if self.curacc == "Wizard Robe":
            resistance += 15

        return resistance

    @property
    def agility(self):
        agility = self.base_agility
        if self.curacc == "Quick Ring":
            agility += 1

        if self.curacc == "Agile Ring":
            agility += 3

        if self.curacc == "Ranger Ring":
            agility += 5

        if self.curweapon == "Dagger":
            agility += 1

        if self.curweapon == "Iron Dagger":
            agility += 3

        if self.curarmor == "Shadow Cloak":
            agility += 5

        if self.curarmor == "Chain Mail":
            agility -= 2

        if self.curarmor == "Plate Mail":
            agility -= 5

        return agility

    @property
    def luck(self):
        luck = self.base_luck
        if self.curacc == "Lucky Ring":
            luck += 1

        if self.curacc == "Fortune Ring":
            luck += 2

        if self.curacc == "Ranger Ring":
            luck += 3

        return luck

class Warrior(Player):
    def __init__(self, name, charclass):
        self.name = name
        self.idno = 0
        self.level = 1
        self.mHP = 120
        self.hp = self.mHP
        self.hpgrowth = "high"
        self.mMP = 0
        self.mp = self.mMP
        self.mpgrowth = "none"
        self.base_attack = 10
        self.attackgrowth = "high"
        self.base_defense = 5
        self.defensegrowth = "high"
        self.base_wisdom = 3
        self.wisdomgrowth = "low"
        self.base_resistance = 3
        self.resistancegrowth = "med"
        self.base_agility = 4
        self.agilitygrowth = "med"
        self.base_luck = 2
        self.luckgrowth = "low"
        self.fireres = 0
        self.electricres = 0
        self.iceres = 0
        self.healres = 0
        self.status = []
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 1
        self.weapon = ["Rusty Sword"]
        self.curweapon = "None"
        self.armor = ["Leather Tunic"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.items = ["potion"]
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"
        self.battlecommands = []

class Thief(Player):
    def __init__(self, name, charclass):
        self.name = name
        self.idno = 0
        self.level = 1
        self.mHP = 70
        self.hp = self.mHP
        self.hpgrowth = "med"
        self.mMP = 0
        self.mp = self.mMP
        self.mpgrowth = "none"
        self.base_attack = 8
        self.attackgrowth = "med"
        self.base_defense = 4
        self.defensegrowth = "med"
        self.base_wisdom = 4
        self.wisdomgrowth = "med"
        self.base_resistance = 4
        self.resistancegrowth = "med"
        self.base_agility = 8
        self.agilitygrowth = "high"
        self.base_luck = 5
        self.luckgrowth = "high"
        self.fireres = 0
        self.electricres = 0
        self.iceres = 0
        self.healres = 0
        self.status = []
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 1
        self.weapon = ["Dagger"]
        self.curweapon = "None"
        self.armor = ["Leather Tunic"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.items = ["potion"]
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"
        self.battlecommands = []
        
class Mage(Player):
    def __init__(self, name, charclass):
        self.name = name
        self.idno = 0
        self.level = 1
        self.mHP = 50
        self.hp = self.mHP
        self.hpgrowth = "low"
        self.mMP = 20
        self.mp = self.mMP
        self.mpgrowth = "high"
        self.base_attack = 5
        self.attackgrowth = "low"
        self.base_defense = 3
        self.defensegrowth = "med"
        self.base_wisdom = 10
        self.wisdomgrowth = "high"
        self.base_resistance = 5
        self.resistancegrowth = "high"
        self.base_agility = 5
        self.agilitygrowth = "med"
        self.base_luck = 3
        self.luckgrowth = "med"
        self.fireres = 0
        self.electricres = 0
        self.iceres = 0
        self.healres = 0
        self.status = []
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 1
        self.weapon = ["Wand"]
        self.curweapon = "None"
        self.armor = ["Robe"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.items = ["potion"]
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"
        self.battlecommands = []
        self.learnedspells = ["fireball"]
        self.spells = {1:"fireball", 2:"heal", 4:"icicle", 7:"zap"}

class Goblin:
    def __init__(self, name):
        self.name = name
        self.mHP = 15
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 5
        self.defense = 1
        self.wisdom = 0
        self.resistance = 1
        self.fireres = 0
        self.electricres = 0
        self.iceres = 0
        self.healres = 0
        self.agility = 3
        self.luck = 1
        self.status = []
        self.goldgain = 10
        self.expgain = 5
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = []
GoblinIG = Goblin("Goblin")

class Zombie:
    def __init__(self, name):
        self.name = name
        self.mHP = 20
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 7
        self.defense = 3
        self.wisdom = 0
        self.resistance = -5
        self.fireres = -5
        self.electricres = 0
        self.iceres = 0
        self.healres = -10
        self.agility = 2
        self.luck = 1
        self.status = []
        self.goldgain = 15
        self.expgain = 8
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = []
ZombieIG = Zombie("Zombie")

class FastZombie:
    def __init__(self, name):
        self.name = name
        self.mHP = 25
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 10
        self.defense = 4
        self.wisdom = 0
        self.resistance = -5
        self.fireres = -5
        self.electricres = 0
        self.iceres = 0
        self.healres = -10
        self.agility = 7
        self.luck = 1
        self.status = []
        self.goldgain = 20
        self.expgain = 10
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = []
FastZombieIG = FastZombie("Fast Zombie")

class Imp:
    def __init__(self, name):
        self.name = name
        self.mHP = 40
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 12
        self.defense = 5
        self.wisdom = 0
        self.resistance = 3
        self.fireres = 0
        self.electricres = 0
        self.iceres = 0
        self.healres = 0
        self.agility = 5
        self.luck = 2
        self.status = []
        self.goldgain = 20
        self.expgain = 12
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = []
ImpIG = Imp("Imp")

class MagicGoblin:
    def __init__(self, name):
        self.name = name
        self.mHP = 25
        self.hp = self.mHP
        self.mMP = 15
        self.mp = self.mMP
        self.attack = 10
        self.defense = 4
        self.wisdom = 10
        self.resistance = 10
        self.fireres = 10
        self.electricres = 10
        self.iceres = 10
        self.healres = 0
        self.agility = 5
        self.luck = 1
        self.status = []
        self.goldgain = 25
        self.expgain = 15
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = []
MagicGoblinIG = MagicGoblin("Magic Goblin")

class BigBlob:
    def __init__(self, name):
        self.name = name
        self.mHP = 40
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 10
        self.defense = 3
        self.wisdom = 2
        self.resistance = 5
        self.fireres = -2
        self.electricres = -3
        self.iceres = -1
        self.healres = 0
        self.agility = 4
        self.luck = 1
        self.status = []
        self.goldgain = 10
        self.expgain = 10
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = [["Blob", "Blob"], "Big Blob split into two!"]
BigBlobIG = BigBlob("Big Blob")

class Blob:
    def __init__(self, name):
        self.name = name
        self.mHP = 20
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 8
        self.defense = 3
        self.wisdom = 2
        self.resistance = 5
        self.fireres = -2
        self.electricres = -3
        self.iceres = -1
        self.healres = 0
        self.agility = 4
        self.luck = 1
        self.status = []
        self.goldgain = 5
        self.expgain = 5
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = []
BigBlobIG = Blob("Blob")

class BossBlob:
    def __init__(self, name):
        self.name = name
        self.mHP = 75
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 15
        self.defense = 2
        self.wisdom = 2
        self.resistance = 4
        self.fireres = -3
        self.electricres = -4
        self.iceres = -2
        self.healres = 0
        self.agility = 3
        self.luck = 1
        self.status = []
        self.goldgain = 100
        self.expgain = 50
        self.action = "nothing"
        self.chartype = "enemy"
        self.nextform = [["Big Blob"], "Boss Blob shrunk!"]
BossBlobIG = BossBlob("Boss Blob")

class BattleActionClass:
    def __init__(self, name):
        self.name = name
        self.chartype = "player"
        self.charclass = "Warrior"
        self.action = "physical"
        self.target = 0

class Area:
    def __init__(self, name):
        self.name = name
        self.idno = 0
        self.north = ["", 0, "", "normal", "", [], ""]
        self.south = ["", 0, "", "normal", "", [], ""]
        self.east = ["", 0, "", "normal", "", [], ""]
        self.west = ["", 0, "", "normal", "", [], ""]
        self.up = ["", 0, "", "normal", "", [], ""]
        self.down = ["", 0, "", "normal", "", [], ""]
        self.items = []
        self.sign = ""
        self.initswitch = [False,False]
        self.initmessage = ""
        self.message = ""
        self.mapstatus = ""
        self.enemy = False
        self.switches = {}
        self.variables = []
        self.events = []

class Event:
    def __init__(self, name):
        self.name = name
        self.idno = 0
        self.type = ""
        self.commands = []
        self.description = ""
        self.preconditions = {}
        self.states = []
        self.nextstatecond = []
        self.event = {}
        self.hidden = False

class Precondition:
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.detail = ""
        self.value = 0

class Items:
    def __init__(self, name):
        self.name = name
        self.type = "normal"
        self.cost = 0
        self.description = ""
        self.value = 0
        self.consumable = False

class Spell:
    def __init__(self, name):
        self.name = name
        self.type = "magic"
        self.mpcost = 0
        self.description = ""
        self.message = ""
        self.basepower = 0
        self.targettype = "enemy"
        self.target = "single"

class Battlecommand:
    def __init__(self, name):
        self.name = name
        self.label = ""

#Intialize battle commands
attack = Battlecommand("attack")
attack.label = "Attack"
defend = Battlecommand("defend")
defend.label = "Defend"
magic = Battlecommand("magic")
magic.label = "Magic"
item = Battlecommand("item")
item.label = "Item"
run = Battlecommand("run")
run.label = "Run"
summon = Battlecommand("summon")
summon.label = "Summon"
transform = Battlecommand("transform")
transform.label = "Transform"
capture = Battlecommand("capture")
capture.label = "Capture"
steal = Battlecommand("steal")
steal.label = "Steal"

#Initialize spells
fireball = Spell("Fireball")
fireball.type = "fire"
fireball.mpcost = 5
fireball.description = "A single target ball of fire."
fireball.message = "threw a fireball"
fireball.basepower = 5

zap = Spell("Zap")
zap.type = "electric"
zap.mpcost = 10
zap.description = "A single target tongue of lightning."
zap.message = "hurled a bolt of lightning"
zap.basepower = 10

icicle = Spell("Icicle")
icicle.type = "ice"
icicle.mpcost = 7
icicle.description = "A single target icicle."
icicle.message = "threw an icicle"
icicle.basepower = 7

heal = Spell("Heal")
heal.type = "healing"
heal.mpcost = 5
heal.description = "Heals 50 HP for one party member."
heal.message = "sent a wave of healing energy"
heal.basepower = 50

#setup default area
width = 1
height = 1
x = 1
for x in range(x):
    i = x + 1
    AreaIG = Area("Room %i" % i)
    AreaIG.idno = i
#    AreaIG.east = i+1
#    AreaIG.south = i+4
#    AreaIG.west = i-1
#    AreaIG.north = i-4
#    areas.append(AreaIG)
    areas[i] = AreaIG

def main():
    os.system("cls")
    print("Welcome to Python Object RPG!\n")
    print("1.) Start")
    print("2.) Load")
    print("3.) Exit")
    option = input(">")
    if option == "1":
        start()
    elif option == "2":
        loadgame()
    elif option == "3":
        sys.exit()
    else:
        main()

def start():
    os.system("cls")
    global areas
    global width
    global height
    global filename
    while True:
        print("Which game will you load? \nPlease enter the filename of the areaset you would like to load.")
        filename = input(">")
        try:
            areas, width, height, position = loadareaset(filename)
            break
        except:
            print("That filename is invalid.\n")
    print("\nHello, what is your name?")
    name = input(">")
    print("Greetings %s!" % name)
    option = input("Press enter to continue.")
    print("What is your class?")
    global PlayerIG
    charclass = input("Warrior, Thief, or Mage? \n>").lower()
    if charclass == "warrior":
        PlayerIG = Warrior(name, charclass.capitalize())
    elif charclass == "thief":
         PlayerIG = Thief(name, charclass.capitalize())
    elif charclass == "mage":
        PlayerIG = Mage(name, charclass.capitalize())
    else:
        PlayerIG = Player(name, "Nothing")
    currentparty.append(PlayerIG)
    PlayerIG.currentposition = position
    PlayerIG.idno = 1
    readintro(areas)
    start1()

def newchar():
    os.system("cls")
    if len(currentparty) > 0:
        global newplayer
        print("Hello, what is your name?")
        newplayer = input(">")
        print("Greetings %s!" % newplayer)
        option = input("Press enter to continue.")
        print("What is your class?")
        charclass = input("Warrior, Thief, or Mage? \n>").lower()
        if charclass == "warrior":
            newplayer = Warrior(newplayer, charclass.capitalize())
        elif charclass == "thief":
            newplayer = Thief(newplayer, charclass.capitalize())
        elif charclass == "mage":
            newplayer = Mage(newplayer, charclass.capitalize())
        else:
            newplayer = Player(newplayer, "Nothing")
        newid = checkcharid()
        newplayer.idno = newid + 1
        currentparty.append(newplayer)
        if "potion" in newplayer.items:
            PlayerIG.potions += 1
        start1()

def newchar2(name, charclass):
    os.system("cls")
    global newplayer
    print("Name: {}".format(name))
    print("Class: {}".format(charclass))
    while True:
        print("Change name?")
        print("1.) Keep name")
        print("2.) Edit name")
        choice = input(">")
        if choice == "1":
            break
        elif choice == "2":
            newname = ""
            while True:
                if newname == name:
                    break
                print("Please enter a new name for {}.".format(name))
                newname = input(">")
                while True:
                    print("Is {} ok? (y or n)".format(newname))
                    option = input(">")
                    if option == "y":
                        name = newname
                        break
                    else:
                        break
            break
        else:
            print("Pleae enter a valid selection.")
    newplayer = name       
    if charclass == "warrior":
        newplayer = Warrior(newplayer, charclass.capitalize())
    elif charclass == "thief":
        newplayer = Thief(newplayer, charclass.capitalize())
    elif charclass == "mage":
        newplayer = Mage(newplayer, charclass.capitalize())
    else:
        newplayer = Player(newplayer, "Nothing")
    newid = checkcharid()
    newplayer.idno = newid + 1
    currentparty.append(newplayer)
    if "potion" in newplayer.items:
        PlayerIG.potions += 1
    start1()

def checkcharid():
    latestid = 0
    for char in currentparty:
        if char.idno > latestid:
            latestid = char.idno
    for char in outofparty:
        if char.idno > latestid:
            latestid = char.idno
    return latestid

def readintro(areaset):
    areas = areaset
    intro = areas[0].initmessage
    print(intro)
    areas[0].initswitch[0] = True

def showstatus(areaset, currentposition):
    areas = areaset
    position = currentposition
    #print(areas)
    print("********")
    print("Area: {}".format(areas[position].name))
    if areas[position].initswitch[1] == False:
        if not areas[position].initmessage:
            pass
        else:
            print("{}".format(areas[position].initmessage))
        areas[position].initswitch[1] = True
    if not areas[position].message:
        pass
    else:
        print("{}".format(areas[position].message))
    if areas[position].north[1] != 0:
        print(areas[position].north[2])
    if areas[position].south[1] != 0:
        print(areas[position].south[2])
    if areas[position].east[1] != 0:
        print(areas[position].east[2])
    if areas[position].west[1] != 0:
        print(areas[position].west[2])
    if areas[position].up[1] != 0:
        print(areas[position].up[2])
    if areas[position].down[1] != 0:
        print(areas[position].down[2])
    if not areas[position].sign:
        pass
    else:
        print("There is a sign nearby.")
    if not areas[position].items:
        pass
    else:
        for item in areas[position].items:
            print("You see a {} lying on the ground.".format(item))
    if not areas[position].events:
        pass
    else:
        for event in areas[position].events:
            for preconditionset in event.preconditions:
                checkpreconditions(preconditionset, event, areas[position], areas)
        for event in areas[position].events:
            if event.hidden == False:
                #check preconditions
                print(event.description)
                commands = []
                for command in event.commands:
                    commands.append(command)
                x = {"" if len(event.commands) == 1 else ", "}
                #print("Interact using the following command(s): " + "".join("{0}{1}".format(command, {"" if len(event.commands) == 1 else ", "}) for command in event.commands))
                if event.commands:
                    print("Interact using the following command(s): " + "".join("{0}".format(commands)))
                #print("Interact using the following command(s): " + "".join("{0}".format(command + ", " if len(commands) > 1 else command) for x in range(len(commands) - 1)))
                #if len(commands) == 1:
                #    print("Interact using the following command(s): " + "".join("{}".format(command)))
                #print("Interact using the following command(s): " + "".join("{}".format(command + ", ") for command in range(len(commands) - 1)) + "".join("{}".format(commands[-1])))
                #print("[" + "".join("{}".format("-") for i in range(before)) + "*" + "".join("{}".format("-") for k in range(after)) + "]")
                #print("[" + "".join("{}".format("-") for k in range(width)) + "]")
    if areas[position].enemy == True:
        print("You sense danger nearby...")
        #Set up chance that battle starts immediately with ambush attack, else enter battle via command
        totalagility = 0
        for char in currentparty:
            totalagility += char.agility
        averageagility = totalagility / len(currentparty)
        ambush = random.randint(1,99)
        if ambush > 75:
            print("Ambush attack!")
            prefight()
    print("********")
        
def getpotioncount():
    count = 0
    for player in currentparty:
        for item in player.items:
            if item == "potion":
                count += 1
    return count

def start1():
    os.system("cls")
    global areas
    global width
    global height
    showmap(width, height, PlayerIG.currentposition)
    currentarea = areas[PlayerIG.currentposition]
    showstatus(areas, PlayerIG.currentposition)
    PlayerIG.potions = getpotioncount()
    print("Hello %s what would you like to do?\n" % PlayerIG.name)
    print("Gold: %i" % PlayerIG.gold)
    print("Potions: %i\n" % PlayerIG.potions)
    for char in currentparty:
        displayhp(char)
        displaymp(char)
        print("Level: %i" % char.level)
        print("Class: %s" % char.charclass)
    commands = []
    for event in currentarea.events:
        if event.hidden == False:
            for command in event.commands:
                commands.append(command)
        #Check preconditions of events
        #for preconditionset in event.preconditions:
        #   checkpreconditions(preconditionset, event, currentarea, areas)
    
    print("********")
    print("1.) Fight")
    print("2.) Store")
    print("3.) Save")
    print("4.) Inventory")
    print("5.) Inn")
    print("6.) Exit")
    print("7.) Status")
    print("8.) Recruit new party member")
    print("9.) Display classes")
    print("10.) Load Area Set")
    print("********")
    option = input(">")
    if option == "1":
        prefight()
    elif option == "2":
        store()
    elif option == "3":
        savegame()
    elif option == "4":
        inventory()
    elif option == "5":
        inn()
    elif option == "6":
        sys.exit()
    elif option == "7":
        status()
    elif option == "8":
        newchar()
    elif option == "9":
        displayclass()
    elif option == "10":
        while True:
            print("Please enter the filename of the areaset you would like to load.")
            filename = input(">")
            try:
                areas, width, height, PlayerIG.currentposition = loadareaset(filename)
                break
            except:
                print("That filename is invalid.")
        start1()
    elif "read" in option:
        if not currentarea.sign:
            print("There is nothing here to read.\n")
        else:
            print("Reading the nearby sign:")
            print("{}".format(currentarea.sign))
            print("\n")
        start1()
    elif "look" in option:
        print("{}".format(areas[PlayerIG.currentposition].initmessage))
        print("********")
        start1()
    elif "take" in option:
        if not areas[PlayerIG.currentposition].items:
            print("There is nothing to take in this area.")
            start1()
        else:
            if len(areas[PlayerIG.currentposition].items) == 1:
                if len(currentparty) == 1:
                    print("{} took the {}.".format(currentparty[0].name,areas[PlayerIG.currentposition].items[0]))
                    currentparty[0].items.append(areas[PlayerIG.currentposition].items[0])
                    if areas[PlayerIG.currentposition].items[0] == "potion":
                        PlayerIG.potions += 1
                    areas[PlayerIG.currentposition].items.remove(areas[PlayerIG.currentposition].items[0])
                    start1()
                else:
                    print("Give {} to who?".format(areas[PlayerIG.currentposition].items[0]))
                    while True:
                        for char in currentparty:
                            print(char.name)
                        option = input(">")
                        for char in currentparty:
                            if option == char.name:
                                print("{} took the {}.".format(char.name,areas[PlayerIG.currentposition].items[0]))
                                char.items.append(areas[PlayerIG.currentposition].items[0])
                                if areas[PlayerIG.currentposition].items[0] == "potion":
                                    PlayerIG.potions += 1
                                areas[PlayerIG.currentposition].items.remove(areas[PlayerIG.currentposition].items[0])
                                start1()
                        print("Please specify a valid party member.")
            else:
                print("Take which item?")
                while True:
                    for item in areas[PlayerIG.currentposition].items:
                        print(item)
                    option = input(">")
                    for item in areas[PlayerIG.currentposition].items:
                        if option == item:
                            if len(currentparty) == 1:
                                print("{} took the {}.".format(currentparty[0].name,item))
                                currentparty[0].items.append(item)
                                if item == "potion":
                                    PlayerIG.potions += 1
                                areas[PlayerIG.currentposition].items.remove(item)
                                start1()
                            else:
                                print("Give {} to who?".format(item))
                                while True:
                                    for char in currentparty:
                                        print(char.name)
                                    option = input(">")
                                    for char in currentparty:
                                        if option == char.name:
                                            print("{} took the {}.".format(char.name, item))
                                            char.items.append(item)
                                            if item == "potion":
                                                PlayerIG.potions += 1
                                            areas[PlayerIG.currentposition].items.remove(item)
                                            start1()
                                    print("Please specify a valid party member.")
                    break
            start1()
    #Check commands
    elif option in commands:
        tempeventlist = []
        print("{} for which?".format(option))
        for event in currentarea.events:
            if event.hidden == False:
                for command in event.commands:
                    if option == command:
                        print(event.name)
                        tempeventlist.append(event)
        choice = input(">")
        for event in tempeventlist:
            if choice == event.name:
                runevent(option, event, currentarea, areas)
                break
        start1()
    elif "go" in option and "east" not in option and "west" not in option and "north" not in option and "south" not in option:
        print("Go where?")
        start1()
    elif "go" and "east" in option:
        movesuccess = False
        if currentarea.east[1] != 0:
            if currentarea.east[3] != "normal":
                print("Can't go that way.")
                #print("East: {} vs {}".format(currentarea.east[3], "normal"))
                print("Message: {}".format(currentarea.east[4]))
                if currentarea.east[3] == "locked":
                    for char in currentparty:
                        if "key" in char.items:
                            while True:
                                print("Use key?")
                                print("1.) Yes.")
                                print("2.) No.")
                                option = input(">")
                                if option == "2":
                                    break
                                elif option == "1":
                                    print("{} used a key to open the door.".format(char.name))
                                    currentarea.east[3] = "normal"
                                    char.items.remove("key")
                                    movesuccess = True
                                    break
                                else:
                                    print("Please enter a valid selection.")
                else:
                    for char in currentparty:
                        for item in char.items:
                            for key in currentarea.east[5]:
                                if item == key:
                                    while True:
                                        print("Use {}?".format(key))
                                        print("1.) Yes.")
                                        print("2.) No.")
                                        option = input(">")
                                        if option == "2":
                                            break
                                        elif option == "1":
                                            print(currentarea.east[6])
                                            currentarea.east[3] = "normal"
                                            char.items.remove(key)
                                            movesuccess = True
                                            break
                                        else:
                                            print("Please enter a valid selection.")
            elif currentarea.east[3] == "normal":
                #print(currentarea.east[3])
                movesuccess = True
            
            if currentarea.east[0] != areas[0].name and movesuccess == True:
                #save current areaset to retain object permanence
                previousareaset = "temp" + areas[0].name
                saveareaset(previousareaset, areas, width, height, PlayerIG.currentposition)
                #load next area
                nextareaset = "temp" + areas[PlayerIG.currentposition].east[0]
                if path.exists(nextareaset + ".pkl"):
                    #print("Temp exists!")
                    #load saved instance of areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(nextareaset)
                    PlayerIG.currentposition = currentarea.east[1]
                else:
                    #print("Temp doesn't exist...")
                    #load original areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(areas[PlayerIG.currentposition].east[0])
                    PlayerIG.currentposition = currentarea.east[1]
            else:
                if movesuccess == True:
                    PlayerIG.currentposition = currentarea.east[1]
        else:
            print("There is no path in that direction.")
        start1()
    elif "go" and "west" in option:
        movesuccess = False
        if currentarea.west[1] != 0:
            if currentarea.west[3] != "normal":
                print("Can't go that way.")
                #print("West: {} vs {}".format(currentarea.west[3], "normal"))
                print("Message: {}".format(currentarea.west[4]))
                if currentarea.west[3] == "locked":
                    for char in currentparty:
                        if "key" in char.items:
                            while True:
                                print("Use key?")
                                print("1.) Yes.")
                                print("2.) No.")
                                option = input(">")
                                if option == "2":
                                    break
                                elif option == "1":
                                    print("{} used a key to open the door.".format(char.name))
                                    currentarea.west[3] = "normal"
                                    char.items.remove("key")
                                    movesuccess = True
                                    break
                                else:
                                    print("Please enter a valid selection.")
                else:
                    for char in currentparty:
                        for item in char.items:
                            for key in currentarea.west[5]:
                                if item == key:
                                    while True:
                                        print("Use {}?".format(key))
                                        print("1.) Yes.")
                                        print("2.) No.")
                                        option = input(">")
                                        if option == "2":
                                            break
                                        elif option == "1":
                                            print(currentarea.west[6])
                                            currentarea.west[3] = "normal"
                                            char.items.remove(key)
                                            movesuccess = True
                                            break
                                        else:
                                            print("Please enter a valid selection.")
            elif currentarea.west[3] == "normal":
                #print(currentarea.west[3])
                movesuccess = True
            
            if currentarea.west[0] != areas[0].name and movesuccess == True:
                #save current areaset to retain object permanence
                previousareaset = "temp" + areas[0].name
                saveareaset(previousareaset, areas, width, height, PlayerIG.currentposition)
                #load next area
                nextareaset = "temp" + areas[PlayerIG.currentposition].west[0]
                if path.exists(nextareaset + ".pkl"):
                    #print("Temp exists!")
                    #load saved instance of areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(nextareaset)
                    PlayerIG.currentposition = currentarea.west[1]
                else:
                    #print("Temp doesn't exist...")
                    #load original areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(areas[PlayerIG.currentposition].west[0])
                    PlayerIG.currentposition = currentarea.west[1]
            else:
                if movesuccess == True:
                    PlayerIG.currentposition = currentarea.west[1]
        else:
            print("There is no path in that direction.")
        start1()
    elif "go" and "north" in option:
        movesuccess = False
        if currentarea.north[1] != 0:
            if currentarea.north[3] != "normal":
                print("Can't go that way.")
                #print("North: {} vs {}".format(currentarea.north[3], "normal"))
                print("Message: {}".format(currentarea.north[4]))
                if currentarea.north[3] == "locked":
                    for char in currentparty:
                        if "key" in char.items:
                            while True:
                                print("Use key?")
                                print("1.) Yes.")
                                print("2.) No.")
                                option = input(">")
                                if option == "2":
                                    break
                                elif option == "1":
                                    print("{} used a key to open the door.".format(char.name))
                                    currentarea.north[3] = "normal"
                                    char.items.remove("key")
                                    movesuccess = True
                                    break
                                else:
                                    print("Please enter a valid selection.")
                else:
                    for char in currentparty:
                        for item in char.items:
                            for key in currentarea.north[5]:
                                if item == key:
                                    while True:
                                        print("Use {}?".format(key))
                                        print("1.) Yes.")
                                        print("2.) No.")
                                        option = input(">")
                                        if option == "2":
                                            break
                                        elif option == "1":
                                            print(currentarea.north[6])
                                            currentarea.north[3] = "normal"
                                            char.items.remove(key)
                                            movesuccess = True
                                            break
                                        else:
                                            print("Please enter a valid selection.")
            elif currentarea.north[3] == "normal":
                #print(currentarea.north[3])
                movesuccess = True
            
            if currentarea.north[0] != areas[0].name and movesuccess == True:
                #save current areaset to retain object permanence
                previousareaset = "temp" + areas[0].name
                saveareaset(previousareaset, areas, width, height, PlayerIG.currentposition)
                #load next area
                nextareaset = "temp" + areas[PlayerIG.currentposition].north[0]
                if path.exists(nextareaset + ".pkl"):
                    #print("Temp exists!")
                    #load saved instance of areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(nextareaset)
                    PlayerIG.currentposition = currentarea.north[1]
                else:
                    #print("Temp doesn't exist...")
                    #load original areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(areas[PlayerIG.currentposition].north[0])
                    PlayerIG.currentposition = currentarea.north[1]
            else:
                if movesuccess == True:
                    PlayerIG.currentposition = currentarea.north[1]
        else:
            print("There is no path in that direction.")
        start1()
    elif "go" and "south" in option:
        movesuccess = False
        if currentarea.south[1] != 0:
            if currentarea.south[3] != "normal":
                print("Can't go that way.")
                #print("South: {} vs {}".format(currentarea.south[3], "normal"))
                print("Message: {}".format(currentarea.south[4]))
                if currentarea.south[3] == "locked":
                    for char in currentparty:
                        if "key" in char.items:
                            while True:
                                print("Use key?")
                                print("1.) Yes.")
                                print("2.) No.")
                                option = input(">")
                                if option == "2":
                                    break
                                elif option == "1":
                                    print("{} used a key to open the door.".format(char.name))
                                    currentarea.south[3] = "normal"
                                    char.items.remove("key")
                                    movesuccess = True
                                    break
                                else:
                                    print("Please enter a valid selection.")
                else:
                    for char in currentparty:
                        for item in char.items:
                            for key in currentarea.south[5]:
                                if item == key:
                                    while True:
                                        print("Use {}?".format(key))
                                        print("1.) Yes.")
                                        print("2.) No.")
                                        option = input(">")
                                        if option == "2":
                                            break
                                        elif option == "1":
                                            print(currentarea.south[6])
                                            currentarea.south[3] = "normal"
                                            char.items.remove(key)
                                            movesuccess = True
                                            break
                                        else:
                                            print("Please enter a valid selection.")
            elif currentarea.south[3] == "normal":
                #print(currentarea.south[3])
                movesuccess = True
            
            if currentarea.south[0] != areas[0].name and movesuccess == True:
                #save current areaset to retain object permanence
                previousareaset = "temp" + areas[0].name
                saveareaset(previousareaset, areas, width, height, PlayerIG.currentposition)
                #load next area
                nextareaset = "temp" + areas[PlayerIG.currentposition].south[0]
                if path.exists(nextareaset + ".pkl"):
                    #print("Temp exists!")
                    #load saved instance of areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(nextareaset)
                    PlayerIG.currentposition = currentarea.south[1]
                else:
                    #print("Temp doesn't exist...")
                    #load original areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(areas[PlayerIG.currentposition].south[0])
                    PlayerIG.currentposition = currentarea.south[1]
            else:
                if movesuccess == True:
                    PlayerIG.currentposition = currentarea.south[1]
        else:
            print("There is no path in that direction.")
        start1()
    elif "go" and "up" in option:
        movesuccess = False
        if currentarea.up[1] != 0:
            if currentarea.up[3] != "normal":
                print("Can't go that way.")
                #print("Up: {} vs {}".format(currentarea.up[3], "normal"))
                print("Message: {}".format(currentarea.up[4]))
                if currentarea.up[3] == "locked":
                    for char in currentparty:
                        if "key" in char.items:
                            while True:
                                print("Use key?")
                                print("1.) Yes.")
                                print("2.) No.")
                                option = input(">")
                                if option == "2":
                                    break
                                elif option == "1":
                                    print("{} used a key to open the door.".format(char.name))
                                    currentarea.up[3] = "normal"
                                    char.items.remove("key")
                                    movesuccess = True
                                    break
                                else:
                                    print("Please enter a valid selection.")
                else:
                    for char in currentparty:
                        for item in char.items:
                            for key in currentarea.up[5]:
                                if item == key:
                                    while True:
                                        print("Use {}?".format(key))
                                        print("1.) Yes.")
                                        print("2.) No.")
                                        option = input(">")
                                        if option == "2":
                                            break
                                        elif option == "1":
                                            print(currentarea.up[6])
                                            currentarea.up[3] = "normal"
                                            char.items.remove(key)
                                            movesuccess = True
                                            break
                                        else:
                                            print("Please enter a valid selection.")
            elif currentarea.up[3] == "normal":
                #print(currentarea.up[3])
                movesuccess = True
            
            if currentarea.up[0] != areas[0].name and movesuccess == True:
                #save current areaset to retain object permanence
                previousareaset = "temp" + areas[0].name
                saveareaset(previousareaset, areas, width, height, PlayerIG.currentposition)
                #load next area
                nextareaset = "temp" + areas[PlayerIG.currentposition].up[0]
                if path.exists(nextareaset + ".pkl"):
                    #print("Temp exists!")
                    #load saved instance of areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(nextareaset)
                    PlayerIG.currentposition = currentarea.up[1]
                else:
                    #print("Temp doesn't exist...")
                    #load original areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(areas[PlayerIG.currentposition].up[0])
                    PlayerIG.currentposition = currentarea.up[1]
            else:
                if movesuccess == True:
                    PlayerIG.currentposition = currentarea.up[1]
        else:
            print("There is no path in that direction.")
        start1()
    elif "go" and "down" in option:
        movesuccess = False
        if currentarea.down[1] != 0:
            if currentarea.down[3] != "normal":
                print("Can't go that way.")
                #print("Down: {} vs {}".format(currentarea.down[3], "normal"))
                print("Message: {}".format(currentarea.down[4]))
                if currentarea.down[3] == "locked":
                    for char in currentparty:
                        if "key" in char.items:
                            while True:
                                print("Use key?")
                                print("1.) Yes.")
                                print("2.) No.")
                                option = input(">")
                                if option == "2":
                                    break
                                elif option == "1":
                                    print("{} used a key to open the door.".format(char.name))
                                    currentarea.down[3] = "normal"
                                    char.items.remove("key")
                                    movesuccess = True
                                    break
                                else:
                                    print("Please enter a valid selection.")
                else:
                    for char in currentparty:
                        for item in char.items:
                            for key in currentarea.down[5]:
                                if item == key:
                                    while True:
                                        print("Use {}?".format(key))
                                        print("1.) Yes.")
                                        print("2.) No.")
                                        option = input(">")
                                        if option == "2":
                                            break
                                        elif option == "1":
                                            print(currentarea.down[6])
                                            currentarea.down[3] = "normal"
                                            char.items.remove(key)
                                            movesuccess = True
                                            break
                                        else:
                                            print("Please enter a valid selection.")
            elif currentarea.down[3] == "normal":
                #print(currentarea.down[3])
                movesuccess = True
            
            if currentarea.down[0] != areas[0].name and movesuccess == True:
                #save current areaset to retain object permanence
                previousareaset = "temp" + areas[0].name
                saveareaset(previousareaset, areas, width, height, PlayerIG.currentposition)
                #load next area
                nextareaset = "temp" + areas[PlayerIG.currentposition].down[0]
                if path.exists(nextareaset + ".pkl"):
                    #print("Temp exists!")
                    #load saved instance of areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(nextareaset)
                    PlayerIG.currentposition = currentarea.down[1]
                else:
                    #print("Temp doesn't exist...")
                    #load original areaset
                    areas, width, height, PlayerIG.currentposition = loadareaset(areas[PlayerIG.currentposition].down[0])
                    PlayerIG.currentposition = currentarea.down[1]
            else:
                if movesuccess == True:
                    PlayerIG.currentposition = currentarea.down[1]
        else:
            print("There is no path in that direction.")
        start1()
    else:
        start1()

def checkpreconditions(preconditionset, currentevent, currentarea, areas):
    preconditionsetstatus = True
    global PlayerIG
    for precondition in currentevent.preconditions[preconditionset]:
        if precondition.type == "none":
            pass
            #runevent(preconditionset, currentevent, currentarea, areas)
        elif precondition.type == "item":
            preconditionsetstatus = False
            for player in currentparty:
                if precondition.detail in player.items:
                    preconditionsetstatus = True
        elif precondition.type[0] == "switch":
            #global switches
            if precondition.type[1] == "global":
                pass
            #areaset switches
            elif precondition.type[1] == "areaset":
                booleanresult = False
                if precondition.detail == "True":
                    booleanresult = True
                else:
                    booleanresult = False
                if booleanresult != areas[0].switches[precondition.name]:
                    preconditionsetstatus = False
                    #print(precondition.name)
                    #print("{} == {}".format(precondition.detail, areas[0].switches[precondition.name]))
                    #print("False!")
                else:
                    #print(precondition.name)
                    #print("{} == {}".format(precondition.detail, areas[0].switches[precondition.name]))
                    #print("True!")
                    pass
            #local area switches
            elif precondition.type[1] == "local" or precondition.type[1] == "local area":
                #print("local area switch found!")
                booleanresult = False
                if precondition.detail == "True":
                    booleanresult = True
                else:
                    booleanresult = False
                if booleanresult != currentarea.switches[precondition.name]:
                    preconditionsetstatus = False
                    #print(precondition.name)
                    #print("{} == {}".format(precondition.detail, currentarea.switches[precondition.name]))
                    #print("False!")
                else:
                    #print(precondition.name)
                    #print("{} == {}".format(precondition.detail, currentarea.switches[precondition.name]))
                    #print("True!")
                    pass
                #runevent(preconditionset, currentevent, currentarea, areas)
        elif precondition.type[0] == "variable":
            pass
        elif precondition.type == "gold":
            goldvalue = precondition.value
            print("gold is {}".format(goldvalue))
            if precondition.detail == "atleast":
                if PlayerIG.gold < goldvalue:
                    #print("{} < {}".format(PlayerIG.gold, goldvalue))
                    preconditionsetstatus = False
                    #print("False!")
            elif precondition.detail == "lessthan":
                if PlayerIG.gold >= goldvalue:
                    #print("{} >= {}".format(PlayerIG.gold, goldvalue))
                    preconditionsetstatus = False
                    #print("False!")
            elif precondition.detail == "exactly":
                if PlayerIG.gold != goldvalue:
                    #print("{} == {}".format(PlayerIG.gold, goldvalue))
                    preconditionsetstatus = False
                    #print("False!")
        elif precondition.type == "partysize":
            partysize = precondition.value
            if precondition.detail == "atleast":
                if len(currentparty) < partysize:
                    preconditionsetstatus = False
            elif precondition.detail == "lessthan":
                if len(currentparty) >= partysize:
                    preconditionsetstatus = False
            elif precondition.detail == "exactly":
                if len(currentparty) != partysize:
                    preconditionsetstatus = False
        else:
            break
    if preconditionsetstatus == True:
        if preconditionset != "none":
            #print("Run event!")
            runevent(preconditionset, currentevent, currentarea, areas)
    

def runevent(command, event, area, areaset):
    #print("{} to {}".format(command, event.name))
    #if command == "text"
    #if event.event[
    success = True
    #print(event.event[command])
    for actiongroup in event.event[command]:
        for action in actiongroup:
            if success == True:
                if action == "success":
                    if actiongroup[4] == False:
                        success = False
                    else:
                        success = True
                if action == "nothing":
                    pass
                elif action == "text":
                    print(actiongroup[1])
                    option = input("Please press enter to continue.")
                elif action == "itemgive":
                    item = actiongroup[1]
                    message = actiongroup[2]
                    print(message)
                    choice = input(">")
                    if choice == item:
                        itemlist = []
                        for char in currentparty:
                            if item in char.items:
                                itemlist.append(item)
                        if itemlist:
                            for char in currentparty:
                                if item in char.items:
                                    char.items.remove(item)
                                    if item == "potion":
                                        PlayerIG.potions -= 1
                                    print("{} gave {} to {}.".format(char.name, item, event.name))
                                    option = input("Please press enter to continue.")
                                    break
                        else:
                            print("You do not have {}.".format(item))
                            option = input("Please press enter to continue.")
                            success = False
                            break
                    else:
                        print("{} does not accept {}.".format(event.name, choice))
                        success = False
                        break
                elif action == "itemtake":
                    item = actiongroup[1]
                    message = actiongroup[2]
                    itemlist = []
                    for char in currentparty:
                        if item in char.items:
                            itemlist.append(item)
                    if itemlist:
                        for char in currentparty:
                            if item in char.items:
                                char.items.remove(item)
                                print(message)
                                if item == "potion":
                                    PlayerIG.potions -= 1
                                break
                elif action == "itemget":
                    item = actiongroup[1]
                    PlayerIG.items.append(item)
                elif action == "goldexchange":
                    PlayerIG.gold += actiongroup[1]
                    if actiongroup[1] > 0:
                        print("You received {} gold!".format(actiongroup[1]))
                    else:
                        print("You lost {} gold!".format(actiongroup[1]))
                elif action == "switch":
                    if actiongroup[1] == "global":
                        pass
                    elif actiongroup[1] == "areaset":
                        if actiongroup[3] == "True":
                            areaset[0].switches[actiongroup[2]] = True
                            #print("Switch {} set to True.".format(actiongroup[2]))
                        elif actiongroup[3] == "False":
                            areaset[0].switches[actiongroup[2]] = False
                            #print("Switch {} set to False.".format(actiongroup[2]))
                        elif actiongroup[3] == "toggle":
                            if areaset[0].switches[actiongroup[2]] == True:
                                areaset[0].switches[actiongroup[2]] = False
                                #print("Switch {} set to False.".format(actiongroup[2]))
                            else:
                                areaset[0].switches[actiongroup[2]] = True
                                #print("Switch {} set to True.".format(actiongroup[2]))
                    elif actiongroup[1] == "local":
                        if actiongroup[3] == "True":
                            area.switches[actiongroup[2]] = True
                            #print("Switch {} set to True.".format(actiongroup[2]))
                        elif actiongroup[3] == "False":
                            area.switches[actiongroup[2]] = False
                            #print("Switch {} set to False.".format(actiongroup[2]))
                        elif actiongroup[3] == "toggle":
                            if area.switches[actiongroup[2]] == True:
                                area.switches[actiongroup[2]] = False
                                #print("Switch {} set to False.".format(actiongroup[2]))
                            else:
                                area.switches[actiongroup[2]] = True
                                #print("Switch {} set to True.".format(actiongroup[2]))
                elif action == "variable":
                    if actiongroup[1] == "global":
                        pass
                    elif actiongroup[1] == "areaset":
                        pass
                    elif actiongroup[1] == "local":
                        pass
                elif action == "hidden":
                    if actiongroup[1] == "hide":
                        event.hidden = True
                    elif actiongroup[1] == "unhide":
                        event.hidden = False
                    elif actiongroup[1] == "toggle":
                        if event.hidden == True:
                            event.hidden = False
                        else:
                            event.hidden = True
                elif action == "direction":
                    #"direction", direction, areaflag, newsreaset, destinationflag, destination, status, statusmessage
                    #Update direction code to implement items to resolve statuses.
                    #Position 0 is the areaset name
                    #Position 1 is the destination ID
                    #Position 2 is the message for how the path appears
                    #Position 3 is the status
                    #Position 4 is the status message
                    #Position 5 is the item that resolves the status. This will be an array in case multiple items resolve it.
                    #Position 6 is the resolution message
                    direction = actiongroup[1]
                    areaflag = actiongroup[2]
                    newareaset = actiongroup[3]
                    destinationflag = actiongroup[4]
                    destination = actiongroup[5]
                    appearance = actiongroup[6]
                    status = actiongroup[7]
                    statusmessage = actiongroup[8]
                    itemflag = actiongroup[9]
                    item = actiongroup[10]
                    resolution = actiongroup[11]
                    
                    if areaflag == "current":
                        newareaset = areaset[0].name
                    if direction == "north":
                        if areaflag != "same":
                            area.north[0] = newareaset
                        if destinationflag != "same":
                            area.north[1] = destination
                        if appearance != "same":
                            area.north[2] = appearance
                        if status != "same":
                            area.north[3] = status
                        if statusmessage != "same":
                            area.north[4] = statusmessage
                        if item != "same":
                            area.north[5] = item
                        if resolution != "same":
                            area.north[6] = resolution
                    elif direction == "south":
                        if areaflag != "same":
                            area.south[0] = newareaset
                        if destinationflag != "same":
                            area.south[1] = destination
                        if status != "same":
                            area.south[3] = status
                        if statusmessage != "same":
                            area.south[4] = statusmessage
                    elif direction == "east":
                        if areaflag != "same":
                            area.east[0] = newareaset
                        if destinationflag != "same":
                            area.east[1] = destination
                        if appearance != "same":
                            area.east[2] = appearance
                        if status != "same":
                            area.east[3] = status
                        if statusmessage != "same":
                            area.east[4] = statusmessage
                        if itemflag != "same":
                            area.east[5] = item
                        if resolution != "same":
                            area.east[6] = resolution
                    elif direction == "west":
                        if areaflag != "same":
                            area.west[0] = newareaset
                        if destinationflag != "same":
                            area.west[1] = destination
                        if status != "same":
                            area.west[3] = status
                        if statusmessage != "same":
                            area.west[4] = statusmessage
                    elif direction == "up":
                        if areaflag != "same":
                            area.up[0] = newareaset
                        if destinationflag != "same":
                            area.up[1] = destination
                        if status != "same":
                            area.up[3] = status
                        if statusmessage != "same":
                            area.up[4] = statusmessage
                    elif direction == "down":
                        if areaflag != "same":
                            area.down[0] = newareaset
                        if destinationflag != "same":
                            area.down[1] = destination
                        if status != "same":
                            area.down[3] = status
                        if statusmessage != "same":
                            area.down[4] = statusmessage                  
                    else:
                        pass
                elif action == "party":
                    operation = actiongroup[1]
                    charname = actiongroup[2]
                    charclass = actiongroup[3]
                    if operation == "addnew":
                        newchar2(charname, charclass)
                        print("{} joined the party!".format(charname))
                    elif operation == "addexisting":
                        for char in outofparty:
                            if char.name == charname:
                                currentparty.append(char)
                                outofparty.remove(char)
                                print("{} added to the party.".format(charname))
                    elif operation == "remove":
                        for char in currentparty:
                            if char.name == charname:
                                outofparty.append(char)
                                currentparty.remove(char)
                                print("{} removed from the party.".format(charname))
                elif action == "combat":
                    print(actiongroup)
                    enemylist = actiongroup[1]
                    scriptedbattle = actiongroup[2]
                    runfrombattle = actiongroup[3]
                    lossactionenabled = actiongroup[4]
                    battlescripts = actiongroup[5]
                    GameDataIG.scriptedbattles = [scriptedbattle, runfrombattle, lossactionenabled]
                    GameDataIG.battlescripts = battlescripts
                    prefightspecial(enemylist)
                elif action == "deleteevent":
                    print("Delete event")
                    eventselection = actiongroup[1]
                    for event in area.events:
                        if eventselection == event:
                            #print("{} removed.".format(event.name))
                            area.events.remove(event)
                elif action == "deletecommand":
                    eventname = actiongroup[1]
                    commandname = actiongroup[2]
                    for event in area.events:
                        if eventname == event.name:
                            for command in event.commands:
                                if commandname == command:
                                    #print("{} removed from {}.".format(commandname, eventname))
                                    event.commands.remove(commandname)
                elif action == "gameover":
                    messageflag = actiongroup[1]
                    messagelist = actiongroup[2]
                    gameover(messageflag, messagelist)
                elif action == "restoreparty":
                    restoretype = actiongroup[1]
                    print("restoreparty")
                    if restoretype == "full":
                        for char in currentparty:
                            #print(char.name)
                            char.hp = char.mHP
                            char.mp = char.mMP
                        print("Party restored!")
                    if restoretype == "1hp":
                        for char in currentparty:
                            #print(char.name)
                            char.hp = 1
                    if restoretype == "firstonly":
                        currentparty[0].hp = currentparty[0].mHP
                #template for new actions
                elif action == "newaction":
                    pass
                else:
                    #Catch any other input
                    pass
            else:
                break
    
    

def status():
    print("********")
    showmap(width, height, PlayerIG.currentposition)
    print("********")
    print("Gold: %i" % PlayerIG.gold)
    print("Potions: %i\n" % PlayerIG.potions)
    for char in currentparty:
        print("********")
        print("Name: %s" % char.name)
        print("Id: {}".format(char.idno))
        print("Level: %i" % char.level)
        print("Class: %s" % char.charclass)
        print("Health: %i/%i" % (char.hp, char.mHP))
        print("MP: %i/%i\n" % (char.mp, char.mMP))
        print("Attack: %i" % char.attack)
        print("Defense: %i" % char.defense)
        print("Wisdom: %i" % char.wisdom)
        print("Magic resistance: %i" % char.resistance)
        print("Agility: %i" % char.agility)
        print("Luck: %i" % char.luck)
        print("Exp: %i/%i Next: %i" % (char.exp, nextlevel(char.level+1),(char.nextlevel - char.exp)))
        print("Current Weapon: %s" % char.curweapon)
        print("Current Armor: %s" % char.curarmor)
        print("Current Acc: %s" % char.curacc)
        print("********")
        option = input(" ")
    start1()

def showmap(areawidth, areaheight, currentposition):
    global width
    global height
    width = areawidth
    height = areaheight
    PlayerIG.currentposition = currentposition
    print("Map:",end="")
    #get column
    column = PlayerIG.currentposition % width
    #get row
    row = int(PlayerIG.currentposition / width)
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
        #print("[-----]")
        print("[" + "".join("{}".format("-") for k in range(width)) + "]")
        count -= 1
    #print location
    if column == 0:
        print("[" + "".join("{}".format("-") for k in range(width-1)) + "*" + "]")
    else:
        before = column % width - 1
        after = width - before - 1
        print("[" + "".join("{}".format("-") for i in range(before)) + "*" + "".join("{}".format("-") for k in range(after)) + "]")
    #print rows after current location
    count = height - 1 - row
    while count > 0:
        print("[" + "".join("{}".format("-") for k in range(width)) + "]")
        count -= 1

def showmap2(areawidth, areaheight, currentposition):
    global width
    global height
    global areas
    width = areawidth
    height = areaheight
    product = width * height
    PlayerIG.currentposition = currentposition
    print("Map:",end="")
    #get column
    column = PlayerIG.currentposition % width
    #get row
    row = int(PlayerIG.currentposition / width)
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
        #print("[-----]")
        print("[" + "".join("{}".format("-") for k in range(width)) + "]")
        count -= 1
    #print location
    if column == 0:
        print("[" + "".join("{}".format("-") for k in range(width-1)) + "*" + "]")
    else:
        before = column % width - 1
        after = width - before - 1
        print("[" + "".join("{}".format("-") for i in range(before)) + "*" + "".join("{}".format("-") for k in range(after)) + "]")
    #print rows after current location
    count = height - 1 - row
    while count > 0:
        print("[" + "".join("{}".format("-") for k in range(width)) + "]")
        count -= 1


    
def savegame():
    os.system("cls")
    global filename
    #save current areaset as temp version to retain object permanence
    filename = areas[0].name
    tempareaname = "temp" + filename
    saveareaset(tempareaname, areas, width, height, PlayerIG.currentposition)
    with open("savefile", "wb") as f:
        #pickle.dump(PlayerIG, f)
        pickle.dump(currentparty, f)
        pickle.dump(filename, f)
        print("********")
        print("\nGame has been saved!\n")
        print("********")
    option = input(" ")
    start1()

def loadgame():
    if os.path.exists("savefile") == True:
        os.system("cls")
        global filename
        with open("Savefile", "rb") as f:
            global PlayerIG
            global currentparty
            #PlayerIG = pickle.load(f)
            currentparty = pickle.load(f)
            filename = pickle.load(f)
        PlayerIG = currentparty[0]
                
        #print("Please enter the filename of the areaset you would like to load.")
        #filename = input(">")
        global areas
        global width
        global height
        #position here is not used because the area loads the start position but the game data save contains the saved location
        tempfilename = "temp" + filename
        if os.path.exists(tempfilename + ".pkl") == True:
            #print("temp exists")
            areas, width, height, position = loadareaset(tempfilename)
            print("********")
            print("Save has been loaded...")
            print("********")
            start1()
            option = input(" ")
        else:
            if os.path.exists(filename + ".pkl") == True:
                #Fall back to loading the original copy of the area if the temp version got deleted.
                areas, width, height, position = loadareaset(filename)
                print("********")
                print("Save has been loaded...")
                print("********")
                start1()
                option = input(" ")
            else:
                #Print("Failed...")
                pass
            
    else:
        print("********")
        print("You have no save file for this game.")
        print("********")
        option =  input(" ")
        main()

def saveareaset(filename, areaset, areawidth, areaheight, currentposition):
    #print(filename)
    #print(areaset)
    #create filename string
    newareas = str(filename) + ".pkl"
    fi = open(newareas, "bw")
    pickle.dump(areaset,fi)
    pickle.dump(areawidth, fi)
    pickle.dump(areaheight, fi)
    pickle.dump(currentposition, fi)
    fi.close()
    #print("Areas saved!")

def loadareaset(filename):
    #create filename string
    newareas = str(filename) + ".pkl"
    #print("Areas: ")
    #print(newareas)
    try:
        fi = open(newareas, "rb")
    except IOError:
        print("Can't load", newareas)
    else:
        tempareas = pickle.load(fi)
        width = pickle.load(fi)
        height = pickle.load(fi)
        position = pickle.load(fi)
        #print("New areas loaded successfully!")
        return  tempareas, width, height, position

def displayclass():
    os.system("cls")
    for char in currentparty:
        print("Name: %s" % char.name)
        print("Class: %s" % char.charclass)
        print("HP Growth: %s" % char.hpgrowth)
        print("MP Growth: %s" % char.mpgrowth)
        print("Attack Growth: %s" % char.attackgrowth)
        print("Defense Growth: %s" % char.defensegrowth)
        print("Wisdom Growth: %s" % char.wisdomgrowth)
        print("Magic Resistance Growth: %s" % char.resistancegrowth)
        print("Agility Growth: %s" % char.agilitygrowth)
        print("Luck Growth: %s" % char.luckgrowth)
        option = input(" ")
    start1()

def displayhp(char):
    name = char.name
    hp = char.hp
    mHP = char.mHP
    temp = round(hp/mHP*10)
    diff = 10 - temp
    print("%s:" % char.name)
    print("HP: {} [".format(hp), end="")
    while temp > 0:
        print("=", end="")
        temp -= 1
    while diff > 0:
        print(" ", end="")
        diff -= 1
    print("]")

def displaymp(char):
    #name = char.name
    mp = char.mp
    mMP = char.mMP
    if mMP > 0:
        temp = round(mp/mMP*10)
        diff = 10 - temp
        #print("%s:" % char.name)
        print("MP: {} [".format(mp), end="")
        while temp > 0:
            print("=", end="")
            temp -= 1
        while diff > 0:
            print(" ", end="")
            diff -= 1
        print("]")
    else:
        pass

def round(n):
    if n < 0:
        return math.ceil(n - 0.5)
    else:
        return math.floor(n + 0.5)

def nextleveld(level):
    return 500 * (level ^ 2) - (500 * level)

def nextlevelp(level):
    return round((4* (level ^ 3)) / 5)

def nextlevelg(level):
    return round(0.04 * (level ** 3) + 0.8 * (level ** 2) + 2 * level)

def nextlevelold(level):
    exponent = 1.3
    baseXP = 10
    return math.floor(baseXP * (level ** exponent))

def nextlevel(level):
    exponent = 1.3
    baseXP = 10
    constant = 1
    return math.floor(baseXP * (exponent ** level) + constant) + math.floor(baseXP * (exponent ** (level - 1) + constant))

#experience for next level
#for n in range(100):
#    print(nextlevel(n))

#print("\n\n")


#Difference between levels
#for n in range(1,100):
#    print(nextlevel(n)-nextlevel(n-1))

def inn():
    os.system("cls")
    #update to take in a price value to have more expensive inns later
    cost = 10 * len(currentparty)
    print("Welcome to the inn!")
    print("It's only %i gold to rest." % cost)
    print("1.) Rest")
    print("b.) go back")
    option = input(">")
    if option == "1":
        if PlayerIG.gold <cost:
            print("You don't have enough gold...")
            option = input(" ")
            inn()
        else:
            PlayerIG.gold -= cost
            rest()
    elif option == "b" or "back":
        start1()

def rest():
    os.system("cls")
    print("You feel refeshed!")
    print("HP and MP restored!\n")
    for char in currentparty:
        char.hp = char.mHP
        char.mp = char.mMP
    start1()

def inventory():
    os.system("cls")
    print("What do you want to do?")
    print("1.) Equip")
    print("2.) View items")
    print("b.) go back")
    option = input(">")
    if option == "1":
        equip()
    elif option == "2":
        viewitems()
    elif option == "b" or option == "back":
        start1()

def viewitems():
    os.system("cls")
    print("Please select a party member.")
    for char in currentparty:
        print(char.name)
    option = input(">")
    for char in currentparty:
        if option == char.name:
            currentplayer = char
            viewitems1(currentplayer)
    print("Please specify a valid party member.")
    viewitems()

def viewitems1(player):
    os.system("cls")
    currentplayer = player
    for item in currentplayer.items:
        print(item)
    print("1.) Use")
    print("2.) Drop")
    print("b.) go back")
    option = input(">")
    if option == "1":
        print("To be implemented later.")
        inventory()
    elif option == "2":
        print("Drop which item?")
        for item in currentplayer.items:
            print(item)
        print("b.) Back")
        option = input(">")
        if option in currentplayer.items:
            currentplayer.items.remove(option)
            areas[PlayerIG.currentposition].items.append(option)
            print("{} has been dropped.".format(option))
            viewitems1(currentplayer)
        elif option == "b" or option == "back":
            inventory()
        else:
            print("{} does not have {} to drop.".format(currentplayer.name, option))
            viewitems1(currentplayer)
    elif option == "b" or option == "back":
        inventory()
    else:
        print("Please enter a valid selection.")
        viewitems1(currentplayer)

def equip():
    os.system("cls")
    print("Equip who?")
    for char in currentparty:
        print(char.name)
    option = input(">")

    for char in currentparty:
        if option == char.name:
            currentplayer = char
            equip1(currentplayer)
    print("Please specify a valid party member.")
    equip()

def equip1(player):
    os.system("cls")
    currentplayer = player
    print("What do you want to equip for %s?" % currentplayer.name)
    for weapon in currentplayer.weapon:
        print(weapon)
    for armor in currentplayer.armor:
        print(armor)
    for acc in currentplayer.acc:
        print(acc)
    print("b.) go back")
    option = input(">")
    if option == "b" or option == "back":
        inventory()
    elif option == currentplayer.curweapon:
        print(currentplayer.curweapon)
        print("You already have that weapon equipped.")
        option = input(" ")
        equip1(currentplayer)
    elif option in currentplayer.weapon:
        if currentplayer.curweapon == "None":
            currentplayer.curweapon = option
        else:
            currentplayer.weapon.append(currentplayer.curweapon)
            currentplayer.curweapon = option
        currentplayer.weapon.remove(option)
        print("You have equipped %s." % option)
        option = input(" ")
        equip1(currentplayer)
    elif option == currentplayer.curarmor:
        print(currentplayer.curarmor)
        print("You already have that armor equipped.")
        option = input(" ")
        equip1(currentplayer)
    elif option in currentplayer.armor:
        if currentplayer.curarmor == "None":
            currentplayer.curarmor = option
        else:
            currentplayer.armor.append(currentplayer.curarmor)
            currentplayer.curarmor = option
        currentplayer.armor.remove(option)
        print("You have equipped %s." % option)
        option = input(" ")
        equip1(currentplayer)
    elif option == currentplayer.curacc:
        print(currentplayer.curacc)
        print("You already have that accessory equipped.")
        option = input(" ")
        equip1(currentplayer)
    elif option in currentplayer.acc:
        if currentplayer.curacc == "None":
            currentplayer.curacc = option
        else:
            currentplayer.acc.append(currentplayer.curacc)
            currentplayer.curacc = option
        currentplayer.acc.remove(option)
        print("You have equipped %s." % option)
        option = input(" ")
        equip1(currentplayer)
    else:
        print("You don't have %s in your inventory." % option)
        equip1(currentplayer)

def setenemyparty():
    #reset enemy counts
    for monster in enemies:
        enemies[monster]["count"] = 0
    #establish average level of party
    leveltotal = 0
    for char in currentparty:
        leveltotal += char.level
    averagelevel = int(leveltotal/len(currentparty))
    #set enemy party length
    maxenemyparty = int(2 + (averagelevel/5))
    if maxenemyparty >= 26:
        maxenemyparty = 26
    #set enemy party count
    enemycount = random.randint(1, maxenemyparty)
    print("Avg: %i" % averagelevel)
    print("Max: %i" % maxenemyparty)
    tempenemyparty = []
    for n in range(enemycount):
        tempenemyparty.append(getenemy())
    addenemy(tempenemyparty, False)

def setenemypartyspecial(enemylist):
    tempenemyparty = []
    #reset enemy counts
    for monster in bosses:
        bosses[monster]["count"] = 0
        for enemy in enemylist:
            if bosses[monster]["name"].lower() == enemy.lower():
                tempenemyparty.append(capnames(enemy))
    for monster in enemies:
        enemies[monster]["count"] = 0
        for enemy in enemylist:
            if enemies[monster]["name"].lower() == enemy.lower():
                tempenemyparty.append(capnames(enemy))
    addenemy(tempenemyparty, False)

def addenemy(tempenemies, newflag):
    tempenemyparty = tempenemies
    for monster in tempenemyparty:
        if monster == "Goblin":
            GoblinIGA = Goblin("Goblin %s" % alphabet[enemies[1]["count"]])
            enemies[1]["count"] += 1
            if newflag == False:
                enemyparty.append(GoblinIGA)
                battlemembers.append(GoblinIGA)
            else:
                newlyaddedbattlemembers.append(GoblinIGA)
        if monster == "Zombie":
            ZombieIGA = Zombie("Zombie %s" % alphabet[enemies[2]["count"]])
            enemies[2]["count"] += 1
            if newflag == False:
                enemyparty.append(ZombieIGA)
                battlemembers.append(ZombieIGA)
            else:
                newlyaddedbattlemembers.append(ZombieIGA)
        if monster == "Fast Zombie":
            FastZombieIGA = FastZombie("Fast Zombie %s" % alphabet[enemies[3]["count"]])
            enemies[3]["count"] += 1
            if newflag == False:
                enemyparty.append(FastZombieIGA)
                battlemembers.append(FastZombieIGA)
            else:
                newlyaddedbattlemembers.append(FastZombieIGA)
        if monster == "Imp":
            ImpIGA = Imp("Imp %s" % alphabet[enemies[4]["count"]])
            enemies[4]["count"] += 1
            if newflag == False:
                enemyparty.append(ImpIGA)
                battlemembers.append(ImpIGA)
            else:
                newlyaddedbattlemembers.append(ImpIGA)
        if monster == "Magic Goblin":
            MagicGoblinIGA = MagicGoblin("Magic Goblin %s" % alphabet[enemies[5]["count"]])
            enemies[5]["count"] += 1
            if newflag == False:
                enemyparty.append(MagicGoblinIGA)
                battlemembers.append(MagicGoblinIGA)
            else:
                newlyaddedbattlemembers.append(MagicGoblinIGA)
        if monster == "Big Blob":
            BigBlobIGA = BigBlob("Big Blob %s" % alphabet[enemies[6]["count"]])
            enemies[6]["count"] += 1
            if newflag == False:
                enemyparty.append(BigBlobIGA)
                battlemembers.append(BigBlobIGA)
            else:
                newlyaddedbattlemembers.append(BigBlobIGA)
        if monster == "Blob":
            BlobIGA = Blob("Blob %s" % alphabet[enemies[7]["count"]])
            enemies[7]["count"] += 1
            if newflag == False:
                enemyparty.append(BlobIGA)
                battlemembers.append(BlobIGA)
            else:
                newlyaddedbattlemembers.append(BlobIGA)
        if monster == "Boss Blob":
            BossBlobIGA = BossBlob("Boss Blob %s" % alphabet[bosses[1]["count"]])
            bosses[1]["count"] += 1
            if newflag == False:
                enemyparty.append(BossBlobIGA)
                battlemembers.append(BossBlobIGA)
            else:
                newlyaddedbattlemembers.append(BossBlobIGA)
    #Add the new enemies to the enemyparty and battlemembers
    for monster in newlyaddedbattlemembers:
        enemyparty.append(monster)
        battlemembers.append(monster)
        #if these are new enemies add a battle action of nothing.
        if newflag == True:
            BattleActionA = BattleActionClass(monster.name)
            BattleActionA.chartype = monster.chartype
            BattleActionA.action = "nothing"
            BattleActionA.target = 0
            battleactionqueue.append(BattleActionA)
    newlyaddedbattlemembers.clear()
  

def getenemy():
    #TODO set cap based on average level of which enemies can be ecountered.
    index = random.randint(1, len(enemies))
    enemyname = enemies[index]["name"]
    return enemyname

def capnames(string):
    return " ".join(word.capitalize() for word in string.split())

def setenemypartyold():
    #establish enemy party
    global enemy
    enemynum = random.randint(1, 100)
    #print(enemynum)
    if enemynum <= 20:
        #enemy = GoblinIG
        GoblinIGA = Goblin("Goblin A")
        enemyparty.append(GoblinIGA)
    elif enemynum > 20 and enemynum <= 30:
        #enemy = GoblinIG
        GoblinIGA = Goblin("Goblin A")
        GoblinIGB = Goblin("Goblin B")
        enemyparty.append(GoblinIGA)
        enemyparty.append(GoblinIGB)
    elif enemynum > 30 and enemynum <= 40:
        #enemy = ZombieIG
        ZombieIGA = Zombie("Zombie A")
        enemyparty.append(ZombieIGA)
    elif enemynum > 40 and enemynum <= 50:
        #enemy = ZombieIG
        ZombieIGA = Zombie("Zombie A")
        ZombieIGB = Zombie("Zombie B")
        enemyparty.append(ZombieIGA)
        enemyparty.append(ZombieIGB)
    elif enemynum > 50 and enemynum <= 70:
        enemy = ImpIG
        enemyparty.append(ImpIG)
    elif enemynum > 70 and enemynum <= 90:
        GoblinIGA = Goblin("Goblin A")
        FastZombieIGA = FastZombie("Fast Zombie A")
        enemyparty.append(GoblinIGA)
        enemyparty.append(FastZombieIGA)
    else:
        enemy = MagicGoblinIG
        enemyparty.append(MagicGoblinIG)

def prefight():
    global enemy
    global battleturncounter
    #establish battle participants
    battlemembers.clear()
    sortedbattlemembers.clear()
    battlepartymembers.clear()
    battleactionqueue.clear()
    battleturncounter = 0
    
    setenemyparty()
    #setenemyparty2()

    #sort enemyparty:
    enemyparty.sort(key=lambda x: x.agility, reverse=True)
    for char in currentparty:
        if char.hp > 0:
            battlemembers.append(char)
            battlepartymembers.append(char)
    #for monster in enemyparty:
    #    battlemembers.append(monster)
    #Show battle participants
    os.system("cls")
    for char in battlepartymembers:
        print("%s" % char.name)
    print("vs")
    for monster in enemyparty:
        print("%s" % monster.name)
    print("\nPotions: %i\n" % PlayerIG.potions)
    print("1.) Fight")
    print("2.) Run")
    option = input(">")
    if option == "2":
        runsuccess = run()
        if runsuccess:
            start1()
        else:
            fight()
    else:
        fight()

def prefightspecial(enemylist):
    global enemy
    global battleturncounter
    #establish battle participants
    battlemembers.clear()
    sortedbattlemembers.clear()
    battlepartymembers.clear()
    battleactionqueue.clear()
    battleturncounter = 0
    
    #set enemy party
    setenemypartyspecial(enemylist)

    #sort enemyparty:
    enemyparty.sort(key=lambda x: x.agility, reverse=True)
    for char in currentparty:
        if char.hp > 0:
            battlemembers.append(char)
            battlepartymembers.append(char)
    #for monster in enemyparty:
    #    battlemembers.append(monster)
    #Show battle participants
    os.system("cls")
    for char in battlepartymembers:
        print("%s" % char.name)
    print("vs")
    for monster in enemyparty:
        print("%s" % monster.name)
    fight()

def fight():
    os.system("cls")
    global battleturncounter
    battleturncounter += 1
    print("********")
    for char in battlepartymembers:
        displayhp(char)
        displaymp(char)
    for monster in enemyparty:
        displayhp(monster)
        displaymp(monster)
    print("\nPotions: %i" % PlayerIG.potions)
    print("********")
    print("\n**** Turn {} ****\n".format(battleturncounter))
    #sort battle participants by agility for turn order
    battlemembers.sort(key=lambda x: x.agility, reverse=True)

    #check if this is a scripted battle
    if GameDataIG.scriptedbattles[0] == True:
        #check preconditions
        #print("scripted battle")
        #print(GameDataIG.battlescripts)
        for script in GameDataIG.battlescripts:
            #print(script)
            for precondition in script.preconditions:
                #print(precondition)
                if precondition == "turn count":
                    #print("turn count")
                    for precond in script.preconditions[precondition]:
                        if battleturncounter == precond.value:
                            runevent(precondition, script, PlayerIG.currentposition, areas)
                if precondition == "loss":
                    GameDataIG.scriptedbattles[2] = True
   
    #determine actions for each party member
    for char in battlemembers:
        if char.chartype == "enemy":
            BattleActionA = BattleActionClass(char.name)
            BattleActionA.chartype = char.chartype
            #print("Battle Class: %s" % BattleActionA.name)
            enemyaction = enemyactionselector(char)
            BattleActionA.action = enemyaction
            #print("Battle Action: %s" % BattleActionA.action)
            #battleactionqueue.append(enemyaction)
            enemytarget = getplayertargetforenemy()
            BattleActionA.target = enemytarget
            #print("Battle Target: %s" % BattleActionA.target)
            #print(battlepartymembers[BattleActionA.target].name)
            #pause = input(" ")

            battleactionqueue.append(BattleActionA)
            
            #print("********")
            #print("%s's turn!" % BattleActionA.name)
            #print("Added enemy: %s" % BattleActionA.name)
            #print("Action: %s" % BattleActionA.action)
            #print("Target: %s: %s" % (BattleActionA.target, battlepartymembers[BattleActionA.target].name))
        else:
            BattleActionA = BattleActionClass(char.name)
            BattleActionA.chartype = char.chartype
            BattleActionA.charclass = char.charclass
            print("********")
            print("%s's turn!" % BattleActionA.name)
            print("Class: %s" % BattleActionA.charclass)
            print("1.) Attack")
            print("2.) Magic")
            print("3.) Drink Potion")
            if GameDataIG.scriptedbattles[1] == True:
                print("4.) Run")
            while True:
                option = input(">")
                try:
                    option = int(option)

                    try:
                        if option == 2:
                            #check player mp
                            if char.mp <= 0:
                                raise
                    except:
                        print("You are out of MP!\n")
                        print("Changing to physical attack!")
                        option = 1
                    if GameDataIG.scriptedbattles[1] == True:
                        if option < 1 or option > 4:
                            print("Bad number")
                            raise# print("Please enter a valid selection.")
                        else:
                            break
                    elif GameDataIG.scriptedbattles[1] == False:
                        if option < 1 or option > 3:
                            print("Bad number")
                            raise# print("Please enter a valid selection.")
                        else:
                            break
                except:
                    print("Please enter a valid selection.")
                    print("\n")
                    print("%s's turn!" % BattleActionA.name)
                    print("Class: %s" % BattleActionA.charclass)
                    print("1.) Attack")
                    print("2.) Magic")
                    print("3.) Drink Potion")
                    if GameDataIG.scriptedbattles[1] == True:
                        print("4.) Run")
            #if option > 0 and option <= 4:
            #print(option)
            if option == 1:
                #attack("physical")
                playeraction = "physical"
                #battleactionqueue.append(playeraction)
                target = getenemytarget()
                
                
                #print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                #print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                #print("Battle Target: %s" % BattleActionA.target)
                #print(enemyparty[BattleActionA.target].name)
                #pause = input(" ")

                battleactionqueue.append(BattleActionA)
                
                #print("Added character: %s" % BattleActionA.name)
                #print("Action: %s" % BattleActionA.action)
                #print("Target: %s" % BattleActionA.target)
                #print(enemyparty[BattleActionA.target].name)
            elif option == 2:
                playeraction = "magic"

                target = getenemytarget()

                BattleActionA = BattleActionClass(char.name)
                #print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                #print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                #print("Battle Target: %s" % BattleActionA.target)
                #print(enemyparty[BattleActionA.target].name)
                #pause = input(" ")

                battleactionqueue.append(BattleActionA)
                
                #print("Added character: %s" % char.name)
                #print("Action: %s" % playeraction)
                #print("Target: %s" % target)
                #print(enemyparty[target].name)
            elif option == 3:
                playeraction = "drink"
                
                target = getplayertarget()


                BattleActionA = BattleActionClass(char.name)
                #print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                #print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                #print("Battle Target index: %s" % BattleActionA.target)
                #print(enemyparty[BattleActionA.target].name)
                #pause = input(" ")

                battleactionqueue.append(BattleActionA)
                
                #print("Added character: %s" % char.name)
                #print("Action: %s" % playeraction)
                #print("Target: %s" % target)
                #print(currentparty[target].name)
            elif option == 4 and GameDataIG.scriptedbattles[1] == True:
                playeraction = "run"

                target = 0

                BattleActionA = BattleActionClass(char.name)
                #print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                #print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                #print("Battle Target index: %s" % BattleActionA.target)
                #print(enemyparty[BattleActionA.target].name)
                #pause = input(" ")

                battleactionqueue.append(BattleActionA)
                
                #print("Added character: %s" % char.name)
                #print("Action: %s" % playeraction)
                #else:
                    #fight()
    runbattleactionqueue()

def runbattleactionqueue():
    #for char in battlemembers:
    i = 0
    j = 0
    
    #for n in range(len(battlemembers)):
    #    print(battlemembers[n].name)
    #for n in range(len(battleactionqueue)):
    #    print(battleactionqueue[n])
    #option = input(" ")

    #for n in range(len(battleactionqueue)):
        #print("Name: %s Action: %s Target index: %s" % (battleactionqueue[n].name, battleactionqueue[n].action, battleactionqueue[n].target))
    #option = input(" ")
    
    while i < len(battlemembers):
        if battlemembers[i].chartype == "enemy":
            print(battlemembers[i].name + "'s turn!")
            enemy = battlemembers[i]
            choice = battleactionqueue[i].action
            #print("Enemy choice baq: %s" % choice1)
            enemytarget = battleactionqueue[i].target
            #print("Enemy target baq %i:" % enemytarget1)
            #check if target still exists:
            if enemytarget > len(battlepartymembers):
                enemytarget = 0
            if choice == "physical":
                enemyattack(enemy, enemytarget)
            elif choice == "magic":
                enemymagicattack(enemy, enemytarget)
            elif choice == "nothing":
                print("%s did nothing!" % (enemy.name))
            i += 1
        elif battlemembers[i].chartype == "player":
            print(battlemembers[i].name + "'s turn!")
            player = battlemembers[i]
            action = battleactionqueue[i].action
            #print("Player action baq: %s" % action1)
            playertarget = battleactionqueue[i].target
            #print("Player target baq %i:" % playertarget1)
            #check if target still exists:
            if playertarget > len(enemyparty):
                playertarget = 0
            if action == "physical":
                playerattack(player, playertarget)
            elif action == "magic":
                #check player mp
                if player.mp <= 0:
                    print("You are out of MP!\n")
                    break
                else:
                    magicattack(player, playertarget)
            elif action == "drink":
                drinkpotion(player, playertarget)
            elif action == "run":
                runsuccess = run()
                if runsuccess:
                    start1()
            i += 1
            j += 1
        #for char in battlepartymembers:
        #    displayhp(char)
        #for char in battlepartymembers:
        #    displaymp(char)
        #for monster in enemyparty:
        #    displayhp(monster)
        #for monster in enemyparty:
        #    displaymp(monster)
        else:
            #print("Done\n")
            print("\n")
        for char in battlepartymembers:
            displayhp(char)
            displaymp(char)
        for monster in enemyparty:
            displayhp(monster)
            displaymp(monster)
        option = input(" ")
        #else:
            #print("Done\n")
    battleactionqueue.clear()
    fight()
            

def enemyactionselector(enemy):
    #check if enemy has MP
    hasmp = 0
    choice = "physical"
    if enemy.mp >= 5:
        hasmp = 1
    if hasmp > 0:
        usemagic = random.randint(1,100)
        if usemagic >= 70:
            choice = "magic"
    return choice
        

def getenemytarget():
    enemytotal = len(enemyparty)
    t = range(enemytotal)
    i = 0
    if enemytotal > 1:
        #Select target
        print("Attack which enemy?")
        for monster in enemyparty:
            print("%i.) %s" % (t[i] + 1, monster.name))
            i += 1
        while True:
            while True:
                option = input(">")
                try:
                    option = int(option)
                    break
                except:
                    print("Please enter a number for the monster you want to attack.")
            if option > 0 and option <= enemytotal:
                target = option - 1
                break
            else:
                print("Please enter a number for the monster you want to attack.")
    else:
        target = 0
    #print("Target index: %d" % target)
    return target

def getplayertarget():
    playertotal = len(currentparty)
    t = range(playertotal)
    i = 0
    if playertotal > 1:
        #Select target
        print("Use on which party member?")
        for char in currentparty:
            print("%i.) %s" % (t[i] + 1, char.name))
            i += 1
        while True:
            while True:
                option = input(">")
                try:
                    option = int(option)
                    break
                except:
                    print("Please enter a number for the character you want to use the item on.")
            if option > 0 and option <= playertotal:
                target = option - 1
                break
            else:
                print("Please enter a number for the character you want to use the item on.")
    else:
        target = 0
    return target

def getplayertargetforenemy():
    playertotal = len(battlepartymembers)
    if playertotal > 1:
        target = random.randint(0, playertotal - 1)
    else:
        target = 0
    return target


def updatetargetindex(index, charactertype):
    #when an enemy/player is killed, update target indices higher than the index of the enemy/player that was killed.
    target = index
    chartype = charactertype
    #print("Indexcurrent: %i" % target)
    #print("Chartype: %s" % chartype)
    for action in battleactionqueue:
        if action.chartype != chartype:
            #print("Action name: %s" % action.name)
            #print("Action Chartype: %s" % action.chartype)
            #print("Target index: %i" % action.target)
            if action.target >= target:
                action.target -= 1
                #print("New target index: %i" % action.target)
                if action.target < 0:
                    action.target = 0
                #print("Fixed target index: %i" % action.target)
            #print("Target index: %i" % action.target)
    

def attack(attacker, chartype, attacktype, statuseffect, chance, targetside, targetindex):
    os.system("cls")
    #To be conpleted later as a combined function to handle all attacks

def playerattack(player, targetindex):
    os.system("cls")
    currentplayer = player
    target = targetindex
    #verify target still alive
    if target + 1 > len(enemyparty):
        try:
            target = random.randint(0, len(enemyparty)-1)
        except:
            target = 0
    #print("Target Index: %d" % target)
    enemy = enemyparty[target]
    PAttack = math.floor((random.randint(math.floor(currentplayer.attack / 2), currentplayer.attack)) * (10 / (10 + enemy.defense)))
    if PAttack == currentplayer.attack / 2:
        print("%s's attack on %s misses!" % (currentplayer.name, enemy.name))
        #option = input(" ")
    else:
        #check for crit
        crit = round(currentplayer.luck / 5)
        if 99 - crit < random.randint(0,100):
            PAttack *= 2
            print("Critical hit!")
        enemy.hp -= PAttack
        print("%s deals %i damage to %s!" % (currentplayer.name, PAttack, enemy.name))
        #option = input(" ")
        if enemy.hp <= 0:
            #Check if enemy has a next form
            if enemy.nextform:
                print(enemy.nextform[1])
                nextform = True
            else:
                print("%s defeated!\n" % enemy.name)
                nextform = False
            index = enemyparty.index(enemy)
            updatetargetindex(index, "enemy")
            enemy.hp = enemy.mHP
            defeatedenemyparty.append(enemy)
            #sortedbattlemembers.remove(enemy)
            enemyname = enemy.name
            if nextform == True:
                addenemy(enemy.nextform[0], True)
                enemyparty.remove(enemy)
                battlemembers.remove(enemy)
                for participant in battleactionqueue:
                    if participant.chartype == "enemy":
                        if participant.name == enemyname:
                            battleactionqueue.remove(participant)
            else:
                enemyparty.remove(enemy)
                battlemembers.remove(enemy)
                for participant in battleactionqueue:
                    if participant.chartype == "enemy":
                        if participant.name == enemyname:
                            battleactionqueue.remove(participant)
                win()
        os.system("cls")

def enemyattack(enemy, targetindex):
    os.system("cls")
    currentenemy = enemy
    target = targetindex
    #verify target still alive
    if target + 1 > len(battlepartymembers):
        try:
            target = random.randint(0, len(battlepartymembers)-1)
        except:
            target = 0
    playertarget = battlepartymembers[target]
    EAttack = math.floor((random.randint(math.floor(enemy.attack / 2), enemy.attack)) * (10 / (10 + playertarget.defense)))
    if EAttack == enemy.attack / 2:
        print("%s's attack on %s missed!" % (enemy.name, playertarget.name))
        #option = input(" ")
    else:
        #check for crit
        crit = round(enemy.luck / 5)
        if 99 - crit < random.randint(0,100):
            EAttack *= 2
            print("Critical hit!")
        playertarget.hp -= EAttack
        print("%s deals %i damage to %s!" % (enemy.name, EAttack, playertarget.name))
        #option = input(" ")
        if playertarget.hp <= 0:
            playername = playertarget.name
            print("%s was slain!\n" % playertarget.name)
            playertarget.hp = 0
            index = battlepartymembers.index(playertarget)
            updatetargetindex(index, "player")
            battlepartymembers.remove(playertarget)
            for participant in battleactionqueue:
                    if participant.chartype == "player":
                        if participant.name == playername:
                            battleactionqueue.remove(participant)
            battlemembers.remove(playertarget)
            dead()

def magicattack(player, targetindex):
    os.system("cls")
    currentplayer = player
    target = targetindex
    #verify target still alive
    if target + 1 > len(enemyparty):
        try:
            target = random.randint(0, len(enemyparty)-1)
        except:
            target = 0
    enemy = enemyparty[target]
    if currentplayer.mp <= 0:
        print("%s is out of MP!\n" % currentplayer.name)
        #fight()
    else:
        currentplayer.mp -= 5
        PAttack = math.floor((random.randint(math.floor(currentplayer.wisdom / 2), currentplayer.wisdom)) * (10 / (10 + enemy.resistance)))
        if PAttack == currentplayer.wisdom / 2:
            print("%s's fireball missed %s!" % (currentplayer.name, enemy.name))
            #option = input(" ")
        else:
            #check for crit
            crit = round(enemy.luck / 5)
            if 99 - crit < random.randint(0,100):
                PAttack *= 2
                print("Critical hit!")
            enemy.hp -= PAttack
            print("%s's fireball deals %i damage to %s!" % (currentplayer.name, PAttack, enemy.name))
            #option = input(" ")
            if enemy.hp <= 0:
                #Check if enemy has a next form
                if enemy.nextform:
                    print(enemy.nextform[1])
                    nextform = True
                else:
                    print("%s defeated!\n" % enemy.name)
                    nextform = False
                index = enemyparty.index(enemy)
                updatetargetindex(index, "enemy")
                enemy.hp = enemy.mHP
                defeatedenemyparty.append(enemy)
                enemyname = enemy.name
                if nextform == True:
                    addenemy(enemy.nextform[0], True)
                    enemyparty.remove(enemy)
                    battlemembers.remove(enemy)
                    for participant in battleactionqueue:
                        if participant.chartype == "enemy":
                            if participant.name == enemyname:
                                battleactionqueue.remove(participant)
                else:
                    enemyparty.remove(enemy)
                    battlemembers.remove(enemy)
                    for participant in battleactionqueue:
                        if participant.chartype == "enemy":
                            if participant.name == enemyname:
                                battleactionqueue.remove(participant)
                    win()
            os.system("cls")

def enemymagicattack(enemy, targetindex):
    os.system("cls")
    currentenemy = enemy
    target = targetindex
    #verify target still alive
    if target + 1 > len(battlepartymembers):
        try:
            target = random.randint(0, len(battlepartymembers)-1)
        except:
            target = 0
    playertarget = battlepartymembers[target]
    enemy.mp -= 5
    EAttack = math.floor((random.randint(math.floor(enemy.wisdom / 2), enemy.wisdom)) * (10 / (10 + playertarget.resistance)))
    if EAttack == enemy.wisdom / 2:
        print("%s's fireball missed %s!" % (enemy.name, playertarget.name))
        #option = input(" ")
    else:
        #check for crit
        crit = round(enemy.luck / 5)
        if 99 - crit < random.randint(0,100):
            EAttack *= 2
            print("Critical hit!")
        playertarget.hp -= EAttack
        print("The fireball of %s deals %i damage to %s!" % (enemy.name, EAttack, playertarget.name))
        #option = input(" ")
        if playertarget.hp <= 0:
            playername = playertarget.name
            print("%s was slain!\n" % playertarget.name)
            playertarget.hp = 0
            index = battlepartymembers.index(playertarget)
            updatetargetindex(index, "player")
            battlepartymembers.remove(playertarget)
            for participant in battleactionqueue:
                    if participant.chartype == "player":
                        if participant.name == playername:
                            battleactionqueue.remove(participant)
            battlemembers.remove(playertarget)
            dead()

def drinkpotion(char, targetindex):
    os.system("cls")
    player = char
    target = targetindex
    targetchar = currentparty[target]
    if "potion" not in player.items:
        print("You don't have any potions!")
        #option = input(" ")
    #if PlayerIG.potions == 0:
    #    print("You don't have any potions!")
    #    option = input(" ")
        #fight()
    elif targetchar.hp == targetchar.mHP:
        print("%s is already at max health!" % targetchar.name)
        #option = input(" ")
        #fight()
    else:
        if player != targetchar:
            print("%s threw a potion to %s!" % (player.name, targetchar.name))
        print("%s drank a potion" % targetchar.name)
        #check if player was dead
        if targetchar.hp == 0:
            print("%s is revived!" % targetchar.name)
            battlepartymembers.append(targetchar)
        targetchar.hp += 50
        if targetchar.hp > targetchar.mHP:
            targetchar.hp = targetchar.mHP
        PlayerIG.potions -= 1
        player.items.remove("potion")
    option = input(" ")

def run():
    os.system("cls")
    runnum = random.randint(1, 3)
    success = False
    if GameDataIG.scriptedbattles[0] == True:
        #check if run is disabled
        if GameDataIG.scriptedbattles[1] == False:
            print("You failed to get away!")
            os.system("cls")
            return success
    if runnum == 1:
        print("You ran away successfully!")
        enemyparty.clear()
        option = input(" ")
        success = True
        return success
    else:
        print("You failed to get away!")
        option = input(" ")
        os.system("cls")
        return success

def win():
    os.system("cls")
    #check if enemyparty is empty
    if not enemyparty:
        #get total experience gain
        goldgain = 0
        for monster in defeatedenemyparty:
            goldgain += monster.goldgain
        expgain = 0
        for monster in defeatedenemyparty:
            expgain += monster.expgain
        PlayerIG.gold += goldgain
        #PlayerIG.exp += expgain
        #give exp to each party member that is alive
        for char in battlepartymembers:
            char.exp += expgain
        #for monster in defeatedenemyparty:
        #    print("You have defeated the %s" % monster.name)
        print("You have won the battle!")
        print("You found %i gold!" % goldgain)
        print("You gained %i experience!\n" % expgain)
        for char in battlepartymembers:
            print("%s:" %char.name)
            if char.nextlevel - char.exp <= 0:
                print("Experience to next level: 0")
                while char.exp >= char.nextlevel:
                    levelup(char)
            else:
                print("Experience to next level: %d" % (char.nextlevel - char.exp))
                option = input("Press Enter to continue.")
        enemyparty.clear()
        defeatedenemyparty.clear()
        battlepartymembers.clear()
        if GameDataIG.scriptedbattles[0] == True:
            #check preconditions
            #print("scripted battle win")
            #print(GameDataIG.battlescripts)
            for script in GameDataIG.battlescripts:
                #print(script)
                for precondition in script.preconditions:
                    #print(precondition)
                    if precondition == "win":
                        #print("win")
                        runevent(precondition, script, PlayerIG.currentposition, areas)
        start1()
    else:
        #fight()
        pass

def dead():
    os.system("cls")
    #check if battlepartymembers is empty
    if not battlepartymembers:
        enemyparty.clear()
        if GameDataIG.scriptedbattles[2] == True:
            #check preconditions
            #print("scripted battle loss")
            #print(GameDataIG.battlescripts)
            for script in GameDataIG.battlescripts:
                #print(script)
                for precondition in script.preconditions:
                    #print(precondition)
                    if precondition == "loss":
                        #print("loss")
                        runevent(precondition, script, PlayerIG.currentposition, areas)
            GameDataIG.scriptedbattles[2] = False
            start1()
        else:
            print("You died!")
            option = input(" ")
            print("Thanks for playing! Better luck next time!")
            sys.exit()
    else:
        pass

def gameover(messageflag, messagelist):
    if messageflag == "y":
        for message in messagelist:
            print(message)
    print("Thanks for playing! Better luck next time!")
    sys.exit()

def rollgain(mod):
    modifier = mod
    if modifier == "low":
        gain = round(random.randint(0,10) * 1 / 10)
    if modifier == "med":
        gain = round(random.randint(0,20) * 1 / 10)
    if modifier == "high":
        gain = round(random.randint(0,30) * 1 / 10)
    if modifier == "none":
        gain = 0
    return gain

def levelup(char):
    os.system("cls")
    player = char
    print("%s gained a level!" % char.name)
    print("Level: %i" % player.level + " +1")
    player.level += 1
    gain = rollgain(player.hpgrowth) * 10
    if gain > 0:
        print("Health: %i/%i +%i" % (player.hp, player.mHP, gain))
        #PlayerIG.hp += gain
        player.mHP += gain
    else:
        print("Health: %i/%i" % (player.hp, player.mHP))
    gain = rollgain(player.mpgrowth) * 10
    if gain > 0:
        print("MP: %i/%i +%i" % (player.mp, player.mMP, gain))
        #PlayerIG.mp += gain
        player.mMP += gain
    else:
        print("MP: %i/%i" % (player.mp, player.mMP))
    gain = rollgain(player.attackgrowth)
    if gain > 0:
        print("Attack: %i +%i" % (player.attack, gain))
        player.base_attack += gain
    else:
        print("Attack: %i" % player.attack)
    gain = rollgain(player.defensegrowth)
    if gain > 0:
        print("Defense: %i +%i" % (player.defense, gain))
        player.base_defense += gain
    else:
        print("Defense: %i" % player.defense)
    gain = rollgain(player.wisdomgrowth)
    if gain > 0:
        print("Wisdom: %i +%i" % (player.wisdom, gain))
        player.base_wisdom += gain
    else:
        print("Wisdom: %i" % player.wisdom)
    gain = rollgain(player.resistancegrowth)
    if gain > 0:
        print("Magic Resistance: %i +%i" % (player.resistance, gain))
        player.base_resistance += gain
    else:
        print("Magic Resistance: %i" % player.resistance)
    gain = rollgain(player.agilitygrowth)
    if gain > 0:
        print("Agility: %i +%i" % (player.agility, gain))
        player.base_agility += gain
    else:
        print("Agility: %i" % player.agility)
    gain = rollgain(player.luckgrowth)
    if gain > 0:
        print("Luck: %i +%i\n" % (player.luck, gain))
        player.base_luck += gain
    else:
        print("Luck: %i\n" % player.luck)
    player.nextlevel = nextlevel(player.level+1)
    print("Exp: %i/%i" % (player.exp, nextlevel(player.level+1)))
    option = input(" ")
    #if player.nextlevel - player.exp <= 0:
        #levelup(player)


def purchaseforwho(itembought):
    item = itembought
    print("Who will take the %s?" % item)
    for char in currentparty:
        print(char.name)
    option = input(">")
    for char in currentparty:
        if option == char.name:
            currentplayer = char
            print(currentplayer.name)
            print(item)
            return currentplayer
    print("Please specify a valid party member.")
    print("You said: %s" % option)
    print(item)
    purchaseforwho(item)
    #store()

def sellforwho():
    print("Who will sell?")
    for char in currentparty:
        print(char.name)
    option = input(">")
    for char in currentparty:
        if option == char.name:
            currentplayer = char
            print(currentplayer.name)
            return currentplayer
    print("Please specify a valid party member.")
    print("You said: %s" % option)
    sellforwho()

def store():
    os.system("cls")
    print("Welcome to the shop!")
    print("Current gold: %i" % PlayerIG.gold)
    print("1.) Buy")
    print("2.) Sell")
    print("b.) Back")
    option = input(">")
    if option == "1":
        storebuy()
    elif option == "2":
        storesell()
    elif option == "b" or option == "back":
        start1()
    else:
        print("Please enter a valid entry.")

def storebuy():
    os.system("cls")
    print("Current gold: %i" %PlayerIG.gold)
    print("What would you like to buy?")
    itemtotal = len(weapons) + len(armors) + len(potions) + len(accs)
    t = range(itemtotal)
    i = 0
    for weapon in weapons:
        print("%i.) %s - %i gold" %(t[i] + 1, weapon, weapons[weapon]))
        i += 1
    for potion in potions:
        print("%i.) %s - %i gold" %(t[i] + 1, potion, potions[potion]))
        i += 1
    for armor in armors:
        print("%i.) %s - %i gold" %(t[i] + 1, armor, armors[armor]))
        i += 1
    for acc in accs:
        print("%i.) %s - %i gold" %(t[i] + 1, acc, accs[acc]))
        i += 1
    print("b.) back")
    print(" ")
    option = input(">")
    if option in weapons:
        if PlayerIG.gold >= weapons[option]:
            os.system("cls")
            player = purchaseforwho(option)
            player.weapon.append(option)
            print("You have purchased %s" % option)
            PlayerIG.gold -= weapons[option]
            option = input(" ")
            storebuy()
        else:
            os.system("cls")
            print("You don't have enough gold...")
            option = input(" ")
            storebuy()
    elif option in potions:
        if PlayerIG.gold >= potions[option]:
            os.system("cls")
            player = purchaseforwho(option)
            PlayerIG.gold -= potions[option]
            PlayerIG.potions += 1
            player.items.append("potion")
            print("You have purchased a potion.")
            option = input(" ")
            storebuy()
        else:
            os.system("cls")
            print("You don't have enough gold...")
            option = input(" ")
            storebuy()
    elif option in armors:
        if PlayerIG.gold >= armors[option]:
            os.system("cls")
            player = purchaseforwho(option)
            PlayerIG.gold -= armors[option]
            player.armor.append(option)
            print("You have purchased %s" % option)
            option = input(" ")
            storebuy()
    elif option in accs:
        if PlayerIG.gold >= accs[option]:
            os.system("cls")
            player = purchaseforwho(option)
            PlayerIG.gold -= accs[option]
            player.acc.append(option)
            print("You have purchased %s" % option)
            option = input(" ")
            storebuy()
        else:
            os.system("cls")
            print("You don't have enough gold...")
            option = input(" ")
            storebuy()
    elif option == "back" or "b":
        store()
    else:
        os.system("cls")
        print("That item does not exist!")
        option = input(" ")
        storebuy()

def storesell():
    os.system("cls")
    invtosell.clear()
    print("Current gold: %i" %PlayerIG.gold)
    char = sellforwho()
    storesell2(char)

def storesell2(character):
    os.system("cls")
    char = character
    print("Current gold: %i" %PlayerIG.gold)
    print("What do you want to sell?")
    for item in char.weapon:
        print("%s - %i" % (item, 3*weapons[item]/4))
        invtosell.append(item)
    for item in char.armor:
        print("%s - %i" % (item, 3*armors[item]/4))
        invtosell.append(item)
    for item in char.acc:
        print("%s - %i" % (item, 3*accs[item]/4))
        invtosell.append(item)
    print("b.) back")
    option = input(">")
    if option in invtosell:
        if option in weapons:
            value = 3*weapons[option]/4
        if option in armors:
            value = 3*armors[option]/4
        if option in accs:
            value = 3*accs[option]/4
        print("Thank you very much!")
        print("You have sold the %s for %i gold!" % (option, value))
        PlayerIG.gold += value

        if option in char.weapon:
            char.weapon.remove(option)
        if option in char.armor:
            char.armor.remove(option)
        if option in char.acc:
            char.acc.remove(option)
        storesell2(char)
    elif option == "b" or option == "back":
        store()
    else:
        print("%s does not have a %s to sell." % (char.name, option))
        storesell2(char)


main()
