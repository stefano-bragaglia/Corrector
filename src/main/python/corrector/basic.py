import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Counter, Hashable, Iterable, List, Mapping, Optional, Set, Union

_logger = logging.getLogger(__name__)


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

    return re.findall(r'\w+', content.lower())
    # return re.findall(r'\b[a-z]+[\'-][a-z]+[\'-][a-z]+\b|'
    #                   r'\b[a-z]+[\'-][a-z]+\b|'
    #                   r'\b[a-z]+\b', content.lower())


characters = "abcdefghijklmnopqrstuvwxyz'-"


def edit(word: str) -> Set[str]:
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    result = {lx + rx[1:] for lx, rx in splits if rx}
    result |= {lx + rx[1] + rx[0] + rx[2:] for lx, rx in splits if len(rx) > 1}
    result |= {lx + ch + rx[1:] for lx, rx in splits if rx for ch in characters}
    result |= {lx + ch + rx for lx, rx in splits for ch in characters}

    return result


def get_candidates(word: str, d: int = 2):
    if d <= 0:
        return {word}
    elif d == 1:
        return edit(word)
    elif d == 2:
        return {item for e in edit(word) for item in edit(e)}
    else:
        result = {word}
        for _ in range(d):
            with ThreadPoolExecutor(8) as pool:
                futures = {pool.submit(edit, candidate) for candidate in result}
                result = set()
                for candidate in as_completed(futures):
                    result |= candidate.result()

    return result


def correct(word: str, dictionary: 'Model', errors: 'Model', d: int = 2) -> str:
    best, result = None, None
    for i in range(d):
        candidates = get_candidates(word, d)
        candidates = dictionary.filter(candidates)
        for candidate in candidates:
            # prob = errors.prob(i) * dictionary.prob(candidate)
            prob = dictionary.prob(candidate)
            if best is None or prob > best:
                best, result = prob, candidate

    return result or word


def review(text: str, dictionary: 'Model', errors: 'Model', d: int = 2) -> str:
    return ' '.join([correct(word, dictionary, errors) for word in text.split()])


class Model:
    @staticmethod
    def load(filename: str) -> 'Model':
        with open(filename, 'r') as file:
            return Model({int(k) if k.isdigit() else k: v for k, v in json.load(file).items()})

    def __init__(self, data: Union[Iterable, Mapping]):
        self._data = Counter(data)

    def best(self, n: int = 1) -> List[Hashable]:
        return [x[0] for x in self._data.most_common(n)]

    def filter(self, keys: Iterable[Hashable]) -> Set[Hashable]:
        return set(keys).intersection(self._data)

    def freq(self, key: Hashable) -> int:
        return self._data[key]

    def keys(self) -> Iterable[Hashable]:
        return self._data.keys()

    def prob(self, key: Hashable) -> float:
        return self._data[key] / self.total()

    def save(self, filename: str):
        with open(filename, 'w') as file:
            json.dump({k: v for k, v in self._data.items()}, file, indent=4, sort_keys=True)

    def size(self):
        return len(self._data)

    def subtract(self, data: Union[Iterable, Mapping]):
        self._data.subtract(data)
        self._data = self._data._keep_positive()

    def total(self) -> int:
        return sum(self._data.values())

    def update(self, data: Union[Iterable, Mapping]):
        self._data.update(data)


if __name__ == '__main__':
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'content.txt')
    content = load(filename)
    words = parse(content)

    errors = Model.load('errors.json')

    dictionary = Model(words)
    dictionary.save('words.json')

    print('Size:', dictionary.size())
    print('Total:', dictionary.total())
    print('Best 5:', dictionary.best(5))
    for key in dictionary.best():
        print('Freq 1st:', dictionary.freq(key))
    print('Prob(the):', dictionary.prob('the'))
    print('Prob(outrivaled):', dictionary.prob('outrivaled'))
    print('Prob(unmentioned):', dictionary.prob('unmentioned'))
    print('Filter(the,outrivaled,unmentioned):', dictionary.filter({'the', 'outrivaled', 'unmentioned'}))

    sentence = 'korrectud speling'
    print('|'+ sentence +'|')
    print('Did you mean:', review(sentence, dictionary, errors))
