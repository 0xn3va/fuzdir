import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as file:
    readme = file.read()

setup(
    name='fuzdir',
    version='1.0.0',
    description='Web path fuzzer',
    url='https://github.com/n3v4/fuzdir',
    author='n3va',
    keywords='fuzzing web security bruteforce testing',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    packages=find_packages(exclude=['fuzdir.test.*', 'fuzdir.test']),
    data_files=[
        ('banner', ['fuzdir/banner.txt']),
        ('logs', ['fuzdir/logs/.gitignore'])
    ],
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=[
        'requests',
        'pysocks',
        'urllib3',
        'colorama'
    ],
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
