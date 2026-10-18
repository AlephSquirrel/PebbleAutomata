import re

EPS = 1e-6

def parse(s):
    m = (0,0,0),
    for i,t in enumerate(s.split('_')):
        l = int(t[0])
        r = int(t[1])
        m += (l,i+1-l-r,r),
    return m

def stringify(a):
    return '_'.join(f'{t[0]}{t[2]}' for t in a[1:])

def normalize(board):
    first = next(i for i in range(len(board)) if board[i] != 0)
    last  = next(i for i in range(len(board) - 1, -1, -1) if board[i] != 0)
    return (tuple(board[first:last+1]), first, last)

def separate_objs(board):
    s = ''.join(map(str, board))
    result = []
    for mat in re.finditer(r'[1-9](0?[1-9])*', s):
        result.append((tuple(map(int, mat.group())), mat.start(), mat.end() - 1))
    return result
    # return [tuple(map(int, obj)) for obj in re.split(r'00+', s) if obj != '']

def envelope(obj, automaton):
    board = [0] * 10 + [*obj] + [0] * 10
    firsts = []
    lasts = []
    for t in range(10):
        next_board = [0] * len(board)
        for x in range(1, len(board) - 1):
            next_board[x-1] += automaton[board[x]][0]
            next_board[x]   += automaton[board[x]][1]
            next_board[x+1] += automaton[board[x]][2]
        board = next_board
        normed_board, first, last = normalize(board)
        firsts.append(first)
        lasts.append(last)
        if normed_board == obj:
            start_pos = 10
            end_pos = first
            speed = (end_pos - start_pos) / (t + 1)
            return (speed, start_pos - min(firsts[i] - speed * (i+1) for i in range(t+1)), max(lasts[i] - speed * (i+1) for i in range(t+1)) - (start_pos + len(obj) - 1))
    return (None, None, None)

def simulate(automaton, n_pebbles):
    board = [0] * 199
    board[99] = n_pebbles
    for t in range(99):
        next_board = [0] * 199
        for x in range(1, 198):
            next_board[x-1] += automaton[board[x]][0]
            next_board[x]   += automaton[board[x]][1]
            next_board[x+1] += automaton[board[x]][2]
        board = next_board
    return board

n = 7
f = open(f'holdouts100stepsp{n}.txt', 'r')
f_out = open(f'holdouts2p{n}.txt', 'w')
count = 0
for line in f.readlines():
    m = parse(line.rstrip())
    board = simulate(m, n)
    objs = separate_objs(board)
    envs = [envelope(obj[0], m) for obj in objs]
    speeds = [e[0] for e in envs]
    if None in speeds:
        result = 'undecided (non-ship)'
    elif (speeds != sorted(speeds)) or any(objs[i][2] + envs[i][2] > objs[i+1][1] - envs[i+1][1] - EPS for i in range(len(objs) - 1)):
        result = 'undecided (collision)'
    else:
        result = 'safe'
    # print(m, objs, envs)
    if result != 'safe': count += 1; f_out.write(f'{stringify(m)}\n')
f.close()
f_out.close()
print(f'Done. {count} machines left undecided')