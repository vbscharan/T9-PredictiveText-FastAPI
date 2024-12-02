class Trie:
    def __init__(self):
        self.rootid = 1
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

    # Add Contact Name and number to Tries 
    def addContact(self, name, number, cursor, conn,username):
        self.addContactNameToTrie(name, cursor, conn,username)
        self.addContactNumberToTrie(number, cursor, conn,username)
        #self.addContactName(name,cursor,conn,username)
        self.addContactNumber(name,number,cursor,conn,username)
        # self.nameToNumberMap[name]=number
        # self.numberToNameMap[number]=name

    def deleteContactName(self,name,cursor,conn,username):
        try:
            cursor.execute("select * from numbers where username=(%s) and name=(%s)",(username,name))
            fetchedRows=cursor.fetchall()
            print(fetchedRows)
            if fetchedRows is None:
                return False
            if not self.deleteContactNameInTrie(name,cursor,conn,username):
                raise Exception()
            for i in fetchedRows:
                if not self.deleteContactNumberInTrie(i['numbers'],cursor,conn,username):
                    raise Exception()
            cursor.execute("delete from numbers where username=(%s) and name=(%s)",(username,name))
            conn.commit() 
            return True
        except Exception as error:
            print(error)
            conn.rollback()
            return False

    # Add ContactName to Trie
    def addContactNameToTrie(self, word, cursor, conn,username):
        parentid = self.rootid
        for i in word:
            cursor.execute("select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",(parentid, i,username))
            fetchedRow = cursor.fetchone()

            if fetchedRow is None:
                cursor.execute("insert into contactsbook (letter,parentid,username) values(%s,%s,%s) returning id",(i, parentid,username))
                parentid = cursor.fetchone()["id"]
            else:
                parentid = fetchedRow["id"]

        cursor.execute("UPDATE contactsbook SET iseod=True WHERE id=(%s) and username=(%s)", (parentid,username))
        conn.commit()
        
        

    # Add ContactNumber to Trie
    def addContactNumberToTrie(self, number, cursor, conn,username):
        parentid = self.rootid
        for i in number:
            cursor.execute(
                "select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",(parentid, i,username))
            fetchedRow = cursor.fetchone()
            if fetchedRow is None:
                cursor.execute("insert into contactsbook (letter,parentid,username) values(%s,%s,%s) returning id",(i, parentid,username))
                parentid = cursor.fetchone()["id"]
            else:
                parentid = fetchedRow["id"]

        cursor.execute("UPDATE contactsbook SET iseod=True WHERE id=(%s) and username=(%s)", (parentid,username))
        conn.commit()
    '''
    def addContactName(self,name,cursor,conn,username):
        try:
            cursor.execute("INSERT INTO contacts (name) VALUES (%s)ON CONFLICT (name) DO NOTHING;",(name,))
            #cursor.execute("INSERT INTO contacts (name) values(%s)",(name,))
            conn.commit()
        except Exception as error:
            conn.rollback()
            print(error)
    '''  

    def addContactNumber(self,name,number,cursor,conn,username):
        try:
            cursor.execute("INSERT INTO numbers (numbers, name,username) SELECT (%s),(%s),(%s) where not exists (select 1 from numbers where numbers=(%s) and name=(%s) and username=(%s))",(number,name,username,number,name,username) )
            #cursor.execute("INSERT INTO numbers (name,numbers) values(%s,%s)",(name,number))
            conn.commit()
        except Exception as error:
            conn.rollback()
            print(error)
  
    def deleteContactNameInTrie(self, name, cursor, conn,username):
        parentid = self.rootid
        for i in name:
            cursor.execute("select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",(parentid, i,username))
            fetchedRow = cursor.fetchone()

            if fetchedRow is None:
                return False
            else:
                parentid = fetchedRow["id"]
        if fetchedRow["iseod"] == True:
            cursor.execute("update contactsbook set iseod=false where id=(%s) and username=(%s)", (parentid,username))
            conn.commit()
            return True
        return False

    def deleteContactNumberInTrie(self, number, cursor, conn,username):
        parentid = self.rootid
        for i in number:
            cursor.execute("select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",(parentid, i,username))
            fetchedRow = cursor.fetchone()

            if fetchedRow is None:
                return False
            else:
                parentid = fetchedRow["id"]
        if fetchedRow["iseod"] == True:
            cursor.execute("update contactsbook set iseod=false where id=(%s) and username=(%s)", (parentid,username))
            conn.commit()
            return True
        return False

    def updateContactName(self, oldname, newname, cursor, conn,username):
        if not self.deleteContactNameInTrie(oldname, cursor, conn,username):
            return "oldname was not found"
        self.addContactNameToTrie(newname, cursor, conn)
        cursor.execute("update numbers set name=(%s) where name=(%s) and username=(%s)",(newname,oldname,username))
        conn.commit()
        return ""

    def updateContactNumber(self, oldnumber, newnumber, cursor, conn,username):
        if not self.deleteContactNumberInTrie(oldnumber, cursor, conn,username):
            return "oldnumber was not found"
        self.addContactNumberToTrie(newnumber, cursor, conn)
        cursor.execute("update numbers set numbers=(%s) where numbers=(%s) and username=(%s)",(newnumber,oldnumber,username))
        conn.commit()
        return ""

    # Check if a particular name or number is present in the Trie
    def checkContactOrNumber(self, inputString, cursor,username):
        parentid = self.rootid
        for i in inputString:
            cursor.execute("select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",(parentid, i,username))
            fetchedRow = cursor.fetchone()

            if fetchedRow is None:
                return False
            else:
                parentid = fetchedRow["id"]

        if fetchedRow["iseod"] == True:
            return True
        return False

    async def searchContact(self, userInput, cursor,username):
        ans = {}
        cursor.execute("select * from contactsbook where id=(%s)", (self.rootid,))
        currRow = cursor.fetchone()
        self.solveForName(0, userInput, ans, currRow, "", 0, cursor,username)
        self.solveForNumber(0, userInput, ans, currRow, "", 0, cursor,username)
        if len(ans) == 0:
            print("No contact name/number available with the given input")
            return

        printableCollection = {}
        for i in sorted(ans.keys(),reverse=True):
            for item in set(ans[i]):
                if item.isdigit():
                    cursor.execute("SELECT name FROM numbers where numbers=(%s) and username=(%s);",(item,username))
                    ot=cursor.fetchone()
                    printableCollection[ot['name']]=item
                else:
                    cursor.execute("SELECT STRING_AGG(numbers, ', ') as num FROM numbers where name=(%s) and username=(%s) GROUP BY name;",(item,username))
                    ot=cursor.fetchall()
                    print(ot)
                    printableCollection[item]=ot[0]['num']
        return printableCollection
        

    def solveForName(self, index, userInput, ans, currRow, ts, count, cursor,username):

        # Check if combination of given input is a substring of contact present in the Trie.
        # If yes then add it as a result
        # While adding check if a same length of substring is matched in another contact. If yes add the current result to the exisiting list
        # Otherwise create a new list
        if currRow["iseod"] == True and count == len(userInput):
            if ans.get(len(ts)):
                ans[len(ts)].append(ts)
            else:
                ans[len(ts)] = [ts]

        # From current character(based on index) in the given input string check if there exists a node
        # If yes increment index to match from next character in the input string

        for i in range(index, len(userInput)):

            # This condition is just for a check that the user does not give inputstring containing characters apart from 2-9

            if self.keypadCombo.get(userInput[i]):
                for chars in self.keypadCombo[userInput[i]]:
                    cursor.execute(
                        "select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",
                        (currRow["id"], chars,username),
                    )
                    childRow = cursor.fetchone()
                    if childRow is not None:
                        self.solveForName(
                            i + 1,
                            userInput,
                            ans,
                            childRow,
                            ts + childRow["letter"],
                            count + 1,
                            cursor,username
                        )

            # If you dont find a substring in the Trie whose length is equal to given input string and also trie doesn't
            # hold a string with the characters formed by the combination of input number then set the count to zero
            # By setting back to zero we are looking for a substring further next in the Trie that matches the above critertia.

            count = 0

        # If the Trie doesn't match with any of the input character at present, we'll go through all other available nodes
        # with a hope that we might find the input substring combination in further nodes.

        for k in range(26):
            cursor.execute(
                "select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",
                (currRow["id"], chr(97 + k),username),
            )
            childRow = cursor.fetchone()
            if childRow is not None:
                self.solveForName(
                    index,
                    userInput,
                    ans,
                    childRow,
                    ts + childRow["letter"],
                    count,
                    cursor,username
                )

        # An additional check for the node " "(space).

        cursor.execute(
            "select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",
            (currRow["id"], " ",username),
        )
        childRow = cursor.fetchone()

        if childRow is not None:
            self.solveForName(
                index, userInput, ans, childRow, ts + childRow["letter"], count, cursor,username
            )

    def solveForNumber(self, ind, userInput, ans, currRow, ts, count, cursor,username):
        # Check if combination of given input is a substring of contact present in the Trie.
        # If yes then add it as a result
        # While adding check if a same length of substring is matched in another contact. If yes add the current result to the exisiting list
        # Otherwise create a new list
        if currRow["iseod"] == True and count == len(userInput):
            if ans.get(len(ts)):
                ans[len(ts)].append(ts)
            else:
                ans[len(ts)] = [ts]
        # From current character(based on ind) in the given input string check if there exists a node
        # If yes increment ind to match from next character in the input string
        for i in range(ind, len(userInput)):
            cursor.execute(
                "select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",
                (currRow["id"], userInput[i],username),
            )
            childRow = cursor.fetchone()
            if childRow is not None:
                self.solveForNumber(
                    i + 1,
                    userInput,
                    ans,
                    childRow,
                    ts + userInput[i],
                    count + 1,
                    cursor,username
                )
            # If you dont find a substring in the Trie whose length is equal to given input string and also trie doesn't
            # hold a string with the characters formed by the combination of input number then set the count to zero
            # By setting back to zero we are looking for a substring further next in the Trie that matches the above critertia.
            count = 0
        # If the Trie doesn't match with any of the input character at present, we'll go through all other available nodes
        # with a hope that we might find the input substring combination in further nodes.
        for k in range(10):
            cursor.execute(
                "select * from contactsbook where parentid=(%s) and letter=(%s) and username=(%s)",
                (currRow["id"], str(k),username),
            )
            childRow = cursor.fetchone()
            if childRow is not None:
                self.solveForNumber(
                    ind,
                    userInput,
                    ans,
                    childRow,
                    ts + childRow["letter"],
                    count,
                    cursor,username
                )

