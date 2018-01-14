import spacy
nlp = spacy.load('en')
string = "John had 6 apples and ate 2 of them"
##string = "john has 3 apples his bag"
doc = nlp(string)
pn = ['NN','NNP','NNPS','NNS']

pre_verb = []
verb = []
post_verb = []
prep_ph = []

def find_nummod(t):
    for c in t.children:
        if c.dep_ == 'nummod':
            return 1
    return 0

def get_val(t):
    for c in t.children:
        if c.dep_ == 'nummod':
            return c.text
    return 0
    
##for ent in doc.noun_chunks:
####    print(ent.root.text,ent.root.tag_)
##    if ent.root.tag_ in pn and find_nummod(ent.root):
##        entity.append((ent.root.text,get_val(ent.root)))
##    elif ent.root.tag_ in pn:
##        owner.append(ent.root.text)
##
##for token in doc:
##    if token.pos_ == 'VERB':
##        verb.append(token.text)
##
##print(owner)
##print(entity)
##print(verb)

def lts(l):
    s = ""
    for w in l:
        s = s + w + " "
    return s


def resolve_conj(s):
    doc1 = nlp(s)
    temp = []
    p = ""
    vs = 0
    for d in doc1:
        if d.pos_ == 'VERB':
            vs = 1
            if lts(temp):
                pre_verb.append(lts(temp))
            else:
                pre_verb.append("###")
            verb.append(d.text)
            temp = []
            continue
        elif d.pos_ == 'ADP':
            p = d.text
        temp.append(d.text)
    if p:
        inner_temp = []
        for t in temp:
            if t == p:
                post_verb.append(lts(inner_temp))
                inner_temp = []
            inner_temp.append(t)
        prep_ph.append(lts(inner_temp))
    else:
        post_verb.append(lts(temp))
        prep_ph.append("###")
    if not vs:
        pre_verb.append("###")
        verb.append("###")
    print(pre_verb,verb,post_verb,prep_ph)
    
statement = []
l = []
for t in doc:
    if t.tag_ == 'CC':
        statement.append(lts(l))
        l = []
    else:
        l.append(t.text)

statement.append(lts(l))        
print(statement)

for s in statement:
    resolve_conj(s)
