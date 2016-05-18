import unittest
import math
from humanid import HumanId

class TestHumanid(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHumanid, self).__init__(*args, **kwargs)
        self.hid = HumanId()

    def test_chunk(self):
        hexin = 'e5dc0c113b1541b4b97a029be34904aa'
        res3 = ['e5dc0c113b1', '541b4b97a02', '9be34904aae']
        res4 = ['e5dc0c11', '3b1541b4', 'b97a029b', 'e34904aa']
        res5 = ['e5dc0c1', '13b1541', 'b4b97a0', '29be349', '04aae5d']
        self.assertEqual(self.hid._chunk(hexin, 3), res3)
        self.assertEqual(self.hid._chunk(hexin, 4), res4)
        self.assertEqual(self.hid._chunk(hexin, 5), res5)
        #hey, works for lists too, but it would pad...
        self.assertEqual(
            self.hid._chunk(range(0,10), 5),
            [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
        )

    def test_indices(self):
        hexin = '03FF20'
        res = list(self.hid._indices(hexin, (10, 300, 30)))
        expected = [
            3, # 0x03 =   3 in range  10
          255, # 0xFF = 255 in range 300
            2  # 0x20 =  32 in range  30: overflow of 2
        ]
        self.assertEqual(res, expected)

    def test_combo_stats(self):
        noun_count = len(self.hid.nouns)
        adj_count = len(self.hid.adjectives)
        stuff_count = len(self.hid.ofstuff)
        print("\n====combination stats====")
        print("nouns: {}".format(noun_count))
        print("adjectives: {}".format(adj_count))
        print("stuff: {}".format(stuff_count))
        rpg_count = noun_count * adj_count * stuff_count
        band_count = noun_count * adj_count * noun_count
        def prob_table(n):
            def prob(k, n):
                return 1.0 - math.exp((-1.0 * k * (k - 1.0)) / (2.0 * n))
            for order in xrange(1,8):
                guesses = 10 ** order
                p = prob(guesses, n)
                print("{:8} ids: {}".format(guesses, p))
        print("rpg item combinations: {:,}".format(rpg_count))
        print("probability for collisions with rpg item:")
        prob_table(rpg_count)
        print("\nband name combinations: {:,}".format(band_count))
        print("probability for collisions with band names:")
        prob_table(band_count)
        self.assertTrue(True)

    def test_words(self):
        hexin = 'e5dc0c113b1541b4b97a029be34904aa'
        lists = (self.hid.nouns, self.hid.adjectives, self.hid.ofstuff)
        (noun, adj, stuff) = self.hid._words(hexin, lists)
        self.assertEqual((noun, adj, stuff), ('norse', 'instructive', 'primality'))
        # now test that not providing a hash does not match
        self.assertNotEqual(
            self.hid._words(None, lists),
            self.hid._words(None, lists)
        )

    def test_pluralize(self):
        self.assertEqual(self.hid._pluralize("dude"), "dudes")
        self.assertEqual(self.hid._pluralize("guy"), "guys")
        self.assertEqual(self.hid._pluralize("party"), "parties")
        self.assertEqual(self.hid._pluralize("dash"), "dashes")
        self.assertEqual(self.hid._pluralize("glass"), "glass")

    def test_rpg_item(self):
        hexin = 'e5dc0c113b1541b4b97a029be34904aa'
        expected = "foregoing##ballpark##of##primality"
        rpg = self.hid.rpg_item(separator='##', hexstr=hexin)
        self.assertEqual(rpg, expected)
        (uuid, rpg) = self.hid.rpg_item(separator='##', hexstr=hexin, return_hash=True)
        self.assertEqual(uuid, hexin)
        (uuid, rpg) = self.hid.rpg_item(separator='##', return_hash=True)
        self.assertNotEqual(uuid, hexin)
        self.assertNotEqual(rpg, expected)

    def test_band_name(self):
        hexin = 'e5dc0c113b1541b4b97a029be34904aa'
        expected = "norse and the instructive wounds"
        band = self.hid.band_name(separator=' ', hexstr=hexin)
        self.assertEqual(band, expected)
        (uuid, band) = self.hid.band_name(separator=' ', hexstr=hexin, return_hash=True)
        self.assertEqual(uuid, hexin)
        (uuid, band) = self.hid.band_name(separator=' ', return_hash=True)
        self.assertNotEqual(uuid, hexin)
        self.assertNotEqual(band, expected)

    def test_any_id(self):
        hexin = 'e5dc0c113b1541b4b97a029be34904aa'
        d = dict(reversed(self.hid.any_id(separator=' ', hexstr=hexin, return_hash=True)) for i in xrange(1000))
        self.assertEqual(len(d.keys()), 2)
        self.assertTrue(all([v == hexin for v in d.values()]))

if __name__ == '__main__':
    unittest.main()
