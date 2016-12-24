from setuptools import setup


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="htbayes",
    version="2016.12.24",
    description="",
    long_description=readfile('README.md'),
    author="Eric J. Ma",
    author_email="ericmajinglong@gmail.com",
    url="https://github.com/ericmjl/bayesian-measurement-paper",
    py_modules=['htbayes'],
    license=readfile('LICENSE'),
    entry_points={
        'console_scripts': [
            'htbayes = htbayes:main'
        ]
    },
)
