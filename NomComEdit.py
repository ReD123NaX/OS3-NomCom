# !/usr/bin/python
__author__ = 'Xander Lammertink'

# Import libraries
import hashlib
import struct


def askCandidates(listname):
    # Ask for candidates and put them into a list
    print "\nPlease enter the names of the " + listname + " in alphabetic order."
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
    print "\nPlease enter the numbers of the keysources."
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


def executeNomCom(candidates, keysource, pool):
    # candidates: The names you would like to select in alphabetical order
    # keysource: The keysource you would like to use
    # pool: Amount of values you would like to select

    # Create variables for function
    result = []

    # Execute function
    for i in range(0, pool):
        m = hashlib.md5()
        pre = struct.pack('>H', i)
        m.update(pre)
        m.update(str(keysource))
        m.update(pre)

        hex = m.hexdigest()
        inter = int("0x" + hex, 0)
        selected = inter % (pool - i)
        result.append(candidates[selected])
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

# List 0: New Full-Time Students
candidates.append(askCandidates("new full-time students"))
splitsize.append(askSplitSize(classrooms))

# List 1: New Part-Time Students
candidates.append(askCandidates("new part-time students"))
splitsize.append(askSplitSize(classrooms))

# List 2: Returning Students
candidates.append(askCandidates("returning students"))
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

print str(len(splitsize[0]))

# Separate candidates over classrooms
for lijst in range(0, len(candidates)):
    candidatenumber = 0
    for lokaal in range(0, len(splitsize[0])):
        temp = []
        for entry in range(candidatenumber, splitsize[lijst][lokaal]):
            temp.append(candidates[lijst][entry])
        # THIS GOES WRONG !!
        if lijst == 0:
            classroomcandidates.append(temp)
        else:
            classroomcandidates[lokaal].extend(temp)

# Execute NomCom per classroom
for i in range(0, classrooms):
    print "Classroom " + str(i) + ":\n"
    print "^ Seat ^ Name ^"
    classroomcandidates[i] = executeNomCom(classroomcandidates[i], keysource, len(classroomcandidates[i]))
    for j in range(0, len(classroomcandidates[i])):
        print "| " + str((j + 1)) + " | " + classroomcandidates[i][j] + " |"
