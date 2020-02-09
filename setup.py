from setuptools import setup

setup(
    name='FarleyFile',
    version='0.1.0',
    py_modules=['farley'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        farley=farley:cli
    ''',
)
