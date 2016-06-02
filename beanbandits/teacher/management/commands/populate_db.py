from django.core.management.base import BaseCommand
from teacher.models import WordSet, Word
import os
import csv
import codecs

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_characters(self):
        self._most_common()
        self._least_common()
        self._numbers()
        self._animals()
        self._difficult1()
        self._difficult2()

    def _difficult1(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        dataset = current_path + "/../../../../Datasets/difficult1.csv"
        new_word_set = WordSet(name="difficult1", description="difficult characters for advanced and native speakers")
        new_word_set.save()
        with open(dataset, 'rb') as fin:
            rank = 0
            reader = UnicodeReader(fin)
            for line in reader:
                if rank == 0:
                    pass
                else:
                    new_char = Word(word=unicode(line[0].encode("utf-8"), "UTF-8"), definition=line[2], pinyin=line[1], rank=rank, wordset=new_word_set)
                    new_char.save()
                rank += 1

    def _difficult2(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        dataset = current_path + "/../../../../Datasets/difficult2.csv"
        new_word_set = WordSet(name="difficult2", description="difficult characters for advanced and native speakers")
        new_word_set.save()
        with open(dataset, 'rb') as fin:
            rank = 0
            reader = UnicodeReader(fin)
            for line in reader:
                if rank == 0:
                    pass
                else:
                    new_char = Word(word=unicode(line[0].encode("utf-8"), "UTF-8"), definition=line[2], pinyin=line[1], rank=rank, wordset=new_word_set)
                    new_char.save()
                rank += 1

    def _animals(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        dataset = current_path + "/../../../../Datasets/animals.csv"
        new_word_set = WordSet(name="animals", description="animals")
        new_word_set.save()
        with open(dataset, 'rb') as fin:
            rank = 0
            reader = UnicodeReader(fin)
            for line in reader:
                if rank == 0:
                    pass
                else:
                    new_char = Word(word=unicode(line[0].encode("utf-8"), "UTF-8"), definition=line[2], pinyin=line[1], rank=rank, wordset=new_word_set)
                    new_char.save()
                rank += 1

    def _numbers(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        dataset = current_path + "/../../../../Datasets/numbers.csv"
        new_word_set = WordSet(name="numbers", description="1-10")
        new_word_set.save()
        with open(dataset, 'rb') as fin:
            rank = 0
            reader = UnicodeReader(fin)
            for line in reader:
                if rank == 0:
                    pass
                elif rank == 11:
                    break
                else:
                    new_char = Word(word=unicode(line[0].encode("utf-8"), "UTF-8"), definition=line[2], pinyin=line[1], rank=rank, wordset=new_word_set)
                    new_char.save()
                rank += 1

    def _least_common(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        dataset = current_path + "/../../../../Datasets/dataset.csv"
        new_word_set = WordSet(name="intermediate", description="990th most common characters")
        new_word_set.save()
        with open(dataset, 'rb') as fin:
            rank = 0
            reader = UnicodeReader(fin)
            for line in reader:
                if rank < 982:
                    pass
                else:
                    new_char = Word(word=unicode(line[0].encode("utf-8"), "UTF-8"), definition=line[2], pinyin=line[1], rank=rank, wordset=new_word_set)
                    new_char.save()
                rank += 1

    def _most_common(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        dataset = current_path + "/../../../../Datasets/dataset.csv"
        new_word_set = WordSet(name="most common", description="top 10 most common characters")
        new_word_set.save()
        with open(dataset, 'rb') as fin:
            rank = 0
            reader = UnicodeReader(fin)
            for line in reader:
                if rank == 0:
                    pass
                elif rank == 11:
                    break
                else:
                    new_char = Word(word=unicode(line[0].encode("utf-8"), "UTF-8"), definition=line[2], pinyin=line[1], rank=rank, wordset=new_word_set)
                    new_char.save()
                rank += 1

    def handle(self, *args, **options):
        Word.objects.all().delete()
        WordSet.objects.all().delete()
        self._create_characters()
