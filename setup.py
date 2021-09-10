"""Die Anmeldungen für einen Jamulus-Workshop."""

import os
from distutils.util import convert_path
from fnmatch import fnmatchcase

from setuptools import find_packages, setup

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = (
    '.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')


def long_description():
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
        return f.read()


def find_package_data(where='.', package='', exclude=standard_exclude,
                      exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                            or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                            or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix + name)
    return out


setup(
    name='docassemble.mailgun',
    version='0.0.9',
    description=__doc__,
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Kim Wittenburg',
    author_email='admin@lmr-hh.de',
    license='The MIT License (MIT)',
    url='https://github.com/lmr-hamburg/docassemble-mailgun',
    packages=find_packages(),
    namespace_packages=['docassemble'],
    install_requires=['requests'],
    zip_safe=False,
    package_data=find_package_data(where='docassemble/mailgun/',
                                   package='docassemble.mailgun'),
)
