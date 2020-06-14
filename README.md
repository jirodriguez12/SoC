Summer of Code

Project 1-1: Diner Frenzy

How to run my code:
	Run diner.py. 
	You must have the library arcade installed either through your virtual environment (PyCharm recommended) or in your local machine.
	
Motivation:
	I was playing a cooking game on Snapchat and I missed diner on campus, so I combined the two thoughts.
	
Description:
	A customer goes into diner with an order in mind. The player's job is to replicate that order and deliver it to the customer.
	There are eggs and bagels on the counter to aid the player. Delivering an order to a customer increments a player's total amount of points.
	
Keys:
	Arrow (LEFT, RIGHT): 
		Moves chef
		Not necessary to play game
	Mouse Click (LEFT):
		Picks up items such as the ingredients on the counter or the food on the grill
	Mouse Click (RIGHT):
		Places items on grill and gives items to customer
		
Python Concepts Utilized:
	if-statements to check for item currently held, item given to customer, and area clicked on screen.
		example:
			if x in range(550, 650, 1) and y in range(275, 338, 1):
            	self._hold = True
           		self._items.append("egg")
			checks if player clicked on egg cartons and gives player an egg to cook.
	
	List indexing to keep track of all items a player has cooked.
	
Arcade Features Utilized:
	Drawing and moving sprites
	Playing sounds
	Making clickable objects
	
Challenges/Lessons:
	Clicking objects
		I learned to use range in a different way that I'm accustomed to in order to check if the location 
		of the mouse was within the bounds of the location of the object.
		
	Drawing sprites
		Gave me a really difficult time at first. I learned to change the root of the interpreter to get into the correct directory.
		
Future Steps:
	Include more ingredients
	Include food variation
	Include specific time to cook/burn
	Include more sophisticated point system
	Include more diner aesthetics
