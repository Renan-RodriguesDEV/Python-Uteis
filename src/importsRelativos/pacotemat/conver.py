import sys, os

# maneira 1 de imports relativos
# sys.path.append(os.getcwd())

# maneira 2 de imports relativos
# path_abs = os.path.abspath(os.curdir)
# sys.path.insert(0, path_abs)

# maneira 3 de imports relativoso
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
print(sys.path)

from pacoteconv.mat import mostranome

mostranome()
