import time
import resource
import sys
from collections import OrderedDict
import heapq


#define rows and coloumns
ROWS = 3
COLS = 3
#define goal state
goal_state = 	[0,1,2,3,4,5,6,7,8]



class Node:
	state = None
	depth = 0
	# child_nodes=[]
	def __init__(self,state,parent=None,move=None,depth=0):
		self.state = state
		self.parent = parent
		self.move = move
		self.depth = depth

	def add_childnode(self,node):
		self.child_nodes.append(node)


#game functions wrt zero, i.e. move_up function moves the zero one row up
def Up(state):
	temp_state = state[:]
	i = temp_state.index(0)
	if i>=3:
		val= temp_state[i]
		temp_state[i]= temp_state[i-3]
		temp_state[i-3] = val
		return temp_state,"Up"
	return None,None

def Down(state):
	temp_state = state[:]
	i = temp_state.index(0)
	if i<= 5:
		val= temp_state[i]
		temp_state[i] = temp_state[i+3]
		temp_state[i+3] = val
		return temp_state,"Down"
	return None,None

def Right(state):
	temp_state = state[:]
	i = temp_state.index(0)
	if i not in [2,5,8]:
		val = temp_state[i]
		temp_state[i] = temp_state[i+1]
		temp_state[i+1] = val
		return temp_state,"Right"
	return None,None

def Left(state):
	temp_state = state[:]
	i = temp_state.index(0)
	if i not in [0,3,6]:
		val = temp_state[i]
		temp_state[i] = temp_state[i-1]
		temp_state[i-1] = val
		return temp_state,"Left"
	return None,None

def find_neighbours_nodes(node,order):
	state = node.state
	neighbours_nodes = []
	depth = node.depth+1
	temp_state,move = order[0](state)
	if temp_state:
		neighbours_nodes.append(Node(temp_state,node,move,depth))
	temp_state,move = order[1](state)
	if temp_state:
		neighbours_nodes.append(Node(temp_state,node,move,depth))
	temp_state,move = order[2](state)
	if temp_state:
		neighbours_nodes.append(Node(temp_state,node,move,depth))
	temp_state,move = order[3](state)
	if temp_state:
		neighbours_nodes.append(Node(temp_state,node,move,depth))
	return neighbours_nodes

def get_2D_cood(cood):
	if cood>2 and cood<6:
		return 1,cood-3
	elif cood>5 and cood<9:
		return 2, cood-6
	else:
		return 0,cood

def calculate_manhattan_distance(state):
	distance = 0
	for i in range(1,9):
		x_i_g, y_i_g = get_2D_cood(i)
		x_i_s, y_i_s = get_2D_cood(state.index(i))
		distance += abs(x_i_s- x_i_g)+abs(y_i_s- y_i_g)
	return distance

def write_to_file(path_to_goal,cost_of_path,nodes_expanded,search_depth,max_search_depth,running_time,max_ram_usage=0):
	with open("output.txt",'w') as fid:
		fid.write("path_to_goal: ")
		fid.write(str(path_to_goal))
		fid.write("\ncost_of_path: ")
		fid.write(str(cost_of_path))
		fid.write("\nnodes_expanded: ")
		fid.write(str(nodes_expanded))
		fid.write("\nsearch_depth: ")
		fid.write(str(search_depth))
		fid.write("\nmax_search_depth: ")
		fid.write(str(max_search_depth))
		fid.write("\nrunning_time: ")
		fid.write(str(running_time))
		fid.write("\nmax_ram_usage: ")
		fid.write(str(max_ram_usage)+"\n")

def bfs(initial_state):

	start = time.time()

	#define statistics
	path_to_goal = []	#sequence of moves taken to reach the goal
	cost_of_path = 0	#number of moves taken to reach the goal
	nodes_expanded = 0	#number of nodes that has been expanded
	search_depth = 0	#depth when the goal is found
	max_search_depth=0	#max depth of search tree in the lifetime of the algorithm
	running_time =0 	#total running time
	max_ram_usage =0	#max RAM usage in the lifetime of the algorithm


	#define explored, fringe, unexplored nodes
	root_node = Node(initial_state)
	explored=OrderedDict()#holds the explored nodes
	frontier=OrderedDict()
	frontier[hash(str(root_node.state))]=root_node #holds the node queue


	while frontier:
		current_node= frontier.popitem(last=False)[1]

		#goalTest
		if current_node.state==goal_state:
			cost_of_path = current_node.depth
			search_depth = cost_of_path
			while current_node.parent:
				path_to_goal.append(current_node.move)
				current_node = current_node.parent
			end = time.time()
			path_to_goal = [x for x in reversed(path_to_goal)]


			running_time = end - start
			max_ram_usage = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/(1024)
			write_to_file(path_to_goal,cost_of_path,nodes_expanded,search_depth,max_search_depth,running_time,max_ram_usage)
			return True

		st=time.time()
		neighbour_nodes= find_neighbours_nodes(current_node,[Up,Down,Left,Right])


		unexplored_neighbour = []
		for x in neighbour_nodes:
			hash_val = hash(str(x.state))
			try:
				frontier[hash_val]  #raises error if key is absent
				continue
			except KeyError:
				try:
					explored[hash_val]
					continue
				except KeyError:
					unexplored_neighbour.append(x)

		if unexplored_neighbour: #there are unexplored child nodes
			for neighbour in unexplored_neighbour:
				max_search_depth = max(max_search_depth,neighbour.depth)
				frontier[hash(str(neighbour.state))]=neighbour

		nodes_expanded+=1
		explored[hash(str(current_node.state))]=current_node

	return False

def dfs(initial_state):
	start = time.time()

	#define statistics
	path_to_goal = []	#sequence of moves taken to reach the goal
	cost_of_path = 0	#number of moves taken to reach the goal
	nodes_expanded = 0	#number of nodes that has been expanded
	search_depth = 0	#depth when the goal is found
	max_search_depth=0	#max depth of search tree in the lifetime of the algorithm
	running_time =0 	#total running time
	max_ram_usage =0	#max RAM usage in the lifetime of the algorithm


	#define explored, fringe, unexplored nodes
	root_node = Node(initial_state)
	explored=OrderedDict()#holds the explored nodes
	frontier=OrderedDict()
	frontier[hash(str(root_node.state))]=root_node #holds the node queue


	while frontier:
		current_node= frontier.popitem()[1]
		max_search_depth=max(current_node.depth,max_search_depth)

		#goalTest
		if current_node.state==goal_state:
			cost_of_path = current_node.depth
			search_depth = cost_of_path
			while current_node.parent:
				path_to_goal.append(current_node.move)
				current_node = current_node.parent
			end = time.time()
			path_to_goal = [x for x in reversed(path_to_goal)]


			running_time = end - start
			max_ram_usage = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/(1024)
			write_to_file(path_to_goal,cost_of_path,nodes_expanded,search_depth,max_search_depth,running_time,max_ram_usage)
			return True

		st=time.time()
		neighbour_nodes= find_neighbours_nodes(current_node,[Right,Left,Down,Up])


		unexplored_neighbour = []
		for x in neighbour_nodes:
			hash_val = hash(str(x.state))
			try:
				frontier[hash_val]  #raises error if key is absent
				continue
			except KeyError:
				try:
					explored[hash_val]
					continue
				except KeyError:
					unexplored_neighbour.append(x)

		if unexplored_neighbour: #there are unexplored child nodes
			for neighbour in unexplored_neighbour:
				frontier[hash(str(neighbour.state))]=neighbour

		nodes_expanded+=1
		# print nodes_expanded

		explored[hash(str(current_node.state))]=current_node

	return False

def ast(initial_state):
	start = time.time()

	#define statistics
	path_to_goal = []	#sequence of moves taken to reach the goal
	cost_of_path = 0	#number of moves taken to reach the goal
	nodes_expanded = 0	#number of nodes that has been expanded
	search_depth = 0	#depth when the goal is found
	max_search_depth=0	#max depth of search tree in the lifetime of the algorithm
	running_time =0 	#total running time
	max_ram_usage =0	#max RAM usage in the lifetime of the algorithm


	#define explored, fringe, unexplored nodes
	root_node = Node(initial_state)
	explored=OrderedDict()#holds the explored nodes
	frontier = []#create an empty heap
	frontier_state=OrderedDict()
	frontier_state[hash(str(root_node.state))]=root_node #holds the node queue
	heapq.heappush(frontier,(root_node.depth+calculate_manhattan_distance(root_node.state),root_node))#add root node to the heap
	while frontier:
		tot_cost,current_node = heapq.heappop(frontier)
		max_search_depth=max(current_node.depth,max_search_depth)
		#goalTest
		if current_node.state==goal_state:
			# print len(explored)
			cost_of_path = current_node.depth
			search_depth = cost_of_path
			while current_node.parent:
				path_to_goal.append(current_node.move)
				current_node = current_node.parent
			end = time.time()
			path_to_goal = [x for x in reversed(path_to_goal)]


			running_time = end - start
			max_ram_usage = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/(1024)
			write_to_file(path_to_goal,cost_of_path,nodes_expanded,search_depth,max_search_depth,running_time,max_ram_usage)
			return True

		st=time.time()
		neighbour_nodes= find_neighbours_nodes(current_node,[Up,Down,Left,Right])


		unexplored_neighbour = []
		for x in neighbour_nodes:
			hash_val = hash(str(x.state))
			try:
				explored[hash_val]
				continue
			except KeyError:
				try:
					frontier_state[hash_val]
					continue
				except KeyError:
					frontier_state[hash(str(x.state))]=x
					# print calculate_manhattan_distance(x.state)
					# raw_input("show")
					heapq.heappush(frontier,(x.depth+calculate_manhattan_distance(x.state),x))


		nodes_expanded+=1
		explored[hash(str(current_node.state))]=current_node
	return False




def main():
	#get method and initial state

	arguments = sys.argv
	method = arguments[1]
	initial_state = [int(x) for x in list(arguments[2]) if x!= ',']
	if method=="bfs":
		bfs(initial_state)
	elif method=="dfs":
		dfs(initial_state)
	elif method=="ast":
		ast(initial_state)
	import driver
	# driver.read_file_output()


if __name__ == '__main__':
	main()
