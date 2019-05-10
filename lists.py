import random
import datetime
from difflib import SequenceMatcher

import os

def say(string):
    os.system('say "%s" -r 300 &' % string)

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def seconds_since_1970():
    return int(datetime.datetime.now().timestamp())

def check_similar(guess,correct_lst):
    for w in correct_lst:
        if(similar(guess,w) >= 0.8):
            if w.split("|")[0].strip().lower() != guess.split("|")[0].strip().lower() and input("Did you mean: '" + w + "'? (y/n)\n> ").lower() == "y":
                return w
    return ""

def getLists(filename):
    with open(filename) as y:
        one_list = []
        all_lists = []
        for line in y:
            line = line.strip()
            if len(line) > 0:
                one_list.append(line)
            else:
                if len(one_list) > 0:
                    all_lists.append(one_list)
                one_list = []
        if len(one_list) != 0:
            all_lists.append(one_list)
    return all_lists

def clear_screen():
    print("\n"*50)

def lower_in(guess,lst):
    for i in lst:
        if i.split("|")[0].strip().lower() == guess.split("|")[0].strip().lower():
            return True
    return False

def display_guesses(l2,correct_lst,letters_only=False):
    for i in range(len(correct_lst)):
        print(str(i+1) + ")",end=" ")
        if lower_in(correct_lst[i],l2):
            print(correct_lst[i])
        else:
            if letters_only:
                print(correct_lst[i][0])
            else:
                print()

def correct(title,l2,correct_lst):
    clear_screen()
    print("CORRECT!")
    print(title,"(Score = %d) " % get_score(correct_lst))
    display_guesses(l2,correct_lst)

def wrong(guess,title,l2,correct_lst):
    clear_screen()
    print("Incorrect! (%r is not in this list)" % guess)
    print(title,"(Score = %d) " % get_score(correct_lst))
    display_guesses(l2,correct_lst)

def remove_lower(guess,lst):
    for i in lst:
        if i.split("|")[0].strip().lower() == guess.split("|")[0].strip().lower():
            lst.remove(i)
            return

scores = {}
def set_scores_to_zero(lists):
    for l in lists:
        scores[tuple(l[1:])] = 0

def get_score(lst):
    return scores[tuple(lst)]

def increment_score(lst):
    scores[tuple(lst)] += 1

def decrement_score(lst):
    scores[tuple(lst)] -= 1

def game(lists):
    set_scores_to_zero(lists)
    random.shuffle(lists)
    while len(lists) > 0:
        l = lists[0]
        l2 = []
        guesses = []
        title = l.pop(0)
        correct_lst = l[:]
        clear_screen()
        print("\t"*11,"(Cards left: %d)" % len(lists))
        print(title,"(Score = %d) " % get_score(l))
        display_guesses(l2,correct_lst)
        while len(l) > 0:
            guess = input("\n> ")
            if guess == "save_progress":
                filename = "list_progress_" + str(seconds_since_1970()) + ".txt"
                print("Saving progress to %s..." % filename)
                with open(filename,"w") as y:
                    lists[0] = [title] + correct_lst
                    for i in lists:
                        for j in i:
                            print(j,file=y)
                        print(file=y)
                continue
            elif guess in guesses and guess not in ("`","``","l","hint"):
                print("You already guessed that!")
                continue
            similar = check_similar(guess,correct_lst)
            if similar:
                guess = similar
            guesses.append(guess)
            if guess == "":
                pass
            elif guess == "hint":
                say(l[0])
            elif guess == "l":
                for i in range(5):
                    decrement_score(correct_lst)
                clear_screen()
                print(title,"(Score = %d) " % get_score(correct_lst))
                display_guesses(l2,correct_lst,letters_only=True)
            elif guess == "`":
                print(l)
                for i in range(10):
                    decrement_score(correct_lst)
            elif guess == "``":
                for i in range(100):
                    decrement_score(correct_lst)
                clear_screen()
                print(title)
                display_guesses(correct_lst,correct_lst,letters_only=True)
                break
            elif lower_in(guess,l):
                say(guess)
                l2.append(guess)
                remove_lower(guess,l)
                increment_score(correct_lst)
                correct(title,l2,correct_lst)
            else:
                decrement_score(correct_lst)
                wrong(guess,title,l2,correct_lst)
        lists.pop(0)

        print("All Done! Do you wanna study this one again? y/n")
        j = input("\n> ")
        if j.lower() == "y":
            lists.append([title] + correct_lst)

    print("That's a Wrap!")

DICT_MODE = True

def setup():
    clear_screen()
    # print(getLists("lists.txt"))
    if DICT_MODE:
        lists = getLists("lists.txt")
        assert(len(lists[0]) == 1)
        d = {}
        minigame = []
        key = lists[0][0]
        for i in range(1,len(lists)):
            if len(lists[i]) == 1:
                d[key] = minigame
                minigame = []
                key = lists[i][0]
            else:
                minigame.append(lists[i])
        d[key] = minigame
        c = 0
        valid = {}
        print("Choose a game!")
        for key in d:
            c += 1
            valid[str(c)] = key
            print("%d) %s (%d lists)" % (c,key,len(d[key])))
        g = ""
        while g not in valid and "," not in g:
            g = input("\n> ")
        if "," in g:
            keys = g.split(",")
            lst = []
            for k in keys:
                lst += d[valid[k]]
            game(lst)
        else:
            game(d[valid[g]])
        setup()
    else:
        game(getLists("lists.txt"))

setup()
