'''
	Problem Solving for Computer Science - Assignment
	Wojciech Tyziniec, student of Computer Science
	Goldsmiths, University of London 2017


	INTRODUCTION
	----------------------------------------------------------------------------------------
	Consider a Toy world, containing a finite number n of objects.
	Each object is specified by a unique name.

	The current state of the world is described using a set of properties which specify
	the state the objects are in. 

	Only 3 possibly propositions are used to describe the state of the world:
	- ON(x, y)		- in the current state, object x is on top of object y
	- CLEAR(x)		- object x is clear, it has nothing on top of it
	- HEAVIER(x, y)	- object x is heavier than object y

	The current state of the world if specified by a finite sest of "ground instances"
	of the above propositions - instances obtained by replacing all the variables (x and y)
	with specific object names. 

	s1 = { 
			ON(A, table1), 
			HEAVIER(table1, A), 
			HEAVIER(table2, A), 
			CLEAR(A), 
			CLEAR(table2)} 

	The state above contains 5 propositions involving 3 objects (A, table1, table2).
	Here s1 describes a state in which object A is clear and is on top of table1, table2 is clear
	and table1 and table2 are both heavier than A.

	Note that the order of the propositions is irrelevant - a state is a set, not a sequence.

	In this Toy world only 1 action is possible, moving an object from its current location
	to a different one. This action is described by the "Move" operator below:

	Move(x, y, z):
		Preconditions: ON(x, y), CLEAR(x), HEAVIER(z, x)
		Add: ON(x, z), CLEAR(y)
		Delete: ON(x, y) CLEAR(z)


	Move(A, table1, table2) - moves object A from table1 to table2
'''

'''
Class: Operator(object)
----------------------------------------------------------------------------------------
Stores the details of our operators
'''
class Operator(object):
	def __init__(self, action, preconditions, add, delete):
		self.action = action
		self.preconditions = preconditions # List of preconditions 
		self.add = add
		self.delete = delete


'''
Class: Property(object)
----------------------------------------------------------------------------------------
Class for storing details of prepositions
Variable 'obj2' is optional. Our operator may require only one operator - e.g. CLEAR(x) vs HEAVIER(x, y). Its default value is set to be - "".
'''

class Property(object):
	def __init__(self, preposition, obj1, obj2):
		self.preposition = preposition
		self.obj1 = obj1
		self.obj2 = obj2

		'''
		Found on StackOverflow -> compares two object instances
		http://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python
		'''
		def __str__(self):
			return str(self.__dict__)

    	def __eq__(self, other): 
    		return self.__dict__ == other.__dict__


'''
Function: printCurrentState(object):
----------------------------------------------------------------------------------------
Helper function which prints out the content of problem['current_state'] list
'''
def printCurrentState(object):
	for x in range(0, len(object['current_state'])):
		print("Current state = " + object['current_state'][x].preposition + " " + object['current_state'][x].obj1  + " " + object['current_state'][x].obj2)


'''
Function: printOperators(object):
----------------------------------------------------------------------------------------
Helper function which prints out the content of problem['operators'] list
'''
def printOperators(object):
	for x in range(0, len(object['operators'])):
		print("Operator ",x," = ", object['operators'][x].action)

'''
Function: splitInputStringIntoProperties(object):
----------------------------------------------------------------------------------------
In this function the object (input from the user) is being parsed and chop up into small objects (Property).
'''
def splitInputStringIntoProperties(object):
	stringToSplit = object
	for x in range(0, len(object)):
		obj2 = "" # This variable is prepared for optional parameter - it may or may not exist
		tempState = stringToSplit[x]
		temp_pos1 = tempState.find("(")
		temp_pos2 = tempState.find(",")
		temp_pos3 = tempState.find(")")
		preposition = tempState[:temp_pos1]
		if tempState.find(",") == -1:
			obj1 = tempState[temp_pos1+1: temp_pos3]
		else:
			obj1 = tempState[temp_pos1+1: temp_pos2]
			obj2 = tempState[temp_pos2+1: temp_pos3]
		property = Property(preposition, obj1, obj2)
		object[x] = property # Replace string with created property


'''
Function: getInputFromUserAndSaveInsideProblemDictionary(object)
----------------------------------------------------------------------------------------
I think the function name explains everything.
'''

def getInputFromUserAndSaveInsideProblemDictionary(object):
	_problem = object

	obj = raw_input("Please enter object names: ")
	_problem['objects'] = obj.split()

	state = raw_input("Please enter the initial state: ")
	_problem['current_state'] = state.split()

	goal = raw_input("Please enter the goal state: ")
	_problem['goal_state'] = goal.split()


'''
Function: applyOperator(operator, current_state)
----------------------------------------------------------------------------------------
Function performs action of executing operator in the current_state.
It adds and deletes properties to and from the current_state.
'''
def applyOperator(operator, current_state):
	print("Applying operator: ", operator.action)
	indexesOfElementsToDelete = []
	# Adding two properties from the passed operator to the current_state
	current_state.append(operator.add[0])
	current_state.append(operator.add[1])
	for q in range(0, len(current_state)):
		if current_state[q] == operator.delete[0] or current_state[q] == operator.delete[1]:
			indexesOfElementsToDelete.append(q)

	for index in sorted(indexesOfElementsToDelete, reverse=True):
		del current_state[index]



'''
Function: generateOperatorsForCurrentState(objects, current_state, operators)
----------------------------------------------------------------------------------------
Explanation later...
'''
def generateOperatorsForCurrentState(objects, current_state, operators, reset):
	print("Generating operators...")
	# Reset current list of operators
	if reset == True:
		for z in range(0, len(operators)):
			del operators[0]

	for a in range(0, len(objects)):
		for b in range(0, len(current_state)):
			if current_state[b].preposition == "ON" and current_state[b].obj1 == objects[a]:
				preconditionProperty1 = Property(current_state[b].preposition, current_state[b].obj1, current_state[b].obj2)
				for c in range(0, len(current_state)):
					if current_state[c].preposition == "CLEAR" and current_state[c].obj1 == objects[a]:
						preconditionProperty3 = Property(current_state[c].preposition, current_state[c].obj1, "")
						for d in range(0, len(current_state)):
							if current_state[d].preposition == "HEAVIER" and current_state[d].obj2 == objects[a]:
								heavierFirstObject = current_state[d].obj1
								preconditionProperty4 = Property(current_state[d].preposition, heavierFirstObject, objects[a])
								for e in range(0, len(current_state)):
									if current_state[e].preposition == "CLEAR" and current_state[e].obj1 == heavierFirstObject:
										preconditionProperty2 = Property(current_state[e].preposition, heavierFirstObject, "")
										op = Operator(["Move",preconditionProperty1.obj1, preconditionProperty1.obj2, preconditionProperty2.obj1], #from X on Y to Z
												[preconditionProperty1, preconditionProperty2, preconditionProperty3, preconditionProperty4], 
												[Property(preconditionProperty1.preposition, preconditionProperty1.obj1, preconditionProperty2.obj1), Property(preconditionProperty2.preposition, preconditionProperty1.obj2, "")],
												[Property(preconditionProperty1.preposition, preconditionProperty1.obj1, preconditionProperty1.obj2), Property(preconditionProperty2.preposition, preconditionProperty2.obj1, "")])
										operators.append(op)
										print("Operator added to the list = ", op.action)

'''
Function: removeSolvedStatesFromTheGoalState(goal_state, current_state)
----------------------------------------------------------------------------------------
This function removes states from the goal_state list which are included in the current_state list.
'''
def removeSolvedStatesFromTheGoalState(goal_state, current_state):
	print("There are " + str(len(goal_state)) + " states in the goal_state before comparing with current_state")
	indexesOfElementsToDelete = []
	for x in range(0, len(goal_state)):
		for y in range(0, len(current_state)):
			if current_state[y] == goal_state[x]:
				indexesOfElementsToDelete.append(x)
				print("I have found state from the goal_state which is included in the current_state list! I'm gonna remove it from the goal_state.")

	print("I should delete ", len(indexesOfElementsToDelete), " states.")
	for index in sorted(indexesOfElementsToDelete, reverse=True):
		del goal_state[index]

	print("There are " + str(len(goal_state)) + " states left in the goal_state list.")


'''
Function: makeSpaceForObjectFromTheGoalState(goal_state, current_state)
----------------------------------------------------------------------------------------
Explanaition blahblahblah
'''
def makeSpaceForObjectFromTheGoalState(goal_state, current_state):
	for x in range(0, len(goal_state)):
		if goal_state[x].preposition == "ON":
			for m in range(0, len(current_state)):			
				if current_state[m].preposition == "CLEAR" and current_state[m].obj1 == goal_state[x].obj2:
					print("Jest miejsce!")
				else:													#table2				table2
					if current_state[m].preposition == "ON" and current_state[m].obj2 == goal_state[x].obj2:
						print("first condition")
						for k in range(0, len(current_state)):					
							if current_state[k].preposition == "HEAVIER" and current_state[k].obj2 == current_state[m].obj1:
								print("second condition")
								for s in range(0, len(current_state)):
									if current_state[s].preposition == "CLEAR" and current_state[s].obj1 == current_state[k].obj1:
										print("third cond")
										print("Move ", current_state[m].obj1, " from ", current_state[m].obj2, " to ", current_state[s].obj1)
										preconditionProperty1 = Property(current_state[m].preposition, current_state[m].obj1, current_state[m].obj2)
										preconditionProperty2 = Property(current_state[s].preposition, current_state[s].obj1, "")
										preconditionProperty3 = Property(current_state[s].preposition, current_state[m].obj1, "")
										preconditionProperty4 = Property(current_state[k].preposition, current_state[s].obj1, current_state[m].obj1)
										op = Operator(["Move", current_state[m].obj1, current_state[m].obj2, current_state[s].obj1],
											[preconditionProperty1, preconditionProperty2, preconditionProperty3, preconditionProperty4],
											[Property(current_state[m].preposition, current_state[m].obj1, current_state[s].obj1), Property(current_state[s].preposition, current_state[m].obj2, "")],
											[Property(current_state[m].preposition, current_state[m].obj1, current_state[m].obj2), Property(current_state[s].preposition, current_state[s].obj1, "")])
										return op

'''
Function: main()
----------------------------------------------------------------------------------------
The main function is called at the program startup,
it is the designated entry point to a program that is executed in hosted environment.
'''
def main():

	'''
	Variable: problem
	----------------------------------------------------------------------------------------
	The most important variable in this application. 
	It stores objects, states and operators throughout the execution time.
	'''
	problem = {
	"objects": [],
	"current_state": [],
	"goal_state": [],
	"operators":[]}



	'''
	Temporarily commented - for tests purpose
	getInputFromUserAndSaveInsideProblemDictionary(problem)
	'''

	temp_obj = "table1 table2 A"
	temp_state = "ON(A,table1) HEAVIER(table1,A) HEAVIER(table2,A) CLEAR(A) CLEAR(table2)"
	temp_goal = "CLEAR(table1) CLEAR(A)"

	problem['objects'] = temp_obj.split()
	problem['current_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()

	splitInputStringIntoProperties(problem['current_state'])
	splitInputStringIntoProperties(problem['goal_state'])
	removeSolvedStatesFromTheGoalState(problem['goal_state'], problem['current_state'])
	generateOperatorsForCurrentState(problem['objects'], problem['current_state'], problem['operators'], True)
	#printOperators(problem)

	# Trying to solve all goals - it is not an infinite loop, because we can assume that our problem is solvable
	# Do while there are states in the goal_state list to be solved - we delete a single state when we solve it
	while problem['goal_state']:
		print("There are ", len(problem['operators']), " operators in the list" + "\n")
		printOperators(problem)
		# Searching for operators which may solve the state from the goal_states
		for x in range(0, len(problem['goal_state'])): #for all goal states
			for y in range(0, len(problem['operators'])): #look through all operators
				for z in range(0, len(problem['operators'][y].add)): #and check if its property from add list is equal to property from the goal state
					if (problem['operators'][y].add[z].preposition == problem['goal_state'][x].preposition) and (problem['operators'][y].add[z].obj1 == problem['goal_state'][x].obj1) and (problem['operators'][y].add[z].obj2 == problem['goal_state'][x].obj2):
						print("I have found operator which can solve " + problem['goal_state'][x].preposition + " " + problem['goal_state'][x].obj1 + " " + problem['goal_state'][x].obj2 + " state from the goal_state!")
						print("To achieve your goals you have to: " + problem['operators'][y].action[0] + " " + problem['operators'][y].action[1] + " " + problem['operators'][y].action[2] + " " + problem['operators'][y].action[3])
						print("Current state before taking action: ")
						printCurrentState(problem)
						applyOperator(problem['operators'][y], problem['current_state'])
						print("\nCurrent state after taking action: ")
						printCurrentState(problem)

						
					#else:						
						#print("Still searching...")
		generateOperatorsForCurrentState(problem['objects'], problem['current_state'], problem['operators'], True)
		removeSolvedStatesFromTheGoalState(problem['goal_state'], problem['current_state'])

		if not problem['goal_state']:
			break
		else:
			print("space space space space")
			opMove = makeSpaceForObjectFromTheGoalState(problem['goal_state'], problem['current_state'])
			if(type(opMove) == Operator):
				applyOperator(opMove, problem['current_state'])
				printCurrentState(problem)

	




if __name__ == "__main__":
	main()