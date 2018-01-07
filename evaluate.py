sub = ['subtraction','subtract','difference','minus','-']
add = ['add','sum','addition','plus']
mult = ['multiply','product','multiplication','into']
div = ['division','divide','by']
brac = ['(',')']

def cal_root(new_list):
     del new_list[0]
     m = []
     bc = 0
     if new_list[0][1] == 'CD':
          g = (int(new_list[0][0])**0.5)
          return (int(new_list[0][0])**0.5)
     else:
          for w in new_list:
               if w[1] != ')':
                    if w[1] == '(':
                         bc += 1
                    m.append(w)
               else:
                    m.append(w)
                    bc -= 1
                    if bc == 0:
                         break
          v = evaluate(m)
          return (int(v)**0.5)

def cal_sq(new_list):
    bc = 0
    m = []
    if new_list[0][1] == 'CD':
        g = (int(new_list[0][0])**2)
        return g
    else:
        for w in new_list:
            if w[1] != ')':
                if w[1] == '(':
                    bc += 1
                m.append(w)
            else:
                m.append(w)
                bc -= 1
                if bc == 0:
                    break
        v = evaluate(m)
        return (int(v)**2)


def evaluate(q):
    final_ques = ""
    count = 0
    for w in q:
              count += 1
              if w[1] != "CD":
                   if w[0] in sub:
                        final_ques += "-"
                   elif w[0] in add:
                        final_ques += "+"
                   elif w[0] in mult:
                        final_ques += "*"
                   elif w[0] in div:
                        final_ques += "/"
                   elif w[0] in brac:
                        final_ques += str(w[0])
                   elif w[0] == "square":
                        new_list = q[count:]
                        gen = iter(new_list)
                        next_value = gen.__next__()
                        x = next_value
                        if str(x[0]) == "root":
                              rr = cal_root(new_list)
                              del q[count]
                              final_ques += str(rr)
                        else:
                             sq = cal_sq(new_list)
                             final_ques += str(sq)
                        cc = 1
                        bc = 0
                        ll = new_list
                        for ww in new_list:
                             if ww[1] == 'CD' and cc:
                                  del q[count]
                                  break
                             elif ww[1] == '(':
                                  bc += 1
                                  del q[count]
                                  cc = 0
                             elif ww[1] == ')':
                                  bc -= 1
                                  del q[count]
                                  if bc == 0:
                                       break
                             else:
                                  del q[count]                                   
              else:
                   final_ques += str(w[0])
##    print("before eval method: ",final_ques)
    return eval(final_ques)
