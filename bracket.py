def precedence(l):
    before = []
    after = []
    count = 0
    seen = 0
    distance = 0
    shift = 1
    first = 0
    m = []
    for w in l:
        if w[1] == 'CD':
            if shift and not seen:
                first = count
            if seen:
                before.append(first)
                after.append(count+1)
            else:
                seen = 1
            distance = 0
        else:
            if seen:
                if distance > 1:
                    distance = 0
                    seen = 0
                else:
                    distance = distance + 1
        count = count + 1
    acc = 0
    print(before)
    print(after)
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
    return l 
