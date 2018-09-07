import logging
import os
import re
from typing import Counter, Dict, List

from jellyfish import damerau_levenshtein_distance

_folder = os.path.abspath(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)


def do_abodat() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'ABODAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        comment = ''
        for line in lines:
            if line.startswith('$'):
                comment = line[1:]
            else:
                line = line[:-1]
            for block in line.split(','):
                block = block.strip()
                parts = block.split()
                if parts[0] != parts[1]:
                    note = re.search(r'\[.+\]', block)
                    freq = re.search(r'\d+', block)
                    rows.append({
                        'error': parts[0],
                        'correct': parts[1],
                        'note': '' if not note else note.group(0)[1:-1],
                        'freq': '1' if not freq else freq.group(0),
                        'comment': comment.split()[-1],
                        'source': 'abo.dat'
                    })
    finally:
        return rows


def do_appling1() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'APPLING1DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        comment = ''
        for line in lines:
            if line.startswith('$'):
                comment = line[1:]
            else:
                parts = line.split(maxsplit=2)
                if parts[0] != parts[1]:
                    rows.append({
                        'error': parts[0],
                        'correct': parts[1],
                        'note': parts[2],
                        'freq': '1',
                        'comment': comment.split()[-1],
                        'source': 'appling1.dat'
                    })
    finally:
        return rows


def do_appling2() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'APPLING2DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        comment = ''
        for line in lines:
            if line.startswith('$'):
                comment = line[1:]
            else:
                parts = line.split(maxsplit=1)
                if parts[0] != parts[1]:
                    rows.append({
                        'error': parts[0],
                        'correct': parts[1],
                        'note': '',
                        'freq': '1',
                        'comment': comment.split()[-1],
                        'source': 'appling2.dat'
                    })
    finally:
        return rows


def do_bloor() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'BLOORDAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        for line in lines:
            if line[-1] == ']':
                line, note = [part.strip() for part in line.split('[', maxsplit=1)]
            else:
                note = ''
            parts = line.split()
            for i in range(2, len(parts)):
                if parts[i] != parts[0]:
                    rows.append({
                        'error': parts[i],
                        'correct': parts[0],
                        'note': note,
                        'freq': parts[1],
                        'comment': 'Algerian',
                        'source': 'bloor.dat'
                    })
    finally:
        return rows


def do_ches() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'CHESDAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        table = '_ often visited aunt magnificent house opposite gallery remember splendid purple curtains wrote' \
                ' poetry problem understand latest poems wanted laugh pretend really special refreshment there' \
                ' blue juice cake biscuits stomach contented'.split()
        note = ''
        for line in lines:
            if line:
                if line[-1] == '!':
                    line = line[:-1].strip()
                tokens = line.split()
                if tokens[0] != '+':
                    note = tokens[0]
                pos = 1
                while pos < len(tokens):
                    error = tokens[pos + 1]
                    correct = table[int(tokens[pos])]
                    if error not in ['..', correct]:
                        rows.append({
                            'error': error,
                            'correct': correct,
                            'note': note,
                            'freq': '1',
                            'comment': 'British',
                            'source': 'ches.dat'
                        })
                    pos += 2
    finally:
        return rows


if __name__ == '__main__':
    dataset = do_abodat() + do_appling1() + do_appling2() + do_bloor() + do_ches()
    # dataset = do_ches()
    # print(dataset)

    values = [damerau_levenshtein_distance(error, correct)
              for error, correct in {(row['error'], row['correct']) for row in dataset}]

    counter = Counter(values)
    size = sum(counter.values())
    for key in sorted(counter.keys()):
        value = counter[key]
        print('%s | %s - %s' % (key, value, value / size))
