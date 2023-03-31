import json
import random


"""
test maps
"""


# ['A white room', 'A blue room', 'A green room', 'A red room']


class Game:

    def __init__(self):
        self.items = []
        self.name = input("What is your name? ")
        self.health = 5  # current health of the player
        self.current_room = 0  # current room that is room 0
        self.inventory = []  # current inventory

    def open_file(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data


    def room(self):
        data = self.open_file("./test.map")
        all_rooms = []
        for room in data:
            all_rooms.append(room['name'])
        # print(all_rooms)
        current_room = data[0]['desc']
        print(current_room)


    def get_directions(self):
        data = self.open_file("./test.map")
        self.current_room = self.room()
        available_directions = {}
        for room in data:
            if room['name'] == self.current_room:
                available_directions = room['exits']
                break
        print("Available directions:", list(available_directions.keys()))
        direction = input("What direction do you want to go in? ")
        if direction in available_directions:
            self.current_room = available_directions[direction]
            print("You have entered the", self.current_room)
            self.get_items()
        else:
            print("Invalid direction")


    def get_user_item_choice(self):
        data = self.open_file("./test.map")
        while True:
            item_choice = input("What item do you want to get from the room? ")
            if item_choice.lower() == "look":
                self.get_items()
                break
            else:
                for room in data:
                    if room["name"] == self.current_room:
                        if item_choice in room["items"]:
                            self.items.append(item_choice)
                            room["items"].remove(item_choice)
                            print("You picked up the", item_choice)
                            self.get_directions()
                            break
                else:
                    print("Invalid choice. Choose a valid item or type 'look' to see the items in the room again.")


    # def look(self):

    # def help(self):

    def state(self):
        a = [
            {"name": "A white room",
             "desc": "You are in a simple room with white walls.",
             "exits": {"north": 1, "east": 3}
             },
            {"name": "A blue room",
             "desc": "This room is simple, too, but with blue walls.",
             "exits": {"east": 2, "south": 0}
             },
            {"name": "A green room",
             "desc": "You are in a simple room, with bright green walls.",
             "exits": {"west": 1, "south": 3},
             "items": []
             },
            {"name": "A red room",
             "desc": "This room is fancy. It's red!",
             "exits": {"north": 2, "west": 0},
             "items": ["rose"]
             }
        ]
        for i in a:
            if self.current_room == 0:
                print(i['desc'])
        return 

def play_game():
    game = Game()
    # print("You are in a simple room with white walls.")
    game.room()
    game.get_directions()
    game.get_user_item_choice()
    # game.state()


play_game()
