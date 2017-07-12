import sys
import time
import logging
import resource
import Queue

logging.basicConfig(format='%(levelname)s : %(asctime)s : %(lineno)d : %(message)s', datefmt='%I:%M:%S %p',level=logging.CRITICAL)

class Node:
	def __init__(self,state,parent,pathToGoal,costOfPath,priorityFunc):
		self.state = state
		self.parent = parent
		self.pathToGoal = pathToGoal
		self.costOfPath = costOfPath
		self.priorityFunc = priorityFunc

def create_node(state,parent,pathToGoal,costOfPath,priorityFunc=None):
	return Node(state,parent,pathToGoal,costOfPath,priorityFunc)



def move(node,direction):
	nodeState = node.state[:] # list of states
	blankIndex = node.state.index(0) #index of blank
	skipSwap = False

	if direction == "Up":
		threshold = boardSize
		if blankIndex < threshold:
			skipSwap = True
		else:
			swapIndex = blankIndex-boardSize

	elif direction == "Down":
		threshold = boardSize*(boardSize-1)
		if blankIndex >= threshold:
			skipSwap = True
		else:
			swapIndex = blankIndex+boardSize
	elif direction == "Left":
		if blankIndex in leftThreshold:
			skipSwap = True
		else:
			swapIndex = blankIndex - 1

	elif direction == "Right":

		if blankIndex in rightThreshold:
			skipSwap = True
		else:
			swapIndex = blankIndex + 1
	else:
		logging.error("Invalid move direction!")
	if skipSwap:
		logging.debug("Move Skipped!")
		return "skipped"
	else:
		nodeState[blankIndex],nodeState[swapIndex] = nodeState[swapIndex],0 #swap blank to the direction
	# display(nodeState)

	return nodeState

def expand_node(algorithm,node):
	childNodes = []
	if algorithm == "bfs":
		for direction in directionList:
			newNodeState = move(node,direction)
			if (newNodeState != "skipped"):
				logging.info("skipped creation of childNode"+str(newNodeState))
				childNodes.append(create_node(newNodeState,node,node.pathToGoal+" "+direction, node.costOfPath+1))
	elif algorithm == "dfs":
		for direction in reversed(directionList):
			# logging.debug(direction)
			newNodeState = move(node,direction)
			if (newNodeState != "skipped"):
				childNodes.append(create_node(newNodeState,node,node.pathToGoal+" "+direction, node.costOfPath+1))
	elif algorithm == "ast":
		for direction in directionList:
			newNodeState = move(node,direction)
			if (newNodeState != "skipped"):
				logging.info("skipped creation of childNode"+str(newNodeState))
				childNodes.append(create_node(newNodeState,node,node.pathToGoal+" "+direction, node.costOfPath+1,manPriorFunc(node) + node.costOfPath))

	return childNodes


def bfs():

	logging.debug("In BFS")
	# display(initialState)
	initialNode = create_node(initialState, None, "", 0)

	# frontier = [] #put get
	childSet = set() #add remove
	frontierQueue = Queue.Queue()

	childSet.add(str(initialNode.state))

	# frontier.append(initialNode)
	frontierQueue.put(initialNode)

	nodesExpanded = 1
	maxSearchDepth = 0
	while not frontierQueue.empty():
		# print "len of frontierQueue",frontierQueue.qsize()
		checkNode = frontierQueue.get() #pop the queue
		# print "len frontierQueue",frontierQueue.qsize()

		if checkNode.state == goalState:

			solution = [checkNode,nodesExpanded-1,maxSearchDepth]
			return solution

		tempFrontier = []
		nodesExpanded= nodesExpanded+1
		tempFrontier.append(expand_node("bfs",checkNode))
		for x in tempFrontier:
			for tempNode in x:
				if str(tempNode.state) not in childSet:
					maxSearchDepth = max(tempNode.costOfPath,maxSearchDepth)
					# display(tempNode.state)
					frontierQueue.put(tempNode)
					# logging.info("index for blank"+str(tempNode.state.index(0)))
					childSet.add(str(tempNode.state))
					# print "len frontierQueue",frontierQueue.qsize()
				else:
					logging.info("already visited")
		# raw_input()

	return "None Solution"


def dfs():
	'''
	TODO:
		frontier class
		child nodes  too in nodein tempFrontier
		remove O(n^2)
		python -m cProfile -s tottime driver.py bfs 8,6,7,2,3,1,5,4,0
	'''
	logging.debug("In DFS")
	initialNode = create_node(initialState, None, "", 0)

	# frontier = [] #put get
	childSet = set() #add remove
	frontierStack = [] #append pop as stack from right

	childSet.add(str(initialNode.state))

	# frontier.append(initialNode)
	frontierStack.append(initialNode)

	nodesExpanded = 1
	maxSearchDepth = 0
	while len(frontierStack)!=0:
		# raw_input()
		# print "len of frontierStack",len(frontierStack)
		checkNode = frontierStack.pop() #pop the queue
		# print "len frontierQueue",frontierQueue.qsize()

		# display(checkNode.state)

		if checkNode.state == goalState:
			solution = [checkNode,nodesExpanded-1,maxSearchDepth]
			return solution

		tempFrontier = []
		nodesExpanded= nodesExpanded+1
		tempFrontier.extend(expand_node("dfs",checkNode))

		for tempNode in tempFrontier:
			# for tempNode in x:

				if str(tempNode.state) not in childSet:
					if tempNode.state == goalState:
						solution = [tempNode,nodesExpanded-1,maxSearchDepth]
						return solution
					maxSearchDepth = max(tempNode.costOfPath,maxSearchDepth)
					# logging.debug("expanded")
					# display(tempNode.state)
					frontierStack.append(tempNode)
					childSet.add(str(tempNode.state))
					# print "len frontierQueue",frontierQueue.qsize()
				else:
					logging.debug("already visited")
		# raw_input()

	return [initialNode,nodesExpanded-1,maxSearchDepth]

'''	logging.debug("In DFS")

	nodesQueue = []
	frontier = set()

	node = create_node(initialState, None, "", 0)
	# display(initialState)

	# while True:
	# 	direction = raw_input()
	# 	node = create_node(move(node,direction),node,node.pathToGoal+direction+" ", node.costOfPath+1)
	# 	if direction not in ["up","down","left","right"]:
	# 		break
	solution = "DUMMY SOLUTION"
	return solution'''
def ast():
	max_search_depth = 0

	logging.debug("In AST")
	nodesQueue = []
	nodesExpanded = set()
	nodesCheck = set()

	initialNode = create_node(initialState, None, "", 0, 0)
	nodesQueue.append(initialNode)
	# print initialNode.priorityFunc
	nodesCheck.add(str(nodesQueue[0].state))
	while len(nodesQueue) != 0:
		# Priority Queue
		nodesQueue = sorted(nodesQueue, key = lambda x: (x.priorityFunc))
		# Remove the First One of the Queue
		nodeNext = nodesQueue.pop(0)
		nodesExpanded.add(str(nodeNext.state))
		nodesCheck.remove(str(nodeNext.state))
		# Goal Check
		if nodeNext.state == goalState:
			#Max_Search_Depth
			for node in nodesQueue:
				max_search_depth = max(node.costOfPath,max_search_depth)
			solution = [nodeNext, len(nodesExpanded) - 1, max_search_depth]
			return solution
		# Extend
		tempQueue = []
		tempQueue.extend(expand_node("ast",nodeNext))
		for tempNode in tempQueue:
			# Visited Check
			if str(tempNode.state) not in nodesExpanded and str(tempNode.state) not in nodesCheck:
				nodesCheck.add(str(tempNode.state))
				nodesQueue.append(tempNode)

	return None
# Manhattan Priority Function mpf
def manPriorFunc(currentNode):
	mpf = 0
	if currentNode != None:
		for i in range(1,len(currentNode.state)):
			mpf += abs((currentNode.state.index(i) % 3 + 1) - (goalState.index(i) % 3 +1 )) + abs(3 - (currentNode.state.index(i) // 3) - (3 - (goalState.index(i) // 3)))
		return mpf

def file_output(*args):
	output = open("output.txt","wb")
	output.write("path_to_goal: %s \n" % (list(args[0].split(" ")[1:]))); #the sequence of moves taken to reach the goal
	output.write("cost_of_path: %s \n" % (args[1]));#the number of moves taken to reach the goal
	output.write("nodes_expanded: %i \n" % (args[2])); # the number of nodes that have been expanded
	output.write("search_depth: %i \n" % (args[3])); #the depth within the search tree when the goal node is found
	output.write("max_search_depth: %i \n" % (args[4]));#the maximum depth of the search tree in the lifetime of the algorithm
	output.write("running_time: %.8f \n" % (time.time() - startTime));# the total running time of the search instance, reported in seconds
	output.write("max_ram_usage: %.8f \n" % (float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024))
	output.close()

	read_file_output()
def read_file_output():
	output = open("output.txt","r+")
	# logging.debug("OPENING FILE OUTPUT\n"+output.read())
	print output.read()
	output.close()
def display(state): #display pretty
	if logging.getLogger().getEffectiveLevel() < logging.info:
		print "-------------"
		print "| %i | %i | %i |" % (state[0], state[1], state[2])
		print "-------------"
		print "| %i | %i | %i |" % (state[3], state[4], state[5])
		print "-------------"
		print "| %i | %i | %i |" % (state[6], state[7], state[8])
		print "-------------"


startTime = time.time()
algorithmName = sys.argv[1]
initialState = map(int,sys.argv[2].split(','))
goalState = sorted(initialState)

boardSize = 3
leftThreshold = set([0,3,6])
rightThreshold = set([2,5,8])
directionList = ["Up","Down","Left","Right"]

if initialState == goalState:
	logging.debug("No operation Needed. Input state is the goal state.")

else:
	possibles = globals().copy()
	possibles.update(locals())
	algorithm = possibles.get(algorithmName)
	if not algorithm:
	     raise NotImplementedError("Method %s not implemented" % algorithmName)
	solution = algorithm()  # call respective algorithms
	if solution:
		file_output(solution[0].pathToGoal,solution[0].costOfPath,solution[1],solution[0].costOfPath,solution[2])
	'''
	TODO:
		child of a node also has child ehich is his parent
		frontier class
		child nodes  too in nodein tempFrontier
		remove O(n^2)
		python -m cProfile -s tottime driver.py bfs 8,6,7,2,3,1,5,4,0
	'''
