import csv
import random

class TilePool(object):

    def __init__(self):
        self.tile_data = self.set_tile_data()
        self.tile_keys = self.tile_data.keys()

    def set_tile_data(self):
        tile_data = {}
        sum_of_letters = 0
        with open("tiles.txt", "rb") as file_obj:
            try:
                data = file_obj.readline()
                while not data == "":
                    letters_list = [l for l in data][:-1]
                    sum_of_letters += len(letters_list)
                    tile_data[data[0]] = letters_list
                    data = file_obj.readline()
            except:
                pass
        print sum_of_letters
        return tile_data

    def __len__(self):
        tile_pool = filter(lambda x: len(self.tile_data[x]), self.tile_keys)
        return len(tile_pool)

    def pop(self, tile_count=7):
        letters = []
        if tile_count > 7:
            tile_count = 7
        while not tile_count == 0 and self.tile_keys:
            random_tile = random.choice(self.tile_keys)
            random_tile_data = self.tile_data[random_tile]
            if random_tile_data:
                letters.append(random_tile_data.pop())
                tile_count -= 1
            else:
                self.tile_keys.remove(random_tile)
        return letters

    def get_letters(self, tile_count):
        if tile_count == 0:
            return
        random_tile = random.choice(self.tile_keys)
        random_tile_data = self.tile_data[random_tile]
        if random_tile_data:
            tile_count -= 1
            return random_tile_data.pop()
        else:
            self.tile_keys.remove(random_tile)
            return self.get_letters(tile_count)

class WordFinder(object):
    def __init__(self):
        csv_file = open("tiles.csv", "rb")
        csv_reader = csv.reader(csv_file, delimiter=",")
        self.score_data = {row[0]: row[1:] for row in csv_reader}

    def get_word_list_by_tile_count(self, tile_letters, cross_letter):
        tile_count = len(tile_letters)
        word_list = []
        with open("word_dictionary.txt", "rb") as wd:
            word = wd.readline().rstrip("\r\n")
            while not word == "":
                if len(word) <= tile_count:
                    i, letter_scores = 0, []
                    letter_dict = {}
                    for letter in word:
                        if not letter in tile_letters:
                            break
                        if letter not in letter_dict:
                            letter_dict[letter] = 1
                        else:
                            letter_dict[letter] += 1
                        if letter_dict[letter] >= tile_letters.count(letter):
                            break
                        letter_scores.append(self.get_letter_score(letter))
                        i += 1
                    if i == len(word):
                        word_list.append((word,sum(letter_scores)))
                word = wd.readline().rstrip("\r\n")
        return word_list

    def list_words(self, letters, cross_letter=None):
        word_list = self.get_word_list_by_tile_count(letters, cross_letter)
        return sorted(word_list, key=lambda x: x[1])[::-1]

    def get_letter_score(self, letter):
        if self.score_data[letter][0]:
            return int(self.score_data[letter][0])
        return 0

import sys

cross_letters = [chr(x) for x in xrange(97, 123)]
cross_letters.insert(0, None) # the first word will not have a cross letter

def main():
    tile_pool = TilePool()
    word_finder = WordFinder()
    while len(tile_pool):
        letters = tile_pool.pop(3)
        list_words = word_finder.list_words(letters)
        print "Word Count {} and Letter Tiles {}.".format(len(list_words), letters)
        # for cross_letter in cross_letters:
        for word, score in list_words:
            print word, score

if __name__=='__main__':
    main()
    sys.exit(0)
