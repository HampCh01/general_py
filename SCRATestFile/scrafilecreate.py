from pathlib import Path
import string
import yaml
import sys
from dateutil import parser
from datetime import datetime, timedelta
import random

def main() -> None:
    path = ''
    args = sys.argv[1:]
    if len(args) > 0:
        path = Path(args[0])
    else:
        path = Path(yaml.safe_load(open('settings.yml'))['path'])

    if not path.exists():
            raise FileNotFoundError(f"{path} does not exist")
    if not path.is_file():
        for file in path.iterdir():
            if file.name.endswith('.txt'):
                openfile(file)



def openfile(path:str) -> None:
    with open(path, 'r') as in_file:
        if (path.parents[1] / '3FromSCRA').exists():
            with open(path.parents[1] / '3FromSCRA' / f'SCRA_5_18_{path.name}', 'w') as out_file:
                for line in in_file:
                    out_file.write(add_test_data(parse_input(line.replace('\n', ''))) + '\n')
        else:
            with open(path.parents[1] / f'SCRA_5_18_{path.name}', 'w') as out_file:
                for line in in_file:
                    out_file.write(add_test_data(parse_input(line.replace('\n', ''))) + '\n')

def parse_input(line:str) -> list:
    if line == 'EOF':
        return ['EOF']
    return [
        line[0:9],
        line[9:17],
        line[17:43],
        line[43:63],
        line[63:91],
        line[91:99] if parser.parse(line[91:99]) else datetime.now().strftime('%Y%m%d'),
        line[99:119]
    ]

def add_test_data(pieces:list) -> str:
    if len(pieces) == 1:
        return ''
    mname = pieces.pop(-1)
    adedate, adbdate, adstatus = ad_random()
    pieces.append(f' {adstatus}{adbdate}09{datetime.now().strftime("%Y%m%d")}{adedate}{"0"*16}ZZZZ{mname}{get_cert()}')
    return ''.join(pieces)

def get_cert() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

def ad_random():
    result = random.choices([0, 1, 2], weights=(0.88, 0.1, 0.02), k=1)[0]
    td = timedelta(days=random.randrange(0, 350))
    now = datetime.now()
    day = timedelta(days=1)
    form = '%Y%m%d'
    if result == 0:
        return f'{"0"*8}', f'{"0"*8}', 'NNN'
    elif result == 1:
        return (now + td).strftime(form), ((now + td) + day - timedelta(days=365*random.randrange(1,5))).strftime(form), 'YNN'
    elif result == 2:
        return (now - td).strftime(form), ((now - td) + day - timedelta(days=365*random.randrange(1,5))).strftime(form), 'NYN'
    


if __name__ == "__main__":
    main()