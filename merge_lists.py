import sys

def read_list(name):
    with open(name) as f:
        return [l for l in f.read().splitlines() if len(l) > 2]

print("\n".join(list(set(sum([read_list(l) for l in sys.argv[1:]], [])))))


