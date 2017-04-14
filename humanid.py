import random
import uuid
import math
import os
import re
import sys


class HumanId(object):
    def __init__(self):
        """ create easy to remember, readable ids at random or based on a uuid """
        datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

        def read_list(name):
            with open(os.path.join(datadir, name)) as f:
                return f.read().splitlines()

        self.adjectives = sorted(read_list('adjectives'))
        self.nouns = sorted(read_list('nouns'))
        self.verbs = sorted(read_list('action_verbs'))
        ofstuff_files = ['ity', 'ence', 'ance', 'ment', 'tent', 'ncy', 'ness']
        self.ofstuff = sorted(sum([read_list(l) for l in ofstuff_files], []))
        self._rx_non_letter = re.compile('([^a-zA-Z])')
        self.rap_titles = ['lil', 'big', 'mc', 'dj', 'dr', 'young', 'notorious', 'phat', 'slim', 'tha']

    def _chunk(self, hexstr, count):
        """ chunk a string into 'count' equal parts, padding if necessary """
        l = len(hexstr)
        m = l % count
        # number of characters in chunk
        n = int(math.ceil(float(l) / count))
        # make string fitting len by appending the front
        hexstr += hexstr[0:n - m]
        # divide the string in equal chunks
        chunks = [hexstr[i:i+n] for i in range(0, l, n)]
        return chunks

    def _indices(self, hexstr, lengths):
        """ generate a set of numbers 0-len for each length, based on a hex string """
        chunks = self._chunk(hexstr, len(lengths))
        return (int(t[0], 16) % t[1] for t in zip(chunks, lengths))

    def _words(self, hexstr, lists):
        """ picks a set of words from the lists, optionally based on a hex string """
        if hexstr is None:
            # significantly faster than creating and processing a uuid
            return (random.choice(l) for l in lists)
        idxs = self._indices(hexstr, [len(l) for l in lists])
        return (l[i] for l, i in zip(lists, idxs))

    def _mksub(self, token):
        """ shorthand maker """
        def sub(s):
            return self._rx_non_letter.sub(token, s)
        return sub

    def _pluralize(self, noun):
        """ do a poor job of pluralizing a noun """
        if len(noun) > 1:
            if noun.endswith('s'):
                return noun
            if any(noun.endswith(s) for s in ['sh', 'x', 'o', 'ch']):
                return noun + 'es'
            if noun.endswith('y'):
                if noun[-2] not in "aeoui":
                    return noun[:-1] + 'ies'
        return noun + 's'

    def _rapify(self, word):
        """ drop g's because 'real g's move in silence like lasagna'. Also turn -er words in to -ah words. """
        if len(word) > 4:
            if word.endswith('ing'):
                return word[:-1]
            elif word.endswith('er'):
                return word[:-2] + 'ah'
        return word

    def rpg_item(self, separator='_', hexstr=None, return_hash=False):
        """ create an id in the form of an item from a Role Playing Game:
        e.g. sick_gear_of_elegance """
        if return_hash and hexstr is None:
            hexstr = uuid.uuid4().hex
        sub = self._mksub(separator)
        (adj, noun, stuff) = self._words(hexstr, (self.adjectives, self.nouns, self.ofstuff))
        humid = separator.join([sub(word) for word in [adj, noun, 'of', stuff]])
        return humid if not return_hash else (hexstr, humid)

    def band_name(self, separator='_', hexstr=None, return_hash=False):
        """ create an id in the form of a band name: surprise_and_the_anxious_toys"""
        if return_hash and hexstr is None:
            hexstr = uuid.uuid4().hex
        sub = self._mksub(separator)
        (lead, adj, band) = self._words(hexstr, (self.nouns, self.adjectives, self.nouns))
        humid = separator.join([sub(word) for word in [lead, 'and', 'the', adj, self._pluralize(band)]])
        return humid if not return_hash else (hexstr, humid)

    def rap_name(self, separator='_', hexstr=None, return_hash=False):
        """ create an id in the form of a rap name: dj_exclusive_trousers_feat_tha_junk"""
        if return_hash and hexstr is None:
            hexstr = uuid.uuid4().hex
        sub = self._mksub(separator)

        (title1, adj, noun, title2, feature) = self._words(hexstr, (self.rap_titles, self.adjectives, self.nouns, self.rap_titles, self.nouns))
        humid = separator.join([sub(word) for word in [
            title1, self._rapify(adj), self._rapify(noun),
            'feat', title2, self._rapify(feature)
        ]])
        return humid if not return_hash else (hexstr, humid)

    def dadism(self, separator='_', hexstr=None, return_hash=False):
        """create an id like a dad: money does not grow on trees"""
        if return_hash and hexstr is None:
            hexstr = uuid.uuid4().hex
        sub = self._mksub(separator)

        (noun, action, plural_noun) = self._words(hexstr, (self.nouns, self.verbs, self.nouns))
        does = 'does'
        if noun.endswith('s') and not noun.endswith('ss'):  # bad plural check
            does = 'do'
        humid = separator.join([noun, does, 'not', action, 'on', self._pluralize(plural_noun)])
        return humid if not return_hash else (hexstr, humid)

    def any_id(self, *args, **kwargs):
        """ create either a band name of an rpg item id """
        return random.choice([
            self.rpg_item,
            self.band_name,
            self.rap_name,
            self.dadism
        ])(*args, **kwargs)


if __name__ == "__main__":
    hid = HumanId()
    uid = uuid.uuid4().hex
    print(hid.rpg_item(hexstr=uid))
    print(hid.rpg_item(hexstr=uid))
    print(hid.band_name(hexstr=uid))
    print(hid.band_name(hexstr=uid))
    print(hid.rap_name(hexstr=uid))
    print(hid.rap_name(hexstr=uid))
    print(hid.dadism(hexstr=uid))
    print(hid.dadism(hexstr=uid))
    print(hid.rpg_item())
    print(hid.band_name())
    print(hid.rap_name())
    print(hid.dadism())
