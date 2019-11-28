from subprocess import Popen, PIPE
from pathlib import Path

proctable = []
cwd = Path.cwd()
print(cwd)
for p in [ cwd / 'tsu', cwd / 'tests'  ] :
    pg = ( str(pp) for pp in Path(p).rglob('*.py') )
    for f in pg:
        cmd = ["black", f ] 
        proctable.append( Popen(cmd))

for proc in proctable:
    proc.wait()
    out, err = proc.communicate()

