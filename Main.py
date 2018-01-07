import spacy
import nltk
from word2number import w2n
import trial3 as file_list
import bracket as b
import addtods as dev
import evaluate as e
nlp = spacy.load("en")

##GLOBAL VARIABLES
c1 = ['NN','VB','VBN','VBG','JJ']
c2 = ['CC','TO','SYM',',']
prep = ['with','to','from','by']
prep_direct = ['into','minus']
nn_exp = ['result','cube','root','square','minus','point']
conj_exp = ['minus','plus']
check = ['NN','CC','CD','IN','JJ','TO','VB','VBN','SYM',',','HYPH']
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

## for merging CD like one hundred two to 102
def merge_cd(l):
     start = 0
     end = 0
     ctr = 0 #have seen 1 cardinal
     m = ""
     for w in l:
          if w[1] == 'CD' or w[0] == 'point':
               ctr = 1
               m += str(w[0])
               m += " "
               end = end + 1
          else:
               if ctr == 1:
                    value = w2n.word_to_num(m.strip())
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


    
def remove_hash(l):
     res = []
     for w in l:
          if w != "###":
               res.append(w)
     l = res
     return l

## check 2 CD are not together, effective in subtraction after from is removing
def check_two_cd(l):
     t = 0 #have seen 1 cd
     z = 0 #counter
     y = 0
     for w in l:
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

## Main function taking NLP queries and converting into expression list
def calculate(string):
     f_ques = string
     list_ques = []
     stack = Stack()
     temporary = ""
     doc = nlp(string)
     main = ""
     for token in doc:
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
     list_ques = remove_hash(list_ques)
     for w in list_ques:
          tl = w
##        print("for:",w[0],"list becomes: ",ques)
          if w[1] in c1:
               if w[0] in nn_exp:
                    ques.append((w[0],w[1]))
               elif w[0] in union:
                    stack.push(w[0])
                    temporary = w[0]
          elif w[1] in c2:
               if w[1] == "SYM":
                    ques.append((w[0],w[1]))
               elif w[1] == "CC":
                    if w[0] in conj_exp:
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

     if not stack.isEmpty():
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


##zzz = "multiply the square of 2 plus 3 to five"
##answer = calculate(zzz)
##print("The answer: ",answer)
##print("do u wanna add this a test case (y/n)")
##choice = str(input("enter: "))
##if choice == "y" or "Y":
##     dev.add_element(zzz+"\t"+str(answer))
     
