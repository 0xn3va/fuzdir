from pathlib import Path

from setuptools import setup, find_packages


def read(filename: str) -> str:
    with open(Path(__file__).parent.joinpath(filename), encoding='utf-8') as file:
        return file.read()


setup(
    name='fuzdir',
    version='1.0.2',
    description='Web path fuzzer',
    url='https://github.com/0xn3v4/fuzdir',
    author='n3va',
    keywords=['fuzzing', 'web security', 'bruteforce', 'testing'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    package_data={
        'fuzdir': ['banner.txt']
    },
    packages=find_packages(exclude=['fuzdir.test.*', 'fuzdir.test']),
    include_package_data=True,
    python_requires='>=3.5',
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
