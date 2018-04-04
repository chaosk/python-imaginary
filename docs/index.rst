.. python-imaginary documentation master file, created by
   sphinx-quickstart on Sun Apr  1 14:27:51 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

python-imaginary documentation
==============================

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://travis-ci.org/chaosk/python-imaginary.svg?branch=master
    :target: https://travis-ci.org/chaosk/python-imaginary
    :alt: Build status

.. image:: https://coveralls.io/repos/github/chaosk/python-imaginary/badge.svg?branch=master
    :target: https://coveralls.io/github/chaosk/python-imaginary?branch=master
    :alt: Coverage status


Python client library for interacting with imaginary_, an image processing microservice.


Six lines example
-----------------

    >>> from imaginary import Imaginary
    >>> imaginary = Imaginary('http://imaginary_server_url')
    >>> with open('banana.png', 'rb') as banana:
    ...     image = imaginary(banana)
    ...     with open('banana-cropped.png', 'wb') as target:
    ...         target.write(image.crop(width=100, height=100))

User Guide
----------

.. toctree::
   :maxdepth: 2

   user/install
   user/quickstart


Developer Interface
-------------------

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _imaginary: https://github.com/h2non/imaginary
