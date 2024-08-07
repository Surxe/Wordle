import colorama #pip install colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import os
import datetime
from datetime import timedelta
from random import sample
import time
from collections import Counter

def clearConsole():
  command = 'clear'
  if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
    command = 'cls'
  os.system(command)
clearConsole()
def makeWordList(fileName):
  #take .txt and make it into a list
  f = open('src/'+fileName, 'r')
  lst = f.readlines()
  for i in range(len(lst)):
    if ("\n" in lst[i]): #elem contains \n, remove it
      lst[i] = lst[i][0:len(lst[i])-1] #substring of elem without 1char \n
  return lst

def getTodaysWord(wordList): #returns number of days since the first wordle
  today = datetime.date.today()
  todayEST = today + timedelta(hours=0) #adjust for eastern timezone
  firstDay = datetime.date(2021, 6, 16)
  numDaysDiff = (todayEST-firstDay).days #days since first wordle, to be index for wordList
  word = wordList[numDaysDiff-1]
  #print(word) #debug
  #time.sleep(3) #debug
  return word

def getTodaysNum():
  today = datetime.date.today()
  todayEST = today + timedelta(hours=0, minutes=-43) #adjust for eastern timezone
  firstDay = datetime.date(2021, 6, 16)
  numDaysDiff = (todayEST-firstDay).days #days since first wordle, to be index for wordList
  wordleNum = numDaysDiff-3 #wordle number
  return wordleNum


def getRandomWord(wordPool): #get a random word for continuous playing
  while True:
    word = sample(wordPool, 1)[0] #yields 1word array, so get 0th index
    if isUniqueChars(word):
      break #satifying condition = no duplicates
  #print(word) #debug
  #time.sleep(3) #debug
  return word

def isUniqueChars(word):
  freq = Counter(word)
  return (len(freq) == len(word)) #returns True or False

def buildMatrix(rows, cols, defaultText):
  matrix=[[defaultText for x in range(cols)] for y in range(rows)] #initialize matrix with correct size
  return matrix

def makeWordArray(word): #put each character of word into 1 element in a list
  wordArray = []
  for i in range(len(word)):
    wordArray.append(word[i:i+1])
  return wordArray

def inputMode(displayHeader, canShare):
  if (displayHeader == True):
    print("Choose a mode by typing an option:", sep='')
    print(f"- \"Help\" {Style.DIM}to receive instructions on how WORDLE works")
    print(f"- \"Today\" {Style.DIM}to play for today's word")
    print(f"- \"Play\" {Style.DIM}to play the game for a random word")
    print(f"- \"Quit\" {Style.DIM}to exit the program")
  if (displayHeader == True and canShare == True):
    print(f"- \"Share\" {Style.DIM}to share your results spoiler-free")
  #print(f"- \"Average\" {Style.DIM}to check the average amount of \n  guesses to guess a specific word")
  #print(f"- \"AI\" {Style.DIM}to have a smart AI try to guess a specific word")
  modeChoice = input(Fore.MAGENTA + ">")
  return modeChoice.lower()

def printKeyboard(letters, numGuess, guesses, lettersStatus, keyboardStatus): #go back and use getCharColor()
  #update first
  for i in reversed(range(numGuess)):
    for j in range(len(lettersStatus[0])):
      elemStatus = lettersStatus[i][j] #letter status/color
      elem = guesses[i][j]             #letter
      elemI = letters.index(elem)      #letter index 0-25
      if (keyboardStatus[elemI] != "Green"):
        keyboardStatus[elemI] = elemStatus
      else:
        keyboardStatus[elemI] = "Green"
  
  #print next
  for i in range(len(keyboardStatus)): 
    elem = keyboardStatus[i]
    if (elem=="White"):
      print(Back.BLACK + " " + letters[i] + " ", " ", sep='', end='')
    elif (elem=="Green"):
      print(Back.GREEN + " " + letters[i] + " ", " ", sep='', end='')
    elif (elem=="Yellow"):
      print(Back.YELLOW + " " + letters[i] + " ", " ", sep='', end='')
    elif (elem=="Red"):
      print(Back.RED + " " + letters[i] + " ", " ", sep='', end='')
      #print(Style.RESET_ALL, Back.BLACK, sep='', end='')
    else:
      print("error, element status not found")

    if (i==10-1): #formatting for each row to look like a keyboard
      print()
      for j in range(26+4):
        print(" ", sep='', end='')
      print("\n", "  ", sep='', end='')
    elif(i==19-1):
      print(" ", sep='')
      for k in range(26+4):
        print(" ", sep='', end='')
      print("\n", "  ", sep='', end='')
      print("  ", end='')
    elif(i==26-1):
      print("     ", sep='')
  
def printHelp():
  colorama.init(autoreset=True)
  print(Style.RESET_ALL)
  print("Guess the WORDLE in 6 tries.")
  print("Each guess must be a valid 5 letter word. \nHit the enter button to submit.")
  print("After each guess, the color of the tiles will\nchange to show how close your guess was to the word.")
  print(f"\n{Back.BLACK} W ", " = ", sep='', end='') #Red
  print(f"{Style.DIM}The letter W has not been involved in a guess", sep='')
  print(f"\n{Back.GREEN} A ", " = ", sep='', end='') #Green
  print(f"{Style.DIM}The letter A is in the word and in the correct spot", sep='')
  print(f"\n{Back.YELLOW} S ", " = ", sep='', end='') #Yellow
  print(f"{Style.DIM}The letter S is in the word but in the wrong spot", sep='')
  print(f"\n{Back.RED} D ", " = ", sep='', end='') #Red
  print(f"{Style.DIM}The letter D is not in the word in any spot", sep='')
  print()
  print(f"Credit to: {Style.DIM}https://www.nytimes.com/games/wordle/index.html", sep='')
  print()

def printPlayBoard(matrix, letters, lettersStatus, numGuess, isCorrect):
  for j in range(43):
    print(Style.RESET_ALL + "_", end='')
  print()
  for i in range(len(matrix)):
    for j in range(len(matrix[i])):
      elem=matrix[i][j]
      color = getCharColor(i, j, lettersStatus)
      if i==numGuess-1:
        if isCorrect:
          color = Style.RESET_ALL
        else:
          color = Back.WHITE
      print("│" + color + "‾‾‾‾‾", "│", sep='', end='  ')
    print()
    for j in range(len(matrix[i])):
      elem=matrix[i][j]
      color = getCharColor(i, j, lettersStatus)
      if i==numGuess-1:
        if isCorrect:
          color = Style.RESET_ALL
        else:
          color = Back.WHITE
      if (elem == " "): #empty, bc theres no guesses yet
        print("│", color + "  " + matrix[i][j] + "  ", "│  ", sep='', end='')
      else:
        print("│", color + "  " + elem + "  ", "│", sep='', end='  ')
    print()
    for j in range(len(matrix[0])):
      elem=matrix[i][j]
      color = getCharColor(i, j, lettersStatus)
      if i==numGuess-1:
        if isCorrect:
          color = Style.RESET_ALL
        else:
          color = Back.WHITE
      print("│", color + "_____", "│", sep='', end='  ')
    print()
  for j in range(43):
    print("‾", end='')
  print()

def guessWord(numGuess, wordList):
  guess=""
  print("\nGuess ", f"{Style.DIM}a 5-letter word, ", "\"quit\"", f"{Style.DIM} to quit, ", "\"help\"", f"{Style.DIM} for instructions, or ", "\"hint\"", f"{Style.DIM} for a hint:", "\n", sep='', end='')
  while True: 
    #ask for input
    guess = input(Fore.MAGENTA + ">")
    if guess.upper()=="HELP": #asked to see instructions during a game
      printHelp()
      print("\nGuess ", f"{Style.DIM}a 5-letter word, ", "\"quit\"", f"{Style.DIM} to quit, ", "\"help\"", f"{Style.DIM} for instructions, or ", "\"hint\"", f"{Style.DIM} for a hint:", "\n", sep='', end='')
      guess = input(Fore.MAGENTA + ">")
      

    if guess=="quit" or guess=="help" or guess=="hint":
      break #if you quit, no regular conditions have to be met
    print(Style.RESET_ALL, sep='', end='')
    if (len(guess)!=5): #words can only be 5 long
      print(Style.RESET_ALL, "Word must be 5 letters long.", "\n", sep='', end='')
    elif (isUniqueChars(guess)==False):
      print(Style.RESET_ALL, "Word cannot contain duplicate letters.", "\n", sep='', end='')
    elif (guess in wordList): #break once guess is 5 letters long and in wordList 
      break
    else:
      print("Word not in word list.", "\n", sep='', end='')
  guess=guess.upper()
  return guess

def updateGuesses(guess):
  for i in range(5):
    guesses[numGuess-1][i] = guess[i:i+1]
  return guesses

def updateLStatus(guesses, numGuess, word, wordArray, letters, lettersStatus):
  for j in range(len(guesses[0])):
    elem = guesses[numGuess-1][j]
    if (elem == word[j:j+1]):
      lettersStatus[numGuess-1][j] = "Green"
    elif (elem in wordArray):
      if (lettersStatus[numGuess-1][j]) != "Green": #prevents changing green to yellow from user error
        lettersStatus[numGuess-1][j] = "Yellow"
    else:
      lettersStatus[numGuess-1][j] = "Red"

def getCharColor(i, j, lettersStatus):
  char = lettersStatus[i][j]
  if (char == " " or char == "White"):
    return Style.RESET_ALL
  if (char == "Green"):
    return Back.GREEN
  if (char == "Yellow"):
    return Back.YELLOW
  if (char == "Red"):
    return Back.RED

def checkIfCorrect(guess, word): #was originally more complex. staying as its own function in case it becomes complex with the addition of duplicate letters
  return guess==word

def hasFourGreen(lettersStatusRow):
  numGreen=0
  for s in range(len(lettersStatusRow)):
    if lettersStatusRow[s].upper() == "Green".upper():
      numGreen = numGreen+1
  return numGreen==4





def updateWordList_AI(wordList_AI, guessRow, lettersStatusRow, greenGuess): #all word options, all yellow characters, all green characters
  newList = []
  yellowList = getColorList(guesses, guessRow, lettersStatusRow, "Yellow", keyboardStatus, letters, lettersStatus)
  redList = getColorList(guesses, guessRow, lettersStatusRow, "Red", keyboardStatus, letters, lettersStatus)
  #greenList = getColorList(guessRow, lettersStatusRow, "Green", keyboardStatus, letters)
  numGreen = 0 #the number of greens the word should have that are in the correct spot
  for s in range(len(keyboardStatus)):
    if keyboardStatus[s].upper() == "Green".upper():
      numGreen = numGreen+1
  for i in range(len(wordList_AI)): #loop thru words
    word = wordList_AI[i] #current word
    totalYellows = 0
    totalGreens = 0
    redCondition = True
    yellowCondition2 = True
    for l in range(len(word)): #loop thru each word's letter
      letter = word[l:l+1] #current letter
      #check red condition
      if redCondition == True:
        for r in range(len(redList)):
          if letter.upper() == redList[r].upper():
            redCondition = False
            break
      #add words that contain every green in the right spot
      if letter.upper() in greenGuess: #if it is any green
        if l == greenGuess.index(letter.upper()): #if greens in same position
          totalGreens=totalGreens+1      
      #add words that contain every yellow
      for yellowLetter in range(len(yellowList)):
        if (yellowList[yellowLetter].upper() == letter.upper()):
          totalYellows = totalYellows+1
      #check yellow condition 2 (yellows arent in the same spot)
      for row in range(6):
        if lettersStatus[row][l].upper() == "YELLOW":
          if letter.upper()==guesses[row][l].upper():
            yellowCondition2 = False
            break
    #yellow condition, non-duplicate, and green condition
    yellowCondition = totalYellows==len(yellowList)
    uniqueCondition = isUniqueChars(word)
    greenCondition = totalGreens==numGreen
    #redCondition is above in the form of break
    if yellowCondition and yellowCondition2 and greenCondition and redCondition and uniqueCondition:
      newList.append(word)

  #return newList
  
  wordListScores = getWordListScores(newList, natOccur, letters) #get scores
  wordListScores, newList = zip(*sorted(zip(wordListScores, newList))) #sort both lists by score list
  wordListScores = list(wordListScores) #convert back from tuple to list
  newList = list(newList) #convert back from tuple to list
  wordListScores.reverse()
  newList.reverse()
  updateCurrentOptions(newList, 'currentOptions.txt')
  

def updateCurrentOptions(wordList, fileName):
  #write into .txt
  f = open('src/'+fileName, 'w')
  f.write("All viable words remaining:\n")
  for i in range(len(wordList)):
    f.writelines(wordList[i])
    f.write("\n")
    
def getColorList(guesses, guessRow, lettersStatusRow, color, keyboardStatus, letters, lettersStatus):
  #make a list of the letters that are red/yellow
  colorList = []
  if(color.upper()=="Yellow".upper()):
    for row in range(6):
      for col in range(5):
        if lettersStatus[row][col].upper() == color.upper(): #if anywhere
          if not(guesses[row][col].upper() in colorList): #exclude duplicates
            colorList.append(guesses[row][col])

  elif(color.upper()=="Red".upper()):
    for i in range(len(keyboardStatus)):
      if keyboardStatus[i].upper() == color.upper():
        colorList.append(letters[i])

  elif(color.upper()=="Green".upper()):
    for i in range(len(keyboardStatus)):
      if keyboardStatus[i].upper() == color.upper():
        colorList.append(letters[i])
      else:
        colorList.append("-1")
  return colorList

def updateGreenGuess(guesses, numGuess):
  greenGuess = ["", "", "", "", ""]
  for row in range(numGuess):
    for col in range(5):
      if lettersStatus[row][col].upper() == "GREEN":
        greenGuess[col] = guesses[row][col]
  return greenGuess




#game
def getNatOccur(wordList, letters):
  natOccur = []
  for i in range(len(letters)):
    numOccur = 0
    totalWords = len(wordList)
    for w in range(totalWords): #loop thru each word
      word = wordList[w]
      for l in range(5): #loop thru each letter
        if word[l:l+1].upper() == letters[i].upper(): #if current letter is the passed letter
          numOccur=numOccur+1
          break #dont need to check the rest of the word to ignore duplicates
    natOccur.append(numOccur/totalWords)
  return natOccur
        
  

def getWordListScores(wordList, natOccur, letters): #get nat occur for each letter and sum it to get score
  wordListScores = []
  for w in range(len(wordList)): #loop thru each word in list
    word = wordList[w]
    wordScore = 0
    for l in range(len(word)): #loop thru each letter in word
      letter = word[l:l+1]
      wordScore = wordScore + natOccur[letters.index(letter.upper())]
    wordListScores.append(wordScore)
  return wordListScores



  
def getHint(wordList_AI): #shows top 3 word choices
  print(Style.RESET_ALL, sep='', end='')
  if len(wordList_AI)>=3:
    print("Top 3 choices the AI would pick:")
    print(f"{Style.DIM}", wordList_AI[0], wordList_AI[1], wordList_AI[2])
  elif len(wordList_AI)==2:
    print("Top 2 choices the AI would pick:")
    print(f"{Style.DIM}", wordList_AI[0], wordList_AI[1])
  elif len(wordList_AI)==1:
    print("Top choice the AI would pick:")
    print(f"{Style.DIM}", wordList_AI[0])

def shareWin(numGuess, lettersStatus, numWordle):
  # ⬜🟩🟨
  red = "⬜"
  green = "🟩"
  yellow = "🟨"

  #header
  print(Style.RESET_ALL, "\nWordle ", numWordle, " ", numGuess, "/6\n", sep='')

  #guesses table
  for row in range(numGuess):
    for col in range(5):
      elem = lettersStatus[row][col]
      if elem == "Red":
        print(red, end='')
      elif elem == "Green":
        print(green, end='')
      elif elem == "Yellow":
        print(yellow, end='')
    print("") #new line
  print("\nHighlight the above text, right click, click copy, then share!\n")
  
  
  

wordList_AI = makeWordList('wordlist.txt')
wordList = makeWordList('wordlist.txt') 
wordPoolHard = makeWordList('wordpoolhard.txt')
dailyWords = makeWordList('dailywords.txt')
letters      =["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
                 "A", "S", "D", "F", "G", "H", "J", "K", "L",
                    "Z", "X", "C", "V", "B", "N", "M"]
natOccur = [0.008556891766882516, 0.07924761023743447, 0.4397934011717545, 0.3013413506012951, 0.23381128584643848, 0.15656799259944496, 0.1877890841813136, 0.27667283379586805, 0.301495528831329, 0.14531298180696886, 0.41088498304039467, 0.45760098674067223, 0.17715078630897318, 0.07631822386679, 0.11894850447116867, 0.131668208448967, 0.022278754239901326, 0.11131668208448967, 0.2400555041628122, 0.030141843971631204, 0.022124576009867405, 0.14801110083256244, 0.05195806352143077, 0.11709836571076164, 0.2148473635522664, 0.14400246685168056] #natural occurence of each letter out of 1
#netOccur = getNatOccur(wordList, letters) #only done once, then numbers stored above to save time

#play
while True:
  firstInput = True
  canShare = False
  while True:
    modeSelection = inputMode(firstInput, canShare) #if you have to re-enter input, don't reprint the header
    
    
    if (canShare == True and modeSelection.upper()=="share".upper()):
      try: 
        shareWin(numGuess, lettersStatus, numWordle) #copy the win to clipboard
      except:
        a=1 # TODO
      break
    if (modeSelection.upper()=="ai".upper()):
      print("This feature is not yet implemented. Sorry!")
      break
    if (modeSelection.upper()=="average".upper()):
      print("This feature is not yet implemented. Sorry!")
      break
    if (modeSelection=="help"):
      printHelp()
      break
    if (modeSelection.lower() == "quit"):
      exit()
    elif (modeSelection=="play" or modeSelection=="today"):
      #updateCurrentOptions([], 'currentOptions.txt')
      keyboardStatus=[] #define array that tracks the color of each letter in keyboard format
      for i in range(26):                         #reset
        keyboardStatus.append("White")            #reset
      greenGuess=[] #define array that tracks the guess that includes all greens
      for i in range(5):
        greenGuess.append("")
      lettersStatus = buildMatrix(6, 5, "White")  #reset
      guesses = buildMatrix(6, 5, " ")            #reset
      numGuess=1
      whenFourGreen = 0                                 #reset
      #initialize wordlist scores for funzies
      wordListScores = getWordListScores(wordList, natOccur, letters) #get scores
      wordListScores, wordList = zip(*sorted(zip(wordListScores, wordList))) #sort both lists by score list
      wordList = list(wordList) #convert back from tuple to list
      wordList.reverse()
      updateCurrentOptions(wordList, 'currentOptions.txt')
      
      if (modeSelection=="play"): #play random word
        word = getRandomWord(wordPoolHard).upper()
        #print(word)
        #time.sleep(4)
        wordArray = makeWordArray(word)
      elif (modeSelection=="today"):#play todays word
        word=getTodaysWord(dailyWords).upper()
        numWordle = getTodaysNum()
        if not isUniqueChars(word):
          firstInput = False
          print("Today's word has a duplicate letter, and this program cannot handle duplicate letters yet, sorry!")
          break
        wordArray = makeWordArray(word)
      clearConsole() #pre-first-guess
      printPlayBoard(guesses, letters, lettersStatus, numGuess, False) #pre-first-guess
      while True: #play > win/lose/continue loop
        guess = guessWord(numGuess, wordList)
        if guess=="HINT": #hint requested
          #getHint(wordList_AI)
          print("Open files and open currentOptions.txt. The smart AI suggestions the words at the very top!")
          continue
        if guess=="QUIT": #uppered
          print("\n", Fore.RED + "You quit. The word was \"", Fore.WHITE+Style.DIM + str(word.capitalize()), Fore.RED + "\".", sep='', end='\n')
          print("\n")
          break
        else: #regular guess
          guesses = updateGuesses(guess)
        clearConsole()
        updateLStatus(guesses, numGuess, word, wordArray, letters, lettersStatus) 
        printPlayBoard(guesses, letters, lettersStatus, numGuess+1, checkIfCorrect(guess, word))
        printKeyboard(letters, numGuess, guesses, lettersStatus, keyboardStatus)
        greenGuess = updateGreenGuess(guesses, numGuess)
        updateWordList_AI(wordList_AI, guesses[numGuess-1], lettersStatus[numGuess-1], greenGuess)
        if checkIfCorrect(guess, word) == True: #win
          if (modeSelection.upper() == "today".upper()): #can only share if on "today" mode
            canShare = True
          if numGuess==1:
            print("\n", Fore.GREEN + "You guessed the Wordle in ", Fore.WHITE + str(numGuess), Fore.GREEN + " guess!", sep='')
          else: #>1
            print("\n", Fore.GREEN + "You guessed the Wordle in ", Fore.WHITE + str(numGuess), Fore.GREEN + " guesses!", sep='')
          #print(Fore.GREEN + "You figured out 4 of 5 letters in " + str(whenFourGreen) + " guesses!")
          time.sleep(3)
          print("\n")
          break
        if whenFourGreen==0:
          if hasFourGreen(lettersStatus[numGuess-1]) == True:
            whenFourGreen = numGuess
        numGuess=numGuess+1 #continue
        if (numGuess>6): #lose
          print("\n", Fore.RED + "You took all 6 tries. The word was \"", Fore.WHITE + word.capitalize(), Fore.RED + "\".", sep='')
          time.sleep(3)
          print("\n")
          break
    
    else: #skips the break, and re-enter Input
      print(Style.RESET_ALL + "Error: Input was not a valid option.")
      firstInput = False
      