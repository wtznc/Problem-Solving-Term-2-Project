'''
Class: Operator(object)
-------------------------------------------------------------
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
--------------------------------------------------------------
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
-------------------------------------------------------------
Helper function which prints out the content of problem['current_state'] list
'''
def printCurrentState(object):
	for x in range(0, len(object['current_state'])):
		print("Current state = " + object['current_state'][x].preposition + " " + object['current_state'][x].obj1  + " " + object['current_state'][x].obj2)


'''
Function: splitInputStringIntoProperties(object):
----------------------------------------------------------------
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
------------------------------------------------------------------
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
-------------------------------------------------------------------
Function performs action of executing operator in the current_state.
It adds and deletes properties to and from the current_state.
'''
def applyOperator(operator, current_state):
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
---------------------------------------------------------------------
Explanation later...
'''
def generateOperatorsForCurrentState(objects, current_state, operators):
	# Reset current list of operators
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
-----------------------------------------------------------------------------
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
Function: main()
-----------------------------------------------------------------
The main function is called at the program startup,
it is the designated entry point to a program that is executed in hosted environment.
'''
def main():

	'''
	Variable: problem
	--------------------------------------------------
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

	temp_obj = "table1 table2 A table3 table4 B "
	temp_state = "ON(A,table1) HEAVIER(table1,A) HEAVIER(table2,A) CLEAR(A) CLEAR(table2) ON(B,table3) HEAVIER(table3,B) HEAVIER(table4,B) CLEAR(B) CLEAR(table4) HEAVIER(table4,A) HEAVIER(table1,B)"
	temp_goal = "ON(B,table4)"

	problem['objects'] = temp_obj.split()
	problem['current_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()

	splitInputStringIntoProperties(problem['current_state'])
	splitInputStringIntoProperties(problem['goal_state'])
	removeSolvedStatesFromTheGoalState(problem['goal_state'], problem['current_state'])

	# Trying to solve all goals
	# Do while there are states in the goal_state list to be solved
	while problem['goal_state']:
		generateOperatorsForCurrentState(problem['objects'], problem['current_state'], problem['operators'])
		print("There are ", len(problem['operators']), " operators in the list")

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
						removeSolvedStatesFromTheGoalState(problem['goal_state'], problem['current_state'])
						if(not problem['goal_state']):
							break
					else:
						print("I don't know how to solve it!")




if __name__ == "__main__":
	main()