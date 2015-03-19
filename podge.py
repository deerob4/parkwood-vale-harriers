import random
import os
import sqlite3 as lite

if os.path.isfile('classes.db'):
    con = lite.connect('classes.db')
else:
    con = lite.connect('classes.db')
    for x in range(1, 4):

        # Creates the database, but with 3 extra columns - NextScore, Score1, Score2, Score3, for storing the last 3 scores
        con.execute('CREATE TABLE class%s(ID INTEGER PRIMARY KEY, Name TEXT, NextScore INTEGER, Score1 INTEGER DEFAULT 0, Score2 INTEGER DEFAULT 0, Score3 INTEGER DEFAULT 0);' % x)


def generate_questions():
    question_matrix = [[0 for x in range(2)] for x in range(10)]
    operators = ['+', '-', '*']

    for x in range(10):
        first_number = random.randint(1, 20)
        second_number = random.randint(1, first_number)
        operator = random.choice(operators)

        if operator == '+':
            question_matrix[x][0] = str(first_number) + ' + ' + str(second_number)
            question_matrix[x][1] = first_number + second_number
        elif operator == "-":
            question_matrix[x][0] = str(first_number) + ' - ' + str(second_number)
            question_matrix[x][1] = first_number - second_number
        elif operator == "*":
            question_matrix[x][0] = str(first_number) + ' x ' + str(second_number)
            question_matrix[x][1] = first_number * second_number

    return question_matrix


def display_questions():
    while True:
        class_number = int(input('\nWhich class do you belong to (1-3)? '))

        if 1 <= class_number <= 3:
            break
        else:
            print('Number must be between 1 and 3!')

    name = input('\nWhat is your full name? ').title()
    questions = generate_questions()
    correct = 10

    for x in range(10):

        while True:
            answer = input('\n%s. What is %s? ' % (x + 1, questions[x][0]))
            if answer.isdigit():
                answer = int(answer)
                break
            else:
                print('You must enter a digit!')

        if int(answer) == int(questions[x][1]):
            print('That\'s correct!')
        else:
            correct -= 1
            print('Oops, the answer was %s!' % questions[x][1])

    print('\nWell done %s, you got %s out of 10!' % (name, correct))

    record_score(name, class_number, correct)


def record_score(name, class_number, correct):
    table = 'class%s' % class_number

    with con:
        cur = con.cursor()

        cur.execute('SELECT * FROM ' + table + ' WHERE Name = "%s";' % name)
        already_recorded = len(cur.fetchall())

        # If a record with the user's name hasn't been written - if it is their first attempt
        if already_recorded == 0:

            # Create a new record with their name and score - add it to Score1
            cur.execute('INSERT INTO %s(Name, Score1) VALUES ("%s", %i);' % (table, name, correct))

            # Set the NextScore column to 2, so the program knows where to write the next attempt
            cur.execute('UPDATE %s SET NextScore = 2 WHERE Name = "%s";' % (table, name))

        # If the user has previously attempted the test
        else:

            # Get the value of the NextScore column, so the program knows where to write the next attempt
            cur.execute('SELECT NextScore FROM %s WHERE Name = "%s"' % (table, name))
            next_score = (cur.fetchall())[0][0]

            # Add the user's score to the Score-x column, where x is the value of NextScore
            cur.execute('UPDATE %s SET Score%s = %i WHERE Name = "%s";' % (table, next_score, correct, name))
            
            # If the value of NextScore is 3
            if next_score == 3:

                # Set NextScore back to 1, creating a loop of sorts
                cur.execute('UPDATE %s SET NextScore = 1 WHERE Name = "%s";' % (table, name))
            else:

                # If not, set NextScore to NextScore + 1, incrementing it
                cur.execute('UPDATE %s SET NextScore = %i WHERE Name = "%s";' % (table, next_score + 1, name))


# Function for viewing the results, called from the choose_task() function
def view_results():
    class_number = int(input('Which class do you want to view (1-3)? '))
    
    # Prints a multiline message explaining the possible options for outputting the results
    print(
        '\nHow do you want to view the results? There are three ways:\n1. Alphabetically\n2. By highest score\n3. By average score')

    # Ensures that only 1, 2 or 3 can be entered, loops forever until one of those values is entered
    while True:
        method = input('\nEnter 1, 2 or 3: ')

        with con:
            cur = con.cursor()

            # If the method selected is 1 - if it is Alphabetically
            if method == '1':

                # Select the Name of the student and the maximum of their three scores, and order it alphabetically
                cur.execute('SELECT Name, max(Score1, Score2, Score3) FROM class%s ORDER BY Name' % class_number)
                sentence = '\nClass %s sorted by alphabetical order' % class_number
                break

            # If the method selected is 2 - if it is By highest score
            elif method == '2':

                # Select the name of the student and the maximum of their three scores, and order by the highest of these
                cur.execute('SELECT Name, max(Score1, Score2, Score3) FROM class%s ORDER BY max(Score1, Score2, Score3) DESC;' % class_number)
                sentence = '\nClass %s sorted by highest score first' % class_number
                break

            # If the method selected is 3 - if it is By average score
            elif method == '3':
                print("Haven't worked out how to do this yet. Sorry.")
                break
            else:
                print('You must enter 1, 2 or 3.')

    # Set the scores variable to the data as selected by the executed SQL statement. Is a list.
    scores = cur.fetchall()

    # Print the contextual sentence
    print(sentence)

    # Print as many dashes as there are letters in the sentence, for neatness
    print('-' * len(sentence))

    # Print out the values as defined in the scores variable, using a loop to loop through each row
    for x in range(len(scores)):

        # x + 1 is the index value. scores[x][0] is the student's name. scores[x][1] is their score.
        print('%s. %s - %s' % (x + 1, scores[x][0], scores[x][1]))

    print('\n')


# Pretty self explanatory, accepts input and calls the correct functions as defined above
def choose_task():
    while True:
        task = input('\nDo you want to take the test(1) or view results(2)? ')
        if task == '1':
            display_questions()
            break
        elif task == '2':
            view_results()
            break
        else:
            print('You must enter 1 or 2.')


# Starts of the program, executing the choose_task() function above
choose_task()