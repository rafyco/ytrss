Testing & Quality Assurance
===========================

This project uses tox to automate testing and ensure code consistency. Tox creates isolated virtual
environments for each task, ensuring that tests run in a clean, reproducible environment.

Prerequisites
-------------

Before running the suite, ensure you have the following installed:

* *Python 3.10+*
* *tox*: Install via pip: ``pip install tox``
* *Docker*: Required only for the megalinter environment.

Quick start
-----------

To run the entire testing pipeline (Style, Typing, Unittests, Documentation, and Execution checks):

.. code-block:: bash

    tox

To run specific environment:

.. code-block::

    tox -e <env_name>
    # Example: tox -e unittests

Available Environments
----------------------

.. list-table:: Available environments
    :header-rows: 1

    * - Command
      - Environment
      - Purpose

    * - tox -e style
      - **Linter**
      - Runs `pycodestyle` and `pylint` to check for PEP 8 compliance.

    * - tox -e typing
      - **Static Analysis**
      - Uses `mypy` for strict type checking to catch bugs before runtime.

    * - tox -e unittests
      - **Unit Testing**
      - Runs all unittests in `tests/unit` using `pytest`.

    * - tox -e integration
      - **Integration**
      - Runs integration tests in `tests/integration` to check module interaction.

    * - tox -e documentation
      - **Docs**
      - Builds the project documentation via Sphinx.

    * - tox -e execute
      - **Smoke Test**
      - Verifies the `ytrss` CLI tool installs and responds correctly.

    * - tox -e megalinter
      - **Deep Scan**
      - Runs 70+ linters via Docker (useful before a major PR).