from random import randint
from time import time, strftime, gmtime

#Wyświetlanie interakcji z użytkownikiem
def welcome_screen():
    print(50 * "=")
    print("Quiz")
    print(50 * "=")
    print("Program Quiz jest to program umożliwiający grę w Quiz ze zdefiniowanymi przez użytkownika zasadami i pytaniami.")
    print(50 * "=")
    print("1. Nowa gra")
    print("2. Statystyki poprzednich gier")
    print("3. Wyjście z gry")
    print("> ", end="")

def settings_list_screen():
    print("Proszę wpisać lokalizację pliku zawierającego ustawienia gry.")
    print("> ", end="")

def question_list_screen():
    print(50 * "=")
    print("Proszę wpisać lokalizację pliku zawierającego pytania.")
    print("> ", end="")

def description_display():
    print(50 * "=")
    print("OPIS DOTYCZĄCY ZESTAWU PYTAŃ :")
    for line in description.split(";"):
        print(line)

def question_display():
    print(50 * "-")
    print(questions[question_number][0])
    print_answers()
    print("> ", end="")

def print_answers():
    if type_of_questions == "CLOSED":
        answer_counter = 1
        for i in questions[question_number][1]:
            print("%d) %s" % (answer_counter, i))
            answer_counter += 1

#Wczytywanie i sprawdzanie struktur danych użytych w programie
def make_settings_dictionary(file_settings_location, default_settings, allowed_settings):
    temporary_list = []
    settings = {}
    counter = 0
    was_any_error = False
    try:
        file_settings = open(file_settings_location, 'r')
        for line in file_settings:
            line = line.rstrip('\n')
            line = line.split(':')
            if len(line) == 2:
                temporary_list.append(line)
        file_settings.close()
        for i in temporary_list:
            if i[0] in default_settings.keys():
                try:
                    if int(temporary_list[counter][1]) >= allowed_settings[i[0]]:
                        settings[i[0]] = int(temporary_list[counter][1])
                    else:
                        settings[i[0]] = default_settings[i[0]]
                        was_any_error = True
                except:
                    if temporary_list[counter][1] in allowed_settings[i[0]]:
                        settings[i[0]] = temporary_list[counter][1]
                    else:
                        settings[i[0]] = default_settings[i[0]]
                        was_any_error = True
            counter += 1
        was_few_settings = False
        for i in default_settings:
            if i not in settings.keys():
                settings[i] = default_settings[i]
                was_few_settings = True
        if was_any_error == True:
            print("Wystąpiły błędne wartości w ustawieniach. Wartości błędne zmieniono na domyślne.")
        if was_few_settings == True:
            print("Ustawienia nieznalezione w pliku ustawień zastąpiono domyślnymi.")
        print("Zakończono wczytywanie pliku ustawień.")
        return settings
    except FileNotFoundError:
        print("Nie znaleziono danego pliku ustawień. Wczytano domyślne ustawienia.")
        return default_settings

def make_question_dictionary(file_questions_location):
    questions = {}
    counter = 1
    try:
        file_questions = open(file_questions_location, 'r')
        type_of_questions = file_questions.readline().strip()
        description = file_questions.readline().strip()
    except:
        file_questions = []
        type_of_questions = "NONE"
        description = "NONE"
        print("Błędna lokalizacja pliku z pytaniami. Program kończy działanie.")
        exit()
    for line in file_questions:
        line = line.strip()
        result = line.split(";")
        if type_of_questions == "CLOSED" and len(result) == 5:
            result[1] = result[1].split(",")
            questions[counter] = result
            try:
                questions[counter][2] = int(result[2])
                questions[counter][3] = float(result[3])
                questions[counter][4] = float(result[4])
                counter += 1
            except:
                print("Błędny format zapisu pytania nr %s. "
                      "Pytanie nr %s nie zostanie użyte w tej rozgrywce" % (counter, counter))
        elif type_of_questions == "OPEN" and len(result) ==4:
            try:
                questions[counter] = result
                questions[counter][2] = float(result[2])
                questions[counter][3] = float(result[3])
                counter += 1
            except:
                print("Błędny format zapisu pytania nr %s. "
                      "Pytanie nr %s nie zostanie użyte w tej rozgrywce" % (counter, counter))
    if len(questions) < 1:
        print("Niewystarczająca ilość pytań w pliku.")
        print("Program kończy działanie.")
        exit()
    return questions, description, type_of_questions

#Elementy menu
def main_menu():
    welcome_screen()
    select_option = input()
    while select_option not in ['1', '2','3']:
        print("Proszę wybrać poprawną opcję z menu głównego.")
        print("> ", end="")
        select_option = input()
    print(50 * "=")
    choose_option(int(select_option))

def choose_option(select_option):
    if select_option == 1:
        load()
        new_game()
    elif select_option == 2:
        games_statistics()
    else:
        exit()

def load():
    global settings, questions, description, type_of_questions
    settings_list_screen()
    file_settings_location = input()
    settings = make_settings_dictionary(file_settings_location, default_settings, allowed_settings)
    question_list_screen()
    file_questions_location = input()
    temporary_list = make_question_dictionary(file_questions_location)
    questions = temporary_list[0]
    description = temporary_list[1]
    type_of_questions = temporary_list[2]
    del temporary_list

#Wyświetlanie statystyk poprzednich gier
def games_statistics():
    print(50 * "=")
    try:
        scores = open("scores.txt", 'r')
        try:
            for i in scores:
                print(i)
        finally:
            scores.close()
    except:
        print("Nie można otworzyć pliku ze statystykami.")
    print("Aby wrócić do menu, wpisz 1.")
    print("> ", end="")
    back_to_menu = input()
    while back_to_menu != '1':
        print("Aby wrócić do menu, wpisz 1.")
        print("> ", end="")
        back_to_menu = input()
    print(50 * "=")
    main_menu()

#Nowa gra
def new_game():
    print("Rozpoczęto nową grę.")
    global player, win_condition, question_number
    player = player_creation()
    description_display()
    avalible_questions = list(questions.keys())
    lose_condition = game_over_condition()
    win_condition = False
    correct_answers_counter = 0
    while lose_condition == False and win_condition == False:
        if len(avalible_questions) > 0:
            question_number = randint(1, len(questions))
            while question_number not in avalible_questions:
                question_number = randint(1, len(questions))
            player_statistics()
            time_limit = get_time_limit()
            difficulty = get_difficulty()
            question_display()
            time_first = time()
            answer = input()
            time_second = time()
            if time_second - time_first > time_limit:
                timeout_action(difficulty, avalible_questions)
            else:
                result = check_answer(answer)
                if result == 1:
                    good_answer_action(difficulty, avalible_questions)
                    player[3] += 1
                else:
                    bad_answer_action(difficulty, avalible_questions)
        else:
            no_questions_action(avalible_questions)
        lose_condition = game_over_condition()
        win_condition = game_victory_condition()
    game_over()

#Funkcje dotyczące gry
def player_creation():
    print("Proszę podać swoje imię.")
    print("> ", end="")
    name = input()
    return [name, 0, settings["chances_maximum"], 0]

def player_statistics():
    print(50 * "-")
    print("%s | Punkty : %s | Szanse : %s" % (player[0],player[1],player[2]))
    print(50 * "-")

def game_over_condition():
    if settings["defeat_condition"] == "NO_CHANCES":
        return player[2] <= 0
    elif settings["defeat_condition"] == "MINUS_POINTS":
        return player[1] < 0
    elif settings["defeat_condition"] == "BOTH":
        return player[2] <= 0 or player[1] < 0

def game_victory_condition():
    if settings["victory_condition"] == "NONE":
        return False
    elif settings["victory_condition"] == "POINT_LIMIT":
        if player[1] >= settings["victory_parameter"]:
            return True
        else:
            return False
    elif settings["victory_condition"] == "QUESTION_LIMIT":
        if player[3] >= settings["victory_parameter"]:
            return True
        else:
            return False

def get_time_limit():
    if settings["time_limit_location"] == "QUESTIONS":
        if type_of_questions == "OPEN":
            print("Czas na udzielenie odpowiedzi: %s s" % questions[question_number][3])
            return questions[question_number][3]
        elif type_of_questions == "CLOSED":
            print("Czas na udzielenie odpowiedzi: %s s" % questions[question_number][4])
            return questions[question_number][4]
    elif settings["time_limit_location"] == "CONFIG":
        print("Czas na udzielenie odpowiedzi: %s s" % settings["time_limit_maximum"])
        return settings["time_limit_maximum"]

def get_difficulty():
    if settings["difficulty_location"] == "QUESTIONS":
        if type_of_questions == "OPEN":
            print("Poziom trudności pytania: %s" % questions[question_number][2])
            return questions[question_number][2]
        elif type_of_questions == "CLOSED":
            print("Poziom trudności pytania: %s" % questions[question_number][3])
            return questions[question_number][3]
    elif settings["difficulty_location"] == "CONFIG":
        print("Poziom trudności pytania: %s" % settings["difficulty_parameter"])
        return settings["difficulty_parameter"]

def check_answer(answer):
    if type_of_questions == "OPEN":
        if answer.lower() == questions[question_number][1].lower():
            return 1
        else:
            return 0
    elif type_of_questions == "CLOSED":
        try:
            my_answer = int(answer)
        except:
            my_answer = 0
        if my_answer == questions[question_number][2]:
            return 1
        else:
            return 0

def timeout_action(difficulty, avalible_questions):
    if settings["timeout_action"] == "GAME_OVER":
        print("Czas na odpowiedź minął!")
        game_over()
    else:
        print("Czas na odpowiedź minął!")
        if "CHANCES" in settings["timeout_action"] and difficulty >= settings["timeout_chances_difficulty"]:
            print(" Szanse stracone: %s" % settings["timeout_chances"], end="")
            player[2] -= settings["timeout_chances"]
        if "POINTS" in settings["timeout_action"]:
            print(" Punkty stracone: %s" % settings["timeout_points"], end="")
            player[1] -= settings["timeout_points"] * difficulty
        if "LOCK" in settings["timeout_action"]:
            avalible_questions.remove(question_number)
        print("\n")

def good_answer_action(difficulty, avalible_questions):
    print("Poprawna odpowiedź!")
    if "CHANCES" in settings["good_answer_action"] and difficulty >= settings["good_answer_chances_difficulty"]:
        player[2] += settings["good_answer_chances"]
        print(" Szanse otrzymane: %s" % settings["good_answer_chances"], end="")
    if "POINTS" in settings["good_answer_action"]:
        player[1] += settings["good_answer_points"] * difficulty
        print(" Punkty otrzymane: %s" % settings["good_answer_chances"], end="")
    if "LOCK" in settings["good_answer_action"]:
        avalible_questions.remove(question_number)
    print("\n")

def bad_answer_action(difficulty, avalible_questions):
    if settings["bad_answer_action"] == "GAME_OVER":
        game_over()
    else:
        print("Błędna odpowiedż!")
        if "CHANCES" in settings["bad_answer_action"] and difficulty >= settings["bad_answer_chances_difficulty"]:
            print(" Szanse stracone: %s" % settings["bad_answer_chances"], end="")
            player[2] -= settings["bad_answer_chances"]
        if "POINTS" in settings["bad_answer_action"]:
            print(" Punkty stracone: %s" % settings["bad_answer_points"], end="")
            player[1] -= settings["bad_answer_points"] * difficulty
        if "LOCK" in settings["bad_answer_action"]:
            avalible_questions.remove(question_number)
        print("\n")

def no_questions_action(avalible_questions):
    if settings["no_questions_action"] == "GAME_OVER":
        game_over()
    elif settings["no_questions_action"] == "RESET_QUESTIONS":
        avalible_questions = list(questions.keys())

def game_over():
    end_game_time = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    print(50 * "=")
    if win_condition == True:
        print("Zwycięstwo!")
    else:
        if settings["victory_condition"] == "NONE":
            print("Gra zakończona.")
        else:
            print("Przegrana...")
    print("Gracz %s zdobył %s punktów!" % (player[0], player[1]))
    print("Odpowiedziano poprawnie na %s pytań" % player[3])
    try:
        scores = open("scores.txt", 'a')
        print("%s | GRACZ : %s | PUNKTY : %s | POPRAWNE ODPOWIEDZI : %s" % (end_game_time, player[0],player[1],player[3]), file=scores)
        scores.close()
    except:
        print("Nie można zapisać wyniku do pliku.")
    exit()

#Definicje ważnych słowników

default_settings = {
    "chances_maximum": 3,
    "difficulty_location": "CONFIG",
    "difficulty_parameter": 1,
    "time_limit_location": "CONFIG",
    "time_limit_maximum": 60,
    "good_answer_action": "ADD_POINTS",
    "good_answer_points": 10,
    "good_answer_chances": 1,
    "good_answer_chances_difficulty": 10,
    "bad_answer_action": "REMOVE_CHANCES_POINTS",
    "bad_answer_points": 5,
    "bad_answer_chances" :1,
    "bad_answer_chances_difficulty": 1,
    "timeout_action": "REMOVE_CHANCES_POINTS",
    "timeout_points": 5,
    "timeout_chances": 1,
    "timeout_chances_difficulty": 1,
    "victory_condition": "NONE",
    "victory_parameter": 25,
    "defeat_condition": "NO_CHANCES",
    "no_questions_action": "GAME_OVER"
}
allowed_settings = {
    "chances_maximum": 1,
    "difficulty_location": ["CONFIG", "QUESTIONS"],
    "difficulty_parameter": 1,
    "time_limit_location": ["CONFIG", "QUESTIONS"],
    "time_limit_maximum": 1,
    "good_answer_action": ["ADD_LOCK", "ADD_CHANCES", "ADD_POINTS", "ADD_CHANCES_POINTS", "ADD_CHANCES_LOCK",
                           "ADD_LOCK_POINTS", "ADD_CHANCES_LOCK_POINTS"],
    "good_answer_points": 1,
    "good_answer_chances": 1,
    "good_answer_chances_difficulty": 0,
    "bad_answer_action": ["GAME_OVER", "REMOVE_CHANCES", "REMOVE_POINTS", "REMOVE_CHANCES_POINTS","LOCK",
                       "LOCK_REMOVE_CHANCES", "LOCK_REMOVE_POINTS", "LOCK_REMOVE_CHANCES_POINTS"],
    "bad_answer_points": 1,
    "bad_answer_chances": 1,
    "bad_answer_chances_difficulty": 0,
    "timeout_action": ["GAME_OVER", "REMOVE_CHANCES", "REMOVE_POINTS", "REMOVE_CHANCES_POINTS","LOCK",
                       "LOCK_REMOVE_CHANCES", "LOCK_REMOVE_POINTS", "LOCK_REMOVE_CHANCES_POINTS"],
    "timeout_points": 1,
    "timeout_chances": 1,
    "timeout_chances_difficulty": 0,
    "victory_condition": ["NONE", "POINT_LIMIT", "QUESTION_LIMIT"],
    "victory_parameter": 1,
    "defeat_condition": ["NO_CHANCES", "MINUS_POINTS", "BOTH"],
    "no_questions_action": ["GAME_OVER", "RESET_QUESTIONS"]
}

main_menu()
