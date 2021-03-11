from distutils.core import setup

setup(
    name='openephys_fileIO',
    version='0.1.0',
    author='Teris Tam',
    package=['openephys_fileIO'],
    install_requires=[
        'numpy',
        'scipy',
        'pytest',
        'pytest-benchmark'
    ]
)