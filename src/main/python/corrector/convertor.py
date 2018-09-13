import logging
import os
import re
from typing import Dict, List

from jellyfish import damerau_levenshtein_distance

from src.main.python.corrector.basic import Model

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
                        'error': re.sub(r'_', ' ', parts[0]),
                        'correct': re.sub(r'_', ' ', parts[1]),
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
                        'error': re.sub(r'_', ' ', parts[0]),
                        'correct': re.sub(r'_', ' ', parts[1]),
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
                        'error': re.sub(r'_', ' ', parts[0]),
                        'correct': re.sub(r'_', ' ', parts[1]),
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
                        'error': re.sub(r'_', ' ', parts[i]),
                        'correct': re.sub(r'_', ' ', parts[0]),
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
        table = {
            '1': 'often',
            '2': 'visited',
            '3': 'aunt',
            '4': 'magnificent',
            '5': 'house',
            '6': 'opposite',
            '7': 'gallery',
            '8': 'remember',
            '9': 'splendid',
            '10': 'purple',
            '11': 'curtains',
            '12': 'wrote',
            '13': 'poetry',
            '14': 'problem',
            '15': 'understand',
            '16': 'latest',
            '17': 'poems',
            '18': 'wanted',
            '19': 'laugh',
            '20': 'pretend',
            '21': 'really',
            '22': 'special',
            '23': 'refreshment',
            '24': 'there',
            '25': 'blue',
            '26': 'juice',
            '27': 'cake',
            '28': 'biscuits',
            '29': 'stomach',
            '30': 'contented'
        }
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
                    correct = table[tokens[pos]]
                    if error not in ['..', correct]:
                        rows.append({
                            'error': re.sub(r'_', ' ', error),
                            'correct': re.sub(r'_', ' ', correct),
                            'note': note,
                            'freq': '1',
                            'comment': 'British',
                            'source': 'ches.dat'
                        })
                    pos += 2
    finally:
        return rows


def do_exams() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'EXAMSDAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        comment = ''
        for line in lines:
            if line:
                if line.startswith('$'):
                    comment = line[1:].title()
                elif line[0] in '1234567890' or line in ['-', 'I']:
                    continue
                else:
                    note, freq = '', 1
                    if len(line.split()) > 2:
                        error, correct, block = line.split(maxsplit=2)
                        if len(block.split()) > 1 and block[0] in '1234567890':
                            freq, note = block.split(maxsplit=1)
                        elif block[0] in '1234567890':
                            freq = block
                        else:
                            note = block
                        if note.startswith('[') and note.endswith(']'):
                            note = note[1:-1].strip()
                        if correct == '00' and note.startswith('"') and note.endswith('"'):
                            correct = note[1:-1].strip()
                            note = ''
                    else:
                        error, correct = line.split()
                    if error in ['?', correct]:
                        continue
                    if error.startswith('?'):
                        error = error[1:].strip()
                    rows.append({
                        'error': re.sub(r'_', ' ', error),
                        'correct': re.sub(r'_', ' ', correct),
                        'note': note,
                        'freq': freq,
                        'comment': comment,
                        'source': 'exams.dat'
                    })
    finally:
        return rows


def do_fawthrop1() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'FAWTHROP1DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        for line in lines:
            if line:
                correct, error = line.lower().split()
                if error != correct:
                    rows.append({
                        'error': re.sub(r'_', ' ', error),
                        'correct': re.sub(r'_', ' ', correct),
                        'note': '',
                        'freq': 1,
                        'comment': '',
                        'source': 'fawthrop1.dat'
                    })
    finally:
        return rows


def do_fawthrop2() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'FAWTHROP2DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        for line in lines:
            if line:
                correct, error, freq = line.lower().split()
                if error != correct:
                    rows.append({
                        'error': re.sub(r'_', ' ', error),
                        'correct': re.sub(r'_', ' ', correct),
                        'note': '',
                        'freq': freq,
                        'comment': '',
                        'source': 'fawthrop2.dat'
                    })
    finally:
        return rows


def do_sheffield() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'SHEFFIELDDAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        for line in lines:
            if line:
                correct, error = line.lower().split()
                if error != correct:
                    rows.append({
                        'error': re.sub(r'_', ' ', error),
                        'correct': re.sub(r'_', ' ', correct),
                        'note': '',
                        'freq': 1,
                        'comment': '',
                        'source': 'sheffield.dat'
                    })
    finally:
        return rows


def do_gates() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'GATESDAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        for line in lines:
            if line:
                pos = 1
                tokens = line.split()
                while pos < len(tokens):
                    if tokens[pos][0] != '$':
                        error = tokens[pos][1:]
                        if error != tokens[0]:
                            rows.append({
                                'error': re.sub(r'_', ' ', error),
                                'correct': re.sub(r'_', ' ', tokens[0]),
                                'note': '',
                                'freq': tokens[pos + 1],
                                'comment': 'American',
                                'source': 'gates.dat'
                            })
                    pos += 2
    finally:
        return rows


def do_masters() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'MASTERSDAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        correct, comment = '', ''
        for line in lines:
            if line:
                if line.startswith('$'):
                    correct, comment = line[1:].lower().split(maxsplit=1)
                else:
                    error, note = line.lower().split(maxsplit=1)
                    if error != correct:
                        rows.append({
                            'error': re.sub(r'_', ' ', error),
                            'correct': re.sub(r'_', ' ', correct),
                            'note': note,
                            'freq': 1,
                            'comment': comment,
                            'source': 'masters.dat'
                        })
    finally:
        return rows


def do_nfer1() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'NFER1DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        note = ''
        table = {
            '1': 'we',
            '2': 'will',
            '3': 'be',
            '4': 'coming',
            '5': 'to',
            '6': 'leeds',
            '7': 'on',
            '8': 'sunday',
            '9': 'with',
            '10': 'our',
            '11': 'two',
            '12': 'sons',
            '13': 'as',
            '14': 'you',
            '15': 'were',
            '16': 'not',
            '17': 'there',
            '18': 'last',
            '19': 'time',
            '20': 'we',
            '21': 'came',
            '22': 'we',
            '23': 'are',
            '24': 'looking',
            '25': 'forward',
            '26': 'to',
            '27': 'seeing',
            '28': 'you',
            '29': 'again',
            '30': 'best',
            '31': 'wishes',
            '51': 'friends',
            '52': 'station',
            '53': 'babies',
            '54': 'walked',
            '55': 'digging',
            '56': 'cooking',
            '57': 'half',
            '58': 'various',
            '59': 'potatoes',
            '60': 'dining',
            '61': 'admitted',
            '62': 'received',
            '63': 'noticeable'
        }
        for line in lines:
            if line:
                pos = 1
                if line[-1] == '!':
                    line = line[:-1].strip()
                tokens = line.split()
                if tokens[0][0] in '1234567890':
                    note = tokens[0]
                while pos < len(tokens):
                    correct = table[tokens[pos]]
                    error = tokens[pos + 1]
                    if error != correct:
                        rows.append({
                            'error': re.sub(r'_', ' ', error),
                            'correct': re.sub(r'_', ' ', correct),
                            'note': note,
                            'freq': 1,
                            'comment': 'British',
                            'source': 'nfer1.dat'
                        })
                    pos += 2
    finally:
        return rows


def do_nfer2() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'NFER2DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        note = ''
        table = {
            '1': 'we',
            '2': 'will',
            '3': 'be',
            '4': 'coming',
            '5': 'to',
            '6': 'leeds',
            '7': 'on',
            '8': 'sunday',
            '9': 'with',
            '10': 'our',
            '11': 'two',
            '12': 'sons',
            '13': 'as',
            '14': 'you',
            '15': 'were',
            '16': 'not',
            '17': 'there',
            '18': 'last',
            '19': 'time',
            '20': 'we',
            '21': 'came',
            '22': 'we',
            '23': 'are',
            '24': 'looking',
            '25': 'forward',
            '26': 'to',
            '27': 'seeing',
            '28': 'you',
            '29': 'again',
            '30': 'best',
            '31': 'wishes',
            '51': 'friends',
            '52': 'station',
            '53': 'babies',
            '54': 'walked',
            '55': 'digging',
            '56': 'cooking',
            '57': 'half',
            '58': 'various',
            '59': 'potatoes',
            '60': 'dining',
            '61': 'admitted',
            '62': 'received',
            '63': 'noticeable'
        }
        for line in lines:
            if line:
                pos = 1
                if line[-1] == '!':
                    line = line[:-1].strip()
                tokens = line.lower().split()
                if tokens[0][0] in '1234567890':
                    note = tokens[0]
                while pos < len(tokens):
                    correct = table[tokens[pos]]
                    error = tokens[pos + 1]
                    if error != correct:
                        rows.append({
                            'error': re.sub(r'_', ' ', error),
                            'correct': re.sub(r'_', ' ', correct),
                            'note': note,
                            'freq': 1,
                            'comment': 'British',
                            'source': 'nfer2.dat'
                        })
                    pos += 2
    finally:
        return rows


def do_perin1() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'PERIN1DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        note = ''
        table = {
            '1': 'If',
            '2': 'you',
            '3': 'are',
            '4': 'aged 16-19',
            '5': 'and',
            '6': 'unemployed',
            '7': 'you',
            '8': 'should',
            '9': 'take',
            '10': 'advantage',
            '11': 'of',
            '12': 'the',
            '13': 'special',
            '14': 'training',
            '15': 'schemes',
            '16': 'run',
            '17': 'by',
            '18': 'the',
            '19': 'government',
            '20': 'for',
            '21': 'unemployed',
            '22': 'young',
            '23': 'people',
            '24': 'Enquire',
            '25': 'at',
            '26': 'your',
            '27': 'local',
            '28': 'Jobcentre',
            '29': 'about',
            '30': 'the',
            '31': 'different',
            '32': 'schemes',
            '33': 'available',
            '34': 'You',
            '35': 'can',
            '36': 'choose',
            '37': 'to',
            '38': 'work',
            '39': 'for',
            '40': 'an',
            '41': 'employer',
            '42': 'on',
            '43': 'the',
            '44': 'spot',
            '45': 'to',
            '46': 'get',
            '47': 'experience',
            '48': 'of',
            '49': 'a',
            '50': 'particular',
            '51': 'type',
            '52': 'of',
            '53': 'job',
            '54': 'or',
            '55': 'you',
            '56': 'can',
            '57': 'work',
            '58': 'on',
            '59': 'a',
            '60': 'special',
            '61': 'project',
            '62': 'Or',
            '63': 'you',
            '64': 'may',
            '65': 'prefer',
            '66': 'to',
            '67': 'work',
            '68': 'in',
            '69': 'Community',
            '70': 'Industry',
            '71': 'There',
            '72': 'are',
            '73': 'also',
            '74': 'courses',
            '75': 'run',
            '76': 'to',
            '77': 'help',
            '78': 'you',
            '79': 'choose',
            '80': 'which',
            '81': 'kind',
            '82': 'of',
            '83': 'work',
            '84': 'suits',
            '85': 'you',
            '86': 'best',
            '87': 'and',
            '88': 'courses',
            '89': 'to',
            '90': 'train',
            '91': 'you',
            '92': 'for',
            '93': 'a',
            '94': 'particular',
            '95': 'job',
            '96': 'at',
            '97': 'operator',
            '98': 'or',
            '99': 'semi-skilled',
            '100': 'level'
        }
        dictate = True
        for line in lines:
            if line:
                pos = 1
                if line[-1] == '!':
                    line = line[:-1].strip()
                tokens = line.lower().split()
                if tokens[0][0] in '1234567890':
                    note = tokens[0]
                    dictate = True
                if tokens[0][0] == '$':
                    dictate = False
                if tokens[pos] != '#':
                    while pos < len(tokens):
                        correct = table[tokens[pos]] if dictate else tokens[pos + 1][:-1].strip()
                        error = tokens[pos + 1] if dictate else tokens[pos]
                        if error != correct:
                            rows.append({
                                'error': re.sub(r'_', ' ', error),
                                'correct': re.sub(r'_', ' ', correct),
                                'note': note,
                                'freq': 1,
                                'comment': 'British',
                                'source': 'perin1.dat'
                            })
                        pos += 2
    finally:
        return rows


def do_perin2() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'PERIN2DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        note = ''
        for line in lines:
            if line:
                if line.startswith('$'):
                    note = line[:1].strip()
                else:
                    line = line[:-1].strip()
                    for mistake in line.split(','):
                        correct, error = mistake.split(maxsplit=1)
                        if error != correct:
                            rows.append({
                                'error': re.sub(r'_', ' ', error),
                                'correct': re.sub(r'_', ' ', correct),
                                'note': note,
                                'freq': 1,
                                'comment': 'British',
                                'source': 'perin2.dat'
                            })
    finally:
        return rows


def do_perin3() -> List[Dict[str, str]]:
    rows = []
    try:
        filename = os.path.join(_folder, '0643', 'PERIN3DAT.643')
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except Exception as e:
        _logger.warning(str(e))
    else:
        note = ''
        table = {
            '1': 'engine',
            '2': 'climb',
            '3': 'because',
            '4': 'built',
            '5': 'laugh',
            '6': 'curtain',
            '7': 'traffic',
            '8': 'juice',
            '9': 'poetry',
            '10': 'southern',
            '11': 'awful',
            '12': 'stomach',
            '13': 'opposite',
            '14': 'special',
            '15': 'gallery',
            '16': 'scissors',
            '17': 'scarcely',
            '18': 'bicycle',
            '19': 'initials',
            '20': 'receipt',
            '21': 'planted',
            '22': 'reporter',
            '23': 'remind',
            '24': 'chapter',
            '25': 'driven',
            '26': 'pretend',
            '27': 'understand',
            '28': 'remember',
            '29': 'contented',
            '30': 'latest',
            '31': 'problem',
            '32': 'refreshment',
            '33': 'extended',
            '34': 'visited',
            '35': 'splendid',
            '36': 'ventilated',
            '37': 'magnificent',
            '38': 'inconvenient',
            '39': 'establishing',
            '40': 'unexpected'
        }
        for line in lines:
            if line:
                if line[-1] == '!':
                    line = line[:-1].strip()
                tokens = line.split()
                if line[0] in '1234567890':
                    if tokens[2] == '#':
                        continue

                    note = '%s %s' % (tokens[0], tokens[1])
                    pos = 2
                else:
                    pos = 1
                while pos < len(tokens):
                    correct = table[tokens[pos]]
                    error = tokens[pos + 1]
                    if error != correct:
                        rows.append({
                            'error': re.sub(r'_', ' ', error),
                            'correct': re.sub(r'_', ' ', correct),
                            'note': note,
                            'freq': 1,
                            'comment': 'British',
                            'source': 'perin3.dat'
                        })
                    pos += 2
    finally:
        return rows


if __name__ == '__main__':
    dataset = do_abodat() + do_appling1() + do_appling2() + do_bloor() + do_ches() + do_exams() + do_fawthrop1() + \
              do_fawthrop2() + do_sheffield() + do_gates() + do_masters() + do_nfer1() + do_nfer2() + do_perin1() + \
              do_perin2() + do_perin3()
    # dataset = do_perin3()
    # print(dataset)

    values = [damerau_levenshtein_distance(error, correct)
              for error, correct in {(row['error'], row['correct']) for row in dataset}
              if ' ' not in error and ' ' not in correct]

    model = Model(values)

    print('Size:', model.size())
    print('Total:', model.total())
    for key in model.best(5):
        print('%s : %s - %.6f' % (key, model.freq(key), model.prob(key)))

    scaled = {0: 0.975}
    for key in model.keys():
        scaled[key] = (1 - scaled[0]) * model.prob(key)

    model = Model(scaled)
    model.save('errors.json')
    for key in model.best(5):
        print('%s : %s - %.6f' % (key, model.freq(key), model.prob(key)))
