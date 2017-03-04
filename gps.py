'''
	Problem Solving for Computer Science - Assignment
	Wojciech Tyziniec 2017
	Goldsmiths, University of London {


	INTRODUCTION
	----------------------------------------------------------------------------------------
}
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

abc = {
		"current_state": ["ON(A,table1)", "HEAVIER(table1, A)", "HEAVIER(table2, A)", "CLEAR(A)", "CLEAR(table2)"],
		"goal_state": ["CLEAR(table1)", "CLEAR(A)"],
		"operators": [
		{
			"action": "Move(A,table1,table2)",
			"preconditions": ["ON(A,table1)", "CLEAR(table2)", "CLEAR(A)", "HEAVIER(table2,A)"],
			"add": ["ON(A,table2)", "CLEAR(table1)"],
			"delete": ["ON(A,table1)", "CLEAR(z)"]
		},{
			"action": "Move(A,table1,table2)",
			"preconditions": ["ON(A,table1)", "CLEAR(table2)", "CLEAR(A)", "HEAVIER(table2,A)"],
			"add": ["ON(A,table2)", "CLEAR(table1)"],
			"delete": ["ON(A,table1)", "CLEAR(z)"]
		}]
	}
'''





'''
Class: Operator
----------------------------------------------------------------------------------------
Stores the details of our operators
'''
class Operator(object):
	def __init__(self, action, preconditions, add, delete):
		self.action = action
		self.preconditions = preconditions
		self.add = add
		self.delete = delete


'''
Class: Property
----------------------------------------------------------------------------------------
Class for storing details of propositions
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
Function: splitStringsIntoProperties(object)
-----------------------------------------------------------------------------------------
In this function the object (input from the user) is being parsed and chop up into small objects (Property).
'''
def splitStringsIntoProperties(object):
	stringToSplit = object
	for x in range(0, len(object)):
		par2 = "" # This variable is prepared for optional parameter - it may or may not exist
		tempState = stringToSplit[x]
		temp_pos1 = tempState.find("(")
		temp_pos2 = tempState.find(",")
		temp_pos3 = tempState.find(")")
		preposition = tempState[:temp_pos1]
		if tempState.find(",") == -1:
			par1 = tempState[temp_pos1+1:temp_pos3]
		else:
			par1 = tempState[temp_pos1+1: temp_pos2]
			par2 = tempState[temp_pos2+1:temp_pos3]
		property = Property(preposition, par1, par2)
		object[x] = property


'''
Function: main()
-------------------------------------------------------------------------------------------
The main function is called at program startup, 
it is the designated entry point to a program that is executed in hosted environment.
'''
def main():
	'''
	Global variables:
	-------------------------------------------------------------------------------------
	problem - contains objects, current state, goal state and operators 
	'''
	temp_obj = "table1 table2 A"
	temp_state = "ON(A,table1) HEAVIER(table1,A) HEAVIER(table2,A) CLEAR(A) CLEAR(table2)"
	temp_goal = "CLEAR(table1) CLEAR(A)"

	problem = {	"objects": [],
				"current_state": [],
				"goal_state": [],
				"operators": []}

	'''
    Temporarily access data from variables
	obj = raw_input("Please enter object names: ")
	problem['objects'] = obj.split()

	state = raw_input("Please enter the initial state: ")
	problem['current_state'] = state.split()

	goal = raw_input("Please enter the goal state: ")
	problem['goal_state'] = goal.split()
	'''

	problem['objects'] = temp_obj.split()
	problem['current_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()

	splitStringsIntoProperties(problem['current_state'])
	splitStringsIntoProperties(problem['goal_state'])


	'''
		Check preconditions and generate operators
	'''
	lengthOfObjectsInProblemDict = len(problem['objects'])

	lengthOfStatesInProblemDict = len(problem['current_state'])
	heavierFirstObject = ""


	'''
	Remove the elements from goal_state which are already inside the current_state
	'''
	indexesOfElementsToDelete = []	
	for x in range(0, len(problem['goal_state'])):
		for y in range(0, len(problem['current_state'])):
			if problem['current_state'][y] == problem['goal_state'][x]:
				indexesOfElementsToDelete.append(x)

	for x in range(0, len(indexesOfElementsToDelete)):
		del problem['goal_state'][indexesOfElementsToDelete[x]]


	for a in range (0, lengthOfObjectsInProblemDict): #for each object in objects list, check preconditions required to perform the move action
		for b in range(0, lengthOfStatesInProblemDict):
			if problem['current_state'][b].preposition == "ON" and problem['current_state'][b].obj1 == problem['objects'][a]:
				precondProperty1 = Property(problem['current_state'][b].preposition, problem['current_state'][b].obj1, problem['current_state'][b].obj2)
				for c in range(0, lengthOfStatesInProblemDict):
					if(problem['current_state'][c].preposition == "CLEAR" and problem['current_state'][c].obj1 == problem['objects'][a]): #third condition if object = x and CLEAR(x)
						precondProperty3 = Property(problem['current_state'][c].preposition, problem['current_state'][c].obj1, "")
						for d in range(0, lengthOfStatesInProblemDict):
							if(problem['current_state'][d].preposition == "HEAVIER" and problem['current_state'][d].obj2 == problem['objects'][a]): #fourth condition
								heavierFirstObject = problem['current_state'][d].obj1
								precondProperty4 = Property(problem['current_state'][d].preposition, heavierFirstObject, problem['objects'][a])
								for e in range(0, lengthOfStatesInProblemDict):
									if(problem['current_state'][e].preposition == "CLEAR" and problem['current_state'][e].obj1 == heavierFirstObject): #second
										precondProperty2 = Property(problem['current_state'][e].preposition, heavierFirstObject, "")
										print("Preconditions success for object nr: ", a)
										#print("first Precond property = ", precondProperty1.preposition, precondProperty1.obj1, precondProperty1.obj2)
										#print("second Precond property = ", precondProperty2.preposition, precondProperty2.obj1, precondProperty2.obj2)
										#print("third Precond property = ", precondProperty3.preposition, precondProperty3.obj1, precondProperty3.obj2)
										#print("fourth Precond property = ", precondProperty4.preposition, precondProperty4.obj1, precondProperty4.obj2)
										op = Operator(["Move",precondProperty1.obj1, precondProperty1.obj2, precondProperty2.obj1], #from X on Y to Z
											[precondProperty1, precondProperty2, precondProperty3, precondProperty4], 
											[Property(precondProperty1.preposition, precondProperty1.obj1, precondProperty2.obj1), Property(precondProperty2.preposition, precondProperty1.obj2, "")],
											[Property(precondProperty1.preposition, precondProperty1.obj1, precondProperty1.obj2), Property(precondProperty2.preposition, precondProperty2.obj1, "")])
										problem['operators'].append(op)
										print("Operator added to the list ", op)






	
	print("There are ", len(problem['operators']), " operators in the list")


	'''
	Searching for operators which contain goal_states in its "add" list.
	'''

	for x in range(0, len(problem['goal_state'])): #for all goal states
		for y in range(0, len(problem['operators'])): #look through all operators
			for z in range(0, len(problem['operators'][y].add)): #and check if its property from add list is equal to property from the goal state
				if (problem['operators'][y].add[z].preposition == problem['goal_state'][x].preposition) and (problem['operators'][y].add[z].obj1 == problem['goal_state'][x].obj1) and (problem['operators'][y].add[z].obj2 == problem['goal_state'][x].obj2):
					print("I found operator which can solve " + problem['goal_state'][x].preposition + " " + problem['goal_state'][x].obj1 + " " + problem['goal_state'][x].obj2 + " state from the goal_state!")
					print("To achieve your goals you have to: " + problem['operators'][y].action[0] + " " + problem['operators'][y].action[1] + " " + problem['operators'][y].action[2] + " " + problem['operators'][y].action[3])
					'''
					Execute that action -> add and delete states to and from the current_state
					'''

				else:
					print("Could not find another solution!")






	

	'''
	When current_state is changed, delete the list of operators and create a new one, for the state that you've just created.
	print(problem['operators'])
	del problem['operators']
	print("Deleting\n")
	problem['operators'] = []
	print(problem['operators'])
	'''
if __name__ == "__main__":
	main()

