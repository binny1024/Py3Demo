import sys
from cx_Freeze import setup, Executable
sys.path.append(r'../')
# Dependencies are automatically detected, but it might need
# fine tuning.
pkgs = []
pkgs.append('traceback')
pkgs.append('time')
pkgs.append('smbus')
pkgs.append('requests')
pkgs.append('serial')
pkgs.append('calendar')
pkgs.append('re')
buildOptions = dict(packages=pkgs, excludes=[])

base = 'Console'
options = {
    'build_exe':{

    }
}
executables = [
    Executable('./main.py', base=base, targetName='yunda')
]

setup(name='yunda',
      version='1.0',
      description='',
      options=dict(build_exe=buildOptions),
      executables=executables)
