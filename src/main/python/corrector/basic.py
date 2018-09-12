import json
import logging
import os
import re
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

    # FIXME Should I keep numbers? I'm not going to change them...
    return re.findall(r'\b[a-z]+[\'-][a-z]+[\'-][a-z]+\b|'
                      r'\b[a-z]+[\'-][a-z]+\b|'
                      r'\b[a-z]+\b', content.lower())


class Model:
    @staticmethod
    def load(filename: str) -> 'Model':
        with open(filename, 'r') as file:
            return Model({int(k) if k.isdigit() else k: v for k, v in json.load(file).items()})

    def __init__(self, data: Union[Iterable, Mapping]):
        self._data = Counter(data)

    def best(self, n: int = 1) -> List[Hashable]:
        return [x[0] for x in self._data.most_common(n)]

    def filter(self, keys: Set[Hashable]) -> Set[Hashable]:
        return keys.intersection(self._data)

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

    model = Model(words)
    model.save('words.json')

    print('Size:', model.size())
    print('Total:', model.total())
    print('Best 5:', model.best(5))
    for key in model.best():
        print('Freq 1st:', model.freq(key))
    print('Prob(the):', model.prob('the'))
    print('Prob(outrivaled):', model.prob('outrivaled'))
    print('Prob(unmentioned):', model.prob('unmentioned'))
    print('Filter(the,outrivaled,unmentioned):', model.filter({'the', 'outrivaled', 'unmentioned'}))
