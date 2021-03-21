.. felling documentation master file, created by
   sphinx-quickstart on Tue Mar 16 08:52:01 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to felling's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   felling


Felling easily improves repeatability and debugging of code by always initially logging some runtime metadata and ensuring logs are always written to a file in an easy to read format.

Installation and example usage
------------------------------

Installation
~~~~~~~~~~~~

with pip:
   ``pip install felling``

with conda:
   ``conda install -c conda-forge felling``


Example usage
~~~~~~~~~~~~~

.. code-block:: python

   import felling  
   felling.configure()  
   # Done! 

Features
--------
- Ensure logs are always written to a file
- Ensure some runtime metadata is always logged
- Never lose logs/print messages because you've filled your stdout
- Have paper trail on how to reproduce what happened
- Compare logs files to spot where your code is working differently to before
- Easily send emails, for example emailing on errors


Contribute
----------

- Issue Tracker: github.com/this-josh/felling/issues
- Source Code: github.com/this-josh/felling

Support
-------

If you are having issues, please let us know by writing a github issue or contact us on the `discord channel <https://discord.com/channels/816786912383729694/>`_.

License
-------

The project is licensed under the MIT license.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
