============
Installation
============

ATG is a Python library and is designed to save you time by handling the intricacies
of the Riot API for you.

ATG is published on the `Python Package Index <https://pypi.org/project/ATG-lib/>`_ (PyPI) under the name ATG-lib.
The preferred tool for installing packages from PyPi is :command:`pip`, which is included on
all modern versions of Python.

To install run:

.. code-block:: bash

    pip install -U ATG-lib

.. tip::
    This library is under :ref:`active development <active_development>` with many function signature changes expected
    before 2.0 release. It is advisable to pin the version of this library using a `requirements.txt file. <https://pip.pypa.io/en/stable/reference/requirements-file-format/>`_

Setup & Example Usage
---------------------

It is recommended to use a `virtual environment
<https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/>`_
when directly running this library's scripts.

Setup dependencies

.. code-block:: bash

   uv sync

Edit the ``.env`` file with your Riot API key and database connection string.
The `psycopg database driver
<https://www.psycopg.org/psycopg3/docs/basic/install.html>`_ is installed if
this code is installed as a library and is the recommended database driver.

.. code-block:: bash

   uv run main.py
