# !/usr/bin/python
__author__ = 'Xander Lammertink'

# Import libraries
import hashlib
import struct


def askCandidates(listname):
    # Ask for candidates and put them into a list
    print "\nEnter the names of " + listname + " in alphabetic order."
    print "Please be aware that the names should be separated by ', '.\n"

    names = raw_input("Names: ")
    names = names.split(', ')

    return names
    # Determine the size of the pool
    # pool = len(candidates)


def askSplitSize(rooms):
    splitsize = []
    for i in range(0, rooms):
        splitsize.append(int(raw_input("How many candidates should be in room " + str(i) + "? ")))
    return splitsize


def askKeySource():
    # Ask for key sources
    print "\nEnter the numbers of the keysources."
    print "Please be aware that numbers should be separated by a space."
    print "Different key sources should be separated by ', '\n"

    keysource = raw_input("Key sources: ")
    keysource = keysource.split(', ')

    # Format the sources into a key string
    for i in range(0, len(keysource)):
        # Create temp list with all values
        temp_key = str(keysource[i]).split(' ')
        # Convert values to int
        temp_key = map(int, temp_key)
        # Sort values from small to large
        temp_key.sort()
        # Convert back to string
        temp_key = map(str, temp_key)
        # Put them into the original keysource[]
        keysource[i] = " ".join(temp_key)
        # Add '.' between numbers
        keysource[i] = keysource[i].replace(' ', '.') + '.'

    # Add '/' after every source
    keysource = '/'.join(keysource) + '/'
    return keysource


def executeNomCom(candidates, keysource, to_select):
    # candidates: The names you would like to select in alphabetical order
    # keysource: The keysource you would like to use
    # pool: Amount of values you would like to select

    # Create variables for function
    result = []
    pool = len(candidates)

    # Execute function
    for i in range(0, to_select):
        m = hashlib.md5()
        pre = struct.pack('>H', i)
        m.update(pre)
        m.update(str(keysource))
        m.update(pre)

        hex = m.hexdigest()
        inter = int("0x" + hex, 0)
        selected = inter % (pool - i)
        result.append(candidates[selected])
        candidates.pop(selected)
    # Output result
    return result

##
# Varables
##
candidates = []  # The candidates per list
splitsize = []  # The amount of candidates per classroom
classroomcandidates = []  # Candidates separated over classrooms

# Define how many classrooms
classrooms = int(raw_input("How many classrooms are available: "))

##
# Create three pre-defined lists with candidates
##
print "\nEnter the amount of lists that need to be created."
print "Think of lists for: new students, part-time students, returning students and down-/upstairs students"
lists = int(raw_input("How many lists need to be created: "))

# Ask for names
listnames = []
for i in range(0, lists):
    listnames.append(raw_input("Enter the name for list " + str(i) + "? "))

# Ask names for each list
for i in range(0, lists):
    # List 0: New Full-Time Students
    candidates.append(askCandidates(str(listnames[i])))
    splitsize.append(askSplitSize(classrooms))

print candidates
print splitsize

##
# Execute NomCom procedure over the pre-defined lists
##

# Ask for the keysource
keysource = askKeySource()

# Execute NomCom procedure
for i in range(0, len(candidates)):
    candidates[i] = executeNomCom(candidates[i], keysource, len(candidates[i]))

# Separate candidates over classrooms
for lijst in range(0, len(candidates)):
    candidatenumber = 0
    count = 0
    for lokaal in range(0, len(splitsize[0])):
        temp = []
        for entry in range(candidatenumber, splitsize[lijst][lokaal]):
            temp.append(candidates[lijst][count])
            count += 1
        # THIS GOES WRONG !!
        if lijst == 0:
            classroomcandidates.append(temp)
        else:
            classroomcandidates[lokaal].extend(temp)

# Execute per classroom
for i in range(0, classrooms):
    # Ask the seat offset of classroom
    offset = int(raw_input("What is the first seat of classroom " + str(i) + ": ")) - 1
    # Ask the seat where the teacher is located
    teacher_seat = int(raw_input("What is the seat number of the lab teacher? "))
    # Ask seats to be skipped
    empty_seats = raw_input("\n Enter the seat numbers that need to be skipped. \nPlease separate with ', ' and leaf empty when no seats need to be skipped.\n\nSeat: ")
    # Make this an array
    empty_seats = empty_seats.split(', ')
    # Convert to int values if necessary and add teacher seat
    if empty_seats[0] == '':
        empty_seats[0] = teacher_seat
    else:
        empty_seats = map(int, empty_seats)
        empty_seats.append(teacher_seat)
    # Sort values from small to large
    empty_seats.sort()

    # Execute NomCom over the new list
    endlist = executeNomCom(classroomcandidates[i], keysource, len(classroomcandidates[i]))

    # Insert teacher and empty seats
    # If the list is too short, the teacher and empty seats will be added at the end of the list
    for i in range(0, len(empty_seats)):
        # Remove offset
        empty_seats[i] -= offset + 1
        # Is it a teacher seat?
        if empty_seats[i] == teacher_seat - offset - 1:
            # Insert teacher seat
            endlist.insert(empty_seats[i], "Teacher")
        else:
            # Insert empty seat
            endlist.insert(empty_seats[i], "Empty")

    # Print seat order
    print "\n^ Seat ^ Name ^"
    for j in range(0, len(endlist)):
        print "| " + str((j + 1 + offset)) + " | " + endlist[j] + " |"
    print "\n"
