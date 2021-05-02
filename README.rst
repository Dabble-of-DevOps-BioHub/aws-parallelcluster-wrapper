===========================
AWS ParallelCluster Wrapper
===========================


.. image:: https://img.shields.io/pypi/v/aws_parallelcluster_wrapper.svg
        :target: https://pypi.python.org/pypi/aws_parallelcluster_wrapper

.. image:: https://img.shields.io/travis/jerowe/aws_parallelcluster_wrapper.svg
        :target: https://travis-ci.com/jerowe/aws_parallelcluster_wrapper

.. image:: https://readthedocs.org/projects/aws-parallelcluster-wrapper/badge/?version=latest
        :target: https://aws-parallelcluster-wrapper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Wrapper around AWS ParallelCluster CLI to use in an automated setting.


* Free software: MIT license
* Documentation: https://aws-parallelcluster-wrapper.readthedocs.io.


Features
--------

* TODO

Example
--------

aws_parallelcluster_wrapper apply-terraform-state --outdir ~/client/project/slurm-cluster-development/terraform-state ---config ~/client/cookiecutter.json -apply --init

aws_parallelcluster_wrapper deploy-pcluster-resources --outdir ~/client/project/slurm-cluster-development/pcluster-resources --apply --init --config ~/client/cookiecutter.json

aws_parallelcluster_wrapper create-pcluster --outdir ~/client/project/slurm-cluster-development/pcluster-apps --apply --init --config ~/client/cookiecutter.json

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
