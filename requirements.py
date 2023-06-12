import os
import subprocess
from importlib import import_module

import sys
from os.path import join


class Requirements:
    def __init__(self, min_python_version=None):
        self._min_pyver = min_python_version
        self._libs = {}

    def add(self, import_name, pip_name=None):
        self._libs[import_name] = pip_name if pip_name is not None else import_name
        return self

    def critical_check(self, try_install: bool=True):
        if not self.check(try_install):
            print("Requirements problems!", file=sys.stderr)
            raise RuntimeError("Bad environment!")

    def check(self, try_install: bool=True):
        if self._min_pyver and sys.version_info < self._min_pyver:
            print("Too low version of python interpreter. Expected {}.{}.{} or great".format(*self._min_pyver))
            return False

        problems = []
        for lib in self._libs:
            try:
                import_module(lib)
            except Exception as e:
                print("Import module `{}` error: {}".format(lib, e))
                problems.append((lib, self._libs[lib]))

        if len(problems) == 0:
            return True
        if try_install:
            result = InstallTask((i for _, i in problems)).install()
        else:
            result = False
        if result:
            return self.check(False)
        else:
            return False


class InstallTask:
    def __init__(self, modules):
        self._modules = list(modules)

    def install(self):
        pip = find_pip()
        print("Install next modules?" if pip else "Please, install next modules:")
        for module in self._modules:
            print("\t{}".format(module))
        if pip is None:
            return False
        answer = input("[Y]/n: ").lower()
        if answer in ["", "y", "yes", "yep", "ok", "da", "да", "д", "ага", "ок", "угу"]:
            self._install(pip)
            return True
        else:
            return False

    def _install(self, pip):
        for module in self._modules:
            pip_install(pip, module)


def find_pip():
    parent = os.path.dirname(sys.executable)
    folders = [parent, join(parent, 'Scripts'), join('scripts')]
    names = ['pip', 'pip3']
    for dir in folders:
        try:
            for file in os.listdir(dir):
                for name in names:
                    if file.startswith(name):
                        return join(dir, file)
        except Exception:
            pass
    return None


def pip_install(pip, pip_module_name):
    subprocess.call("{} install {}".format(pip, pip_module_name))
