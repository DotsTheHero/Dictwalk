import sys #This is here so that I can use sys.maxsize as infinity for A*
def editDistanceFind(word1,word2):#This is just a convenience function, here so that I can call editDistance without needing to supply all 4 arguments but still get the recursion I want.
	return editDistance(word1, word2, len(word1),len(word2))
def editDistance(word1,word2,len1,len2):#Recursively finds the edit distance between two strings. This value is used as my heuristic when I use A*
	if len1==0:
		return len2
	if len2==0:
		return len1
	if word1[len1-1]==word2[len2-1]:
		return editDistance(word1,word2,len1-1,len2-1)
	return 1+min(editDistance(word1, word2, len1, len2-1), editDistance(word1, word2, len1-1, len2), editDistance(word1, word2, len1-1, len2-1))	
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
def dictionarySteps(start, goal, dictionary):#The meat and potatoes of this program. The A* search
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
		for entry in dictionary:
			if adjacent(current, entry) and entry not in closedSet:#We don't want to waste time with an entry that isn't adjacent, or already investigated.
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
	firstword= input("Please enter the first word\n")
	secondword= input("Please enter the second word\n")
	print(dictionarySteps(firstword,secondword,dictionary))