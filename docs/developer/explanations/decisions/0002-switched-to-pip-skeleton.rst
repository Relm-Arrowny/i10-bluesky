2. Adopt i10-bluesky for project structure
===================================================

Date: 2022-02-18

Status
------

Accepted

Context
-------

We should use the following `https://github.com/DiamondLightSource/python-copier-template'_.
The skeleton will ensure consistency in developer
environments and package management.

Decision
--------

We have switched to using the skeleton.

Consequences
------------

This module will use a fixed set of tools as developed in i10-bluesky
and can pull from this skeleton to update the packaging to the latest techniques.

As such, the developer environment may have changed, the following could be
different:

- linting
- formatting
- pip venv setup
- CI/CD
