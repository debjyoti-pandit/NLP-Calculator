import spacy
import nltk
from word2number import w2n
import trial3 as file_list
import bracket as b
import addtods as dev
import evaluate as e
nlp = spacy.load("en")

##GLOBAL VARIABLES
c1 = ['NN','VB','VBN','VBG','JJ','NNS']
c2 = ['CC','TO','SYM',',']
prep = ['with','to','from','by']
prep_direct = ['into','minus']
sub = ['subtraction','subtract','difference','minus','-']
div = ['division','divide','by']
nn_exp = ['result','cube','root','square','minus','point','time']
conj_exp = ['minus','plus','time']
check = ['NN','CC','CD','IN','JJ','TO','VB','VBN','SYM',',','HYPH',':']
union = ['subtraction','subtract','difference','minus','add','sum','addition','plus',
         'multiply','product','multiplication','into','division','divide','by']

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

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

## for merging CD like one hundred two to 102
def merge_cd(l):
     start = 0
     end = 0
     ctr = 0 #have seen 1 cardinal
     m = ""
     for w in l:
##          print("forrrrrrrrr: ",w," m: ",m)
          if w[1] == 'CD' or w[0] == 'point':
               ctr = 1
               m += str(w[0])
##               print("m :",m)
               m += " "
               end = end + 1
          else:
               if ctr == 1:
                    if is_number(m.strip()):
                         value = float(m.strip())
                    else:
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
     if is_number(m.strip()):
          value = float(m.strip())
     else:
          value = w2n.word_to_num(m.strip())
##          print(l)
     l[start] = (value,'CD')
     start = start + 1
     while (start<end):
          l[start] = "###"
          start = start + 1
##     print(l)
     l = remove_hash(l)
##     print("after",l)
     return l


    
def remove_hash(l):
     res = []
     for w in l:
          if w != "###":
               res.append(w)
     l = res
     return l

## check 2 CD are not together, effective in subtraction after from is removing
def check_two_cd(l):
##     print("ff",l)
     t = 0 #have seen 1 cd
     z = 0 #counter
     y = 0
     for w in l:
##          print("dev")
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
##     print(l)
     return l

## Main function taking NLP queries and converting into expression list
def calculate(string):
     f_ques = string
     list_ques = []
     stack = Stack()
     temporary = ""
     doc = nlp(string)
     main = ""
     for token in doc:
##         print(token.text,token.tag_)
         if token.tag_ != "CD":
             token = str(token.lemma_)
         main += str(token)
         main += " "

     doc2 = nlp(main)
     for token in doc2:
          if token.tag_ in check:
               tag = token.tag_
               token = str(token)
               list_ques.append((token.lower(),tag))

     list_ques = merge_cd(list_ques)
     list_ques = b.precedence(list_ques)
     ques = []
##     print("xXX",list_ques)
     list_ques = remove_hash(list_ques)
     ppp = ""
     for w in list_ques:
          tl = w
##          print("for:",w[0],"list becomes: ",ques)
          if w[1] in c1:
               if w[0] in nn_exp:
                    ques.append((w[0],w[1]))
               elif w[0] in union:
                    stack.push(w[0])
                    temporary = w[0]
                    ppp = temporary
          elif w[1] in c2:
               if w[1] == "SYM":
                    ques.append((w[0],w[1]))
               elif w[1] == "CC":
                    if w[0] in conj_exp:
                         ques.append((w[0],w[1]))
                    else:
                         if not stack.isEmpty():
                              temporary = stack.pop()
                         else:
                              array=ques
                              ra = list(reversed(array))
                              for i in ra:
                                   if i[1] != 'CD' and i[1] != ')' and i[1] != '(' and i[0] not in sub and i[0] not in div:
                                        temporary = str(i[0])
                                        break 
                         ques.append((temporary,w[1]))
               else:
                    if not stack.isEmpty():
                         temporary = stack.pop()
                    ques.append((temporary,w[1]))
          elif w[1] == "IN":
               if w[0] in prep:
                    if not stack.isEmpty():
                         temporary = stack.pop()
                    else:
                         array=ques
                         ra = list(reversed(array))
                         for i in ra:
                              if i[1] != 'CD' and i[1] != ')' and i[1] != '(' and i[0] not in sub and i[0] not in div:
                                   temporary = str(i[0])
                                   break                                
                    if w[0] == 'from' and temporary in sub:
                         h = ques.pop()
                         hh = int(h[0])
                         hh *= -1
                         ques.append((hh,'CD'))
                         ques.append(('add',w[1]))
                    else:
                         ques.append((temporary,w[1]))
               elif w[0] in prep_direct:
                    ques.append((w[0],w[1]))
          else:
               ques.append((w[0],w[1]))

     if not stack.isEmpty():
          if stack.pop() in sub:
               del ques[0]
     ques = check_two_cd(ques)
##     print("Expression for your question is = ",ques)
     ans = e.evaluate(ques)
     return ans

def test():
     l = file_list.test()
     m = []
     ctr = 0
     for w in l:
          m = w.split("\t")
          a = calculate(str(m[0]))
          if str(a) == str(m[1]):
               ctr = ctr + 1
          else:
               print("Actual: ",str(m[1])," and calculated: ",a)
               file_list.error(m[0])
     print("No. of test case runned: ",len(l))
     print("No. of correct answer: ",ctr)
     print("Accuracy: ",(ctr/len(l))*100)


print("press 1 to enter testing mode")
print("press 2 to enter calculate mode")
choice = str(input("please enter your choice: "))
if choice == "1":
     test()
elif choice == "2":
     zzz = str(input("please enter your ques: "))
     answer = calculate(zzz)
     print("The answer: ",answer)
     print("do u wanna add this a test case (y/n)")
     choice = str(input("enter: "))
     if choice == "y" or "Y":
          dev.add_element(zzz+"\t"+str(answer))
else:
     print("please enter a valid input")

##zzz = "subtract 56 from 100"
##answer = calculate(zzz)
##print("The answer: ",answer)
##
##print("do u wanna add this a test case (y/n)")
##choice = str(input("enter: "))
##if choice == "y":
##     dev.add_element(zzz+"\t"+str(answer))
##     print("successfully added")
##else:
##     print("sorry")
