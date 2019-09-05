from setuptools import setup, find_packages

setup(
    name='fuzdir',
    version='0.1.1',
    description='Web path fuzzer',
    url='https://github.com/n3v4/fuzdir',
    author='n3va',
    keywords='fuzzing web security bruteforce testing',
    readme='README.md',
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
