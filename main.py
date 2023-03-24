 #
#MAIN LOOP AT VERY BOTTOM
#
#Please read "readme.txt" for information about the game riddles.
#
#Only use repl.it as I think "getkey" library doesn't work on PC
#But you can try, or you can fix the library too

#Foreword
print("Hey! Welcome to Minery.\n")
print(
    "Before you start, ensure that the terminal \nwindow is as big as possible to avoid \ntext characters being pushed to the next line, \nwhich will mess up the picture."
)

print(
    "\n<------------------------The game is about this wide ------------------------>"
)
print("                   Ensure that this line is all in one row\n")
input("\nOnce you're ready, hit enter and we'll start the game!\n")
running = True

#
#PACKAGES AND STARTUP
#
from time import sleep
from getkey import getkey, keys
from random import randint
from colorama import Fore, Style, Back
from decimal import Decimal
import cursor


def clearBoard() -> None:  #Clear screen
    '''
  Clear the board to remove scrolling up, as well as keep terminal clean.
  '''
    print("\033[H\033[2J", end="", flush=True)


clearBoard()

cursor.hide()  #Disable cursor to reduce flickering in the console

#
# VARIABLES
#

#Dictionary of icons for each object
objectIcons = {
    "Character": "\o/",
    "Steve": "\s/",
    "Door": "|¯|",
    "Sell area": Fore.GREEN + Style.BRIGHT + "[$]" + Style.RESET_ALL,
    "Backpack upgrade": ":[}",
    "Pickaxe upgrade": "--)",
    "Teleport upgrade": Fore.MAGENTA + Style.BRIGHT + "(@)" + Style.RESET_ALL,
    "Rich charm": Fore.GREEN + Style.BRIGHT + "$<}" + Style.RESET_ALL,
    "Strip miner": Fore.BLUE + Style.DIM + "<->" + Style.RESET_ALL,
    "Chest": Back.BLACK + Fore.YELLOW + Style.BRIGHT + "[ᚊ]" + Style.RESET_ALL,
    "Special chest":
    Back.BLACK + Fore.YELLOW + Style.BRIGHT + "[ᚊ]" + Style.RESET_ALL,
    "Stone": Fore.WHITE + Style.DIM + " + " + Style.RESET_ALL,
    "Copper": Fore.RED + Style.BRIGHT + " # " + Style.RESET_ALL,
    "Iron": Fore.WHITE + Style.NORMAL + " ₪ " + Style.RESET_ALL,
    "Gold": Fore.YELLOW + Style.BRIGHT + " ✿ " + Style.RESET_ALL,
    "Diamond": Fore.CYAN + Style.BRIGHT + " ⬙ " + Style.RESET_ALL,
    "Ancient writing": "[≋]",
    "Box in wall": "[≋]",
    "Random letter": "[≣]",
    "Mystery door": Fore.MAGENTA + Style.BRIGHT + "[?]" + Style.RESET_ALL,
    "Dog": "'ᴥ'",
    "Ball": Fore.GREEN + Style.BRIGHT + " ◍ " + Style.RESET_ALL,
    "Ladder down": "↧H↧",
    "Ladder up": "↥H↥",
    "Lever": Fore.RED + "_/_" + Style.RESET_ALL,
    "1": "[ ]",
    "2": "[ ]",
    "3": "[ ]",
    "4": "[ ]",
    "5": "[ ]",
    "Math equation": Fore.CYAN + Style.BRIGHT + "+-X" + Style.RESET_ALL,
    "Portal to the outside": Fore.MAGENTA + Style.BRIGHT + "(!)" + Style.RESET_ALL,
    "Tutorial": Fore.YELLOW + "-?-" + Style.RESET_ALL,
}

#Dictionary of descriptions for each object.
objectsDescription = {
    "Character":
    "Look, its you... wait, this description isn't supposed to be printed!",
    "Steve": "Why are you even here???",
    "Door": "Wow, it's a door! What could possibly go wrong?",
    "Sell area": "There's always demand for those cool rocks you found.",
    "Backpack upgrade":
    "Introducing, the backpack! It holds everything from \nrocks, ores, stolen goods, and uhhh...",
    "Pickaxe upgrade":
    "Purchase pickaxe upgrades. \nThis increases your mining level, meaning you can go deeper.",
    "Teleport upgrade":
    "Walking is lame sometimes. But maybe this thing can help...?",
    "Rich charm":
    "According to myself, you become rich if \nyou carry this around. 100% legit no scam B)",
    "Strip miner":
    "Are you skipping arm day? Well you're in luck! No more mining for you!",
    "Chest": "It's a chest! Perhaps it has some nice treasure?",
    "Special chest": "It's a chest! Wait... this one seems a little off...",
    "Stone": "It's getting kind of rocky in here.",
    "Copper": "Who even wants to buy so much copper?",
    "Iron": "Iron. Super versatile metal. I give it a 10/10",
    "Gold": "Although much less useful than iron, it's very valuable.",
    "Diamond": "Nice. The pinnacle of all mineable ores.",
    "Ancient writing":
    "No clue why you would ever need it. Perhaps it says something?",
    "Box in wall": "Who thought it was a good idea to sell a box from a wall?",
    "Random letter": "This looks like something interesting...",
    "Mystery door":
    "A gateway of mystery and its secrets are forever preserved in the mines.",
    "Dog": "We should name him Doug because it sounds funny",
    "Ball":
    "What is this ball doing here? This mine has been untouched for centuries!",
    "Ladder down": "Into the darkness we go!",
    "Ladder up": "So I did some mining off camera...",
    "Math equation": "Who even does math in here?",
    "1": "The first character.",
    "2": "The second character.",
    "3": "The third character.",
    "4": "The fourth character.",
    "5": "The fifth character.",
    "Lever": "Flippity flip floppity flop.",
    "Portal to the outside": "Win the game. \nFinally. I'm done with programming this.",
    "Tutorial": "Welcome to Minery!",
}
'''These two contain different information.'''
renderList = []  #Responsible for list of object images to display
objectsOnScreen = []  #Responsible for list of object data currently on screen

objectName = ''  #Name of object character is standing on.
useObject = False  #If player is attempting to use an object.
altObject = False  #Alternate function for objects
actionError = ''

moveSpeed = 20  #Character move speed, set 0 for max speed
moveSpeedTicks = 0  #Character move speed buff length
characterX = 3  #Position in the current grid
characterY = 3

mapX = 0  #Position in the world.
mapY = 0

worldSize = 8  #How big the world as a square (size x size)

globalMineList = []  #List of mine data
renderNewMine = True  #Generate new data or not
depthTier = 1

#Bag weights of each ore.
stoneWeight = 1  # $5/kg
copperWeight = 5  # $6/kg
ironWeight = 25  # $8/kg
goldWeight = 100  # $10/kg
diamondWeight = 500  # $16/kg

stonePrice = 2  #Sell prices of each ore.
copperPrice = 15
ironPrice = 100
goldPrice = 500
diamondPrice = 4000

stoneAmount = 0  #The number of each ore in your bag.
copperAmount = 0
ironAmount = 0
goldAmount = 0
diamondAmount = 0

maxBackpack = 20 #Maximum backpack weight
currentBackpack = 0  #Current Backpack weight
backpackTier = 1  #Just for renderShop

pickaxeTier = 1  #Determines what ore can be mined.
autoMine = False

coins = 0
confirmPurchase = False  #If shop is in confirm purchase mode
affordable = False  #If item is affordable
transactionResult = False  #Result of purchase

#
#Shop items
#
teleportUnlocked = False  #TP upgrade
teleportX = 0
teleportY = 0
richCharmUnlocked = False  #Rich charm upgrade
couponRate = 1  #Coupon bonus on top of rich charm
stripMinerUnlocked = False  #Strip miner upgrade
stripMining = False

inMine = False  #If character is in the mines or in the base
inShop = False  #If the character is in lobby or in shop
inCodeRoom = False  #If character is in the code room

#Objective and game variables
#These variables are for the quests and objectives.

dogHintFound = False  #Checks if the dog letter has been found. Activates the dog riddle sequence.
dogUnlocked = False  #If the dog has been found by knocking 5 times.
ballFound = False  #If the ball has been found in the mines.
useCounter = 0

huntCompleted = False  #If scavenging hunt is finished
searchLevel = 0

steveLevel = 0

useShopWall = False  #Shop wall
ancientWritingPurchased = False  #If the ancient paper in the script has been purchased

codeRoomUnlocked = False
codeList = ["", "", "", "", ""]
winCondition = False


#
# FUNCTIONS
#
def printError(string='', update=False):
    '''
  If theres a message that needs to be printed, overrides object function
  Not a very important function.

  @param string - The string to print
  @param update - Update the string to print, or print the current string.
  '''
    global actionError
    if update:
        actionError = string
    else:
        print(actionError)


def round_num(n, decimal=2):
    '''
    Library:  numerize
              by David Sa
  '''
    n = Decimal(n)
    return n.to_integral() if n == n.to_integral() else round(
        n.normalize(), decimal)


def numerize(n, decimal=1):
    '''
    Library:  numerize
              by David Sa
    I just had to change the suffix 'k' since I preferred the lowercase form
    Also fixed some code snippets since it returns "None" instead of 0 when given 0
  '''
    sufixes = ["", "k", "M"]

    sci_expr = [1e0, 1e3, 1e6]

    for x in range(len(sci_expr)):
        if n >= sci_expr[x] and n < sci_expr[x + 1]:
            sufix = sufixes[x]
            if n >= 1e3:
                num = str(round_num(n / sci_expr[x], decimal))
            else:
                num = str(n)
            return num + sufix
        elif n == 0:
            return 0


def nothing():
    '''
  This function does nothing. It is used to prevent crashes when a specified function cannot be found.
  '''
    pass


def renderLobby():  #Loads all of the objects that are on lobby.
    '''
  This function loads objects in the lobby.
  '''

    renderObject(1, 3, "Sell area")  #Sell area
    renderObject(5, 3, "Door")  #Door to shop
    renderObject(3, 5, "Ladder down")
    if pickaxeTier == 1:
        renderObject(3, 3, "Tutorial")
    else:
        renderObject(5, 1, "Tutorial")

    if pickaxeTier >= 3:
        renderObject(5, 5, "Special chest")

    if not codeRoomUnlocked:
        if not dogUnlocked:
            #Checks if dog objective has been complete. If not, keep as mystery door.
            renderObject(3, 1, "Mystery door")
        else:
            renderObject(3, 1, "Dog")
    else:
        renderObject(3, 1, "Door")

    if ancientWritingPurchased:  #Checks if ancient script has been purchased
        renderObject(1, 1, "Ancient writing")


def renderShop():
    '''
  This function loads objects from the shop.
  '''

    global useShopWall
    renderObject(1, 3, "Door")

    if pickaxeTier <= 1:
        objectsDescription[
            "Pickaxe upgrade"] = "Enough of your beat-up stone pickaxe. Let's upgrade to some copper."
        renderObject(1, 1, "Pickaxe upgrade")

    if pickaxeTier <= 2:
        objectsDescription[
            "Pickaxe upgrade"] = "Copper is so useless nowadays. Try iron, I give it 10/10"
        renderObject(2, 1, "Pickaxe upgrade")

    if pickaxeTier <= 3:
        objectsDescription[
            "Pickaxe upgrade"] = "Buy this if you want to flex your financial instability."
        renderObject(3, 1, "Pickaxe upgrade")

    if pickaxeTier <= 4:
        objectsDescription[
            "Pickaxe upgrade"] = "A diamond pickaxe? What is this, Minecraft?"
        renderObject(4, 1, "Pickaxe upgrade")

    if backpackTier <= 1:
        renderObject(1, 5, "Backpack upgrade")
    if backpackTier <= 2:
        renderObject(2, 5, "Backpack upgrade")
    if backpackTier <= 3:
        renderObject(3, 5, "Backpack upgrade")
    if backpackTier <= 4:
        renderObject(4, 5, "Backpack upgrade")
    if backpackTier >= 5:
        renderObject(5, 5, "Backpack upgrade")
        objectsDescription[
            "Backpack upgrade"] = "I mean, bigger is better!"

    if teleportUnlocked == False:
        renderObject(5, 2, "Teleport upgrade")

    if richCharmUnlocked == False:
        renderObject(5, 4, "Rich charm")

    if stripMinerUnlocked == False:
        renderObject(5, 3, "Strip miner")

    if useShopWall and characterX == 5 and characterY == 1:
        if not ancientWritingPurchased:
            if pickaxeTier > 3:
                printError("You broke through the wall! And you found a box.",
                           True)
                renderObject(5, 1, "Box in wall")
            else:
                printError(
                    Fore.WHITE + Style.DIM +
                    "Seems like this cracked wall is pretty sturdy...\nMaybe a better pickaxe might help?"
                    + Style.RESET_ALL, True)
                useShopWall = False


def renderCodeRoom():
    '''
  This function renders the secret code room in order to win
  '''
    renderObject(3, 5, "Door")
    renderObject(1, 5, "Math equation")
    renderObject(1, 2, "1")
    renderObject(2, 2, "2")
    renderObject(3, 2, "3")
    renderObject(4, 2, "4")
    renderObject(5, 2, "5")
    renderObject(5, 5, "Lever")
    if winCondition:
        renderObject(3, 1, "Portal to the outside")


def renderMines():
    '''
  This function processes and renders mine data, and generates new data if needed or empty.
  '''
    global mapX
    global mapY
    global worldSize
    global renderNewMine
    global depthTier

    depth = mapX + mapY

    if depth <= 4 and depth > 1:
        depthTier = 1
    elif depth <= 6 and depth > 4:
        depthTier = 2
    elif depth <= 8 and depth > 6:
        depthTier = 3
    elif depth <= 12 and depth > 8:
        depthTier = 4
    elif depth <= 16 and depth > 12:
        depthTier = 5

    if renderNewMine:  #Create world empty 8x8 mines
        globalMineList.clear()  #clears all mines
        for x in range(worldSize):
            globalMineList.append([])  #Add row
            for y in range(worldSize):
                globalMineList[x].append([])  #Add column
        renderNewMine = False

    currentMine = globalMineList[mapX -
                                 1][mapY -
                                    1]  #Convert coordinates to array index
    if not currentMine:  #if current mine is empty
        generateNewMine(mapX - 1,
                        mapY - 1)  #Convert coordinates to array index

    for x, row in enumerate(globalMineList[mapX - 1][mapY - 1]):
        for y, item in enumerate(row):
            if item != '':
                checkItem = checkSpecialRender(mapX, mapY, x + 1, y + 1)
                if checkItem == False:  #Check if new item added to special renders
                    renderObject(x + 1, y + 1, item)
                else:
                    globalMineList[mapX - 1][mapY -
                                             1][x][y] = checkItem  #Update data
                    renderObject(x + 1, y + 1, checkItem)  #Render new object


def checkSpecialRender(worldX, worldY, x, y):
    '''
  List special cases where mines need to render specific objects at specific cases
  such as ladders, doors, and story objects.

  @param worldX - the object's world X position
  @param worldY - the object's world Y position
  @param x - the object's grid X position
  @param y - the object's grid Y position
  '''
    posX = x
    posY = y
    mapX = worldX
    mapY = worldY

    if mapX == 1 and mapY == 1:
        if posX == 3 and posY == 1:
            return "Ladder up"

    if mapX == 5 and mapY == 3:
        if posX == 4 and posY == 2:
            return "Random letter"

    if dogHintFound:
        if mapX == 7 and mapY == 5:
            if posX == 2 and posY == 5:
                return "Ball"

    if codeRoomUnlocked:
        if mapX == 1 and mapY == 1:
            if posX == 1 and posY == 1:
                return "Dog"

    if pickaxeTier >= 2:
        if mapX == 1 and mapY == 1:
            if posX == 5 and posY == 5:
                return "Steve"

    if searchLevel >= 1:
        if mapX == 2 and mapY == 3:
            if posX == 1 and posY == 1:
                return "Special chest"
    if searchLevel >= 2:
        if mapX == 4 and mapY == 1:
            if posX == 2 and posY == 5:
                return "Special chest"
    if searchLevel >= 3:
        if mapX == 3 and mapY == 6:
            if posX == 3 and posY == 2:
                return "Special chest"
    if searchLevel >= 4:
        if mapX == 5 and mapY == 5:
            if posX == 2 and posY == 3:
                return "Special chest"
    if searchLevel >= 5:
        if mapX == 3 and mapY == 1:
            if posX == 2 and posY == 4:
                return "Special chest"
    if searchLevel >= 6:
        if mapX == 8 and mapY == 2:
            if posX == 3 and posY == 1:
                return "Special chest"
    if searchLevel >= 7:
        if mapX == 5 and mapY == 8:
            if posX == 1 and posY == 4:
                return "Special chest"
    if searchLevel >= 8:
        if mapX == 8 and mapY == 7:
            if posX == 2 and posY == 4:
                return "Special chest"
    if searchLevel >= 9:
        if mapX == 1 and mapY == 1:
            if posX == 5 and posY == 1:
                return "Special chest"

    return False


def generateNewMine(mapX, mapY):
    '''
  This function generates a new array of ore at a specified map location.
  @param mapX - The mine to generate's X position relative to world position.
  @param mapY - The mine to generate's Y position relative to world position.
  '''
    global globalMineList
    global depthTier

    scramble = 0

    objectToRender = ''
    currentMine = globalMineList[mapX][mapY]
    for x in range(5):
        currentMine.append([])  #Add 5 arrays
        for y in range(5):  #Per row in grid
            scramble = randint(1, 100)  #Randomize number
            if checkSpecialRender(
                    mapX + 1, mapY + 1, x + 1,
                    y + 1) == False:  #If no special object in location
                if scramble <= 2:
                    print(x + 1, y + 1)
                    objectToRender = 'Chest'
                elif depthTier == 1:
                    objectToRender = 'Stone'
                elif depthTier == 2:
                    if scramble > 2 and scramble <= 32:
                        objectToRender = 'Copper'
                    else:
                        objectToRender = 'Stone'
                elif depthTier == 3:
                    if scramble > 2 and scramble <= 32:
                        objectToRender = 'Iron'
                    elif scramble > 32 and scramble < 82:
                        objectToRender = 'Copper'
                    else:
                        objectToRender = 'Stone'
                elif depthTier == 4:
                    if scramble > 2 and scramble <= 32:
                        objectToRender = 'Gold'
                    elif scramble > 32 and scramble <= 82:
                        objectToRender = 'Iron'
                    elif scramble > 82 and scramble <= 921:
                        objectToRender = 'Copper'
                    else:
                        objectToRender = 'Stone'
                elif depthTier == 5:
                    if scramble > 2 and scramble <= 17:
                        objectToRender = 'Diamond'
                    elif scramble > 17 and scramble <= 42:
                        objectToRender = 'Gold'
                    elif scramble > 42 and scramble <= 87:
                        objectToRender = 'Iron'
                    elif scramble > 87 and scramble <= 97:
                        objectToRender = 'Copper'
                    else:
                        objectToRender = 'Stone'
                globalMineList[mapX][mapY][x].append(
                    objectToRender)  #In each array in main list add ore
            else:
                globalMineList[mapX][mapY][x].append(
                    checkSpecialRender(mapX + 1, mapY + 1, x + 1, y + 1))


def renderMap():  #Display map
    '''
  This function processes and prints out the map.
  '''
    renderY = 0
    renderX = 0
    printLine = 0
    global inShop

    #Render grid

    for column in range(5):  #For each row
        renderY += 1
        renderX = 0

        for line in range(4):  #Prints lines separating cells
            #Range 4 to make way for broken shop wall
            print(Fore.WHITE + Style.DIM + "+ - ", end='')
        if not inShop or column != 0:
            print(Fore.WHITE + Style.DIM + "+ - ", end='')
        elif column == 0:  #If in shop and has broken wall
            print("+", end='')
            print(Style.RESET_ALL + Fore.BLACK + Style.BRIGHT + " ~ " +
                  Style.RESET_ALL,
                  end='')
        print(Fore.WHITE + Style.DIM + "+", end='')

        printInformation(printLine)
        printLine += 1

        for bars in range(5):  #Per row cell
            renderX += 1
            print(Fore.WHITE + Style.DIM + "|", end='')
            print(Style.RESET_ALL, end='')

            if renderX == characterX and renderY == characterY:
                print(objectIcons["Character"], end='')
            else:
                print(getRenderObject(renderX, renderY), end='')

        print(Fore.WHITE + Style.DIM + "|", end='')
        printInformation(printLine)
        printLine += 1
    for line in range(5):  # Last line
        print(Fore.WHITE + Style.DIM + "+ - ", end='')
    print("+", end='')
    printInformation(printLine)
    printLine += 1


def getRenderObject(checkRenderX, checkRenderY):
    '''
  This function returns the image of the object to render. Only used in renderMap()
  @param checkRenderX - The currently-rendered cell's X position
  @param checkRenderY - The currently-rendered cell's Y position
  '''
    for index, obj in enumerate(renderList):
        posX = obj[0]
        posY = obj[1]
        objectString = obj[2]
        if checkRenderX == posX and checkRenderY == posY:
            del renderList[index]  #Remove from list of items to render.
            return objectString
    return "   "


def renderObject(posX, posY, objectName):  #Render object at specific location
    '''
  This function adds an object to be rendered at a specified position.
  '''
    objectString = objectIcons[objectName]  #Get image of object to render
    objectDescription = objectsDescription[
        objectName]  #Get description of object to render
    renderList.append(
        (posX, posY, objectString))  #Add object image to renderlist at

    if (posX, posY, objectName, objectDescription) not in objectsOnScreen:
        #Checks if object not already in list of objects on screen
        objectsOnScreen.append((posX, posY, objectName, objectDescription))
        #Adds object to list of objects on screen


def printInformation(lineNumber):
    '''
  This function prints out the information sidebar beside the map.

  @param lineNumber - The line number to print specific information on of the map
  '''
    global characterX
    global characterY
    global mapX
    global mapY
    global inMine
    global inShop
    global stoneAmount
    global copperAmount
    global ironAmount
    global goldAmount
    global diamondAmount
    global maxBackpack
    global currentBackpack
    global pickaxeTier
    print(Style.RESET_ALL, end='')  #Clear styling
    if lineNumber == 0:
        print(Style.RESET_ALL + Fore.GREEN + Style.BRIGHT +
              "   -------INFORMATION-------")
        print(Style.RESET_ALL, end='')
    elif lineNumber == 2:
        if not inMine:
            if not inShop:
                print(Fore.CYAN + Style.BRIGHT + "             Lobby" +
                      Style.RESET_ALL)
            else:
                print(Fore.CYAN + Style.BRIGHT + "           Item shop " +
                      Style.RESET_ALL)
        else:
            print(Fore.YELLOW + Style.BRIGHT + "           The Mines " +
                  Style.RESET_ALL)
    elif lineNumber == 4:
        if not inMine:
            print("    Coins:", end='')
            print(Fore.YELLOW + Style.BRIGHT + str(coins).center(11) +
                  Style.RESET_ALL)
        elif inMine:
            print("   ", end='')
            if pickaxeTier == 1:
                print(Fore.WHITE + Style.DIM +
                      str(numerize(stoneAmount)).center(25) + Style.RESET_ALL)
            elif pickaxeTier == 2:
                print(" ", end='')
                print(Fore.WHITE + Style.DIM +
                      str(numerize(stoneAmount)).center(12) + Style.RESET_ALL,
                      end='')
                print(Fore.RED + Style.BRIGHT +
                      str(numerize(copperAmount)).center(12) + Style.RESET_ALL)
            elif pickaxeTier == 3:
                print(" ", end='')
                print(Fore.WHITE + Style.DIM +
                      str(numerize(stoneAmount)).center(8) + Style.RESET_ALL,
                      end='')
                print(Fore.RED + Style.BRIGHT +
                      str(numerize(copperAmount)).center(8) + Style.RESET_ALL,
                      end='')
                print(Fore.WHITE + Style.NORMAL +
                      str(numerize(ironAmount)).center(8) + Style.RESET_ALL)
            elif pickaxeTier == 4:
                print(' ', end='')
                print(Fore.WHITE + Style.DIM +
                      str(numerize(stoneAmount)).center(6) + Style.RESET_ALL,
                      end='')
                print(Fore.RED + Style.BRIGHT +
                      str(numerize(copperAmount)).center(6) + Style.RESET_ALL,
                      end='')
                print(Fore.WHITE + Style.NORMAL +
                      str(numerize(ironAmount)).center(6) + Style.RESET_ALL,
                      end='')
                print(Fore.YELLOW + Style.BRIGHT +
                      str(numerize(goldAmount)).center(6))
            elif pickaxeTier == 5:
                print(Fore.WHITE + Style.DIM +
                      str(numerize(stoneAmount)).center(5) + Style.RESET_ALL,
                      end='')
                print(Fore.RED + Style.BRIGHT +
                      str(numerize(copperAmount)).center(5) + Style.RESET_ALL,
                      end='')
                print(Fore.WHITE + Style.NORMAL +
                      str(numerize(ironAmount)).center(5) + Style.RESET_ALL,
                      end='')
                print(Fore.YELLOW + Style.BRIGHT +
                      str(numerize(goldAmount)).center(5),
                      end='')
                print(Fore.CYAN + str(numerize(diamondAmount)).center(5) +
                      Style.RESET_ALL)
        else:
            print()
    elif lineNumber == 5:
        if inMine:
            print("   ", end='')
            if currentBackpack < maxBackpack / 10 * 4:
                print(Fore.WHITE, end='')
            elif currentBackpack < maxBackpack / 10 * 7:
                print(Fore.GREEN, end='')
            elif currentBackpack < maxBackpack / 10 * 9:
                print(Fore.YELLOW, end='')
            else:
                print(Fore.RED, end='')
            print((str(currentBackpack) + ' / ' + str(maxBackpack)).center(25))
        else:
            print()
    elif lineNumber == 6:
        if inMine:
            print("        ", end='')
            print(Fore.WHITE + Style.DIM + "Pickaxe Tier " + str(pickaxeTier) +
                  Style.RESET_ALL)
        else:
            print()
    elif lineNumber == 7:
        print("          X:", characterX, "  Y:", characterY, end=' ')
        if moveSpeedTicks > 0:
            print(Fore.BLUE + "≈:", numerize(moveSpeedTicks), Style.RESET_ALL)
        else:
            print()
    elif lineNumber == 8:
        if inMine:
            if depthTier == 1:
                print(Fore.WHITE + Style.DIM, end='')
            elif depthTier == 2:
                print(Fore.RED + Style.BRIGHT, end='')
            elif depthTier == 3:
                print(Fore.WHITE + Style.BRIGHT, end='')
            elif depthTier == 4:
                print(Fore.YELLOW + Style.BRIGHT, end='')
            elif depthTier == 5:
                print(Fore.CYAN + Style.BRIGHT, end='')
            print("  " + (" Depth: " + str(mapX + mapY) + "   Layer: " +
                          str(depthTier)).center(25) + Style.RESET_ALL)
        else:
            print()
    elif lineNumber == 9:
        if inMine:
            print("    World X:", mapX, "  World Y:", mapY)
        else:
            print()
    elif lineNumber == 10:
        print(Style.RESET_ALL + Fore.GREEN + Style.BRIGHT +
              "   -------------------------")
        print(Style.RESET_ALL, end='')
    else:
        print()
    #Too confusing so clarify:
    #Prints character location.
    #Format changes based on if character is in lobby, in shop, or in the mines.


def objectDescription(
        printDescription=False):  #Print object name and description
    '''
  This function prints out information of the current object, as well as defining current object name for other functions to use.
  '''
    for index, obj in enumerate(
            objectsOnScreen):  #Check list of objects on screen
        posX = obj[0]
        posY = obj[1]
        global objectName
        objectName = obj[
            2]  #Set current object name to the current object in the list
        objectDescription = obj[3]
        if characterX == posX and characterY == posY:  #If charcter is on object position
            del objectsOnScreen[index]
            #Remove from list of objects on screen
            #This is to prevent double-rendering and having objects stay on screen.

            #Print item description
            if printDescription == True:
                print(Style.RESET_ALL + Fore.BLUE + Style.BRIGHT + "\nΓ ",
                      end='')
                print(objectName, end=' ⅃\n')
                print(Style.RESET_ALL + Fore.CYAN + Style.BRIGHT +
                      objectDescription + Style.RESET_ALL)
            break
        #If object name is found, program stops there. Howvever, if there is no object, objectName will be replaced to empty, which basically means .
        objectName = ""


def moveInterrupt():
    '''
  This function interrupts transactions and other stuff when moving.
  '''
    global actionError
    global confirmPurchase
    global transactionResult
    global moveSpeedTicks
    global moveSpeed
    global useCounter
    useCounter = 0
    confirmPurchase = False
    transactionResult = False
    sleep(1 / moveSpeed)  # Prevent superfast moving
    if moveSpeedTicks == 0:
        moveSpeed = 20
    else:
        moveSpeedTicks -= 1
        moveSpeed = 60
    actionError = ''


def moveCharacter():
    '''
  This function moves the character across maps and areas, while also handling key inputs.
  '''
    global characterY
    global characterX
    global mapX
    global mapY
    global inMine
    global inShop
    global inCodeRoom
    global useObject
    global altObject
    global objectName
    global key
    global worldSize
    global autoMine
    global stripMining
    global stripMinerUnlocked
    global depthTier
    global moveSpeed
    global teleportUnlocked
    global teleportX
    global teleportY
    global teleportMapX
    global teleportMapY
    global useShopWall

    if key == 'w' or key == keys.UP:
        if not inMine:
            if not inShop:
                if not inCodeRoom:
                    if characterY - 1 > 0:
                        characterY -= 1
                        moveInterrupt()
                    if objectName == "Door" and characterY == 1:
                        useObject = True
                else:
                    if characterY - 1 > 0:
                        characterY -= 1
                        moveInterrupt()
            else:
                if characterX == 5 and characterY == 1:
                    if not ancientWritingPurchased:
                        useShopWall = True
                elif characterY - 1 > 0:
                    characterY -= 1
                    moveInterrupt()
        else:
            if characterY - 1 > 0:
                characterY -= 1
                moveInterrupt()
            elif characterY - 1 == 0 and mapY - 1 > 0:
                characterY = 5
                moveInterrupt()
                mapY -= 1

        if objectName == "Ladder up":
            useObject = True

    elif key == 'a' or key == keys.LEFT:
        if not inMine:
            if characterX - 1 > 0:
                characterX -= 1
                moveInterrupt()

            if objectName == "Door":
                useObject = True

        else:
            if characterX - 1 > 0:
                characterX -= 1
                moveInterrupt()
            elif characterX - 1 == 0 and mapX - 1 > 0:
                characterX = 5
                moveInterrupt()
                mapX -= 1

    elif key == 's' or key == keys.DOWN:
        if not inMine:
            if not inCodeRoom:
                if characterY + 1 < 6:
                    characterY += 1
                    moveInterrupt()

                if objectName == "Ladder down":
                    useObject = True
            else:
                if characterY + 1 < 6:
                    characterY += 1
                    moveInterrupt()

                if objectName == "Door":
                    useObject = True

        else:
            if characterY + 1 < 6:
                characterY += 1
                moveInterrupt()
            elif characterY + 1 == 6 and mapY + 1 < worldSize + 1:
                if pickaxeTier >= depthTier:
                    characterY = 1
                    moveInterrupt()
                    mapY += 1
                else:
                    printError(
                        Style.RESET_ALL + Fore.BLUE + Style.DIM +
                        "Seems like the rock wall is too hard to break through.\n   You might need a tougher pickaxe."
                        + Style.RESET_ALL, True)

    elif key == 'd' or key == keys.RIGHT:
        if not inMine:
            if characterX + 1 < 6:
                characterX += 1
                moveInterrupt()

            if objectName == "Door":
                useObject = True

        else:
            if characterX + 1 < 6:
                characterX += 1
                moveInterrupt()
            elif characterX + 1 == 6 and mapX + 1 < worldSize + 1:
                if pickaxeTier >= depthTier:
                    characterX = 1
                    moveInterrupt()
                    mapX += 1
                else:
                    printError(
                        Style.RESET_ALL + Fore.BLUE + Style.DIM +
                        "Seems like the rock wall is too hard to break through.\n   You might need a tougher pickaxe.",
                        True)
    elif teleportUnlocked and key == 't':
        if inMine:
            teleportX = characterX
            teleportY = characterY
            teleportMapX = mapX
            teleportMapY = mapY
            inMine = False
            inShop = False
            characterX = 3
            characterY = 3
        else:
            if teleportX != 0 and teleportY != 0:
                inMine = True
                inShop = False
                characterX = teleportX
                characterY = teleportY
                teleportX = 0
                teleportY = 0
            else:
                printError("Nowhere to teleport back to!", True)
    elif inMine and stripMinerUnlocked and key == 'u':
        if stripMining:
            stripMining = False
        else:
            stripMining = True

    elif key == 'j':  #If player uses object
        useObject = True
    elif key == 'k':
        altObject = True
    elif key == 'h':
        if inMine:
            if autoMine:
                autoMine = False
            else:
                autoMine = True

    if moveSpeed > 0:
        sleep(1 /
              moveSpeed)  #Stop constant update so you don't move at 3000km/h


def getObjectActions():
    '''
  This function calls the function which processes the current object.
  If there is no object, do nothing.
  '''
    #Get list of actions and run object code
    if objectName in objectsActions:
        objectsActions[objectName]()
    else:
        nothing()


def shopScreen(price):
    '''
  This function handles purchases and transactions.
  The parameter intakes the price of the object.

  If not enough coins, the affordable variable will be false, and the transaction will decline on attempt to purchase.

  If the transaction is successful, this method returns true and goes back to the object in the shop.

  If unsuccessful, returns false.
  
  @param price - an integer for the price of the object 
  '''
    global coins
    global useObject
    global confirmPurchase
    global affordable
    global transactionResult

    #Displays coins and price
    print("\nPrice:", Fore.GREEN + Style.BRIGHT + str(price) + Style.RESET_ALL)
    print("You have",
          Fore.YELLOW + Style.BRIGHT + str(coins) + Style.RESET_ALL, "coins.")

    #Check affordability
    if coins - price >= 0:
        affordable = True
    else:
        affordable = False

    #When standing on unpurchased object
    if not useObject and confirmPurchase == False and not transactionResult:
        print("\nPurchase?")
        print("\n  Actions:\n [J] - Purchase item")

    #Go to confirm purchase section
    elif useObject and confirmPurchase == False and not transactionResult:
        confirmPurchase = True

    #Loops here if attempting to confirm purchase
    elif not useObject and confirmPurchase and affordable:
        print(
            "\nConfirm purchase? You will have",
            Fore.YELLOW + Style.BRIGHT + str(coins - price) + Style.RESET_ALL,
            "coins left.")
        print("\n  Actions:\n [J] - Confirm")

    #Make the transaction and return back to object function
    elif useObject and confirmPurchase and affordable:
        confirmPurchase = False
        coins -= price
        return True  #Transaction complete

    #If unable to afford
    elif not useObject and confirmPurchase and not affordable:
        print(Fore.RED + Style.BRIGHT +
              "\nYou don't have enough coins! You need" + Style.RESET_ALL,
              end=' ')
        print(
            Fore.YELLOW + Style.BRIGHT + str(price - coins) + Style.RESET_ALL +
            Fore.RED + Style.BRIGHT, "more coins.")

    return False  #Transaction incomplete if broken


'''
These functions will handle the behaviors of all the object types.
'''


def tutorial():
    global useObject
    if not useObject:
        if coins == 0 and pickaxeTier == 1 and backpackTier == 1 and currentBackpack == 0:
            print("Hey! Welcome to Minery. Let's get you set up.")
            print("\n  Actions:\n [J] - Start")
        elif coins == 0 and pickaxeTier == 1 and backpackTier == 1 and currentBackpack > 0:
            print("Welcome back! Go and sell your ores for money.")
            print("\n  Actions:\n [J] - Next")
        else:
            print("Reread tutorial?")
            print("\n  Actions:\n [J] - Read")
    if useObject:
        if coins == 0 and pickaxeTier == 1 and backpackTier == 1 and currentBackpack == 0:
            print("To move around, use WASD or the arrow keys.")
            print("To interact with objects, press J or K.")
            print(Fore.WHITE + Style.DIM +
                  "Sometimes there won't be an indicator to press J!" +
                  Style.RESET_ALL)
            print("\nThe objective of this game is to mine ore and sell ore.")
            print(
                "\nLet's give it a try. Go down into the mines and mine some ore."
            )
        elif coins >= 0 and pickaxeTier == 1 and backpackTier == 1 and currentBackpack > 0:
            print("The mining world is an 8 x 8 grid. ")
            print("You can move left and right to change worlds.")
            print("The \'Depth\' shows how deep you are.")
            print("Your depth is based on your X and Y world coordinates.")
            print("\nThe deeper you are, the better the ores.")
            print(
                "However, you will need a bigger backpack and pickaxe to mine better ores."
            )
            print("\nYou can find the shop with the door on the right.")
            print(
                Fore.MAGENTA +
                "\nScattered around everywhere are some secrets and puzzles.")
            print(
                "Hope you can solve them and uncover the truth of this world..."
            )
            print("After all, you ARE trying to get up back to the surface.")
        else:
            print("To move around, use WASD or the arrow keys.")
            print("To interact with objects, press J or K.")
            print(Fore.WHITE + Style.DIM +
                  "Sometimes there won't be an indicator to press J!" +
                  Style.RESET_ALL)
            print("\nThe objective of this game is to mine ore and sell ore.")
            print("The mining world is an 8 x 8 grid. ")
            print("You can move left and right to change worlds.")
            print("Your depth is based on your X and Y world coordinates.")
            print("\nThe deeper you are, the better the ores.")
            print(
                "However, you will need a bigger backpack and pickaxe to mine better ores."
            )
            print("\nYou can find the shop with the door on the right.")
            print(
                Fore.MAGENTA +
                "\nScattered around everywhere are some secrets and puzzles.")
            print(
                "Hope you can solve them and uncover the truth of this world..."
            )
            print("After all, you ARE trying to get up back to the surface.")
    useObject = False


def door():
    '''
  This function handles doors and switching between shop and lobby
  '''

    global characterX
    global characterY
    global inMine
    global inShop
    global inCodeRoom
    global useObject

    if not inMine:
        if not inShop:
            if not inCodeRoom:
                if not useObject and characterX == 5:
                    print(Style.NORMAL + "\nThis door takes you to the shop.")
                    print("\n  Actions:\n [D / LEFT] [J] - Use door")
                elif useObject and characterX == 5:  #To shop
                    inShop = True
                    characterX = 1
                elif not useObject and characterY == 1:
                    print(Style.NORMAL +
                          "\nThis door takes you to the secret room.")
                    print("\n  Actions:\n [W / UP] [J] - Use door")
                elif useObject and characterY == 1:  #To Code room
                    inCodeRoom = True
                    characterY = 5
            elif inCodeRoom:
                if not useObject:
                    print(Style.NORMAL +
                          "\nThis door takes you back to the main room.")
                    print("\n  Actions:\n [S / DOWN] [J] - Use door")
                if useObject:
                    characterY = 1
                    inCodeRoom = False
        elif inShop:
            if not useObject:
                print(Style.NORMAL + "\nThis door takes you to the main room.")
                print("\n  Actions:\n [A / RIGHT] [J] - Use door")
            if useObject:
                characterX = 5
                inShop = False


def ladder():
    '''
  This function handles the ladders to and from the mines. 
  Enter the mine, or regenerate the map by pressing K.
  '''
    global characterX
    global characterY
    global inMine
    global useObject
    global renderNewMine
    global mapX
    global mapY
    global teleportX
    global teleportY
    if not inMine:
        if not useObject:
            print(Style.NORMAL + "Enter the mines?")
            print("\n  Actions:\n [S / Down] [J] - Enter mines")
            print("\n [K] - Reset mines")
        elif (useObject or key == 's' or key == keys.DOWN) and not altObject:
            mapX = 1
            mapY = 1
            teleportX = 0
            teleportY = 0
            characterY = 1
            inMine = True
        if altObject:
            renderNewMine = True
            printError(
                Style.BRIGHT + Fore.BLUE + "You have reset the mines!" +
                Fore.MAGENTA +
                "\n\nAll the ores have magically reappeared... \nand perhaps you can find some more treasure~~"
                + Style.RESET_ALL, True)
    else:
        if not useObject:
            print(Style.NORMAL + "\nGo back to lobby?")
            print("\n  Actions:\n [W / Up] [J] - Return to lobby")
        elif useObject or key == 'W' or key == keys.UP:
            teleportX = 0
            teleportY = 0
            mapX = 0
            mapY = 0
            characterY = 5
            inMine = False


def winAward():
    global useObject
    global winCondition
    if not useObject:
        print("A door to the outside appears.")
        print("\n  Actions:\n [J] - Open door")
    elif useObject:
        clearBoard()
        print("+ - + - + - + - + - + - + - + - + - + - +")
        print(" __     __                    _       _ ")
        print(" \ \   / /                   (_)     | |")
        print("  \ \_/ /__  _   _  __      ___ _ __ | |")
        print("   \   / _ \| | | | \ \ /\ / / | '_ \| |")
        print("    | | (_) | |_| |  \ V  V /| | | | |_|")
        print("    |_|\___/ \__,_|   \_/\_/ |_|_| |_(_)")
        print("\n+ - + - + - + - + - + - + - + - + - + - +")
        print("Thanks for playing!\n".center(41))
        print("Game by Leo Lin".center(41))
        print("Jan 26, 2022".center(41))
        print("Last updated: Mar 22, 2023".center(41))
        print("\n  Actions:\n[Move anywhere] - Go back, not that there's a point haha")
        useObject = False


def lever():
    global codeList
    global useObject
    global winCondition
    if not useObject:
        print("Flip the lever?")
        print("\n  Actions:\n [J] - Flip lever")
    elif useObject:
        if ''.join(codeList) == "5USH1":
            print(Fore.MAGENTA + "Something happened..." + Style.RESET_ALL)
            winCondition = True

            #dont let lever do anything if steve, hunt, or code is not found
        else:
            print(Fore.RED + Style.BRIGHT + "The code is incorrect." +
                  Style.RESET_ALL)
        useObject = False


def codeBlock():
    global codeList
    global useObject
    if not useObject:
        print("Enter a character?")
        print("\n  Actions:\n [J] - Enter a letter")
    if useObject:
        print("Enter a character below:")
        codeKey = getkey()
        codeList[characterX - 1] = str(codeKey).upper()
        print("\nYou entered:", Fore.BLUE + codeKey.upper() + Style.RESET_ALL)
        if codeList[characterX - 1].isalnum():
            objectIcons[str(characterX)] = "[" + Fore.BLUE + codeList[
                characterX - 1] + Style.RESET_ALL + "]"
        else:
            print("That isn't a valid character.")
            objectIcons[str(characterX)] = "[ ]"
            if ''.join(codeList) == "5USH1":
                print("You win!")
        useObject = False


def steve():
    '''
  Steve the NPC. 
  '''
    global useObject
    global altObject
    global useCounter
    global stoneAmount
    global copperAmount
    global ironAmount
    global goldAmount
    global diamondAmount
    global currentBackpack
    global coins
    global steveLevel
    global moveSpeedTicks
    if not useObject:
        if steveLevel == 0:
            print("A random person sits there menacingly. Talk to him?")
            print("\n  Actions:\n [J] - Talk")
        if steveLevel == 1:
            print("Steve needs 15 stone for the base of his machine.")
            print("\n  Actions:\n [J] - Give")
        if steveLevel == 2:
            print("Steve is working away on his machine.")
            print("\n  Actions:\n [J] - Talk")
        if steveLevel == 3:
            print("Steve needs 10 copper for the wires.")
            print("\n  Actions:\n [J] - Give")
        if steveLevel == 4:
            print("Steve is busy stringing up wires.")
            print("\n  Actions:\n [J] - Talk")
        if steveLevel == 5:
            print("Steve needs 20 iron for screws and metal plates.")
            print("\n  Actions:\n [J] - Give")
        if steveLevel == 6:
            print("Steve is busy constructing the machine.")
            print("\n  Actions:\n [J] - Talk")
        if steveLevel == 7:
            print("Steve needs 10 gold for the circuits and electronics.")
            print("\n  Actions:\n [J] - Give")
        if steveLevel == 8:
            print("Steve is busy doing nerdy stuff.")
            print("\n  Actions:\n [J] - Talk")
        if steveLevel == 9:
            print("Steve needs 5 diamonds for the magic core.")
            print("\n  Actions:\n [J] - Give")
        if steveLevel == 10:
            print("Steve is making the magic core. Interesting.")
            print("\n  Actions:\n [J] - Talk")
        if steveLevel == 11:
            print("Steve needs 100 coins to test his speed machine.")
            print("\n  Actions:\n [J] - Give")
        if steveLevel == 12:
            print("The machine works! Talk to Steve about it?")
            print("\n  Actions:\n [J] - Talk")
        if steveLevel == 13:
            print(
                "The speed machine will allow you\nto move faster for a certain period of time.\nHowever, it costs coins because well... \nsomeone needs to be paid, right?"
            )
            print("\n  Actions:\n [J] - Talk to Steve")
            print("\n [K] - Use and pay 100 coins")

    if useObject:
        if steveLevel == 0:
            print(
                "\"Hey what's up! \nMight sound funny but could you help fetch me some stone? \nI think 15 might be good enough.\""
            )
            steveLevel += 1
        elif steveLevel == 1:
            if stoneAmount >= 15:
                print(
                    "\"Thanks man. I'm just working on this machine here and \nI think it's gonna be really nice.\""
                )
                stoneAmount -= 15
                currentBackpack -= 15 * stoneWeight
                steveLevel += 1
                objectsDescription[
                    "Steve"] = "Well this weird guy wants to hog your ores..."
            else:
                print("\"Buddy I said 15, you've got too little!\"")
        elif steveLevel == 2:
            print(
                "\"Hey again, could you fetch me some copper? \nI need some for the wires.\n10 copper should be good enough.\""
            )
            steveLevel += 1
        elif steveLevel == 3:
            if copperAmount >= 10:
                print(
                    "\"Thanks a lot. Copper is so useless no one is even selling it anywhere.\""
                )
                copperAmount -= 10
                currentBackpack -= 10 * copperWeight
                steveLevel += 1
            else:
                print("\"I need 10, wires are really important you know!\"")
        elif steveLevel == 4:
            print(
                "\"Alright, the wires are done now. \nI just need some screws and metal plates.\nI need a lot, could you get me 20?\""
            )
            steveLevel += 1
        elif steveLevel == 5:
            if ironAmount >= 20:
                print(
                    "\"Alrighty! This should be good enough. Thanks as always.\""
                )
                ironAmount -= 20
                currentBackpack -= 20 * ironWeight
                steveLevel += 1
            else:
                print("\"This machine won't work without 20 iron!\"")
        elif steveLevel == 6:
            print(
                "\"Now I need some gold for the electronics. \nWould you bother passing me... let's say 10 gold?\""
            )
            steveLevel += 1
        elif steveLevel == 7:
            if goldAmount >= 10:
                print("\"Nice. We're almost done building.\"")
                goldAmount -= 10
                currentBackpack -= 10 * goldWeight
                steveLevel += 1
            else:
                print("\"I need 10 gold for the electronics!\"")
        elif steveLevel == 8:
            print(
                "\"The last thing I need is a few diamonds to build a magic core. \nI only need 5.\""
            )
            steveLevel += 1
        elif steveLevel == 9:
            if diamondAmount >= 5:
                print(
                    "\"Alright, that should be it! We're ready to rock and roll!\""
                )
                diamondAmount -= 5
                currentBackpack -= 5 * diamondWeight
                steveLevel += 1
            else:
                print("\"I just need 5 diamonds. No more.\"")
        elif steveLevel == 10:
            print(
                "\"The machine is done! Now we need to test. I need to put in 100 coins and we'll see...\""
            )
            steveLevel += 1
        elif steveLevel == 11:
            if coins >= 100:
                print(
                    "\"Anddd... we're done! You should now be moving super speedy.\""
                )
                coins -= 100
                steveLevel += 1
                moveSpeedTicks += 100
            else:
                print(
                    "\"100 coins is barely anything. Please. I just need that little.\""
                )
        elif steveLevel == 12:
            print(
                "\"Thanks so much for helping me out! \nI'm going to patent this as soon as I get outside"
            )
            print("Now. Before I go do that, I need to thank you.")
            print(
                "\nThe first thing I'm going to do is allow you to use my machine."
            )
            print(
                "It works like a vending machine: pay 100 coins and it'll give you a speed boost."
            )
            print(
                "\nThe second thing is a little puzzle that will help you if you solve it. \nAre you ready?"
            )
            print("\nIt is:")
            print(
                "The first part of the code is the number of vowels in the English alphabet\""
            )
            steveLevel += 1
            objectsDescription[
                "Steve"] = "Legends say that Steve still didn't patent his machine."
        elif steveLevel == 13:
            print("\"Forgot the puzzle? Here it is again:")
            print(
                "\nThe first part of the code is the number of vowels in the English alphabet\""
            )
        useObject = False

    if altObject:
        if steveLevel == 13:
            if coins >= 100:
                print(
                    "Refreshed your speed boost! It is effective for 100 more blocks."
                )
                coins -= 100
                moveSpeedTicks += 100

            else:
                print("You don't have enough coins!")
            altObject = False


def mathEquation():
    '''
  Prints the math equation riddle
  '''
    print("Slot = 5")
    print("Code = " + Fore.CYAN + "[[( x / 1+8 )^5x/2 ]^3 + ( 5 + x/5 )^9 ]^0")


def mystery():
    '''
  This function handles the mystery and knocking on the door.
  '''
    global useCounter
    global dogHintFound
    global dogUnlocked
    global useObject
    if not useObject:
        if dogHintFound:
            print("  Actions:\n [J] - Knock")
    if useObject:
        useCounter += 1
        if not dogHintFound:
            if useCounter == 1:
                print(Fore.WHITE + Style.DIM + "." + Style.RESET_ALL)
            if useCounter == 3:
                print(Fore.WHITE + Style.DIM + ".." + Style.RESET_ALL)
            if useCounter == 7:
                print(Fore.WHITE + Style.DIM + "..." + Style.RESET_ALL)
            if useCounter >= 10:
                print(Fore.WHITE + Style.DIM + "World (5, 3)....?")
            useObject = False
        else:
            if useCounter == 5:
                dogUnlocked = True


def dogHint():
    '''
  Prints out the dog hint found at world (5,3)
  '''
    global useObject
    global dogHintFound
    if not useObject:
        print("Read the letter?")
        print("\n  Actions:\n  [J] - Read")
    elif useObject:
        print("\nThe letter reads:")
        print("--------------------------------------")
        print("To whoever finds this...\n")
        print("If you knock the door 5 times, my pet dog will answer.")
        print("Don't worry, he can never die of hunger or dehydration.")
        print(
            "However, his only weakness is that he's been bored for centuries."
        )
        print(
            "I've pretty sure I kept his dog toys is somewhere in world (7, 5)"
        )
        print("\nI just needed him to guard something for me...")
        dogHintFound = True
        useObject = False


def ball():
    global useObject
    global ballFound
    if not useObject:
        print("Take the ball?")
        print("\n  Actions:\n  [J] - Take")
    elif useObject:
        print("\nWell you now have a ball. It's in pretty good condition")
        print("considering it's been down here for centuries...")
        print("These mines is getting weirder by the day...")
        ballFound = True
        useObject = False


def dog():
    '''
  Prints out the dog hint found at world (5,3)
  '''
    global useObject
    global ballFound
    global altObject
    global codeRoomUnlocked
    if not useObject:
        if not codeRoomUnlocked:
            print("Grrr.....")
            print("I think he's bored.")
            print("\n  Actions:\n  [J] - Talk")
            if ballFound:
                print("\n  [K] - Give him the ball")
        else:
            print(
                "The happy and joyful dog is bouncing around and playing with his tennis ball."
            )
            print("He seems to be standing above a little hole.")
            print("\n  Actions:\n  [J] - Dig")
    if useObject:
        if not codeRoomUnlocked:
            print("He says:")
            print("bark bark bark bark bark bark bark woof\n")
            print("bark bark bark bark bark woof")
            print(
                "\n\x1B[3mWhy did he bark 7 times, then bark another 5 times?\nIs he trying to tell us a location?"
            )
            print(
                "I don't know. Talking with dogs in the first place is weird enough..."
            )
        else:
            print("You found a stone tablet which says:")
            print("----------------------------------------")
            print("\"Thank you so much for helping my dog. In exchange,")
            print(
                "I want to thank you by telling you a secret that will help you:"
            )
            print("The second one is U\"")
            print("----------------------------------------")
            print(
                "\nYou might never know what it means, but it'll surely come in handy eventually."
            )

        useObject = False
    if altObject:
        if not codeRoomUnlocked:
            if ballFound:
                print(
                    "The dog, now satisfied, runs down into the mines. \nBehind him stood a door that you've never seen before.\n"
                )

                print(
                    "Perhaps it might be a good idea to chase after the dog?\n"
                )
                print(
                    "\x1B[3mWe still don't know what 'guard' means from the letter however..."
                )
                codeRoomUnlocked = True
                altObject = False


def ancientWriting():
    '''
  This function handles purchasing the ancient writing, and displaying in the lobby.
  '''

    global transactionResult
    global ancientWritingPurchased
    global useObject
    if ancientWritingPurchased == False:
        print("But it has a price tag of 50000? It's so expensive...")
        if not transactionResult:
            #Run shop transaction
            transactionResult = shopScreen(50000)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                ancientWritingPurchased = True

                print("\nWeird. You actually bought an overpriced box.")
                print(
                    "\nEven more weird, you open up the box and find a piece of ancient writing? \nWell good luck reading that."
                )

    #This part handles the ancient writing if in the lobby
    if not useObject and ancientWritingPurchased and not inShop:
        print("\nHope you can read scripts in a language that nobody knows.")
        print("\n  Actions:\n  [J] - Read")

    #When reading, print riddle.
    elif useObject and ancientWritingPurchased and not inShop:
        print("\nThe paper reads:")
        print("--------------------------------------")
        print(" 1. abcdefghijklmnopqrstuvwxyz")
        print(" 2. WKH WKLUG FKDUDFWHU LV V")
        print("\n Someone's commentary:")
        print(
            "\n The people here decided that our language was really funny. ")
        print(" So we decided to make a new language.")
        print(" \n Let's see... maybe it should use the same alphabet.")
        print(
            " Oh, and maybe we can translate into the new language\n by moving the letters 3 spaces backwards!"
        )
        print(" This will be a very genius solution!")
        print(" \n- said some random ancient people")
        print("--------------------------------------")
        print("\x1B[3mSeems like a lot of details are irrelevant here.")
        useObject = False


def pickaxeUpgrade():
    '''
  Handles the shop and purchasing the pickaxe upgrades.
  '''
    global currentBackpack
    global pickaxeTier
    global characterX
    global characterY
    global transactionResult
    global stoneAmount
    global copperAmount
    global ironAmount
    global goldAmount
    global stoneWeight
    global copperWeight
    global ironWeight
    global goldWeight
    if characterX == 1:
        print(
            "Upgrade your current pickaxe to Tier 2, allowing you to mine copper."
        )
        print("\nPickaxe refurbishment requirements: 10 stone")
        if stoneAmount < 10:
            print(Fore.RED + "You need more stone!" + Style.RESET_ALL)
        if not transactionResult:
            #Run shop transaction
            transactionResult = shopScreen(1000)
        else:
            #Run when transaction is successful
            if stoneAmount >= 10:
                if transactionResult == True:
                    pickaxeTier = 2
                    stoneAmount -= 10
                    currentBackpack -= stoneAmount * stoneWeight
                    print("\nNice! You can now mine copper.")
            else:
                print(Fore.RED + "You need more stone! You currently have " + stoneAmount + "stone." + Style.RESET_ALL)

    elif characterX == 2:
        print(
            "Upgrade your current pickaxe to Tier 3, allowing you to mine iron."
        )
        print("\nPickaxe refurbishment requirements: 20 copper")
        if copperAmount < 20:
            print(Fore.RED + "You need more copper!" + Style.RESET_ALL)
        if not transactionResult:
            #Run shop transaction
            transactionResult = shopScreen(5000)
        else:
            #Run when transaction is successful
            if copperAmount >= 20:
                if transactionResult == True:
                    pickaxeTier = 3
                    copperAmount -= 20
                    currentBackpack -= copperAmount * copperWeight
                    print("\nNice! You can now mine iron.")
            else:
                print(Fore.RED + "You need more copper! You currently have " + copperAmount + "copper." + Style.RESET_ALL)
    elif characterX == 3:
        print(
            "Upgrade your current pickaxe to Tier 4, allowing you to mine gold."
        )
        print("\nPickaxe refurbishment requirements: 30 iron")
        if ironAmount < 30:
            print(Fore.RED + "You need more iron!" + Style.RESET_ALL)
        if not transactionResult:
            #Run shop transaction
            transactionResult = shopScreen(40000)
        else:
            #Run when transaction is successful
            if ironAmount >= 30:
                if transactionResult == True:
                    pickaxeTier = 4
                    ironAmount -= 30
                    currentBackpack -= ironAmount * ironWeight
                    print("\nNice! You can now mine gold.")
            else:
                print(Fore.RED + "You need more iron! You currently have " + ironAmount + "iron." + Style.RESET_ALL)
    elif characterX == 4:
        print(
            "Upgrade your current pickaxe to Tier 5, allowing you to mine diamonds."
        )
        print("\nPickaxe refurbishment requirements: 50 gold")
        if goldAmount >= 50:
            print(Fore.RED + "You need more gold!" + Style.RESET_ALL)
        if not transactionResult:
            #Run shop transaction
            transactionResult = shopScreen(120000)
        else:
            #Run when transaction is successful
            if goldAmount >= 50:
                if transactionResult == True:
                    pickaxeTier = 5
                    goldAmount -= 50
                    currentBackpack -= goldAmount * goldWeight
                    print("\nNice! You can now mine diamonds.")
            else:
                print(Fore.RED + "You need more gold! You currently have " + goldAmount + "gold." + Style.RESET_ALL)
            


def backpackUpgrade():
    '''
  Handles the shop and purchasing backpack upgrades.
  '''
    global characterX
    global characterY
    global transactionResult
    global maxBackpack
    global backpackTier
    if characterX == 1:
        print(
            "Buy a bigger backpack, which allows you to mine more ore.\nThis bag has 150 capacity."
        )
        if not transactionResult:
            if backpackTier == 1:
                transactionResult = shopScreen(500)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                backpackTier = 2
                maxBackpack = 150
                print("\nYour backpack limit has increased from 20 to 150.")
    if characterX == 2:
        print(
            "Buy a bigger backpack, which allows you to mine more ore.\nThis bag has 500 capacity."
        )
        if not transactionResult:
            if backpackTier == 2:
                transactionResult = shopScreen(4500)
            else:
                print(Fore.RED +
                      "\nYou need to buy the previous backpacks first!" +
                      Style.RESET_ALL)
                print(
                    Fore.WHITE + Style.DIM +
                    "Believe it or not, we stitch the \nold bags onto the new ones so..."
                    + Style.RESET_ALL)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                backpackTier = 3
                maxBackpack = 500
                print("\nYour backpack limit has increased from 150 to 500.")
    if characterX == 3:
        print(
            "Buy a bigger backpack, which allows you to mine more ore.\nThis bag has 2500 capacity."
        )
        if not transactionResult:
            if backpackTier == 3:
                transactionResult = shopScreen(25000)
            else:
                print(Fore.RED +
                      "\nYou need to buy the previous backpacks first!" +
                      Style.RESET_ALL)
                print(
                    Fore.WHITE + Style.DIM +
                    "Believe it or not, we stitch the \nold bags onto the new ones so..."
                    + Style.RESET_ALL)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                backpackTier = 4
                maxBackpack = 2500
                print("\nYour backpack limit has increased from 500 to 2500.")
    if characterX == 4 and backpackTier <= 4:
        print(
            "Buy a bigger backpack, which allows you to mine more ore.\nThis bag has 10000 capacity."
        )
        if not transactionResult:
            if backpackTier == 4:
                transactionResult = shopScreen(100000)
            else:
                print(Fore.RED +
                      "\nYou need to buy the previous backpacks first!" +
                      Style.RESET_ALL)
                print(
                    Fore.WHITE + Style.DIM +
                    "Believe it or not, we stitch the \nold bags onto the new ones so..."
                    + Style.RESET_ALL)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                backpackTier = 5
                maxBackpack = 10000
                print(
                    "\nYour backpack limit has increased from 2500 to 10000.")
    if characterX == 5 and backpackTier >= 5:
        print(
            "Upgrade your current backpack to have more storage. \nThis bag has" + maxBackpack*2 + "capacity."
        )
        if not transactionResult:
                transactionResult = shopScreen(100000 * (backpackTier - 4)*1.5)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                backpackTier = 5
                
                print(
                    "\nYour backpack limit has increased from"+ maxBackpack + "to" + maxBackpack*1.25 + ".")
                maxBackpack *= 1.25



def stripMiner():
    '''
  Only responsible for selling the strip miner. The actual strip mining is in mine()
  '''
    global stripMinerUnlocked
    global transactionResult
    if stripMinerUnlocked == False:

        if transactionResult == False:
            print(
                "Very powerful tool that clears the entire row you're standing on. \nExcess ores over backpack limit don't count toward size limit."
            )
            transactionResult = shopScreen(100000)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                stripMinerUnlocked = True  #Enable riddle quest
                print("You can now strip mine by pressing [U].")


def teleport():
    '''
  Only responsible for selling the teleport. The actual teleporting is in moveCharacter()
  '''
    global teleport
    global transactionResult
    global teleportUnlocked
    if teleportUnlocked == False:

        if transactionResult == False:
            print(
                "Teleport back to base, and back to your previous mine position by pressing T."
            )
            transactionResult = shopScreen(5000)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                teleportUnlocked = True  #Enable riddle quest
                print(
                    "You can now teleport back to base with by pressing [T].")


def richCharm():
    '''
  Only responsible for selling the rich charm. The actual selling is in sellArea()
  '''
    global richCharmUnlocked
    global transactionResult
    if richCharmUnlocked == False:
        if transactionResult == False:
            print("Earn 2x more coins when selling ores.")
            transactionResult = shopScreen(10000)
        else:
            #Run when transaction is successful
            if transactionResult == True:
                richCharmUnlocked = True  #Enable riddle quest
                print("You now earn 2x more coins.")


def sellArea():
    '''
  This function processes selling ore and adding money. 
  '''
    global coins
    global stoneWeight
    global stonePrice
    global stoneAmount

    global copperWeight
    global copperPrice
    global copperAmount

    global ironWeight
    global ironPrice
    global ironAmount

    global goldWeight
    global goldPrice
    global goldAmount

    global diamondWeight
    global diamondPrice
    global diamondAmount

    global maxBackpack
    global currentBackpack

    global useObject
    global richCharmUnlocked
    global couponRate

    totalPrice = 0

    totalPrice += stoneAmount * stonePrice
    totalPrice += copperAmount * copperPrice
    totalPrice += ironAmount * ironPrice
    totalPrice += goldAmount * goldPrice
    totalPrice += diamondAmount * diamondPrice

    #Check bonuses
    totalPrice *= couponRate
    totalPrice = int(totalPrice)  #Round to remove decimals
    if richCharmUnlocked:
        totalPrice *= 2

    if not useObject and currentBackpack > 0:
        print("Sell ores?")
        print("\n  Actions:\n [J] - Sell ores for", totalPrice, "coins")
        if richCharmUnlocked:
            print(Fore.GREEN + "Rich charm bonus: 2x" + Style.RESET_ALL)
        if couponRate > 1:
            print(Fore.CYAN + "         Coupon bonus:",
                  str(int((couponRate - 1) * 100)) + "%", Style.RESET_ALL)
    elif not useObject and currentBackpack == 0:
        print("Sell absolutely nothing?")
        print("\n Actions:\n [J] - cry and cope because you have no ores")

    #Sell
    if useObject and currentBackpack > 0:
        coins += totalPrice
        currentBackpack = 0
        stoneAmount = 0
        copperAmount = 0
        ironAmount = 0
        goldAmount = 0
        diamondAmount = 0
        couponRate = 1

        print("You now have",
              Fore.YELLOW + Style.BRIGHT + str(coins) + Style.RESET_ALL,
              "coins.")
        useObject = False

    elif useObject and currentBackpack == 0:
        print("You have nothing to sell at the moment :(")
        print("Go mine up some ore!")
        useObject = False

    #Price breakdown
    if currentBackpack > 0:
        print("\nPrice breakdown:")
        print("----------------------------------")
        if stoneAmount > 0:
            print(
                "", (str(numerize(stoneAmount)) + " stone").ljust(12),
                'x $ ' + str(stonePrice), '   =', Fore.YELLOW + Style.BRIGHT +
                str(stoneAmount * stonePrice) + Style.RESET_ALL)
        if copperAmount > 0:
            print(
                "", (str(numerize(copperAmount)) + " copper").ljust(12),
                'x $ ' + str(copperPrice), '  =', Fore.YELLOW + Style.BRIGHT +
                str(copperAmount * copperPrice) + Style.RESET_ALL)
        if ironAmount > 0:
            print(
                "", (str(numerize(ironAmount)) + " iron").ljust(12),
                'x $ ' + str(ironPrice), ' =', Fore.YELLOW + Style.BRIGHT +
                str(ironAmount * ironPrice) + Style.RESET_ALL)
        if goldAmount > 0:
            print(
                "", (str(numerize(goldAmount)) + " gold").ljust(12),
                'x $ ' + str(goldPrice), '=', Fore.YELLOW + Style.BRIGHT +
                str(goldAmount * goldPrice) + Style.RESET_ALL)
        if diamondAmount > 0:
            print(
                "", (str(numerize(diamondAmount)) + " diamonds").ljust(12),
                'x $ ' + str(diamondPrice), '=', Fore.YELLOW + Style.BRIGHT +
                str(diamondAmount * diamondPrice) + Style.RESET_ALL)
        if richCharmUnlocked == True:
            print(" Rich charm bonus      = " + Fore.CYAN + "2x" +
                  Style.RESET_ALL)
        if couponRate > 1:
            print(" Coupon bonus          = " + Fore.CYAN + str(couponRate) +
                  "x" + Style.RESET_ALL)


def mine():
    '''
  This function mines ore and adds to the ore count.
  Also handles strip mining
  '''

    global stoneWeight
    global stoneAmount

    global copperWeight
    global copperAmount

    global ironWeight
    global ironAmount

    global goldWeight
    global goldAmount

    global diamondWeight
    global diamondAmount
    global oreAmount
    global oreWeight

    global autoMine
    global pickaxeTier

    global objectName
    global maxBackpack
    global currentBackpack
    global characterX
    global characterY
    global mapX
    global mapY
    global useObject
    global actionError
    global stripMining
    global stripMinerUnlocked
    weight = oreWeight[objectName]
    if weight + currentBackpack <= maxBackpack:
        if not useObject and not autoMine and not actionError:
            print("Mine ore?")
            print("  Actions:\n [J] - Mine")
            print("\n [H] - Enable auto mine")
            if stripMinerUnlocked:
                if stripMining:
                    print("\n [U] - Disable strip mining")
                else:
                    print("\n [U] - Enable strip mining")
        if useObject or autoMine:
            if weight + currentBackpack <= maxBackpack:
                loopCount = 1
                if stripMining:
                    loopCount = 5
                for x in range(loopCount):
                    if objectName == 'Stone':
                        stoneAmount += 1
                        globalMineList[mapX - 1][mapY - 1][characterX -
                                                           1][characterY -
                                                              1] = ''
                        currentBackpack += weight
                    elif objectName == 'Copper':
                        if pickaxeTier >= 2:
                            copperAmount += 1
                            globalMineList[mapX - 1][mapY - 1][characterX -
                                                               1][characterY -
                                                                  1] = ''
                            currentBackpack += weight
                        else:
                            if not stripMining:
                                print(
                                    "You need Pickaxe Tier 2 to mine copper.")
                            useObject = False
                    elif objectName == 'Iron':
                        if pickaxeTier >= 3:
                            ironAmount += 1
                            globalMineList[mapX - 1][mapY - 1][characterX -
                                                               1][characterY -
                                                                  1] = ''
                            currentBackpack += weight
                        else:
                            if not stripMining:
                                print("You need Pickaxe Tier 3 to mine iron.")
                            useObject = False
                    elif objectName == 'Gold':
                        if pickaxeTier >= 4:
                            goldAmount += 1
                            globalMineList[mapX - 1][mapY - 1][characterX -
                                                               1][characterY -
                                                                  1] = ''
                            currentBackpack += weight
                        else:
                            if not stripMining:
                                print(
                                    "You need at least Pickaxe Tier 4 to mine gold."
                                )
                            useObject = False
                    elif objectName == 'Diamond':
                        if pickaxeTier >= 5:
                            diamondAmount += 1
                            globalMineList[mapX - 1][mapY - 1][characterX -
                                                               1][characterY -
                                                                  1] = ''
                            currentBackpack += weight
                        else:
                            if not stripMining:
                                print(
                                    "You need Pickaxe Tier 5 to mine diamonds."
                                )
                            useObject = False
                    if loopCount == 5:
                        if characterX + 1 == 6:
                            characterX = 0
                        characterX += 1
                        objectDescription()
    else:
        if currentBackpack < maxBackpack:
            print("You need more bag space to mine this.")
        else:
            print("Your bag is full!")


def chest():
    '''
  This function handles treasure chests and its loot
  '''
    global stripMining
    global depthTier
    global coins
    global moveSpeed
    global moveSpeedTicks
    global couponRate
    global globalMineList
    global currentBackpack
    global useObject
    global stoneAmount
    global copperAmount
    global ironAmount
    global goldAmount
    global diamondAmount
    if not useObject:
        print("Open chest?")
        print("\n [J] - Open chest")
    elif useObject:
        scramble = randint(1, 100)
        globalMineList[mapX - 1][mapY - 1][characterX - 1][characterY - 1] = ''
        if scramble <= 30:  #Flat amount of money
            chestCoins = 0
            if pickaxeTier == 1:
                chestCoins = randint(25, 100)
            elif pickaxeTier == 2:
                chestCoins = randint(100, 500)
            elif pickaxeTier == 3:
                chestCoins = randint(500, 1000)
            elif pickaxeTier == 4 or depthTier == 5:
                chestCoins = randint(1000, 5000)
            print("You found", chestCoins, "coins!")
            coins += chestCoins
        elif scramble > 30 and scramble <= 60:  #Flat amount of ores in tier
            chestOreAmount = randint(3, 10)
            chestOreName = ''
            if depthTier == 1:
                chestOreName = 'stone!'
                stoneAmount += chestOreAmount
            elif depthTier == 2:
                chestOreName = 'copper!'
                copperAmount += chestOreAmount
            elif depthTier == 3:
                chestOreName = 'iron!'
                ironAmount += chestOreAmount
            elif depthTier == 4:
                chestOreName = 'gold!'
                goldAmount += chestOreAmount
            elif depthTier == 5:
                chestOreName = 'diamonds!'
                diamondAmount += chestOreAmount
            print("You found a bag of", chestOreAmount, chestOreName)
            print(
                "\nThe ores came in another bag so \nthey don't count towards your weight limit."
            )
        elif (scramble > 60
              and scramble <= 80) or (scramble > 90 and scramble <= 100
                                      and couponRate > 1):  #Movement speed
            if moveSpeedTicks == 0:
                print(
                    "You found a movement speed potion!\n It is effective for 75 blocks."
                )
                moveSpeedTicks = 75
            else:
                print(
                    "You refreshed your movement speed!\n It is effective for an extra 75 blocks."
                )
                moveSpeedTicks += 75
        elif (scramble > 80 and scramble <= 90):  #Better ores
            chestOreAmount = randint(1, 3)
            chestOreName = ''
            if depthTier == 1:
                chestOreName = 'copper!'
                copperAmount += chestOreAmount
            elif depthTier == 2:
                chestOreName = 'iron!'
                ironAmount += chestOreAmount
            elif depthTier == 3:
                chestOreName = 'gold!'
                goldAmount += chestOreAmount
            elif depthTier == 4:
                chestOreName = 'diamonds!'
                diamondAmount += chestOreAmount
            print(Fore.GREEN + "Wow! You found a bag of", chestOreAmount,
                  chestOreName + Style.RESET_ALL)
            print(
                "\nThe ores came in another bag so \nthey don't count towards your weight limit."
            )
        elif scramble > 90 and scramble <= 100 and couponRate == 1:  #Coupons
            coupon = randint(1, 4)
            print("You found a coupon for", str(coupon * 25) + "% more coins!")
            print("Your next ore sell will have this added bonus.")
            couponRate = (coupon * 25 / 100) + 1
        useObject = False


def specialChest():
    '''
  This function handles the scavenger hunt treasure chest quest.
  '''
    global useObject
    global huntCompleted
    global searchLevel

    if not useObject:
        print("Open chest?")
        print("\n [J] - Open chest")
    elif useObject:
        if not inMine:
            print("World (2, 3)")
            if searchLevel == 0:
                searchLevel += 1
        if mapX == 2 and mapY == 3:
            print("World (4, 1)")
            if(searchLevel == 1):
                searchLevel += 1
        if mapX == 4 and mapY == 1:
            print("World (3, 6)")
            if(searchLevel == 2):
                searchLevel += 1
        if mapX == 3 and mapY == 6:
            print("World (5, 5)")
            if(searchLevel == 3):
                searchLevel += 1
        if mapX == 5 and mapY == 5:
            print("World (3, 1)")
            if(searchLevel == 4):
                searchLevel += 1
        if mapX == 3 and mapY == 1:
            print("World (8, 2)")
            if(searchLevel == 5):
                searchLevel += 1
        if mapX == 8 and mapY == 2:
            print("World (5, 8)")
            if(searchLevel == 6):
                searchLevel += 1
        if mapX == 5 and mapY == 8:
            print("World (8, 7)")
            if(searchLevel == 7):
                searchLevel += 1
        if mapX == 8 and mapY == 7:
            print("World (1, 1)")
            if(searchLevel == 8):
                searchLevel += 1
            huntCompleted = True
        if mapX == 1 and mapY == 1 and huntCompleted:
            print(
                "That must've taken you a while. \nCongratulations on finishing. \nSlot 4 = H"
            )
        useObject = False


#This dictionary directs ore name with its appropriate ore weight
oreWeight = {
    "Stone": stoneWeight,
    "Copper": copperWeight,
    "Iron": ironWeight,
    "Gold": goldWeight,
    "Diamond": diamondWeight,
    "Chest": 0,
}

#This dictionary directs object name with its appropriate object behavior function.
objectsActions = {
    "Door": door,
    "Sell area": sellArea,
    "Backpack upgrade": backpackUpgrade,
    "Pickaxe upgrade": pickaxeUpgrade,
    "Teleport upgrade": teleport,
    "Rich charm": richCharm,
    "Strip miner": stripMiner,
    "Chest": chest,
    "Special chest": specialChest,
    "Stone": mine,
    "Copper": mine,
    "Iron": mine,
    "Gold": mine,
    "Diamond": mine,
    "Ancient writing": ancientWriting,
    "Box in wall": ancientWriting,
    "Mystery door": mystery,
    "Random letter": dogHint,
    "Dog": dog,
    "Ball": ball,
    "Steve": steve,
    "Ladder down": ladder,
    "Ladder up": ladder,
    "Math equation": mathEquation,
    "1": codeBlock,
    "2": codeBlock,
    "3": codeBlock,
    "4": codeBlock,
    "5": codeBlock,
    "Lever": lever,
    "Portal to the outside": winAward,
    "Tutorial": tutorial,
}

testing = False  #Just for testing purposes and debugging
if testing == True:
    searchLevel = 0
    coins = 10000000
    pickaxeTier = 5
    maxBackpack = 1000000000
    currentBackpack = maxBackpack
    stoneAmount = 100000
    goldAmount = 10000
    ironAmount = 10000
    copperAmount = 10000
    diamondAmount = 10000
    moveSpeedTicks = 10000
    dogFound = True
    dogHintFound = True
    codeRoomUnlocked = True

if False:
    searchLevel = 0
    coins = 10000000
    pickaxeTier = 5
    maxBackpack = 1000000000
    currentBackpack = maxBackpack
    stoneAmount = 100000
    goldAmount = 10000
    ironAmount = 10000
    copperAmount = 10000
    diamondAmount = 10000
    moveSpeedTicks = 10000
    dogFound = True
    dogHintFound = True
    codeRoomUnlocked = True
'''
This is the main loop that runs the game.
'''
while running:

    #Handle rendering screen
    objectsOnScreen.clear()  #Clear list of current objects
    if not inMine:
        if not inShop:
            if not inCodeRoom:
                renderLobby()  #If in lobby, render lobby.
            else:
                renderCodeRoom()  #If in code room, render code room.
        else:
            renderShop()  #If in shop, render shop.
    elif inMine:
        renderMines()  #If in mines, render mines.

    #Clear board
    clearBoard()
    renderMap()  #Print map

    renderList.clear()  #Remove delayed rendering

    #Handle object descriptions and behavior
    objectDescription(True)
    printError()
    getObjectActions()
    if autoMine:
        if inMine:
            print("\n  Actions:\n [H] - Disable auto mine\n")

    if teleportUnlocked:
        if teleportX != 0 and teleportY != 0:
            if autoMine == False:
                print("\n  Actions:")
            print(
                " [T] - Teleport to world (" + str(mapX) + " , " + str(mapY) +
                ") position (" + str(teleportX), ",",
                str(teleportY) + ")")
        else:
            if inMine:
                print("\n [T] - Teleport back to base")

    #Reset useObject
    #skip waiting for a new keypress and loop back to object function
    if useObject == True:
        useObject = False
        key = ""
    elif altObject == True:
        altObject = False
        key = ""
    else:
        key = getkey()  #Get a new key input.

    #Handle character movements
    #character inputs
    moveCharacter()
