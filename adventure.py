import json
import sys

class Game:
    def __init__(self):
        self.current_room = 0  
        self.backpack = []  
        self.valid_verbs = ["go","get", "look", "inventory", "drop", "quiz", "something", "help"]
        self.file_data = self.open_file(sys.argv[1])
        self.result = []
        self.quiz_taken = False

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
        print(f"> {room_name}\n")
        print(room_description + "\n")
        if 'items' in self.file_data[current_room]:
            items = self.file_data[current_room]['items']
            print("Items: " + ", ".join(items) + "\n")
        # print("Exits: " + " ".join(exits) + "\n")
        print("Exits:" + " ".join(exits) + "\n")
        
    def user_input(self):
        i = ""
        while i.lower() != "quit":
            try:
                current_room = self.current_room
                exits = list(self.file_data[current_room]['exits'].keys())
                if 'items' in self.file_data[current_room]:
                    items = self.file_data[current_room]['items']
                    if len(items) == 0:
                        del self.file_data[current_room]['items']
                        items = []
                else:
                    items = []
                i = input("What would you like to do? ").strip()
                if i.lower() == "quit":
                    break  
                i_split = i.split()
                verb = i_split[0].lower()
                if verb in self.valid_verbs:
                    if verb == "go":
                        if len(i_split) > 1:
                            direction = i_split[1].lower()
                            if direction in exits:
                                print(f"You go {direction}.\n")
                                self.current_room = self.file_data[current_room]['exits'][direction]
                                self.print_room_details()
                            else:
                                print(f"There's no way to go {direction}.")
                        else:
                            print("Sorry, you need to 'go' somewhere.")
                    elif verb == "get":
                        if len(i_split) > 1:
                            item_name = " ".join(i_split[1:])
                            if item_name == "Chocolate":
                                print("Sorry, you cannot get chocolate until you pass the quiz.")
                            elif item_name.lower() in [item.lower() for item in items]:
                                item_name = [item for item in items if item.lower() == item_name.lower()][0] # convert item_name to the original case
                                print(f"You pick up the {item_name}.")
                                self.backpack.append(item_name)
                                items.remove(item_name)
                            else:
                                print(f"There's no {item_name} anywhere.")
                        else:
                            print("Sorry, you need to 'get' something.")

                    elif verb == "drop":
                        if len(i_split) > 1:
                            item_name = " ".join(i_split[1:]).lower()
                            if item_name in [item.lower() for item in self.backpack]:
                                item_name = [item for item in self.backpack if item.lower() == item_name][0] # convert item_name to the original case
                                dropped_item = item_name
                                self.backpack.remove(item_name)
                                
                                if 'items' not in self.file_data[current_room]:
                                    self.file_data[current_room]['items'] = []
                                
                                self.file_data[current_room]['items'].append(dropped_item.title())
                                
                                if len(self.file_data[current_room]['items']) == 0:
                                    del self.file_data[current_room]['items']
                                
                                file_data = self.file_data
                                room_name = file_data[current_room]['name']
                                print(f"Dropped {dropped_item} in {room_name}.")
                            else:
                                print("Item is not present in your inventory.")
                        else:
                            print("Sorry, you need to 'drop' something.")

                    elif verb == "look":
                        self.look()
                    elif verb == "help":
                        self.help()
                    elif verb == "inventory":
                        self.inventory()
                    elif verb == "quiz":
                        self.quiz()
                    else:
                        if i in self.valid_verbs:
                            print("Not Implemented")
                        else:
                            print("Please enter a valid input.")
                else:
                    print("Please enter a valid input")
            except KeyboardInterrupt:
                exit(0)

            except EOFError:
                print("Use 'quit' to exit.")
                
        self.quit()


    def quit(self):
        print("Goodbye!")
        exit(0)

    def help(self):
        print("You can run the following commands:")
        for i in self.valid_verbs:
            if i == "go":
                print(f"  {i} ...")
            elif i == "get":
                print(f"  {i} ...")
            else:
                print(f"  {i}")
        self.user_input()

        i = 0
        while i in self.valid_verbs:
            i = input("What would you like to do? ")
            if i.lower() == "go":
                return self.user_input()
            elif i.lower() == "get":
                return self.user_input()
            elif i.lower() == "drop":
                return self.user_input()
            elif i.lower() == "look":
                return self.look()
            elif i.lower() == "inventory":
                return self.inventory()
            elif i.lower() == "quit":
                return self.quit()
            elif i.lower() == "help":
                return self.help()

    def look(self):
        self.print_room_details()
        self.user_input()
    
    def inventory(self):
        if len(self.backpack) == 0:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.backpack:
                print("  " + item)
        self.user_input()

    def quiz(self):
        if self.quiz_taken:
            print("You have already taken the quiz!")
        else:
            file_data = self.file_data
            current_room = self.current_room
            room_name = file_data[current_room]['name']
            if room_name == "Study Room":
                print("Let's Start the quiz!!!")
                self.math_quiz()
            elif room_name != "Study Room":
                print("You are not in your study room to give the quiz.")
            elif "laptop" not in self.backpack:
                print("Please bring your laptop to the study room to start the quiz.")
            else:
                print("Please go to study room with your laptop to start the quiz.")


    def math_quiz(self):
        try:
            score = 0
            answer1 = input("What is 2 + 2? ")
            if answer1 == "4":
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
            answer2 = input("What is 5 x 3? ")
            if answer2 == "15":
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
            answer3 = input("What is 10 / 2? ")
            if answer3 == "5":
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
            answer4 = input("What is the square root of 49? ")
            if answer4 == "7":
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")
            answer5 = input("What is 4 to the power of 2? ")
            if answer5 == "16":
                print("Correct!")
                score += 1  
            else:
                print("Incorrect.")
            print("Your final score is", score, "out of 5.")
            if score >= 3:
                print("Pass")
                self.quiz_taken = True
                self.winning()
            else:
                print("Fail")
        except EOFError:
            print("\nQuiz interrupted.")
        except KeyboardInterrupt:
            print("\nQuiz interrupted.")


            
    def winning(self):
        print("Great") 
        print("Now you can have chocolate.")
        print("Go to Kitchen and grab chocolate!")
        self.flag = True
        self.second_input()

    def second_input(self):
        i = ""
        while i.lower() != "quit":
            try:
                current_room = self.current_room
                exits = list(self.file_data[current_room]['exits'].keys())
                if 'items' in self.file_data[current_room]:
                    items = self.file_data[current_room]['items']
                else:
                    items = []
                i = input("What would you like to do? ").strip()
                if i.lower() == "quit":
                    break  
                i_split = i.split()
                verb = i_split[0].lower()
                if verb in self.valid_verbs:
                    if verb == "go":
                        if len(i_split) > 1:
                            direction = i_split[1]
                            if direction in exits:
                                print(f"You go {direction}.\n")
                                self.current_room = self.file_data[current_room]['exits'][direction]
                                self.print_room_details()
                            else:
                                print(f"There's no way to go {direction}.")
                        else:
                            print("Sorry, you need to 'go' somewhere.")
                    elif verb == "get":
                        if len(i_split) > 1:
                            item_name = " ".join(i_split[1:])
                            if item_name.lower() in [item.lower() for item in items]:
                                item_name = [item for item in items if item.lower() == item_name.lower()][0] # convert item_name to the original case
                                print(f"You pick up the {item_name}.")
                                self.backpack.append(item_name)
                                items.remove(item_name)
                                if "Chocolate" in self.backpack:
                                    return self.if_choco()
                            else:
                                print(f"There's no {item_name} anywhere.")
                        else:
                            print("Sorry, you need to 'get' something.")
                    elif verb == "drop":
                        if len(i_split) > 1:
                            item_name = " ".join(i_split[1:])
                            if item_name in self.backpack:
                                dropped_item = item_name
                                self.backpack.remove(item_name)
                                new_room = self.file_data[current_room]['exits'][exits[0]] 
                                previous_room = self.file_data[current_room]['name']
                                self.file_data[new_room]['items'].append(dropped_item)
                                file_data = self.file_data
                                room_name = file_data[new_room]['name']
                                print(f"Dropped {dropped_item} in {previous_room}.")
                            else:
                                print("Item is not present in your inventory.")
                        else:
                            print("Sorry, you need to 'drop' something.")
                    elif verb == "look":
                        self.look()
                    elif verb == "help":
                        self.help()
                    elif verb == "inventory":
                        self.inventory()
                    elif verb == "quiz":
                        self.quiz()
                    else:
                        if i in self.valid_verbs:
                            print("Not Implemented")
                        else:
                            print("Please enter a valid input.")
                                
            except KeyboardInterrupt:
                exit(0)
            except EOFError:
                print("\nUse 'quit' to exit.")
                continue
        self.quit()
    

    def if_choco(self):
            print("WIN!!!!!!!!")
            exit(0)
   
def play_game():
    game = Game()
    game.print_room_details()
    game.user_input()

play_game()
