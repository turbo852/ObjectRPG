import sys
import os
import random
import math
import pickle


#TODO

weapons = {"Rusty Sword":20, "Dagger":15, "Wand":10, "Great Sword":40, "Battle Axe":50, "Iron Dagger":70, "Rod":50, "Staff":200}
armors = {"Leather Tunic":15, "Robe":10, "Chain Mail":50, "Plate Mail":100, "Magic Cloak":75, "Wizard Robe":200,"Shadow Cloak":150}
accs = {"Ring":75, "Magic Ring":125, "Mystic Ring":200, "Warrior Ring":100, "Iron Ring":100, "Quick Ring":50, "Agile Ring":100, "Lucky Ring":100, "Fortune Ring":200, "Ranger Ring":200}
potions = {"Potion":10}
nothing = {"None"}
currentparty = []
battlepartymembers = []
enemyparty = []
defeatedenemyparty = []
battlemembers = []
sortedbattlemembers = []
battleactionqueue = []
battletargetqueue = []
baq = []
invtosell = []

class Player:
    def __init__(self, name, charclass):
        self.name = name
        self.level = 1
        self.mHP = 100
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
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 2
        self.weapon = ["Rusty Sword"]
        self.curweapon = "None"
        self.armor = ["Leather Tunic"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"

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
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 2
        self.weapon = ["Rusty Sword"]
        self.curweapon = "None"
        self.armor = ["Leather Tunic"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"

class Thief(Player):
    def __init__(self, name, charclass):
        self.name = name
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
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 2
        self.weapon = ["Dagger"]
        self.curweapon = "None"
        self.armor = ["Leather Tunic"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"
        
class Mage(Player):
    def __init__(self, name, charclass):
        self.name = name
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
        self.gold = 100
        self.exp = 0
        self.nextlevel = nextlevel(self.level+1)
        self.potions = 2
        self.weapon = ["Wand"]
        self.curweapon = "None"
        self.armor = ["Robe"]
        self.curarmor = "None"
        self.acc = []
        self.curacc = "None"
        self.charclass = charclass
        self.action = "nothing"
        self.chartype = "player"

class Goblin:
    def __init__(self, name):
        self.name = name
        self.mHP = 50
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 5
        self.defense = 1
        self.wisdom = 0
        self.resistance = 1
        self.agility = 3
        self.luck = 1
        self.goldgain = 10
        self.expgain = 5
        self.action = "nothing"
        self.chartype = "enemy"
GoblinIG = Goblin("Goblin")

class Zombie:
    def __init__(self, name):
        self.name = name
        self.mHP = 70
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 7
        self.defense = 3
        self.wisdom = 0
        self.resistance = -5
        self.agility = 2
        self.luck = 1
        self.goldgain = 15
        self.expgain = 8
        self.action = "nothing"
        self.chartype = "enemy"
ZombieIG = Zombie("Zombie")

class FastZombie:
    def __init__(self, name):
        self.name = name
        self.mHP = 100
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 10
        self.defense = 4
        self.wisdom = 0
        self.resistance = -5
        self.agility = 7
        self.luck = 1
        self.goldgain = 20
        self.expgain = 10
        self.action = "nothing"
        self.chartype = "enemy"
ZombieIG = Zombie("Zombie")

class Imp:
    def __init__(self, name):
        self.name = name
        self.mHP = 150
        self.hp = self.mHP
        self.mMP = 0
        self.mp = self.mMP
        self.attack = 12
        self.defense = 5
        self.wisdom = 0
        self.resistance = 3
        self.agility = 5
        self.luck = 2
        self.goldgain = 20
        self.expgain = 12
        self.action = "nothing"
        self.chartype = "enemy"
ImpIG = Imp("Imp")

class MagicGoblin:
    def __init__(self, name):
        self.name = name
        self.mHP = 100
        self.hp = self.mHP
        self.mMP = 15
        self.mp = self.mMP
        self.attack = 10
        self.defense = 4
        self.wisdom = 10
        self.resistance = 10
        self.agility = 5
        self.luck = 1
        self.goldgain = 25
        self.expgain = 15
        self.action = "nothing"
        self.chartype = "enemy"
MagicGoblinIG = MagicGoblin("Magic Goblin")



class BattleActionClass:
    def __init__(self, name):
        self.name = name
        self.chartype = "Player"
        self.charclass = "Warrior"
        self.action = "physical"
        self.target = 0


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
    print("Hello, what is your name?")
    name = input(">")
    print("Greetings %s!" % name)
    option = input(" ")
    print("What is your class?")
    global PlayerIG
    charclass = input("Warrior, Thief, or Mage? \n>")
    if charclass == "Warrior":
        PlayerIG = Warrior(name, charclass)
    elif charclass == "Thief":
         PlayerIG = Thief(name, charclass)
    elif charclass == "Mage":
        PlayerIG = Mage(name, charclass)
    else:
        PlayerIG = Player(name, "Nothing")
    currentparty.append(PlayerIG)
    start1()

def newchar():
    os.system("cls")
    if len(currentparty) > 0:
        global newplayer
        print("Hello, what is your name?")
        newplayer = input(">")
        print("Greetings %s!" % newplayer)
        option = input(" ")
        print("What is your class?")
        charclass = input("Warrior, Thief, or Mage? \n>")
        if charclass == "Warrior":
            newplayer = Warrior(newplayer, charclass)
        elif charclass == "Thief":
            newplayer = Thief(newplayer, charclass)
        elif charclass == "Mage":
            newplayer = Mage(newplayer, charclass)
        else:
            newplayer = Player(newplayer, "Nothing")
        currentparty.append(newplayer)
        start1()

def start1():
    os.system("cls")
    print("Hello %s What would you like to do?\n" % PlayerIG.name)
    print("Gold: %i" % PlayerIG.gold)
    print("Potions: %i\n" % PlayerIG.potions)
    for char in currentparty:
        displayhp(char)
        displaymp(char)
        print("Level: %i" % char.level)
        print("Class: %s" % char.charclass)
    print("1.) Fight")
    print("2.) Store")
    print("3.) Save")
    print("4.) Inventory")
    print("5.) Inn")
    print("6.) Exit")
    print("7.) Status")
    print("8.) Recruit new party member")
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
    else:
        start1()

def status():

    print("Gold: %i" % PlayerIG.gold)
    print("Potions: %i\n" % PlayerIG.potions)
    for char in currentparty:
        print("Name: %s" % char.name)
        print("Level: %i" % char.level)
        print("Class: %s" % char.charclass)
        print("Health: %i/%i" % (char.hp, char.mHP))
        print("MP: %i/%i\n" % (char.mp, char.mMP))
        print("Attack: %i" % char.attack)
        print("Defense: %i" % char.defense)
        print("Wisdom: %i" % char.wisdom)
        print("Agility: %i" % char.agility)
        print("Luck: %i" % char.luck)
        print("Exp: %i/%i Next: %i" % (char.exp, nextlevel(char.level+1),(char.nextlevel - char.exp)))
        print("Current Weapon: %s" % char.curweapon)
        print("Current Armor: %s" % char.curarmor)
        print("Current Acc: %s" % char.curacc)
        option = input(" ")
    start1()

def savegame():
    os.system("cls")
    with open("savefile", "wb") as f:
        pickle.dump(PlayerIG, f)
        pickle.dump(currentparty, f)
        print("\nGame has been saved!\n")
    option = input(" ")
    start1()

def loadgame():
    if os.path.exists("savefile") == True:
        os.system("cls")
        with open("Savefile", "rb") as f:
            global PlayerIG
            global currentparty
            PlayerIG = pickle.load(f)
            currentparty = pickle.load(f)
        print("Save has been loaded...")
        start1()
        option = input(" ")
    else:
        print("You have no save file for this game.")
        option =  input(" ")
        main()

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
    print("HP: [", end="")
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
        print("MP: [", end="")
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

def nextlevel(level):
    exponent = 1.3
    baseXP = 10
    return math.floor(baseXP * (level ** exponent))

#for n in range(10):
#	print(nextlevel(n))

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
    print("b.) go back")
    option = input(">")
    if option == "1":
        equip()
    elif option == "b" or option == "back":
        start1()

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
    if option == currentplayer.curarmor:
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
    if option == currentplayer.curacc:
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

def prefight():
    #establish enemy party
    global enemy
    enemynum = random.randint(1, 100)
    print(enemynum)
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
    #establish battle participants
    battlemembers.clear()
    sortedbattlemembers.clear()
    battlepartymembers.clear()
    battleactionqueue.clear()
    battletargetqueue.clear()
    baq.clear()
    for char in currentparty:
        battlemembers.append(char)
        battlepartymembers.append(char)
    for monster in enemyparty:
        battlemembers.append(monster)
    #sort battle participants by agility for turn order
    battlemembers.sort(key=lambda x: x.agility, reverse=True)
    #Show battle participants
    for char in battlepartymembers:
        print("%s" % char.name)
    print("vs")
    for monster in enemyparty:
        print("%s" % monster.name)
    print("Potions: %i\n" % PlayerIG.potions)
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

def fight():
    os.system("cls")

    #sort by agility
    #sortedbattledmembers = sorted(battlemembers, key=lambda x: x.agility, reverse=True)
    #print(sortedbattlemembers)
    
    #for char in battlemembers:
    #    print("Char: %s" % char.name)
    #print("%s vs %s" % (PlayerIG.name, enemy.name))
    #print("%s vs " % PlayerIG.name)

    #print("%s's Health: %d/%d\n%s's Health: %i/%i" % (PlayerIG.name, PlayerIG.hp, PlayerIG.mHP, enemy.name, enemy.hp, enemy.mHP))

    #print("%s's MP: %d/%d\n%s's MP: %i/%i" % (PlayerIG.name, PlayerIG.mp, PlayerIG.mMP, enemy.name, enemy.mp, enemy.mMP))
    print("********")
    for char in battlepartymembers:
        displayhp(char)
        displaymp(char)
    for monster in enemyparty:
        displayhp(monster)
        displaymp(monster)
    #for char in battlemembers:
    #    displayhp(char)
    #    displaymp(char)
    print("\nPotions: %i" % PlayerIG.potions)
    #print("********")
    #determine actions for each party member
    for char in battlemembers:
        if char.chartype == "enemy":
            BattleActionA = BattleActionClass(char.name)
            print("Battle Class: %s" % BattleActionA.name)
            enemyaction = enemyactionselector(char)
            BattleActionA.action = enemyaction
            print("Battle Action: %s" % BattleActionA.action)
            battleactionqueue.append(enemyaction)
            enemytarget = getplayertargetforenemy()
            BattleActionA.target = enemytarget
            print("Battle Target: %s" % BattleActionA.target)
            print(battlepartymembers[BattleActionA.target].name)
            pause = input(" ")
            battletargetqueue.append(enemytarget)

            baq.append(BattleActionA)
            
            print("********")
            print("%s's turn!" % BattleActionA.name)
            print("Added enemy: %s" % BattleActionA.name)
            print("Battle Action: %s" % BattleActionA.action)
            print("Battle Target: %s" % BattleActionA.target)
            print(battlepartymembers[BattleActionA.target].name)
        else:
            BattleActionA = BattleActionClass(char.name)
            BattleActionA.charclass = char.charclass
            print("********")
            print("%s's turn!" % BattleActionA.name)
            print("Class: %s" % BattleActionA.charclass)
            print("1.) Attack")
            print("2.) Magic")
            print("3.) Drink Potion")
            print("4.) Run")
            while True:
                option = input(">")
                try:
                    option = int(option)

                    try:
                        if option == 2:
                            #check player mp
                            if char.mp <= 0:
                                print("No MP!")
                                raise
                    except:
                        print("You are out of MP!\n")
                        print("Changing to physical attack!")
                        option = 1
                    if option < 1 or option > 4:
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
                    print("4.) Run")
            #if option > 0 and option <= 4:
            #print(option)
            if option == 1:
                #attack("physical")
                playeraction = "physical"
                battleactionqueue.append(playeraction)
                target = getenemytarget()
                battletargetqueue.append(target)
                
                
                print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                print("Battle Target: %s" % BattleActionA.target)
                print(enemyparty[BattleActionA.target].name)
                pause = input(" ")

                baq.append(BattleActionA)
                
                print("Added character: %s" % BattleActionA.name)
                print("Action: %s" % BattleActionA.action)
                print("Target: %s" % BattleActionA.target)
                print(enemyparty[BattleActionA.target].name)
            elif option == 2:
                playeraction = "magic"

                battleactionqueue.append(playeraction)
                target = getenemytarget()
                battletargetqueue.append(target)

                BattleActionA = BattleActionClass(char.name)
                print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                print("Battle Target: %s" % BattleActionA.target)
                print(enemyparty[BattleActionA.target].name)
                pause = input(" ")

                baq.append(BattleActionA)
                
                print("Added character: %s" % char.name)
                print("Action: %s" % playeraction)
                print("Target: %s" % target)
                #print(enemyparty[target].name)
            elif option == 3:
                playeraction = "drink"
                battleactionqueue.append(playeraction)
                target = getplayertarget()
                battletargetqueue.append(target)

                BattleActionA = BattleActionClass(char.name)
                print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                print("Battle Target index: %s" % BattleActionA.target)
                #print(enemyparty[BattleActionA.target].name)
                pause = input(" ")

                baq.append(BattleActionA)
                
                print("Added character: %s" % char.name)
                print("Action: %s" % playeraction)
                print("Target: %s" % target)
                print(currentparty[target].name)
            elif option == 4:
                playeraction = "run"
                battleactionqueue.append(playeraction)
                target = 0
                battletargetqueue.append(target)

                BattleActionA = BattleActionClass(char.name)
                print("Battle Class: %s" % BattleActionA.name)
                BattleActionA.action = playeraction
                print("Battle Action: %s" % BattleActionA.action)
                BattleActionA.target = target
                print("Battle Target index: %s" % BattleActionA.target)
                #print(enemyparty[BattleActionA.target].name)
                pause = input(" ")

                baq.append(BattleActionA)
                
                print("Added character: %s" % char.name)
                print("Action: %s" % playeraction)
                #else:
                    #fight()
    runbattleactionqueue()

def runbattleactionqueue():
    #for char in battlemembers:
    i = 0
    j = 0
    print("\nTurn start!")
    for n in range(len(battlemembers)):
        print(battlemembers[n].name)
    for n in range(len(battleactionqueue)):
        print(battleactionqueue[n])
    for n in range(len(battletargetqueue)):
        print(battletargetqueue[n])
    option = input(" ")

    for n in range(len(baq)):
        print("Name: %s Action: %s Target index: %s" % (baq[n].name, baq[n].action, baq[n].target))
    option = input(" ")
    
    while i < len(battlemembers):
        if battlemembers[i].chartype == "enemy":
            print(battlemembers[i].name + "'s turn!")
            enemy = battlemembers[i]
            choice = battleactionqueue[i]
            enemytarget = battletargetqueue[i]
            choice1 = baq[i].action
            print("Enemy choice baq: %s" % choice1)
            enemytarget1 = baq[i].target
            print("Enemy target baq %i:" % enemytarget1)
            #check if target still exists:
            if enemytarget1 > len(battlepartymembers):
                enemytarget1 = 0
            if choice1 == "physical":
                enemyattack(enemy, enemytarget1)
            else:
                enemymagicattack(enemy, enemytarget1)
            i += 1
        elif battlemembers[i].chartype == "player":
            print(battlemembers[i].name + "'s turn!")
            player = battlemembers[i]
            action = battleactionqueue[i]
            playertarget = battletargetqueue[i]
            action1 = baq[i].action
            print("Player action baq: %s" % action1)
            playertarget1 = baq[i].target
            print("Player target baq %i:" % playertarget1)
            #check if target still exists:
            if playertarget1 > len(enemyparty):
                playertarget1 = 0
            if action1 == "physical":
                playerattack(player, playertarget1)
            elif action1 == "magic":
                #check player mp
                if player.mp <= 0:
                    print("You are out of MP!\n")
                    break
                else:
                    magicattack(player, playertarget1)
            elif action1 == "drink":
                drinkpotion(player, playertarget1)
            elif action1 == "run":
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
            print("Done\n")
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
    battletargetqueue.clear()
    baq.clear()
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
    print("Target index: %d" % target)
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


def playerattack(player, targetindex):
    os.system("cls")
    currentplayer = player
    target = targetindex
    #verify target still alive
    if target + 1 > len(enemyparty):
        target = random.randint(0, len(enemyparty)-1)
    print("Target Index: %d" % target)
    enemy = enemyparty[target]
    PAttack = math.floor((random.randint(math.floor(currentplayer.attack / 2), currentplayer.attack)) * (10 / (10 + enemy.defense)))
    if PAttack == currentplayer.attack / 2:
        print("%s's attack on %s misses!" % (currentplayer.name, enemy.name))
    else:
        #check for crit
        crit = round(currentplayer.luck / 5)
        if 99 - crit < random.randint(0,100):
            PAttack *= 2
            print("Critical hit!")
        enemy.hp -= PAttack
        print("%s deals %i damage to %s!" % (currentplayer.name, PAttack, enemy.name))
        option = input(" ")
        if enemy.hp <= 0:
            print("%s defeated!\n" % enemy.name)
            enemy.hp = enemy.mHP
            defeatedenemyparty.append(enemy)
            enemyparty.remove(enemy)
            battlemembers.remove(enemy)
            #sortedbattlemembers.remove(enemy)
            win()
        os.system("cls")

def enemyattack(enemy, targetindex):
    os.system("cls")
    currentenemy = enemy
    target = targetindex
    #verify target still alive
    if target + 1 > len(battlepartymembers):
        target = random.randint(0, len(battlepartymembers)-1)
    playertarget = battlepartymembers[target]
    EAttack = math.floor((random.randint(math.floor(enemy.attack / 2), enemy.attack)) * (10 / (10 + playertarget.defense)))
    if EAttack == enemy.attack / 2:
        print("%s's attack on %s missed!" % (enemy.name, playertarget.name))
    else:
        #check for crit
        crit = round(enemy.luck / 5)
        if 99 - crit < random.randint(0,100):
            EAttack *= 2
            print("Critical hit!")
        playertarget.hp -= EAttack
        print("%s deals %i damage to %s!" % (enemy.name, EAttack, playertarget.name))
        option = input(" ")
        if playertarget.hp <= 0:
            print("%s was slain!\n" % playertarget.name)
            battlepartymembers.remove(playertarget)
            battlemembers.remove(playertarget)
            dead()

def magicattack(player, targetindex):
    os.system("cls")
    currentplayer = player
    target = targetindex
    #verify target still alive
    if target + 1 > len(enemyparty):
        target = random.randint(0, len(enemyparty)-1)
    enemy = enemyparty[target]
    print("Magic attack!")
    if currentplayer.mp <= 0:
        print("%s is out of MP!\n" % currentplayer.name)
        #fight()
    else:
        currentplayer.mp -= 5
        PAttack = math.floor((random.randint(math.floor(currentplayer.wisdom / 2), currentplayer.wisdom)) * (10 / (10 + enemy.resistance)))
        if PAttack == currentplayer.wisdom / 2:
            print("%s's fireball missed %s!" % (currentplayer.name, enemy.name))
        else:
            #check for crit
            crit = round(enemy.luck / 5)
            if 99 - crit < random.randint(0,100):
                EAttack *= 2
                print("Critical hit!")
            enemy.hp -= PAttack
            print("%s's fireball deals %i damage to %s!" % (currentplayer.name, PAttack, enemy.name))
            option = input(" ")
            if enemy.hp <= 0:
                print("%s defeated!\n" % enemy.name)
                enemy.hp = enemy.mHP
                defeatedenemyparty.append(enemy)
                enemyparty.remove(enemy)
                battlemembers.remove(enemy)
                win()
            os.system("cls")

def enemymagicattack(enemy, targetindex):
    os.system("cls")
    currentenemy = enemy
    target = targetindex
    #verify target still alive
    if target + 1 > len(battlepartymembers):
        target = random.randint(0, len(battlepartymembers)-1)
    playertarget = battlepartymembers[target]
    enemy.mp -= 5
    EAttack = math.floor((random.randint(math.floor(enemy.wisdom / 2), enemy.wisdom)) * (10 / (10 + playertarget.resistance)))
    if EAttack == enemy.wisdom / 2:
        print("%s's fireball missed %s!" % (enemy.name, playertarget.name))
    else:
        #check for crit
        crit = round(enemy.luck / 5)
        if 99 - crit < random.randint(0,100):
            EAttack *= 2
            print("Critical hit!")
        playertarget.hp -= EAttack
        print("The fireball of %s deals %i damage to %s!" % (enemy.name, EAttack, playertarget.name))
        option = input(" ")
        if playertarget.hp <= 0:
            print("%s was slain!\n" % playertarget.name)
            battlepartymembers.remove(playertarget)
            battlemembers.remove(playertarget)
            dead()

def drinkpotion(char, targetindex):
    os.system("cls")
    player = char
    target = targetindex
    targetchar = currentparty[target] 
    if PlayerIG.potions == 0:
        print("You don't have any potions!")
        option = input(" ")
        #fight()
    elif targetchar.hp == targetchar.mHP:
        print("%s is already at max health!" % targetchar.name)
        option = input(" ")
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
    option = input(" ")

def run():
    os.system("cls")
    runnum = random.randint(1, 3)
    success = False
    if runnum == 1:
        print("You have successfully ran away!")
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
        print("You gained %i experience!" % expgain)
        for char in battlepartymembers:
            print("Checking %s" %char.name)
            if char.nextlevel - char.exp <= 0:
                print("Experience to next level: 0")
            else:
                print("Experience to next level: %d" % (char.nextlevel - char.exp))
            while char.exp >= char.nextlevel:
                levelup(char)
            option = input(" ")
        enemyparty.clear()
        defeatedenemyparty.clear()
        battlepartymembers.clear()
        start1()
    else:
        #fight()
        pass

def dead():
    os.system("cls")
    #check if battlepartymembers is empty
    if not battlepartymembers:
        enemyparty.clear()
        print("You died!")
        option = input(" ")
        print("Thanks for playing! Better luck next time!")
        sys.exit()
    else:
        pass

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
    player.nextlevel = nextlevel(player.level+1)
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
            PlayerIG.gold -= potions[option]
            PlayerIG.potions += 1
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
