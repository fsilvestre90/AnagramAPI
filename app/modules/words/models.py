import walrus
from flask_restplus import fields

from app.extensions import redis
from app.extensions.api import api_v1


class BaseModel(walrus.Model):
    __database__ = redis


class Word(BaseModel):
    word = walrus.TextField(primary_key=True)
    palindrome = walrus.BooleanField(index=True)

    def is_palindrome(word):
        """
        Iterate from n to n/2 (up til half of the word).
        Compare the first & last element until failure, if successful
        then we know it's a palindrome

        :return: Bool
        """
        is_palindrome = True
        for i in range(len(word) // 2):
            if word[i] != word[-i - 1]:
                is_palindrome = False
        return is_palindrome

    @classmethod
    def remove(cls, word):
        try:
            Word.load(word).delete()
        except KeyError:
            return

    @classmethod
    def count_palindromes(cls):
        try:
            return sum(1 for i in Word.query(Word.palindrome == True))
        except KeyError:
            return None

    @classmethod
    def count_words(cls):
        return Word.count()

    @classmethod
    def clear_table(cls):
        redis.flushall()


class AnagramKey(BaseModel):
    anagram_hash = walrus.TextField(primary_key=True)
    words = walrus.SetField()

    @classmethod
    def get_anagram(cls, word):
        anagram_hash = ''.join(sorted(word))
        try:
            anagram = AnagramKey.load(anagram_hash)
            return anagram
        except KeyError:
            return None

    def get_words(self):
        if len(self.words.members()) > 0:
            words = []
            for idx in self.words.members():
                # walrus bugs: 1) doesn't convert set obj from byte code so I needed to manually do it
                # 2) there is a python 3 error with walrus where the indices don't update upon deletion
                for filtered_item in idx.translate(None, b'\'{,}').decode().split():
                    try:
                        words.append(Word.load(filtered_item))
                    except KeyError:
                        break
            return words
        else:
            return None

    @classmethod
    def count_anagrams(cls):
        return AnagramKey.count()


AnagramKeyModel = api_v1.model('AnagramKey', {
    'anagram_hash': fields.String(readOnly=True, description='The anagram hash'),
    'items': fields.Raw(Word, description='A list of words associated with the anagram'),
})

WordModel = api_v1.model('Word', {
    'word': fields.String(readOnly=True, description='A word'),
    'is_palindrone': fields.Boolean(readOnly=True, description='Is the word a palindrone'),
})
