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

	Test data to be solved:
	C)
		objects - A B P1 P2 T1 T2 T3
		initial state - CLEAR(P2) ON(P2,A) ON(A,T2) ON(T2,B) CLEAR(T1) CLEAR(P1) HEAVIER(A,P2) HEAVIER(T2,A) HEAVIER(B,P2) HEAVIER(P1,P2) HEAVIER(T1,A) HEAVIER(P1,T2)
		goal state - ON(P2,A) ON(A,T2) ON(T2,P1)
		Visual representation:
		

		P2							   P2
		|  							   |
		A 							   A
		| 							   |
		T2            				   T2
		| 							   |
		B   T1  P1     			B  T1  P1	




	Trying to identify pegs.
	We can say that we found a peg if that object has nothing under its surface - when we cannot find ON(object, x) property.
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
Function: getInputFromUserAndSaveInsideProblemDictionary(object)
----------------------------------------------------------------------------------------
Hmmm, the function name explains everything.
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
Function: isGoalStateASubsetOfCurrentState(goal, current):
----------------------------------------------------------------------------------------
Checks if all properties from the goal state are included in the current_state. If it is true, then we know that our problem has been solved.
'''
def isGoalStateASubsetOfCurrentState(goal, current):
	counter = 0;
	goalsToBeSolved = []
	for x in range (0, len(current)):
		for y in range(0, len(goal)):
			if(compareTwoObjects(current[x], goal[y])):
				counter = counter + 1
				break;

	if counter == len(goal):
		print("Goal state is a subset of current state! Problem solved!")
	else:
		print("Goal state is not a subset of current state!")
		for x in range(0, len(goal)):
			count = 0
			for y in range(0, len(current)):
				if(compareTwoObjects(goal[x], current[y])):
					count += 1

			if not count > 0:
				goalsToBeSolved.append(goal[x])
				print("The state nr: ", x, " is not in the current_state")


	return goalsToBeSolved


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

	pegs = [];
	#getInputFromUserAndSaveInsideProblemDictionary(problem)

	temp_obj = "A B P1 P2 T1 T2 T3"
	temp_state = "CLEAR(P2) ON(P2,A) ON(A,T2) ON(T2,B) CLEAR(T1) CLEAR(P1) HEAVIER(A,P2) HEAVIER(T2,A) HEAVIER(B,P2) HEAVIER(P1,P2) HEAVIER(T1,A) HEAVIER(P1,T2)"
	#temp_goal = "CLEAR(P2) ON(P2,A)"
	temp_goal = "ON(P2,A) ON(A,T2) ON(T2,P1) ON(P3,R2)"

	problem['objects'] = temp_obj.split()
	problem['current_state'] = temp_state.split()
	problem['goal_state'] = temp_goal.split()

	splitInputStringIntoProperties(problem['current_state'])
	splitInputStringIntoProperties(problem['goal_state'])
	objectsLength = len(problem['objects'])
	currentStateLength = len(problem['current_state'])

	for x in range(0, objectsLength):
		counter = 0;
		for y in range(0, currentStateLength):
			if problem['objects'][x] == problem['current_state'][y].obj1 and problem['current_state'][y].preposition == "ON":
				counter += 1

		if counter == 0:
			pegs.append(problem['objects'][x])
	

	for x in range(0, len(pegs)):
		print("Object ", pegs[x], " is a peg")

	'''
		Means-ends analysis:
		1) Compare the current state with the goal state. If there is no difference between them the problem is solved.
		2) If there is a difference between the current state and the goal state, set a goal to solve that difference.
		   If there is more than one difference, set a goal to solve the largest difference.
		3) Select an operator that will solve the difference identified in Step 2.
		4) If an operator can be applied, apply it. If it cannot, set a new goal to reach a state that would allow the application of the operator.
		5) Return to Step 1 with the new goal set in Step 4.
	'''

	# SOLVING THE PROBLEM

	'''
	If the goal_state is a subset of current_state, then our problem is solved
	'''
	listOfGoalsToSolve = isGoalStateASubsetOfCurrentState(problem['goal_state'], problem['current_state'])
	print("List of goals to solve ", listOfGoalsToSolve)
	
	#While there are states that need to be solved and goal_state is not a subset of the current_state
	while isGoalStateASubsetOfCurrentState(problem['goal_state'], problem['current_state']):
		print("difference!")

if __name__ == "__main__":
	main()