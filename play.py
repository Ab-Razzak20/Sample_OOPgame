from slay.room import Room
from slay.character import Enemy, Friend
from slay.rpginfo import RPGInfo
from slay.item import Item

spooky_castle = RPGInfo('The Spooky Castle')
spooky_castle.welcome()
RPGInfo.info()  #staticmethod belongs to the class, not to the object
RPGInfo.author = 'Raz Raza'

ballroom = Room('Ballroom')
ballroom.set_description("A vast room with a shiny wooden floor. Huge candlesticks guard the entrance.")

drawing_room = Room('Drawing Room')
drawing_room.set_description("A large room with ornate golden decorations on each wall")

prayer_hall = Room('Prayer Hall')
prayer_hall.set_description('Place for conducting canonical prayers')

print('There are ' + str(Room.no_of_rooms) + ' rooms to explore.')

prayer_hall.link_room(drawing_room, 'East')
drawing_room.link_room(prayer_hall, 'West')
drawing_room.link_room(ballroom, 'South')
ballroom.link_room(drawing_room, 'North')

aurora = Friend('Aurora', 'A friendly skeleton')
aurora.set_conversation("'Hi, hello there!'")
drawing_room.set_character(aurora)

superman = Enemy("Superman", "A smelly zombie")
superman.set_conversation("'Brrlgrh... rgrhl... brains...'")
superman.set_weakness('Kryptonite')
ballroom.set_character(superman)

kryptonite = Item('Kryptonite')
kryptonite.set_description('A green, crystalline material originating from Krypton')
ballroom.set_item(kryptonite)

book = Item('Book')
book.set_description("A good book entitled 'Knitting for dummies'")
drawing_room.set_item(book)


current_room = prayer_hall
backpack = []  # to store items

dead = False    # to keep track of whether the player is still alive
while dead == False:
    print('\n')
    current_room.get_details()

    inhabitant = current_room.get_character()
    if inhabitant is not None:
        inhabitant.describe()

    item = current_room.get_item()  # assign it to the Room
    if item is not None:
          item.describe()

    command = input('-> ')
    if command in ['North', 'East', "West", 'South']:  # check whether a direction was typed
        current_room = current_room.move(command)

    elif command == 'Talk':    # Talk to the inhabitant - check whether there is one!
        if inhabitant is not None:
            inhabitant.talk()

    elif command == 'Fight':
        if inhabitant is not None and isinstance(inhabitant, Enemy): # `isinstance()` -"If the character is an Enemy"
            print('What will you fight with?')
            fight_with = input('-> ')
            if fight_with in backpack:
                # when the player chooses an item to use in a fight,
                # the game checks whether the player actually has an item with that name in their backpack
                if inhabitant.fight(fight_with) == True:
                    print('Hooray! You won the fight!')
                    current_room.set_character(None)
                    if Enemy.enemies_to_defeat == 0:
                        # using a class variable to allow the player to win the game
                        # only after they have defeated a specific number of enemies
                        print('Congratulations, you have vanquished the enemy horde!')
                        dead = True
            else:
                print('Oh Dear! You lost the fight!')
                print('Game Over!')
                dead = True

        else:
            print('There is no one to fight with.')

    elif command == 'Hug':
        if inhabitant is not None:
            if isinstance(inhabitant, Enemy): # check whether an object is an instance of a particular class
                print("I'd not do that if I were you .. .")
            else:
                inhabitant.hug()

        else:
            print('There is no one to hug :/')

    elif command == 'Take': # put the name of the current room’s Item into the `backpack`
        if item is not None:
            print('You put the ' + item.get_name() + ' in your backpack')
            backpack.append(item.get_name())
            current_room.set_item(None) # set the Item attribute of the Room to `None`.


RPGInfo.credits()  # classmethod has access to the class, no to the object
