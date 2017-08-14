import logging
from http import HTTPStatus

from celery import chain
from flask_restplus import Resource
from flask_restplus import reqparse
from app.extensions.api import api_v1
from app.extensions.api.http_exceptions import abort
from app.modules.words.models import AnagramKey, Word

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

anagram_ns = api_v1.namespace('anagrams', description="Anagram operations")  # pylint: disable=invalid-name
words_ns = api_v1.namespace('words', description="Words operations")  # pylint: disable=invalid-name
palindrome_ns = api_v1.namespace('palindromes', description="Palindrome operations")  # pylint: disable=invalid-name


@words_ns.route('/')
class WordsIndex(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('words', action='append')
        args = parser.parse_args()
        words = args['words']
        if words is not None:
            from .tasks import map_anagrams, save_words
            task = chain(save_words.s(words), map_anagrams.s()).apply_async()
            # task = (prep_task.s(words) | dmap.s(process_item.s())).apply_async()
            return {"status": "Thank you for your submission. Processing request - job id {0}.".format(task.id)}, 201
        else:
            abort(HTTPStatus.BAD_REQUEST)

    """
     Clear the database
    """
    def delete(self):
        Word.clear_table()
        return


@words_ns.route('/<string:word>/')
class WordbyId(Resource):
    """
     Delete a word in our database
     """
    def delete(self, word):
        Word.remove(word)
        return


@words_ns.route('/count/')
class WordCount(Resource):
    def get(self):
        """
        Get number of words in our DB
        """
        if Word.count_words() is not None:
            return {"count": Word.count_words()}
        else:
            return {"count": "There was an processing error."}


@palindrome_ns.route('/count/')
class PalindromesCount(Resource):
    def get(self):
        """
        Get number of palindromes in our DB
        """
        return {"count": Word.count_palindromes()}


@anagram_ns.route('/<string:word>/')
class AnagramById(Resource):
    def get(self, word):
        """
        Get an anagram and its words
        """
        if word is None:
            return abort(HTTPStatus.NOT_ACCEPTABLE)
        print(word)
        anagram = AnagramKey.get_anagram(word)
        if anagram is None:
            return {"message": "Sorry, word not found"}, 404
        else:
            return {'anagram': anagram.anagram_hash, 'words': [item.word for item in anagram.get_words()]}


@anagram_ns.route('/count/')
class AnagramsCount(Resource):

    def get(self):
        """
        Get number of anagrams in our DB
        """
        return {"count": AnagramKey.count_anagrams()}
