import logging
import os
import re
from collections import Counter
from typing import List, Optional, Set, Iterable

_logger = logging.getLogger(__name__)

_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'content.txt')


def load(filename: str) -> Optional[str]:
    try:
        with open(filename, 'r') as file:
            return file.read()

    except Exception as e:
        _logger.warning(str(e))

    return None


def parse(content: str) -> List[str]:
    if not content:
        return []

    return re.findall(r'[a-z]+[\'-][a-z]+[\'-][a-z]+|'
                      r'[a-z]+[\'-][a-z]+|'
                      r'[a-z]+|'
                      r'\d+,\d{3},\d{3},\d{3}\.\d+|'
                      r'\d+,\d{3},\d{3},\d{3}th|'
                      r'\d+,\d{3},\d{3},\d{3}|'
                      r'\d+,\d{3},\d{3}\.\d+|'
                      r'\d+,\d{3},\d{3}th|'
                      r'\d+,\d{3},\d{3}|'
                      r'\d+,\d{3}\.\d+|'
                      r'\d+,\d{3}th|'
                      r'\d+,\d{3}|'
                      r'\d+\.\d+|'
                      r'\d+th|'
                      r'\d+|'
                      r'1st|2nd|3rd', content.lower())


class Corrector:

    def __init__(self, words: List[str]):
        self._counter = Counter(words)
        self._count = len(words)
        self._size = len(self._counter)

    @property
    def count(self) -> int:
        return self._count

    @property
    def size(self) -> int:
        return self._size

    def get_valid(self, words: Iterable[str]) -> Set[str]:
        if not words:
            return set()

        return {word for word in words if word in self._counter}


    def p(self, word: str) -> float:
        if not words or not self._count:
            return 0

        return self._counter[word] / self._count

    def find_candidates(self, word: str) -> Set[str]:
        pass


if __name__ == '__main__':
    content = load(_filename)
    if content:
        words = parse(content)

        counter = Counter(words)
        print(len(counter))
        print(len(words))
        print(counter.most_common(5))

        print(max(counter.items(), key=lambda x: x[1])[0])

        print(counter['the'] / len(words))
        print(counter['outrivaled'] / len(words))
        print(counter['unmentioned'] / len(words))

        print({'the', 'outrivaled', 'unmentioned'} & set(counter))

        # print(*words, sep='\n')
        # print()
        # print('>>>', len(words))
