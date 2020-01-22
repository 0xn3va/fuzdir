import os
from setuptools import setup, find_packages


def read(filename: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding='utf-8') as file:
        return file.read()


setup(
    name='fuzdir',
    version='1.0.0',
    description='Web path fuzzer',
    url='https://github.com/0xn3v4/fuzdir',
    author='n3va',
    keywords=['fuzzing', 'web security', 'bruteforce', 'testing'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    package_data={
        'fuzdir': ['banner.txt'],
        'fuzdir.logs': ['*']
    },
    packages=find_packages(exclude=['fuzdir.test.*', 'fuzdir.test']),
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=read('requirements.txt').splitlines(),
    extras_require={
        'dev': [
            'wheel',
            'twine'
        ]
    },
    entry_points={
        'console_scripts': [
            'fuzdir=fuzdir.cli:main',
        ]
    },
)
