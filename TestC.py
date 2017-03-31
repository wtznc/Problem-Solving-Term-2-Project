'''
	Problem Solving for Computer Science - Assignment V2
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

# Uncomment all  print() commands to turn on a "debugging mode" :).

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
Variable 'obj2' is optional. Our operators may require only one parameter - e.g. CLEAR(x) vs HEAVIER(x, y). Its default value is set to be - "".
'''

class Property(object):
	def __init__(self, preposition, obj1, obj2):
		self.preposition = preposition
		self.obj1 = obj1
		self.obj2 = obj2
		def __str__(self):
			return '%s %s %s' %(self.preposition, self.obj1, self.obj2)

'''
Function: compareTwoObjects(object1, object2):
----------------------------------------------------------------------------------------
This function compares two Property objects and returns True if they are the same, or False when they are different.
Created as a replacement for the code found on Stack Overflow.
http://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python
'''
def compareTwoObjects(object1, object2):
		if type(object1) != type(object2):
			return False
		if type(object1) == Property and type(object2) == Property:
			if object1.preposition == object2.preposition and object1.obj1 == object2.obj1 and object1.obj2 == object2.obj2:
				return True
			else:
				return False
		else:
			return False

'''
Function: splitInputStringIntoProperties(object):
----------------------------------------------------------------------------------------
In this function the object (input from the user) is being parsed and chopped up into small objects (Property).
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
Function: printCurrentState(object):
----------------------------------------------------------------------------------------
Helper function which prints out the content of problem['current_state'] list
'''
def printCurrentState(object):
	str = ""
	for x in range(0, len(object['current_state'])):
		str += object['current_state'][x].preposition + "(" + object['current_state'][x].obj1 + ", " + object['current_state'][x].obj2 + ") "
	print(str)

def findDifferencesBetweenGoalStateAndCurrentState(goal, current):
	result = []
	for x in current:
		if x not in result:
			result.append(x)
	current = result

	counter = 0;
	goalsToBeSolved = []
	for x in range(0, len(current)):
		for y in range(0, len(goal)):
			if(compareTwoObjects(current[x], goal[y])):
				counter = counter + 1
				break;
	if counter == len(goal):
		print("Goal state is a subset of current state! Problem is solved!")
	else:
		print("Goal state is not a subset of current state!")
		for x in range(0, len(goal)):
			count = 0;
			for y in range(0, len(current)):
				if(compareTwoObjects(goal[x], current[y])):
					count += 1
			if not count > 0:
				goalsToBeSolved.append(goal[x])
				print("The state: " + goal[x].preposition + "(" + goal[x].obj1 + "," + goal[x].obj2 + ") is not in the current state!")

	return goalsToBeSolved

def addSubgoals(state, current_state, goal_state):
	# If my object has something on top of it
	for x in range(0, len(current_state)):
		if state.obj1 == current_state[x].obj2 and current_state[x].preposition == "ON":
			print("On top of object " + state.obj1 + " is object " + current_state[x].obj1)
			goal_state.append(Property("CLEAR", state.obj1, ""))
			addSubgoals(Property("CLEAR", current_state[x].obj1, ""), current_state, goal_state)
	# If the source place has something on top of it
	for y in range(0, len(current_state)):
		if state.obj2 == current_state[y].obj2 and current_state[y].preposition == "ON":
			print("On top of object " + state.obj2 + " is object " + current_state[y].obj1)
			goal_state.append(Property("CLEAR", state.obj2, ""))
			addSubgoals(Property("CLEAR", current_state[y].obj1, ""), current_state, goal_state)

def generateOperatorsForCurrentState(objects, current_state, operators, reset):
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
										#print("It adds " + op.add[0].preposition + "(" + op.add[0].obj1 + "," + op.add[0].obj2 + ")")
										#print("It adds " + op.add[1].preposition + "(" + op.add[1].obj1 + "," + op.add[1].obj2 + ")")
										#print("It deletes " + op.delete[0].preposition + "(" + op.delete[0].obj1 + "," + op.delete[0].obj2 + ")")
										#print("It deletes " + op.delete[1].preposition + "(" + op.delete[1].obj1 + "," + op.delete[1].obj2 + ")")

def applyOperator(operator, current_state):
	print("Applying operator: ", operator.action)
	indexesOfElementsToDelete = []

	# Adding two properties from the passed operator to the current_state
	current_state.append(operator.add[0])
	current_state.append(operator.add[1])

	# Removing two properties from the current_state
	for q in range(0, len(current_state)):
		if compareTwoObjects(current_state[q], operator.delete[0]) == True or compareTwoObjects(current_state[q], operator.delete[1]) == True:
			indexesOfElementsToDelete.append(q)

	for index in sorted(indexesOfElementsToDelete, reverse=True):
		del current_state[index]

def removeSolvedStatesFromTheGoalState(goal_state, current_state):
	if goal_state > 0:
		print("There are " + str(len(goal_state)) + " states in the goal_state before comparing with current_state")
		indexesOfElementsToDelete = []
		for x in range(0, len(goal_state)):
			for y in range(0, len(current_state)):
				if compareTwoObjects(current_state[y], goal_state[x]):
					indexesOfElementsToDelete.append(x)
					print("I have found state from the goal_state which is included in the current_state list! I'm gonna remove it from the goal_state.")
					break

		print("I should delete ", len(indexesOfElementsToDelete), " states.")
		for index in sorted(indexesOfElementsToDelete, reverse=True):
			del goal_state[index]

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
		"operators": []}

	temp_obj = "A B C D E table1 table2 table3 table4 table5 table6 table7 table8 table9 table10"
	temp_state = "ON(A,table1) ON(B,table2) ON(C,table3) ON(D,table4) ON(E,table5) CLEAR(A) CLEAR(B) CLEAR(C) CLEAR(D) CLEAR(D) CLEAR(E) HEAVIER(A,table1) HEAVIER(B,table2) HEAVIER(C,table3) HEAVIER(D,table4) HEAVIER(E,table5) CLEAR(table6) CLEAR(table7) HEAVIER(table6,A) HEAVIER(table7,B) CLEAR(table8) CLEAR(table9) CLEAR(table10) HEAVIER(table8,C)"
	#temp_goal = "CLEAR(P2) ON(P2,A)"
	temp_goal = "ON(A,table6) ON(B,table7) ON(C,table8)"

	problem['objects'] = temp_obj.split()
	problem['current_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()

	splitInputStringIntoProperties(problem['current_state'])
	splitInputStringIntoProperties(problem['goal_state'])
	printCurrentState(problem)
	goalStates = findDifferencesBetweenGoalStateAndCurrentState(problem['goal_state'], problem['current_state'])

	for x in range(0, len(goalStates)):
		print(goalStates[x].preposition + "(" + goalStates[x].obj1 + "," + goalStates[x].obj2 + ")")

	printCurrentState(problem)
	while len(findDifferencesBetweenGoalStateAndCurrentState(problem['goal_state'], problem['current_state'])) > 0:
		goalStates = findDifferencesBetweenGoalStateAndCurrentState(problem['goal_state'], problem['current_state'])

		while len(goalStates) > 0:
			if len(goalStates) == 1:
				addSubgoals(goalStates[0], problem['current_state'], goalStates)

			generateOperatorsForCurrentState(problem['objects'], problem['current_state'], problem['operators'], True)
			for x in range(0, len(goalStates)): # For all goal states
				for y in range(0, len(problem['operators'])): # Look through all operators
					for z in range(0, len(problem['operators'][y].add)): # And check if its property from the add list is equal to the property from the goal state
						if (problem['operators'][y].add[z].preposition == goalStates[x].preposition) and (problem['operators'][y].add[z].obj1 == goalStates[x].obj1) and (problem['operators'][y].add[z].obj2 == goalStates[x].obj2):
							print("I have found operator which can solve " + goalStates[x].preposition + " " + goalStates[x].obj1 + " " + goalStates[x].obj2 + " state from the goal_state!")
							print("To achieve your goals you have to: " + problem['operators'][y].action[0] + " " + problem['operators'][y].action[1] + " " + problem['operators'][y].action[2] + " " + problem['operators'][y].action[3])
							applyOperator(problem['operators'][y], problem['current_state'])
							print(problem['operators'][y].action[0] + "(" + problem['operators'][y].action[1] + "," + problem['operators'][y].action[2] + "," + problem['operators'][y].action[3]) + ")"
				generateOperatorsForCurrentState(problem['objects'], problem['current_state'], problem['operators'], True)

			if len(goalStates) > 0:
				removeSolvedStatesFromTheGoalState(goalStates, problem['current_state'])


		for x in range(0, len(goalStates)):
			print(goalStates[x].preposition + "(" + goalStates[x].obj1 + "," + goalStates[x].obj2 + ")")


	printCurrentState(problem)
if __name__ == "__main__":
	main()