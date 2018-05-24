import json
import sys

obj1 = {}
obj2 = {}

with open(sys.argv[1], 'r') as file1:
    obj1 = json.load(file1)

with open(sys.argv[2], 'r') as file2:
    obj2 = json.load(file2)

if obj1 == obj2:
    sys.exit(0)
else:
    sys.exit(1)
