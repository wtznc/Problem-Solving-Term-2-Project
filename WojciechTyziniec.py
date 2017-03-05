'''
Function: printCurrentState(object):
-------------------------------------------------------------
Helper function which prints out the content of problem['current_state'] list
'''
def printCurrentState(object):
	for x in range(0, len(object['current_state'])):
		print("Current state = " + object['current_state'][x].preposition + " " + object['current_state'][x].obj1  + " " + object['current_state'][x].obj2)


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
Function: splitInputStringIntoProperties(object):
----------------------------------------------------------------
In this function the object (input from the user) is being parsed and chop up into small objects (Property).
'''
def splitInputStringIntoProperties(object):
	stringToSplit = object
	for x in range(0, len(object)):
		obj2 = "" #This variable is prepared for optional parameter - it may or may not exist
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

	temp_obj = "table1 table2 A table3 table4 B"
	temp_state = "ON(A,table1) HEAVIER(table1,A) HEAVIER(table2,A) CLEAR(A) CLEAR(table2) ON(B,table3) HEAVIER(table3,B) HEAVIER(table4,B) CLEAR(B) CLEAR(table4)"
	temp_goal = "CLEAR(table1) CLEAR(A) CLEAR(table3) CLEAR(B)"

	problem['objects'] = temp_obj.split()
	problem['current_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()

	splitInputStringIntoProperties(problem['current_state'])
	splitInputStringIntoProperties(problem['goal_state'])





	'''
	#Remove the elements from goal_state which are already inside the current_state
	'''
	print("There are " + str(len(problem['goal_state'])) + " states in the goal_state before comparing with current_state")
	indexesOfElementsToDelete = []	
	for x in range(0, len(problem['goal_state'])):
		for y in range(0, len(problem['current_state'])):
			if problem['current_state'][y] == problem['goal_state'][x]:
				indexesOfElementsToDelete.append(x)
				print("I have found state from goal_state which is included in the current_state list! I'm gonna remove it from the goal_state.")

	print("I should delete ", len(indexesOfElementsToDelete), " states.")
	print("I should delete state nr: ", indexesOfElementsToDelete[0], " and state nr: ", indexesOfElementsToDelete[1])
	for index in sorted(indexesOfElementsToDelete, reverse=True):
		del problem['goal_state'][index]

	print("There are " + str(len(problem['goal_state'])) + " states left in the goal_state list.")
	asda = 0
	# Do while there are states in the goal_state list to be solved
	while problem['goal_state']:
		# Generate operators for current state
		for a in range(0, len(problem['objects'])):		# For each element in the objects list
			for b in range(0, len(problem['current_state'])):	# For each state in the current_state
				if problem['current_state'][b].preposition == "ON" and problem['current_state'][b].obj1 == problem['objects'][a]: # If there exist object in objects list which has ON preposition
					preconditionProperty1 = Property(problem['current_state'][b].preposition, problem['current_state'][b].obj1, problem['current_state'][b].obj2)
					for c in range(0, len(problem['current_state'])):
						if problem['current_state'][c].preposition == "CLEAR" and problem['current_state'][c].obj1 == problem['objects'][a]: #third condition -> if object = x and CLEAR(x)
							preconditionProperty3 = Property(problem['current_state'][c].preposition, problem['current_state'][c].obj1, "")
							for d in range(0, len(problem['current_state'])):
								if problem['current_state'][d].preposition == "HEAVIER" and problem['current_state'][d].obj2 == problem['objects'][a]: #fourth condition
									heavierFirstObject = problem['current_state'][d].obj1
									preconditionProperty4 = Property(problem['current_state'][d].preposition, heavierFirstObject, problem['objects'][a])
									for e in range(0, len(problem['current_state'])):
										if problem['current_state'][e].preposition == "CLEAR" and problem['current_state'][e].obj1 == heavierFirstObject: #second condition
											preconditionProperty2 = Property(problem['current_state'][e].preposition, heavierFirstObject, "")
											print("Preconditions are fulfilled for object nr: ", a, ". I can create new Move operator for object: ", problem['objects'][a])
											print("first Precond property = ", preconditionProperty1.preposition, preconditionProperty1.obj1, preconditionProperty1.obj2)
											print("second Precond property = ", preconditionProperty2.preposition, preconditionProperty2.obj1, preconditionProperty2.obj2)
											print("third Precond property = ", preconditionProperty3.preposition, preconditionProperty3.obj1, preconditionProperty3.obj2)
											print("fourth Precond property = ", preconditionProperty4.preposition, preconditionProperty4.obj1, preconditionProperty4.obj2)
											op = Operator(["Move",preconditionProperty1.obj1, preconditionProperty1.obj2, preconditionProperty2.obj1], #from X on Y to Z
												[preconditionProperty1, preconditionProperty2, preconditionProperty3, preconditionProperty4], 
												[Property(preconditionProperty1.preposition, preconditionProperty1.obj1, preconditionProperty2.obj1), Property(preconditionProperty2.preposition, preconditionProperty1.obj2, "")],
												[Property(preconditionProperty1.preposition, preconditionProperty1.obj1, preconditionProperty1.obj2), Property(preconditionProperty2.preposition, preconditionProperty2.obj1, "")])
											problem['operators'].append(op)
											print("Operator added to the list ", op.action)
											print("\n")
											

		print("There are ", len(problem['operators']), " operators in the list")
		indexesOfGoalStatesToDelete = []
		for x in range(0, len(problem['goal_state'])): #for all goal states
			for y in range(0, len(problem['operators'])): #look through all operators
				for z in range(0, len(problem['operators'][y].add)): #and check if its property from add list is equal to property from the goal state
					if (problem['operators'][y].add[z].preposition == problem['goal_state'][x].preposition) and (problem['operators'][y].add[z].obj1 == problem['goal_state'][x].obj1) and (problem['operators'][y].add[z].obj2 == problem['goal_state'][x].obj2):
						print("I have found operator which can solve " + problem['goal_state'][x].preposition + " " + problem['goal_state'][x].obj1 + " " + problem['goal_state'][x].obj2 + " state from the goal_state!")
						print("To achieve your goals you have to: " + problem['operators'][y].action[0] + " " + problem['operators'][y].action[1] + " " + problem['operators'][y].action[2] + " " + problem['operators'][y].action[3])
						print("Current state before taking action: ")
						printCurrentState(problem)
						problem['current_state'].append(problem['operators'][y].add[0])
						problem['current_state'].append(problem['operators'][y].add[1])
						indexesOfElementsToDelete = []	
						for q in range(0, len(problem['current_state'])):
							if problem['current_state'][q] == problem['operators'][y].delete[0] or problem['current_state'][q] == problem['operators'][y].delete[1]:
								indexesOfElementsToDelete.append(q)

						for index in sorted(indexesOfElementsToDelete, reverse=True):
							del problem['current_state'][index]


						print("\nCurrent state after taking action: ")
						printCurrentState(problem)
						indexesOfGoalStatesToDelete.append(x)



		for index in sorted(indexesOfGoalStatesToDelete, reverse=True):
			del problem['goal_state'][index]




if __name__ == "__main__":
	main()