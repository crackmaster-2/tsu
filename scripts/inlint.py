from subprocess import Popen, PIPE
from pathlib import Path

proctable = []
cwd = Path.cwd()
print(cwd)
for p in [ cwd / 'tsu', cwd / 'tests'  ] :
    pg = ( str(pp) for pp in Path(p).rglob('*.py') )
    for f in pg:
        print (f)
        cmd = ["black", f ] 
        proctable.append( Popen(cmd, stdout=PIPE, stderr=PIPE))

for proc in proctable:
    proc.wait()
    out, err = proc.communicate()
    print(out.decode('utf-8'))

