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



	SOLUTION -> [means-ends analysis (to generate goal states and operators) + GPS(General Problem Solver, 1959), + knowledge about Tower of Hanoi problem]
	----------------------------------------------------------------------------------------
	How my program works: 

	1) Compare the current state with the goal state. If there is no difference between them the problem is solved.
	2) If there is a difference between the current state and the goal state, set a goal to solve that difference.
	   If there is more than one difference, set a goal to solve the largest difference.
	3) Select an operator that will solve the difference from the step 2
	4) If an operator can be applied, apply it. If it cannot, set a new goal to reach a state that would allow the application of the operator.
	5) Return to Step 1 with the new goal set in Step 4.

'''

# Uncomment all  print() commands to turn on a "debugging mode".

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
Variable 'obj2' is optional. Our prepositions may require only one parameter - e.g. CLEAR(x) vs HEAVIER(x, y). Its default value is set to be - "".
'''

class Property(object):
	def __init__(self, preposition, obj1, obj2):
		self.preposition = preposition
		self.obj1 = obj1
		self.obj2 = obj2
		def __str__(self):
			return '%s %s %s' %(self.preposition, self.obj1, self.obj2)

'''
Function: addSubgoals(state, current_state, goal_state):
----------------------------------------------------------------------------------------
This is a recursive function. 
For a given state, it checks if object from that state has another object on top of it, and so on.
'''
def addSubgoals(state, current_state, goal_state):
	# If my object has something on top of it
	for x in range(0, len(current_state)):
		if state.obj1 == current_state[x].obj2 and current_state[x].preposition == "ON":
			#print("On top of object " + state.obj1 + " is object " + current_state[x].obj1)
			goal_state.append(Property("CLEAR", state.obj1, ""))
			addSubgoals(Property("CLEAR", current_state[x].obj1, ""), current_state, goal_state)

	# If the source place has something on top of it
	for y in range(0, len(current_state)):
		if state.obj2 == current_state[y].obj2 and current_state[y].preposition == "ON":
			#print("On top of object " + state.obj2 + " is object " + current_state[y].obj1)
			goal_state.append(Property("CLEAR", state.obj2, ""))
			addSubgoals(Property("CLEAR", current_state[y].obj1, ""), current_state, goal_state)
'''
Function: applyOperator(operator, current_state):
----------------------------------------------------------------------------------------
Function performs action of executing operator in the current_state.
It adds and deletes properties to and from the current_state.
'''
def applyOperator(operator, current_state):
	#print("Applying operator: ", operator.action)
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
Function: findDifferencesBetweenGoalStateAndCurrentState(goal, current):
----------------------------------------------------------------------------------------
At the beginning, we remove duplicate states from the current state.
Then our goal state and current state are compared to each other, if every element of the goal state is inside the current state,
then we know that our problem is solved.
Function returns states from the goal state which are not a part of the current state yet and have to be solved.
'''
def findDifferencesBetweenGoalStateAndCurrentState(goal, current):
	# Here we remove duplicates
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
		#print("Goal state is a subset of current state! Problem is solved!")
		True
	else:
		#print("Goal state is not a subset of current state!")
		for x in range(0, len(goal)):
			count = 0;
			for y in range(0, len(current)):
				if(compareTwoObjects(goal[x], current[y])):
					count += 1
			if not count > 0:
				goalsToBeSolved.append(goal[x])
				#print("The state: " + goal[x].preposition + "(" + goal[x].obj1 + "," + goal[x].obj2 + ") is not in the current state!")

	return goalsToBeSolved

'''
Function: generateOperatorsForCurrentState(objects, current_state, operators, reset):
----------------------------------------------------------------------------------------
Iterates through a list of objects and current_states and checks preconditions, 
if all four preconditions are fulfilled, then it generates Move operator and adds to the problem['operators'] list.
'''
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
										#print("Operator added to the list = ", op.action)
										#print("It adds " + op.add[0].preposition + "(" + op.add[0].obj1 + "," + op.add[0].obj2 + ")")
										#print("It adds " + op.add[1].preposition + "(" + op.add[1].obj1 + "," + op.add[1].obj2 + ")")
										#print("It deletes " + op.delete[0].preposition + "(" + op.delete[0].obj1 + "," + op.delete[0].obj2 + ")")
										#print("It deletes " + op.delete[1].preposition + "(" + op.delete[1].obj1 + "," + op.delete[1].obj2 + ")")

'''
Function: getInputFromUserAndSaveInsideProblemDictionary(object)
----------------------------------------------------------------------------------------
Hmmm, the function name explains everything.
'''

def getInputFromUserAndSaveInsideProblemDictionary(object):
	_problem = object

	obj = input("Please enter object names: ")
	_problem['objects'] = obj.split()

	state = input("Please enter the initial state: ")
	_problem['current_state'] = state.split()

	goal = input("Please enter the goal state: ")
	_problem['goal_state'] = goal.split()

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

'''
Function: removeSolvedStatesFromTheGoalState(goal_state, current_state):
----------------------------------------------------------------------------------------
This function removes states from the goal_state list which are included in the current_state list (solved).
'''
def removeSolvedStatesFromTheGoalState(goal_state, current_state):
	if len(goal_state) > 0:
		#print("There are " + str(len(goal_state)) + " states in the goal_state before comparing with current_state")
		indexesOfElementsToDelete = []
		for x in range(0, len(goal_state)):
			for y in range(0, len(current_state)):
				if compareTwoObjects(current_state[y], goal_state[x]):
					indexesOfElementsToDelete.append(x)
					#print("I have found state from the goal_state which is included in the current_state list! I'm gonna remove it from the goal_state.")
					break

		#print("I should delete ", len(indexesOfElementsToDelete), " states.")
		for index in sorted(indexesOfElementsToDelete, reverse=True):
			del goal_state[index]

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

	getInputFromUserAndSaveInsideProblemDictionary(problem)
	'''
	During development process, I didn't want to input objects and states every single time I ran the app.
	If you want to test my app this way, comment line getInputFromUserAndSaveInsideProblemDictionary(problem), 
	uncomment following 6 lines and insert your test data.

	temp_obj = "A B P1 P2 T1 T2 T3"
	temp_state = "CLEAR(P2) ON(P2,A) ON(A,T2) ON(T2,B) CLEAR(T1) CLEAR(P1) HEAVIER(A,P2) HEAVIER(T2,A) HEAVIER(B,P2) HEAVIER(P1,P2) HEAVIER(T1,A) HEAVIER(P1,T2)"
	temp_goal = "ON(P2,A) ON(A,T2) ON(T2,P1)"

	problem['objects'] = temp_obj.split()
	problem['current_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()
	'''

	splitInputStringIntoProperties(problem['current_state'])
	splitInputStringIntoProperties(problem['goal_state'])
	goalStates = findDifferencesBetweenGoalStateAndCurrentState(problem['goal_state'], problem['current_state'])

	#printCurrentState(problem)
	#for x in range(0, len(goalStates)):
		#print(goalStates[x].preposition + "(" + goalStates[x].obj1 + "," + goalStates[x].obj2 + ")")
	#printCurrentState(problem)

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
							#print("I have found operator which can solve " + goalStates[x].preposition + " " + goalStates[x].obj1 + " " + goalStates[x].obj2 + " state from the goal_state!")
							#print("To achieve your goals you have to: " + problem['operators'][y].action[0] + " " + problem['operators'][y].action[1] + " " + problem['operators'][y].action[2] + " " + problem['operators'][y].action[3])
							applyOperator(problem['operators'][y], problem['current_state'])
							print(problem['operators'][y].action[0] + "(" + problem['operators'][y].action[1] + "," + problem['operators'][y].action[2] + "," + problem['operators'][y].action[3] + ")")
				generateOperatorsForCurrentState(problem['objects'], problem['current_state'], problem['operators'], True)

			if len(goalStates) > 0:
				removeSolvedStatesFromTheGoalState(goalStates, problem['current_state'])


		#for x in range(0, len(goalStates)):
			#print(goalStates[x].preposition + "(" + goalStates[x].obj1 + "," + goalStates[x].obj2 + ")")
	#printCurrentState(problem)
if __name__ == "__main__":
	main()