============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/castelao/seabird/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

seabird could always use more documentation, whether as part of the
official seabird docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/castelao/seabird/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `seabird` for local development.

1. Fork the `seabird` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/seabird.git

3. Create working environment. There are different options here. I've been using conda, but before I used virtualenv without problems. Pick yours:

   a. Using Conda (assuming you already have it installed)

        I. Python 2::

            $ conda create --name seabird python=2

        II. Or, Python 3::

            $ conda create --name seabird python=3

        Activate your conda environment, and take advantage of conda::

            $ source activate seabird
            $ conda install -n seabird numpy PyYAML pytest flake8

    b. Or, using virtualenv::

        $ mkvirtualenv seabird
        $ pip install pytest flake8

4. Install seabird for your local development, and check if it looks fine::

   $ cd seabird/
   $ python setup.py develop
   $ py.test tests

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 seabird tests
    $ py.test tests

7. Tox is a nice solution to test with multiple versions of Python::

    $ tox

   To get tox, just pip install them into your virtualenv. You might have trouble to have it working with conda.

8. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

9. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.6, 2.7, 3.3, and 3.4, and for PyPy. Check
   https://travis-ci.org/castelao/seabird/pull_requests
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ py.test tests/test_rules.py
