class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEOD = False
        self.word = None

class Trie:
    def __init__(self):
        self.nameRoot = TrieNode()
        self.numRoot=TrieNode()
        self.nameToNumberMap={}
        self.numberToNameMap={}
        self.keypadCombo = {
            "2": ["a", "b", "c"],
            "3": ["d", "e", "f"],
            "4": ["g", "h", "i"],
            "5": ["j", "k", "l"],
            "6": ["m", "n", "o"],
            "7": ["p", "q", "r", "s"],
            "8": ["t", "u", "v"],
            "9": ["w", "x", "y", "z"],
        }

    def getIndex(self, ch):
        return ord("a") - ord(ch)

    #Add Contact Name and number to Triesn and Maps
    def addContact(self,name,number):
        self.addContactName(name)
        self.addContactNumber(number)
        self.nameToNumberMap[name]=number
        self.numberToNameMap[number]=name

    #Add ContactName to Trie
    def addContactName(self, word):
        curr = self.nameRoot
        for i in word:
            if curr.children.get(i) is None:
                curr.children[i] = TrieNode()
            curr = curr.children[i]
            curr.word = i
        curr.isEOD = True
    
    #Add ContactNumber to Trie
    def addContactNumber(self, number):
        curr = self.numRoot
        for i in number:
            if curr.children.get(i) is None:
                curr.children[i] = TrieNode()
            curr = curr.children[i]
            curr.word = i
        curr.isEOD = True

    #Check if a particular name or number is present in the Trie
    def checkContactOrNumber(self,curr, word):
        for i in word:
            if curr.children.get(i) is None:
                return False
            curr = curr.children[i]
        if curr.isEOD:
            return True
        return False
    
    def solveForName(self, ind, userInput, ans, curr, ts, count):

        #Check if combination of given input is a substring of contact present in the Trie. 
        # If yes then add it as a result
        #While adding check if a same length of substring is matched in another contact. If yes add the current result to the exisiting list
        #Otherwise create a new list
        if curr.isEOD == True and count == len(userInput):
            if ans.get(len(ts)):
                ans[len(ts)].append(ts)
            else:
                ans[len(ts)] = [ts]
        
        #From current character(based on ind) in the given input string check if there exists a node
        #If yes increment ind to match from next character in the input string
        for i in range(ind, len(userInput)):
            #This condition is just for a check that the user does not give inputstring containing characters apart from 2-9
            if self.keypadCombo.get(userInput[i]):
                for chars in self.keypadCombo[userInput[i]]:
                    child = curr.children.get(chars)
                    if child:
                        self.solveForName(i + 1, userInput, ans, child, ts + chars, count + 1)
            #If you dont find a substring in the Trie whose length is equal to given input string and also trie doesn't
            #hold a string with the characters formed by the combination of input number then set the count to zero
            #By setting back to zero we are looking for a substring further next in the Trie that matches the above critertia.
            count = 0

        #If the Trie doesn't match with any of the input character at present, we'll go through all other available nodes
        #with a hope that we might find the input substring combination in further nodes.
        for k in range(26):
            child = curr.children.get(chr(97+k))
            if child is not None:
                self.solveForName(ind, userInput, ans, child, ts + child.word, count)
        #An additional check for the node " "(space).
        child = curr.children.get(" ")
        if child is not None:
            self.solveForName(ind, userInput, ans, child, ts + child.word, count)
    
    def solveForNumber(self, ind, userInput, ans, curr, ts, count):
        #Check if combination of given input is a substring of contact present in the Trie. 
        # If yes then add it as a result
        #While adding check if a same length of substring is matched in another contact. If yes add the current result to the exisiting list
        #Otherwise create a new list
        if curr.isEOD == True and count == len(userInput):
            if ans.get(len(ts)):
                ans[len(ts)].append(ts) 
            else:
                ans[len(ts)] = [ts]
        #From current character(based on ind) in the given input string check if there exists a node
        #If yes increment ind to match from next character in the input string
        for i in range(ind, len(userInput)):
            child = curr.children.get(userInput[i])
            if child:
                self.solveForNumber(i + 1, userInput, ans, child, ts + userInput[i], count + 1)
            #If you dont find a substring in the Trie whose length is equal to given input string and also trie doesn't
            #hold a string with the characters formed by the combination of input number then set the count to zero
            #By setting back to zero we are looking for a substring further next in the Trie that matches the above critertia.
            count = 0
        #If the Trie doesn't match with any of the input character at present, we'll go through all other available nodes
        #with a hope that we might find the input substring combination in further nodes.
        for k in range(10):
            child = curr.children.get(str(k))
            if child is not None:
                self.solveForNumber(ind, userInput, ans, child, ts + child.word, count)
    
    def searchContact(self,userInput):
        ans = {}
        self.solveForName(0,userInput, ans, self.nameRoot, "", 0)
        self.solveForNumber(0,userInput,ans,self.numRoot,"",0)
        if len(ans)==0:
            print("No contact name/number available with the given input")
            return
        printableCollection=set()
        for i in ans.keys():
            for item in ans[i]:
                if self.nameToNumberMap.get(item):
                    printableCollection.add((item,self.nameToNumberMap[item]))
                if self.numberToNameMap.get(item):
                    printableCollection.add((self.numberToNameMap[item],item))
        
        contacts={}
        if len(printableCollection)==0:
            return contacts
        
        for i in sorted(printableCollection):
            contacts[i[0]]=i[1]
            print(i[0]," : ",i[1])
        return contacts

'''
t = Trie()
t.addContact("uttez annaya","9494476410")
t.addContact("annaya","9494476410")
t.addContact("amma","9390343074")
t.addContact("bhanu","8897784613")
t.searchContact("2662") 
#print(t.nameToNumberMap["bhanu"])
'''