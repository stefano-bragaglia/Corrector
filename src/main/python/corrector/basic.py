import json
import logging
import os
import re
from collections import Counter
from typing import Dict, Hashable, Iterable, List, Optional, Set, Tuple

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


def crunch(words: List[str]) -> Dict[str, float]:
    counter = Counter(words)
    size = sum(counter.values())

    return {k: v / size for k, v in counter.items()}


class Corrector:
    _characters = "abcdefghijklmnopqrstuvwxyz-' "
    _priors = {
        0: 0.975,
        1: 0.4090437264824186,
        2: 0.2458479304528351,
        3: 0.15421045802517191,
        4: 0.08823147787725444,
        5: 0.047878551965745426,
        6: 0.023744647722849357,
        7: 0.01320228363825094,
        8: 0.006811989100817439,
        9: 0.0035033086804203972,
        10: 0.0024004152069547163,
        11: 0.0011028934734656805,
        12: 0.0011677695601401323,
        13: 0.0006163228234072921,
        14: 0.0006811989100817438,
        15: 0.0004216945633839367,
        16: 0.0002595043466978072,
        17: 0.0002919423900350331,
        18: 9.731413001167769e-05,
        19: 0.0001621902166861295,
        20: 6.48760866744518e-05,
        21: 6.48760866744518e-05,
        22: 3.24380433372259e-05,
        31: 3.24380433372259e-05,
        32: 6.48760866744518e-05,
        37: 3.24380433372259e-05,
        54: 3.24380433372259e-05
    }

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

    def find_candidates(self, word: str, distance: int = 3) -> Set[str]:

        candidates = {word: 0.95 * self._counter[word] / self._count}
        for i in range(distance):
            results = dict(candidates)
            for candidate in candidates:
                results.update(self.edit(candidate))
            candidates = results

        return {candidate for candidate in candidates if candidate in self._counter}

    def edit(self, word: str) -> Set[str]:
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        results = {lx + rx[1:] for lx, rx in splits if rx}
        results |= {lx + rx[1] + rx[0] + rx[2:] for lx, rx in splits if len(rx) > 1}
        results |= {lx + ch + rx[1:] for lx, rx in splits if rx for ch in self._characters}
        results |= {lx + ch + rx for lx, rx in splits for ch in self._characters}

        return results


class Model:
    @staticmethod
    def load(filename: str) -> 'Model':
        with open(filename, 'r') as file:
            table = {}
            for key, value in json.load(file).items():
                if key.isdigit():
                    key = int(key)
                table[key] = value

            return Model(table)

    def __init__(self, data: Dict[Hashable, float]):
        self._data = Counter(data)

    def best(self, n: int = 1) -> List[Tuple[Hashable, float]]:
        return self._data.most_common(n)

    def get(self, key) -> float:
        return self._data[key]

    def save(self, filename: str):
        with open(filename, 'w') as file:
            json.dump({k: v for k, v in self._data.items()}, file, indent=4, sort_keys=True)


if __name__ == '__main__':
    content = load(_filename)
    if content:
        words = parse(content)
        # data = crunch(words)
        # model = Model(data)

        counter = Counter(words)

        print(len(counter))
        print(len(words))
        print(counter.most_common(5))

        print(max(counter.items(), key=lambda x: x[1])[0])

        print(counter['the'] / len(words))
        print(counter['outrivaled'] / len(words))
        print(counter['unmentioned'] / len(words))

        print({'the', 'outrivaled', 'unmentioned'} & set(counter))

        # corrector = Corrector(words)
        # print(corrector.find_candidates('word'))

        # print(*words, sep='\n')
        # print()
        # print('>>>', len(words))
