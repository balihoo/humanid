import random

class HumanId(object):
    def __init__(self):
        def read_list(name):
            with open("data/" + name) as f:
                return f.read().splitlines()

        self.adjectives = read_list('adjectives')
        self.nouns = read_list('nouns')
        ofstuff_files =['ity', 'ence', 'ance', 'ment', 'tent', 'ncy', 'ness']
        self.ofstuff = sum([read_list(l) for l in ofstuff_files], [])

    def _pluralize(self, noun):
        if len(noun) > 1:
            if noun[-1] == 's':
                return noun
            if noun[-1] == 'h':
                return noun + 'es'
            if noun[-1] == 'y':
                if noun[-2] not in "aeoui":
                    return noun[:-1] + 'ies'
        return noun + 's'

    def rpg_item(self, separator='_'):
        return separator.join([
            random.choice(self.adjectives),
            random.choice(self.nouns),
            'of',
            random.choice(self.ofstuff)
        ]).replace('-', separator)

    def band_name(self, separator='_'):
        return separator.join([
            random.choice(self.nouns),
            'and', 'the',
            random.choice(self.adjectives),
            self._pluralize(random.choice(self.nouns))
        ]).replace('-', separator)

    def any_id(self, separator=None):
        return random.choice([
            self.rpg_item,
            self.band_name
        ])(separator)

if __name__ == "__main__":
    hid = HumanId()
    for i in range(100):
        print(hid.any_id(' '))


