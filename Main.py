import spacy
import nltk
from word2number import w2n
import trial3 as file_list
nlp = spacy.load("en")

##GLOBAL VARIABLES
check = ['NN','CC','CD','IN','JJ','TO','VB','VBN','SYM',',']
sub = ['subtraction','subtract','difference','minus']
add = ['add','sum','addition','plus']
mult = ['multiply','product','multiplication','into']
div = ['division','divide','by']
union = ['subtraction','subtract','difference','minus','add','sum','addition','plus',
         'multiply','product','multiplication','into','division','divide','by']
##MENU
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

def merge_cd(l):
##     print(l)
     start = 0
     end = 0
     ctr = 0 #have seen 1 cardinal
     m = ""
     for w in l:
##          print("for: ",w[0],"string: ",m)
          if w[1] == 'CD' or w[0] == 'point':
               ctr = 1
               m += str(w[0])
               m += " "
               end = end + 1
          else:
               if ctr == 1:
                    value = w2n.word_to_num(m.strip())
##                    print("value: ",value)
                    l[start] = (value,'CD')
                    start = start + 1
                    while (start<end):
                         l[start] = "###"
                         start = start + 1
                    m = ""
               end = end + 1
               ctr = 0
               start = end
     value = w2n.word_to_num(m.rstrip())
     l[start] = (value,'CD')
     start = start + 1
     while (start<end):
          l[start] = "###"
          start = start + 1
     l = remove_hash(l)
     return l

def evaluate(q):
    final_ques = ""
    for w in q:
         if w[1] != "CD":
              if w[0] in sub:
                   final_ques += "-"
              elif w[0] in add:
                   final_ques += "+"
              elif w[0] in mult:
                   final_ques += "*"
              elif w[0] in div:
                   final_ques += "/"
##              elif w[0] == "point":
##                   final_ques += "point"
         else:
              final_ques += str(w[0])
    print(final_ques)
    return eval(final_ques)
    
def remove_hash(l):
     res = []
     for w in l:
          if w != "###":
               res.append(w)
     l = res
     return l


def check_two_cd(l):
     t = 0 #have seen 1 cd
     z = 0 #counter
     y = 0
     for w in l:
##          print("check:",w)
          if w[1] == "CD":
               if t == 1:
                    y = 1
                    break
               t = 1
               z = z + 1
          else:
               z = z + 1
               t = 0
     if y == 1:
          l.insert(z,("subtract","NN"))
     return l

def calculate(string):
     f_ques = string
     list_ques = []
     stack = Stack()
     temporary = ""
##     string = 'addition of product of 2 plus 4 and 7 with the difference of 7 from 3'
##     string = input("Enter your question: ")
     doc = nlp(string)
     main = ""
     for token in doc:
##         print(token.text,token.tag_)
         if token.tag_ != "CD":
     ##          tag = token.tag_
             token = str(token.lemma_)
         main += str(token)
         main += " "

     ##print("string lemma:",main)
     doc2 = nlp(main)
     for token in doc2:
##          print(token.text,token.tag_)
          if token.tag_ in check:
               tag = token.tag_
               token = str(token)
               list_ques.append((token.lower(),tag))

##     print("list before expression function: ",list_ques)          
     list_ques = merge_cd(list_ques)
     ques = []
     ##expression function
     c1 = ['NN','VB','VBN','VBG','JJ']
     c2 = ['CC','TO','SYM',',']
     prep = ['with','to','from','by']
     prep_direct = ['into','minus']
     nn_exp = ['result','cube','root','square','minus','point']
     list_ques = remove_hash(list_ques)
     for w in list_ques:
          tl = w
##          print("for:",w[0],"list becomes: ",ques)
          if w[1] in c1:
               if w[0] in nn_exp:
                    ques.append((w[0],w[1]))
               elif w[0] in union:
     ##               print("pushing ",w[0])
                    stack.push(w[0])
                    temporary = w[0]
          elif w[1] in c2:
               if w[1] == "SYM":
                    ques.append((w[0],w[1]))
               elif w[1] == "CC":
                    if w[0] == "plus":
                         ques.append((w[0],w[1]))
                    else:
                         if not stack.isEmpty():
                              temporary = stack.pop()
                         ques.append((temporary,w[1]))
               else:
                    if not stack.isEmpty():
                         temporary = stack.pop()
                    ques.append((temporary,w[1]))
          elif w[1] == "IN":
               if w[0] in prep:
                    if not stack.isEmpty():
                         temporary = stack.pop()
                    ques.append((temporary,w[1]))
               elif w[0] in prep_direct:
                    ques.append((w[0],w[1]))
          else:
               ques.append((w[0],w[1]))

##     print("question: ",ques)
##     print(stack.pop())
     if not stack.isEmpty():
          del ques[0]
     ques = check_two_cd(ques)
##     print("Expression for your question is = ",ques)
     ans = evaluate(ques)
     print("The answer: ",ans)
     f_ques += "\t"+str(ans)
     file_list.add_element(f_ques)
     


##print("press 1 to enter testing mode")
##print("press 2 to enter calculate mode")
##choice = str(input("please enter your choice: "))
##if choice == "1":
##     test()
##elif choice == "2":
##     calculate()
##else:
##     print("please enter a valid input")
calculate("Sum of three,four,five and six")
