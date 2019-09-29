import sys
from cx_Freeze import setup, Executable

with open('tsu/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'


options = {
    'build_exe': {
        'optimize' : 2, 
        'includes' : ['consolejs', 'docopt' ],
    }
}

executables = [
    Executable('tsu/main.py', targetName='tsu')
]

setup(name='tsuexec',
      version=version,
      description='Sample matplotlib script',
      executables=executables,
      options=options
      )
