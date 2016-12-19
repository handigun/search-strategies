from operator import attrgetter

def navigate():
    f = open("input.txt","r")
    s = f.read()
    lst = s.split("\n")
    algo = lst[0]
    start = lst[1]
    goal = lst[2]
    no_live = int(lst[3])
    no_sun = int(lst[4+no_live])
    live = {}
    sun = {}
    for i in range(4, 4+no_live):
        cost_lst = lst[i].strip().split(" ")
        live.setdefault(cost_lst[0],[])
        live.setdefault(cost_lst[1],[])
        live[cost_lst[0]].append({'to':cost_lst[1],'cost':int(cost_lst[2]),'id':i - 4})
    ##print(live)
        
    for i in range(4+no_live+1,4+no_live+1+no_sun):
        sun_lst = lst[i].strip().split(" ")
        sun.setdefault(sun_lst[0],{'cost':int(sun_lst[1]),'id':i})
    ##print(sun)
    f.close()
    if algo == "BFS":
        result = search(live, "BFS", start, goal, sun)

    elif algo == "DFS":
        result = search(live, "DFS", start, goal, sun)

    elif algo == "UCS":
        result = search(live, "UCS", start, goal, sun)

    elif algo == "A*":
        result = search(live, "A*", start, goal, sun)
    write_out(result)
    ##print(result)
        
  
def search(live, algo, start, goal, sun):
    open_lst = []
    explored_lst = []
    open_lst.append(node(0, start, None, 0, 0, 0))
    while open_lst:
        cur = open_lst.pop(0)
        i = 0
        if cur.state == goal:
            explored_lst.append(cur)
            break
        for st in live[cur.state]:
            s = make_list(open_lst)
            e = make_list(explored_lst)
            n =  len(live[cur.state])
            ##print("s = ", s)
            if algo == "BFS":
                if st['to'] not in s and st['to'] not in e:
                    open_lst.append(node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, 0))
            elif algo == "DFS":
                if st['to'] not in s and st['to'] not in e:        
                    open_lst.insert(i,node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, 0))
                    ##print(i, st['to'])
                    i += 1
            elif algo == "UCS":
                #child state is equal to st['to']
                if st['to'] not in s and st['to'] not in e:
                    open_lst.append(node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, 0))
                elif st['to'] in s:
                    i = s.index(st['to'])
                    cst = open_lst[i].cost
                    if st['cost']+ cur.cost < cst:
                        open_lst.pop(i)
                        open_lst.append(node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, 0))
                elif st['to'] in e:
                    i = e.index(st['to'])
                    cst = explored_lst[i].cost
                    if st['cost'] + cur.cost < cst:
                        explored_lst.pop(i)
                        open_lst.append(node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, 0))

            if algo == "A*":
                if st['to'] not in s and st['to'] not in e:
                    open_lst.append(node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, sun[st['to']]['cost'] + st['cost'] + cur.cost))
                elif st['to'] in s:
                    i = s.index(st['to'])
                    cst = open_lst[i].heu_cost
                    if st['cost'] + cur.cost + sun[st['to']]['cost'] < cst:
                        open_lst.pop(i)
                        open_lst.append(node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, sun[st['to']]['cost'] + st['cost'] + cur.cost))
                elif st['to'] in e:
                    i = e.index(st['to'])
                    cst = explored_lst[i].heu_cost
                    if st['cost'] + cur.cost + sun[st['to']]['cost'] < cst:
                        explored_lst.pop(i)
                        open_lst.append(node(st['id'], st['to'], cur.state, 1 + cur.depth, st['cost'] + cur.cost, sun[st['to']]['cost'] + st['cost'] + cur.cost))
                        
##        for elem in open_lst:
##            print(elem)
        explored_lst.append(cur)
        if algo == "UCS":
            open_lst = sorted(open_lst, key=attrgetter('cost'))
        if algo == "A*":
            open_lst = sorted(open_lst, key=attrgetter('heu_cost'))
    result = trace(start, goal, explored_lst, algo)
    return result
                
def make_list(open_lst):
    s = []
    for n in open_lst:
        s.append(n.state)
    return s

def trace(start, goal, explored_lst, algo):
##    for elem in explored_lst:
##        print(elem)
    s = make_list(explored_lst)
    i = s.index(goal)
    par = explored_lst[i].parent
    result = []
    if algo in ["BFS","DFS"]:
        result.append([explored_lst[i].state,explored_lst[i].depth])
    elif algo in ["UCS","A*"]:
        result.append([explored_lst[i].state,explored_lst[i].cost])
    while par != None:
        i = s.index(par)
        par = explored_lst[i].parent
        if algo in ["BFS","DFS"]:
            result.append([explored_lst[i].state,explored_lst[i].depth])
        elif algo in ["UCS","A*"]:
            result.append([explored_lst[i].state,explored_lst[i].cost])
    return result

def write_out(result):
    f = open("output.txt","w")
    reversed_lists = result[::-1]
    s = '' 
    for elem in reversed_lists:
        s += elem[0] + " " + str(elem[1])+"\n"
    f.write(s.strip())
    f.close()

if __name__ == "__main__":
    navigate()
