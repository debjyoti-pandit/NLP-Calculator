def add_element(string):
    path = '/Users/ChiefAmay/Desktop/calculator/addition.txt'
    addfile = open(path,'r')
    init = addfile.readlines()
    updated = ""
    string += "\n"
    if string not in init:
        addfile = open(path,'r')
        updated = addfile.read()
        updated +=string
        addfile = open(path,'w')
        addfile.write(updated)
    addfile.close()

def test():
    path = '/Users/ChiefAmay/Desktop/calculator/addition.txt'
    addfile = open(path,'r')
    init = addfile.readlines()
    l = []
    for w in init:
        l.append(w.strip())
    addfile.close()
    return l

def error(string):
    path = '/Users/ChiefAmay/Desktop/calculator/Subtraction.txt'
    subfile = open(path,'r')
    init = subfile.readlines()
    updated = ""
    string += "\n"
    if string not in init:
        subfile = open(path,'r')
        updated = subfile.read()
        updated +=string
        subfile = open(path,'w')
        subfile.write(updated)
    subfile.close()
