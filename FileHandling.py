def get_list():
    path = '/Users/ChiefAmay/Desktop/calculator/addition.txt'
    string = "what will be the sum of 3 and three thousand thirty six and the product of seven and eight"
    addfile = open(path,'r')
    init = addfile.read()
    print(init)
    updated = init+string+"\n"
    addfile = open(path,'w')
    addfile.write(updated)
    addfile = open(path,'r')
    print(addfile.read())
    addfile.close()

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
