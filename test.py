import json

class Game:
    def __init__(self):
        self.name = input("What is your name? ")
        self.health = 5  # current health of the player
        self.attack = 5
        self.current_room = 0  # current room that is room 0
        self.inventory = []  # current inventory
        self.valid_verbs = ["go","get", "look", "inventory", "quit", "help", "drop"]
        self.file_data = self.open_file("./test.map")

    def open_file(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data
        
    def print_room_details(self):
        file_data = self.file_data
        current_room = self.current_room
        room_name = file_data[current_room]['name']
        room_description = file_data[current_room]['desc']
        exits = file_data[current_room]['exits']
        print(f"> {room_name}")
        print(room_description)
        if 'items' in self.file_data[current_room]:
            items = (self.file_data[current_room]['items'])
            print(items)
        print(exits)

    def user_input(self):
        i = ""
        while i != "quit":
            try:
                current_room = self.current_room
                exits = list(self.file_data[current_room]['exits'].keys())
                if 'items' in self.file_data[current_room]:
                    items = self.file_data[current_room]['items']
                i = input("What would you like to do? ")
                if " " in i:
                    i_split = i.split(" ")

                    if i_split[0] in self.valid_verbs:

                        if i_split[0] == "go":
                            if i_split[1] in exits:
                                self.current_room = self.file_data[current_room]['exits'][i_split[1]]
                                self.print_room_details()
                            else:
                                print(f"There is no way to go {i_split[1]}")
                            
                        elif i_split[0] == "get":
                            if i_split[1] in items:
                                self.inventory.append(i_split[1])
                                print(f"Inventory: {self.inventory}")
                                # del self.file_data[current_room]['items'][i_split[1]]
                                print(f"You have added {i_split[1]} to your inventory.")
                            else:
                                print("Item not found in this room.")

                        elif i_split[0] == "drop":
                            if i_split[1] in self.inventory:
                                dropped_item = i_split[1]
                                self.inventory.remove(i_split[1])
                                print(f"Inventory: {self.inventory}")
                                self.file_data[current_room]['items'].append(dropped_item)
                                file_data = self.file_data
                                current_room = self.current_room
                                room_name = file_data[current_room]['name']
                                print(f"Dropped {dropped_item} in {room_name}")
                            else:
                                print("Item is not present in your inventory.")


                elif i == "look":
                    return self.look()

                elif i == "help":
                    return self.help()
                
                else:
                    print("Please enter a valid input.")
                        
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
                continue
            except EOFError:
                print("\nUse 'quit' to exit.")
                continue
        return self.quit()

        
    def quit(self):
        print("Goodbye!")

    def help(self):
        print("You can run the following commands: ")
        for i in self.valid_verbs:
            if "..." in i:
                print(f"  {i[:-3]} ...")
            else:
                print(f"  {i}")
        self.user_input()

        i = 0
        while i in self.valid_verbs:
            if i == "go":
                return self.user_input()
            elif i == "get":
                return self.user_input()
            elif i == "look":
                return self.look()
            elif i == "inventory":
                return self.inventory()
            elif i == "quit":
                return self.quit()
            elif i == "help":
                return self.help()
    

    def look(self):
        return self.print_room_details()
            

def play_game():
    game = Game()
    game.print_room_details()
    game.user_input()

play_game()


# class Winning():
#     def __init__(self):
#         self.health = 5 
#         self.attack = 5

        

# class winning():

#     def attack():



#     def health():



#     def item_power():

        

#     def attack():


