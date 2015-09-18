#!/usr/bin/python

# Import libraries
import hashlib
import struct

# Ask for candidates and put them into a list
print "\nPlease enter the names of the candidates in alphabetic order."
print "Please be aware that the names should be separated by ', '.\n"

candidates = raw_input("Names: ")
candidates = candidates.split(', ')

# Determine the size of the pool
pool = len(candidates)

# Ask for key sources
print "\nPlease enter the numbers of the keysources."
print "Please be aware that numbers should be separated by a space."
print "Different key sources should be separated by ', '\n"

keysource = raw_input("Key sources: ")
keysource = keysource.split(', ')

# Format the sources into a key string
for i in range(0, len(keysource) ):
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

# Ask for the amount of output values

to_select = input("\nHow many names would you like to select? ")
print to_select * to_select

####
#value = "9319./2.5.8.10.12./9.18.26.34.41.45./"
#value = value.encode(encoding='ascii')
#print value
#print "\n\n\n"
####

# Create variables for function
result = []

# Execute function
for i in range (0, to_select - 1):
    m = hashlib.md5()
    pre = struct.pack('>H', i)
    m.update(pre)
    m.update(keysource)
    m.update(pre)

    hex = m.hexdigest()
    inter = int("0x"+hex, 0)
    print inter
    selected = inter % (pool - i)
    print selected
    result.append(candidates[selected])    

# Output result
print result
