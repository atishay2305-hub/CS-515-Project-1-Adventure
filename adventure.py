import json
import random

class Game:

    def __init__(self):
        self.items = []
        self.name = input("What is your name? ")
        self.health = 5
        self.current_room = ""

    def open_file(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data

    def room(self):
        data = self.open_file("./loop.map")
        all_rooms = []
        for room in data:
            all_rooms.append(room['name'])
        print(all_rooms)
        random_object = random.choice(data)
        current_room = random_object['name']
        return current_room

    def get_directions(self):
        data = self.open_file("./loop.map")
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

    def get_items(self):
        data = self.open_file("./loop.map")
        for room in data:
            if room["name"] == self.current_room:
                self.items = room["items"]
                all_items = self.items
                print("You see the following items in the room:", all_items)
                if "cheese" in all_items:
                    self.win()
                elif "cat" in all_items:
                    self.lose()
                else:
                    self.get_user_item_choice()

    def get_user_item_choice(self):
        data = self.open_file("./loop.map")
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

    def attack(self):
        if self.items in ["Shotgun", "Mouse Trap"]:
            attack_damage = random.randint(1, 5)
            self.health -= attack_damage

    def is_alive(self):
        if self.health > 0:
            return "Alive"
        else:
            self.lose()
    
    def win(self):
        print("Congratulations! You have found the cheese and won the game!")
    
    def lose(self):
        print("Game over! You have been caught by Tom.")
        

def play_game():
    game = Game()
    print("Welcome to the Tom and Jerry game, {}!".format(game.name))
    print("Jerry wants to get some cheese from the kitchen, but Tom is on the lookout.")
    print("You have 5 health points. If Tom catches you, you lose the game.")
    print("Use the following commands to play the game:")
    print("north, south, east, west - move in the corresponding direction")
    print("quit - exit the game")
    game.get_directions()
    game.get_user_item_choice()

play_game()