import json

class Game:
    def __init__(self):
        self.name = input("What is your name? ")
        self.current_room = 0  
        self.backpack = []  
        self.valid_verbs = ["go","get", "look", "inventory", "drop", "quiz", "something"]
        self.file_data = self.open_file("./loop.map")
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
        print(f"> {room_name}")
        print(room_description)
        if 'items' in self.file_data[current_room]:
            items = self.file_data[current_room]['items']
            print("Items: " + ", ".join(items))
        print("Exits: " + ", ".join(exits))


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
                            item_name = " ".join(i_split[1:])
                            if item_name == "Chocolate":
                                print("Sorry, you cannot get chocolate until you pass the quiz.")
                            elif item_name in items:
                                self.backpack.append(item_name)
                                print(f"Inventory: {', '.join(self.backpack)}")
                                items.remove(item_name)
                                print(f"You have added {item_name} to your inventory.")
                            else:
                                print("Item not found in this room.")

                        elif i_split[0] == "drop":
                            item_name = " ".join(i_split[1:])
                            if item_name in self.backpack:
                                dropped_item = item_name
                                self.backpack.remove(item_name)
                                self.file_data[current_room]['items'].append(dropped_item)
                                file_data = self.file_data
                                room_name = file_data[current_room]['name']
                                print(f"Dropped {dropped_item} in {room_name}")
                            else:
                                print("Item is not present in your inventory.")

                elif i == "look":
                    return self.look()

                elif i == "help":
                    return self.help()
                        
                elif i == "inventory":
                    return self.inventory()
                        
                elif i == "quiz":
                    return self.quiz()
                    
                elif i in self.valid_verbs:
                    print("Not Implemented")

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
        exit(0)

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
            i = input("What would you like to do? ")
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
        self.print_room_details()
        self.user_input()
    
    def inventory(self):
        print(f"Inventory: {', '.join(self.backpack)}")
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
            
    def winning(self):
        print("Great") 
        print("Now you can have chocolate.")
        print("Go to Kitchen and grab chocolate!")
        self.flag = True
        self.second_input()

    def second_input(self):
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
                            item_name = " ".join(i_split[1:])
                            if item_name in items:
                                self.backpack.append(item_name)
                                print(f"Inventory: {', '.join(self.backpack)}")
                                items.remove(item_name)
                                print(f"You have added {item_name} to your inventory.")
                                if "Chocolate" in self.backpack:
                                    return self.inventory()
                            else:
                                print("Item not found in this room.")

                        elif i_split[0] == "drop":
                            item_name = " ".join(i_split[1:])
                            if item_name in self.backpack:
                                dropped_item = item_name
                                self.backpack.remove(item_name)
                                self.file_data[current_room]['items'].append(dropped_item)
                                file_data = self.file_data
                                room_name = file_data[current_room]['name']
                                print(f"Dropped {dropped_item} in {room_name}")
                            else:
                                print("Item is not present in your inventory.")

                elif i == "look":
                    return self.look()

                elif i == "help":
                    return self.help()
                        
                elif i == "inventory":
                    return self.inventory()
                        
                elif i == "quiz":
                    return self.quiz()
                    
                elif i in self.valid_verbs:
                    print("Not Implemented")

                else:
                    print("Please enter a valid input.")
                            
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
                continue
            except EOFError:
                print("\nUse 'quit' to exit.")
                continue
        return self.quit()
    


    def if_choco(self):
            print("WIN!!!!!!!!")
            self.quit()
   
# def play_game():
#     game = Game()
#     print(f"Hello there {game.name}")
#     print("Who doesn't love chocolate? But your mum will only give you the chocolate if you pass in an online math quiz you have today.")
#     print("Your task is to grab your laptop, start the quiz and pass. If you pass, go back to kitchen, grab the chocolate and you win!")
#     game.print_room_details()
#     game.user_input()

# play_game()
