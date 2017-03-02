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


	Move(A, table1, table2)

abc = {
		"initial_state": ["ON(A,table1)", "HEAVIER(table1, A)", "HEAVIER(table2, A)", "CLEAR(A)", "CLEAR(table2)"],
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
					SOLUTION
___________________________________________________
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
Function: splitStringsIntoProperties(object)
-----------------------------------------------------------------------------------------
The object is being parsed and chop up into small objects.
'''
def splitStringsIntoProperties(object):
	stringToSplit = object
	for x in range(0, len(object)):
		par2 = "" #Optional parameter - it may or may not exist
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
	problem - contains objects, initial state, goal state and operators 
	'''
	temp_obj = "table1 table2 A"
	temp_state = "ON(A,table1) HEAVIER(table1,A) HEAVIER(table2,A) CLEAR(A) CLEAR(table2)"
	temp_goal = "CLEAR(table1) CLEAR(A)"

	problem = {	"objects": [],
				"initial_state": [],
				"goal_state": [],
				"operators": []}

	'''
    Temporarily access data from variables
	obj = raw_input("Please enter object names: ")
	problem['objects'] = obj.split()

	state = raw_input("Please enter the initial state: ")
	problem['initial_state'] = state.split()

	goal = raw_input("Please enter the goal state: ")
	problem['goal_state'] = goal.split()
	'''

	problem['objects'] = temp_obj.split()
	problem['initial_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()


	#a = Operator('chujchuj', 'chujchuj', 'dsadsa', 'dsdsad')
	#print(a.action)

	splitStringsIntoProperties(problem['initial_state'])
	splitStringsIntoProperties(problem['goal_state'])


	print(problem['initial_state'][1].obj2)
	print(problem['goal_state'][0].preposition)

	print(problem)
	print("\n")

	#for each goal state, check the initial state and then look through the operators list 
	#and find actions which will add goal state to the current state  



	#"initial_state": ["ON(A,table1)", "HEAVIER(table1, A)", "HEAVIER(table2, A)", "CLEAR(A)", "CLEAR(table2)"],
	#wziac pierwszy parametr z initial state ktore maja preposition ON i sprawdzac dla innych

	lengthOfObjectsInProblemDict = len(problem['objects'])
	lengthOfStatesInProblemDict = len(problem['initial_state'])
	heavierFirstObject = ""
	#check preconditions and build operators
	for a in range (0, lengthOfObjectsInProblemDict): #for each object in objects list, check preconditions required to perform the move action
		for b in range(0, lengthOfStatesInProblemDict):
			if problem['initial_state'][b].preposition == "ON" and problem['initial_state'][b].obj1 == problem['objects'][a]:
				precondProperty1 = Property(problem['initial_state'][b].preposition, problem['initial_state'][b].obj1, problem['initial_state'][b].obj2)
				for c in range(0, lengthOfStatesInProblemDict):
					if(problem['initial_state'][c].preposition == "CLEAR" and problem['initial_state'][c].obj1 == problem['objects'][a]): #third condition if object = x and CLEAR(x)
						precondProperty3 = Property(problem['initial_state'][c].preposition, problem['initial_state'][c].obj1, "")
						for d in range(0, lengthOfStatesInProblemDict):
							if(problem['initial_state'][d].preposition == "HEAVIER" and problem['initial_state'][d].obj2 == problem['objects'][a]): #fourth condition
								heavierFirstObject = problem['initial_state'][d].obj1
								precondProperty4 = Property(problem['initial_state'][d].preposition, heavierFirstObject, problem['objects'][a])
								for e in range(0, lengthOfStatesInProblemDict):
									if(problem['initial_state'][e].preposition == "CLEAR" and problem['initial_state'][e].obj1 == heavierFirstObject): #second
										precondProperty2 = Property(problem['initial_state'][e].preposition, heavierFirstObject, "")
										print("Preconditions success for object nr: ", a)
										#print("first Precond property = ", precondProperty1.preposition, precondProperty1.obj1, precondProperty1.obj2)
										#print("second Precond property = ", precondProperty2.preposition, precondProperty2.obj1, precondProperty2.obj2)
										#print("third Precond property = ", precondProperty3.preposition, precondProperty3.obj1, precondProperty3.obj2)
										#print("fourth Precond property = ", precondProperty4.preposition, precondProperty4.obj1, precondProperty4.obj2)
										op = Operator(["Move",precondProperty1.obj1, precondProperty1.obj2, precondProperty2.obj1], 
											[precondProperty1, precondProperty2, precondProperty3, precondProperty4], 
											[Property(precondProperty1.preposition, precondProperty1.obj1, precondProperty2.obj1), Property(precondProperty2.preposition, precondProperty1.obj2, "")],
											[Property(precondProperty1.preposition, precondProperty1.obj1, precondProperty1.obj2), Property(precondProperty2.preposition, precondProperty2.obj1, "")])
										problem['operators'].append(op)




	print(problem)



























if __name__ == "__main__":
	main()

