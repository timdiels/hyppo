from setuptools import setup, find_packages
from collections import defaultdict
from pathlib import Path
import os

setup_args = dict(
    version='0.0.1.dev1',
    name='glycemic_load',
    description='Calculate the glycemic load of your MyFitnessPal logs',
    long_description=Path('README.rst').read_text(),
    url='https://github.com/timdiels/glycemic-load',
    author='Tim Diels',
    author_email='timdiels.m@gmail.com',
    license='LGPL3',
    keywords='myfitnesspal health app glycemic-load glycemic-index glucose blood-sugar sugar glycemic',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'numpydoc==0.*',
            'sphinx==1.*',
            'sphinx-rtd-theme==0.*',
            'coverage-pth==0.*',
            'pytest==3.*',
            'pytest-cov==2.*',
            'pytest-env==0.*',
        ],
    },
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        "Environment :: Handhelds/PDA's",
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Android',
        'Operating System :: iOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Other/Nonlisted Topic',
    ],
)

# Generate extras_require['all'], union of all extras
all_extra_dependencies = []
for dependencies in setup_args['extras_require'].values():
    all_extra_dependencies.extend(dependencies)
all_extra_dependencies = list(set(all_extra_dependencies))
setup_args['extras_require']['all'] = all_extra_dependencies

# Generate package data
#
# Anything placed underneath a directory named 'data' in a package, is added to
# the package_data of that package; i.e. included in the sdist/bdist and
# accessible via pkg_resources.resource_*
project_root = Path(__file__).with_name(setup_args['name'])
package_data = defaultdict(list)
for package in setup_args['packages']:
    package_dir = project_root / package.replace('.', '/')
    data_dir = package_dir / 'data'
    if data_dir.exists() and not (data_dir / '__init__.py').exists():
        # Found a data dir
        for parent, _, files in os.walk(str(data_dir)):
            package_data[package].extend(str((data_dir / parent / file).relative_to(package_dir)) for file in files)
setup_args['package_data'] = {k: sorted(v) for k,v in package_data.items()}  # sort to avoid unnecessary git diffs

# setup
setup(**setup_args)
