.. _api:

Developer Interface
===================

.. module:: imaginary

Client
------

.. autoclass:: Imaginary
   :special-members: __call__
   :inherited-members:

Image
------

.. module:: imaginary.image

.. autoclass:: Image
   :special-members: __call__, __getattr__
   :inherited-members:

Transports
----------

.. module:: imaginary.transports

.. autoclass:: Transport
   :inherited-members:

.. autoclass:: RequestsTransport
   :inherited-members:

Exceptions
----------

.. module:: imaginary.exceptions

.. autoexception:: ImaginaryError
.. autoexception:: TransportError

Types
-----

.. automodule:: imaginary.types
   :members:
   :undoc-members:

