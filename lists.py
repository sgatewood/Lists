import random

def getLists(filename):
    with open(filename) as y:
        one_list = []
        all_lists = []
        for line in y:
            line = line.strip()
            if len(line) > 0:
                one_list.append(line)
            else:
                if len(one_list) > 2:
                    all_lists.append(one_list)
                one_list = []
        if len(one_list) != 0:
            all_lists.append(one_list)
    return all_lists

def clear_screen():
    print("\n"*50)

def lower_in(guess,lst):
    for i in lst:
        if i.lower() == guess.lower():
            return True
    return False

def display_guesses(l2,correct_lst):
    for i in range(len(correct_lst)):
        print(str(i+1) + ")",end=" ")
        if lower_in(correct_lst[i],l2):
            print(correct_lst[i])
        else:
            print()

def correct(title,l2,correct_lst):
    clear_screen()
    print("CORRECT!")
    print(title)
    display_guesses(l2,correct_lst)

def wrong(guess,title,l2,correct_lst):
    clear_screen()
    print("Incorrect! (%r is not in this list)" % guess)
    print(title)
    display_guesses(l2,correct_lst)

def remove_lower(guess,lst):
    for i in lst:
        if i.lower() == guess.lower():
            lst.remove(i)
            return

def game(lists):
    random.shuffle(lists)
    for l in lists:
        l2 = []
        title = l.pop(0)
        correct_lst = l[:]
        clear_screen()
        print(title)
        display_guesses(l2,correct_lst)
        while len(l) > 0:
            guess = input("\n> ")
            if guess == "":
                pass
            if guess == "`":
                print(l + l2)
            elif lower_in(guess,l):
                l2.append(guess)
                remove_lower(guess,l)
                correct(title,l2,correct_lst)
            else:
                wrong(guess,title,l2,correct_lst)

        input("All done! \n<Press Enter to Continue>")
    print("That's a Wrap!")




# print(getLists("lists.txt"))
game(getLists("lists.txt"))
