import re
import sys

def file_as_string(f):
    a = ''
    for x in f:
        a += x
    f.seek(0)
    return a

def parse_op(f):
    file_data = f.read()
    lines = file_data.splitlines()
    a = []
    for x in lines:
        if x != '' and x[0] != '/':
            a.append(list(filter(None ,re.split(', |=> |\t| ', x))))
    f.seek(0)
    return a

def find_range(r, p):
    i, b, e = 0, None, None
    for l in p:
        if r in l and b == None:
            b = i
        elif r in l and b != None:
            e = i
        i += 1
    return (b, e)

def find_occur(r, P):
    l, c = [], 0
    for i in P:
        if r in i:
            l.append(c)
        c+=1
    return tuple(l)

def dist(r, P, cl):
    occur = find_occur(r, P)
    for x in occur:
        if x >= cl:
            return x - cl
    return -1

def get_reg(regs, P, cl): # -> (reg name, dist, index in physical tuple)
    i, d, ds = 0, None, []
    for r in regs:
        if r == None:
            return (None, -1, i)
        else:
            d = dist(r, P, cl)
            if d < 0: return (r, d, i)
            else: ds.append((r, d, i))
        i += 1
    return max_dist(ds)

def max_dist(ds):
    m = (0,0, 0)
    for x in ds:
        if x[1] > m[1]:
            m = x
    return m
 
   


def spill(line, pr, p, mem, spills):
    spills.append([line, 'loadI', str(mem), 'r255'])
    spills.append([line, 'store', 'r' + str(pr[2]), 'r255'])
    p.insert(line+pr[1], ['load', 'r255', pr[0]])
    p.insert(line+pr[1], ['loadI', str(mem), 'r255'])


def add_spills(p, spills):
    i, q = 0, []
    for x in p:
        if i in map((lambda x : x[0]), spills):
            for s in filter((lambda x : True if x[0] == i else False), spills):
                q.append(s[1:])
        q.append(x)
        i +=1
    return q

def allocate(p, k):
    regs, line, pr, mem = (k-1)*[None], 0, None, 4
    spills = []
    for i in p:
        for w in enumerate(i):
            if w[1][0] == 'r': # -> w[1] == 'rn' 
                if w[1] not in regs:
                    pr = get_reg(regs, p, line)
                    regs[pr[2]] = i[w[0]]
                    if pr[1] > -1:
                        spill(line, pr, p, mem, spills)
                        mem +=4
                i[w[0]] = 'r' + str(regs.index(i[w[0]]))
        line += 1
    return add_spills(p, spills)

def write_to_file(p, name):
    one, two = ['store', 'load', 'loadI'], ['add', 'mult', 'sub', 'lshift', 'rshift']
    f = open(name, 'w')
    for i in p:
        if i[0] in one:
            i.insert(2, '=>')
        elif i[0] in two:
            i.insert(2, ',')
            i.insert(4, '=>')
        f.write('\t' + ' '.join(i) + '\n')

def main(args):
    f = open(f'testcases/{args[2]}.i', 'r')
    p = parse_op(f)
    q = allocate(p, int(args[1]))
    write_to_file(q, args[3])

if __name__ == '__main__':
    main(sys.argv)
