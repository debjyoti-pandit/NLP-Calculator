def precedence(l):
##    print(l)
    before = []
    after = []
    count = 0
    seen = 0
    distance = 0
    shift = 1
    first = 0
    m = []
    ssq = 0
    ssc = 0
    for w in l:
##        print("for: ",w[0],"count",count)
        if w[1] == 'CD':
            if shift and not seen:
                first = count
            if seen:
                if ssq:
                    before.append(ssc)
                    after.append(count+1)
                    before.append(first)
                    after.append(count+1)
                    first = ssc
                    ssq = 0
                else:
                    before.append(first)
                    after.append(count+1)
                
            else:
                if w[1] == 'CD':
                    seen = 1
            distance = 0
        else:
            if w[0] == 'square':
                ssq = 1
                ssc = count
            if seen:    
                if distance > 1:
                    distance = 0
                    seen = 0
                else:
                    distance = distance + 1
        count = count + 1
    acc = 0
    before.sort()
    for i in range(len(before)):
        l.insert(before[i]+acc, ('(','('))
        acc += 1
    acc=0
    for i in range(len(after)):
        q = 0
        for j in before:
            if after[i]>j:
                q += 1
        l.insert(after[i]+acc+q, (')',')'))
        acc += 1
##    print("in br: ",l)
    return l 

##ss =[('sum', 'NN'), ('of', 'IN'), ('square', 'JJ'), ('root', 'NN'), ('of', 'IN'), (40.0, 'CD'), ('plus', 'CC'), (60.0, 'CD'), ('and', 'CC'), (21.0, 'CD')]
##precedence(ss)
