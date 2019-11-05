from typing import Dict, List, Tuple


def graph2txt(g: Dict[int, List[Tuple[int, str]]], file_path):
    with open(file_path, 'w') as f:
        for v in g:
            for to in g[v]:
                f.write(f'{v} {to[1]} {to[0]}\n')
