from humanid import HumanId
hid = HumanId()
size = 1000000

def pct(l):
    return 100 * (float(len(set(l))) / float(len(l)))

for f in [hid.rpg_item, hid.band_name, hid.any_id]:
    items = [f('') for i in xrange(size)]
    print("{}: {}".format(f.__name__, pct(items)))

