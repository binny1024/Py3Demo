from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('/Users/binny/PycharmProjects/Py3Utils/app/app.py', base=base, targetName = 'app')
]

setup(name='cx_test',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
