Terrible Python Code for enumerating and deciding pebble automata.

BBChallenge wiki: https://wiki.bbchallenge.org/wiki/Pebble_Automaton

Directions:
- Both Python files contain the line `n = 7`. Make sure to change both of them if you want to search a different number of pebbles.
- `pebblesim.py` enumerates the machines, applies the filters for (translated) cyclers and escaping lightspeed ships, and puts the results into a file called `holdouts100stepsp{n}.txt`.
- `pebbleshipdecider.py` reads the machines from that file, applies the "no collisions" decider, and puts the results into a file called `holdouts2p{n}.txt`.
