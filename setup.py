import codecs
import os
import re
from typing import Text

from setuptools import (
    find_packages,
    setup,
)

NAME = 'imaginary'
PACKAGES = find_packages(where='src')
META_PATH = os.path.join('src', 'imaginary', '__init__.py')
KEYWORDS = []
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
]
INSTALL_REQUIRES = [
    'requests>=2.14.0',
]
TESTS_REQUIRE = [
    'coveralls>=1.3.0',
    'mypy>=0.580',
    'pytest-cov>=2.5.1',
    'pytest-mock>=1.7.1',
    'pytest>=3.5.0',
    'tox>=2.9.1',
]

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts: Text) -> bytes:
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), 'rb', 'utf-8') as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta: Text) -> Text:
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r'^__{meta}__ = [\'"]([^\'"]*)[\'"]'.format(meta=meta),
        META_FILE,
        re.M,
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))


if __name__ == '__main__':
    setup(
        name=NAME,
        description=find_meta('description'),
        license=find_meta('license'),
        url=find_meta('uri'),
        version=find_meta('version'),
        author=find_meta('author'),
        author_email=find_meta('email'),
        maintainer=find_meta('author'),
        maintainer_email=find_meta('email'),
        keywords=KEYWORDS,
        long_description=read('README.md'),
        packages=PACKAGES,
        package_dir={'': 'src'},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        python_requires=">=3.6",
        install_requires=INSTALL_REQUIRES,
        tests_require=TESTS_REQUIRE,
    )
