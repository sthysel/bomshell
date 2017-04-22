========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/bomshell/badge/?style=flat
    :target: https://readthedocs.org/projects/bomshell
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/sthysel/bomshell.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sthysel/bomshell

.. |requires| image:: https://requires.io/github/sthysel/bomshell/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/sthysel/bomshell/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/sthysel/bomshell/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/sthysel/bomshell

.. |version| image:: https://img.shields.io/pypi/v/bomshell.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/bomshell

.. |commits-since| image:: https://img.shields.io/github/commits-since/sthysel/bomshell/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/sthysel/bomshell/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/bomshell.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/bomshell

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/bomshell.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/bomshell

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/bomshell.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/bomshell


.. end-badges

Retrieve weather data from the Australian  Bureau of Meteorology


Installation
============

::

    pip install bomshell

Documentation
=============

https://bomshell.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
