import sys
import subprocess
p = subprocess.getoutput("{} ./adventure.py < solution.txt".format(sys.executable))
print(p)
