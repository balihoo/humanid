import random
import uuid
import math

class HumanId(object):
    def __init__(self):
        """ create easy to remember, readable ids at random or based on a uuid """
        def read_list(name):
            with open("data/" + name) as f:
                return f.read().splitlines()

        self.adjectives = sorted(read_list('adjectives'))
        self.nouns = sorted(read_list('nouns'))
        ofstuff_files =['ity', 'ence', 'ance', 'ment', 'tent', 'ncy', 'ness']
        self.ofstuff = sorted(sum([read_list(l) for l in ofstuff_files], []))

    def _chunk(self, hexstr, count):
        """ chunk a string into 'count' equal parts, padding if necessary """
        l = len(hexstr)
        m = l % count
        #number of characters in chunk
        n = int(math.ceil(float(l) / count))
        #make string fitting len by appending the front
        hexstr += hexstr[0:n - m]
        #divide the string in equal chunks
        chunks = [hexstr[i:i+n] for i in xrange(0, l, n)]
        return chunks

    def _indices(self, hexstr, lengths):
        """ generate a set of numbers 0-len for each length, based on a hex string """
        chunks = self._chunk(hexstr, len(lengths))
        return (int(t[0], 16) % t[1] for t in zip(chunks, lengths))

    def _words(self, hexstr, lists):
        """ picks a set of words from the lists, optionally based on a hex string """
        if hexstr is None:
            #significantly faster than creating and processing a uuid
            return (random.choice(l) for l in lists)
        idxs = self._indices(hexstr, [len(l) for l in lists])
        return (l[i] for l,i in zip(lists, idxs))

    def _pluralize(self, noun):
        """ do a poor job of pluralizing a noun """
        if len(noun) > 1:
            if noun.endswith('s'):
                return noun
            if noun.endswith('sh'):
                return noun + 'es'
            if noun.endswith('y'):
                if noun[-2] not in "aeoui":
                    return noun[:-1] + 'ies'
        return noun + 's'

    def rpg_item(self, separator='_', hexstr=None, return_hash=False):
        """ create an id in the form of an item from a Role Playing Game:
        e.g. sick_gear_of_elegance """
        if return_hash and hexstr is None:
            hexstr = uuid.uuid4().get_hex()
        (adj, noun, stuff) = self._words(hexstr, (self.adjectives, self.nouns, self.ofstuff))
        humid = separator.join([
            adj, noun, 'of', stuff
        ]).replace('-', separator)
        return humid if not return_hash else (hexstr, humid)

    def band_name(self, separator='_', hexstr=None, return_hash=False):
        """ create an id in the form of a band name: surprise_and_the_anxious_toys"""
        if return_hash and hexstr is None:
            hexstr = uuid.uuid4().get_hex()
        (lead, adj, band) = self._words(hexstr, (self.nouns, self.adjectives, self.nouns))
        humid = separator.join([
            lead, 'and', 'the', adj, self._pluralize(band)
        ]).replace('-', separator)
        return humid if not return_hash else (hexstr, humid)

    def any_id(self, *args, **kwargs):
        """ create either a band name of an rpg item id """
        return random.choice([
            self.rpg_item,
            self.band_name
        ])(*args, **kwargs)

if __name__ == "__main__":
    hid = HumanId()
    uid = uuid.uuid4().get_hex()
    print(hid.rpg_item(hexstr=uid))
    print(hid.rpg_item(hexstr=uid))
    print(hid.band_name(hexstr=uid))
    print(hid.band_name(hexstr=uid))
    print(hid.rpg_item())
    print(hid.band_name())


