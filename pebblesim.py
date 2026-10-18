import itertools as it

def transitions(n):
    for l in range(n+1):
        for r in range(n-l+1):
            yield (l, n-l-r, r)

def mirror(a):
    return tuple(t[::-1] for t in a)

def automata(n):
    for a in it.product(((0,0,0),), *[transitions(k) for k in range(1,n+1)]):
        if a <= mirror(a): yield a

def stringify(a):
    return '_'.join(f'{t[0]}{t[2]}' for t in a[1:])

def normalize(board):
    first = next(i for i in range(len(board)) if board[i] != 0)
    last  = next(i for i in range(len(board) - 1, -1, -1) if board[i] != 0)
    return tuple(board[first:last+1])

def canHalt(a):
    # Very simple filter: if the automaton has no 00 rule, it can't halt
    return any(t[0] == t[2] == 0 for t in a[1:])

def simulate(automaton, n_pebbles):
    board = [0] * 201
    board[100] = n_pebbles
    seen = set()
    for t in range(100):
        next_board = [0] * 201
        for x in range(1, 200):
            next_board[x-1] += automaton[board[x]][0]
            next_board[x]   += automaton[board[x]][1]
            next_board[x+1] += automaton[board[x]][2]
        if board == next_board:
            return t
        n = normalize(board)
        seen.add(n)
        if normalize(next_board) in seen: return 'cycler'
        l = n[0]; r = n[-1]
        if automaton[l] == (l,0,0) or automaton[r] == (0,0,r): return 'runaway'
        board = next_board
    return 'undecided'

n = 7
champ = None
champ_runtime = 0
f = open(f'holdouts100stepsp{n}.txt', 'w')
for a in automata(n):
    if not canHalt(a): continue
    r = simulate(a, n)
    if r == 'undecided': f.write(f'{stringify(a)}\n')
    elif type(r) == int and r > champ_runtime:
        champ = a
        champ_runtime = r
f.close()
print(champ, champ_runtime)