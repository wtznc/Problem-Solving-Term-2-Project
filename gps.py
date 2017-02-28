'''
	Problem Solving for Computer Science - Assignment
	Wojciech Tyziniec 2017
	Goldsmiths, University of London


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


	Move(A, table1, table2)

	//The table with operators has to be generated dynamically, during the execution time
	// Dla kazdego obiektu podanego, sprawdzic czy moge utworzyc operator
	// Preconditions - ON(x, y), CLEAR(z), CLEAR(x), HEAVIER(z, x) 
	// porownuje obiekt 


	problem = {
		"initial_state": ["A ON table1", "table1 HEAVIER A", "table2 HEAVIER A", "A CLEAR", "table2 CLEAR"],
		"goal": ["table1 CLEAR", "A CLEAR"]
		"operators": [
		{
			"action": "MOVE A table1 table2"
			"preconditions": "A ON table1", "table2 CLEAR", "A CLEAR", "table2 HEAVIER A"
			"add": "A ON table2", "table1 CLEAR"
			"delete": "A ON table1", "table2 CLEAR"
		},
		{
			"action": 
			"preconditions":
			"add":
			"delete":
		},
		]
	}


	problem = {
	"initial_state": ["ON(A,table1)", "HEAVIER(table1, A)", "HEAVIER(table2, A"), "CLEAR(A)", "CLEAR(table2)"]
	"goal_state": ["CLEAR(table1)", "CLEAR(A)"]
	"operators": [
	{
		"action": "Move(A,table1,table2)"
		"preconditions": "ON(A,table1)", "CLEAR(table2)", "CLEAR(x)", "HEAVIER(table2,A)"
		"add": "ON(A,table2)", "CLEAR(table1)"
		"delete": "ON(A,table1)", "CLEAR(z)"
	},
	{
			"action": 
			"preconditions":
			"add":
			"delete":
	}
	]
	}
'''

obj = raw_input("Please enter object names: ")
objects = obj.split()

for x in range (0, len(objects)):
	print("Object = " + objects[x])


state = raw_input("Please enter the initial state: ")
current_state = state.split()

for x in range(0, len(current_state)):
	print("State = " + current_state[x])

goal = raw_input("Please enter the goal state: ")
goal_state = goal.split()

for x in range(0, len(goal_state)):
	print("Goal state = " + goal_state[x])

problem = "problem = { \n\"initial_state\"😞"
for x in range(0, len(current_state)):
	problem += "\"" + current_state[x] + "\","

problem += "]\n\"goal\": ["
for x in range(0, len(goal_state)):
	problem += "\"" + goal_state[x] + "\","

print(problem)