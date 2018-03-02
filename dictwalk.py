import sys #This is here so that I can use sys.maxsize as infinity for A*
class TrieNode:
	def __init__(self):
		self.children=[None]*26
		self.isEndOfWord=False
	def _charToIndex(self, ch):
		return ord(ch)-ord('a')
	def _indexToChar(self, i):
		return chr(i+ord('a'))
	def search_adjacents(self, word, i, diff, current):
		returnlist=[]
		if i==len(word):
			if diff==True and self.isEndOfWord==True:
				return [current]
			if diff==False:
				for x in range(26):
					if self.children[x] != None and self.children[x].isEndOfWord==True:
						returnlist.extend([current+self._indexToChar(x)])
			return returnlist
		if diff==False:
			returnlist.extend(self.search_adjacents(word, i+1, True, current))
		for x in range(26):
			if self.children[x]==None:
				continue
			elif self._indexToChar(x)==word[i]:
				returnlist.extend(self.children[x].search_adjacents(word, i+1, diff, current+self._indexToChar(x)))
			elif self._indexToChar(x)!=word[i] and diff==False:
				returnlist.extend(self.children[x].search_adjacents(word, i, True, current+self._indexToChar(x)))
				returnlist.extend(self.children[x].search_adjacents(word, i+1, True, current+self._indexToChar(x)))
		return returnlist	
class Trie:
	def __init__(self):
		self.root=self.getNode()
	def getNode(self):
		return TrieNode()
	def _charToIndex(self,ch):
		return ord(ch)-ord('a')
	def insert(self,key):
		pCrawl = self.root
		length = len(key)
		for level in range(length):
			index = self._charToIndex(key[level])
			if not pCrawl.children[index]:
				pCrawl.children[index] = self.getNode()
			pCrawl = pCrawl.children[index]
		pCrawl.isEndOfWord = True
	def find_adjacents(self, word):
		returnlist=[]
		returnlist.extend(self.root.search_adjacents(word, 0, False, ""))
		return returnlist
	def search(self, key):
		pCrawl = self.root
		length = len(key)
		for level in range(length):
			index = self._charToIndex(key[level])
			if not pCrawl.children[index]:
				return False
			pCrawl = pCrawl.children[index]
 
		return pCrawl != None and pCrawl.isEndOfWord
def editDistanceFind(word1,word2):#This is just a convenience function, here so that I can call editDistance without needing to supply all 4 arguments but still get the recursion I want.
	return editDistance(word1, word2, len(word1),len(word2))
def editDistance(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
 
    # Fill d[][] in bottom up manner
    for i in range(m+1):
        for j in range(n+1):
 
            # If first string is empty, only option is to
            # isnert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    return dp[m][n]
def adjacent(word1,word2):#Detects if 2 strings are "adjacent". I could have used editDistance for this but editDistance is O(n^2) for the size of the larger string while this is only O(n) so it's better for time to use this when possible
	if word1==word2:#I decided it would be more convenient for my purposes if strings were not considered to be adjacent to themselves
		return False
	if abs(len(word1)-len(word2)) > 1:#If the length differs by more than 1 we can save time by exiting early
		return False
	if len(word1)>=len(word2):#For this next part, we want to make sure we use the larger string as the first value and the shorter as the second
		first=word1
		second=word2
	else:
		second=word1
		first=word2
	equal = True if len(word1)==len(word2) else False
	diff=False
	i1=0
	i2=0
	while i1<len(first) and i2<len(second):#We iterate through the strings at different rates, trying to see if exactly one difference exists, if more than that exists, we return false at once.
		if first[i1] != second[i2]:
			if diff:
				return False
			diff=True;
			if equal:
				i2+=1
		else:
			i2+=1
		i1+=1
	return True
def dictionarySteps(start, goal):#The meat and potatoes of this program. The A* search
	closedSet=[]#all of the sets that have been analyzed and won't be visited again
	openSet=[start]#set of sets to be investigated
	cameFrom=dict()#saves the path to each node investigated so that we can use it to find the solution when we get to the answer
	cameFrom[start]=[]
	gScore=dict()#Stores the total cost of getting to the node for each node. Is updated as shorter solutions are found. This could have been replaced with calls to len(cameFrom) but keeping it like this makes this code easier to repurpose if I decide to in the future.
	for word in dictionary:#in the beginning, as is typical with A* you assume all paths take infinity to get to, I substitute this for the highest possible value.
		gScore[word]=sys.maxsize
	gScore[start]=0;
	fScore=dict()#The distance from the solution according to our heuristic Heuristic thinks it is. Our heuristic is admissable
	fScore[start]=editDistanceFind(start,goal)
	while len(openSet)>0:#we go until openSet is empty
		curweight=sys.maxsize
		current= openSet[0]
		for word in openSet:#We use this loop to find the most promising openset node
			if fScore[word]<curweight:
				curweight=fScore[word]
				current= word
		if current==goal:#We use this to check to see if we already have the solution, and to return the path if so
			cameFrom[current].append(current)
			return cameFrom[current];
		openSet.remove(current)#Get it out of openset
		closedSet.append(current)#put it in closed set so we don't go through it again. This also prevents us from referencing the value we're already using when we iterate through the dictionary in a few lines.
		adjacentlist=tree.find_adjacents(current)
		for entry in adjacentlist:
			if entry not in closedSet:
				if entry not in openSet:#If it's not already in the open set, add it
					openSet.append(entry)
				temp_gScore=gScore[current]+1#+1 because all paths are weighted 1. You could change this line to make this test for all kinds of things.
				if temp_gScore>=gScore[entry]:#if the G-score is inferior, we dont' want it
					continue
				cameFrom[entry]=list(cameFrom[current])#Otherwise, we want to make sure we save how we got here and how good a path it was
				cameFrom[entry].append(current)
				gScore[entry] = temp_gScore
				fScore[entry] = gScore[entry]+editDistanceFind(entry, goal)
	return []

try:	
	f = open('dictionary.txt', 'r')
except:
	print("File didn't open for some reason. Make sure you have dictionary.txt in the same folder.");
else:
	dictionary = f.read().split("\n")
	f.close()
	tree=Trie()
	print("One moment, building tree")
	for entry in dictionary:
		tree.insert(entry)
	print(tree.search("aan"))
	print("Alright, finished building tree")
	firstword= input("Please enter the first word\n")
	secondword= input("Please enter the second word\n")
	print(dictionarySteps(firstword,secondword))