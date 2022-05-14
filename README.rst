GitHubContrib
==========================================================

|Deployment Status| |Requirements Status| |Codecov|

The web application on Django_ 4, Vue.js_ 2, Bootstrap_ 4. It allows you to have a profile page with your opensource contributions.

The website is live at https://githubcontrib.samarchyan.me.

See more documentation_.

Development
----------------------------
1. Use ubuntu-vm_ as a development VM
2. Use mysql-docker_ to bring up MySQL in Docker
3. Run ``make bootstrap``
4. Run ``make createsuperuser`` to create a superadmin user
5. Edit file ``env.sh``

| Run ``make build`` and ``make run`` to run the server for development.
| Run ``make help`` to get a list of all available commands.

| Open http://localhost:8000/ to access the web application.
| Open http://localhost:8000/admin to access the admin section.
| Open http://localhost:8000/rosetta to access rosetta.

Run in Docker:

1. Run ``make collectstatic``
2. Run ``make docker-build``
3. Run ``make docker-run``

Production
----------------------------
To use production commands edit ``db_env_prod.sh``.

CI/CD
----------------------------
`GitHub Actions`_  are used for CI/CD.

Tests are automatically run on pull requests and in master or dev branches.

Deployment is automatically done in master branch.

The following GitHub Actions are used:

* `Cancel Workflow Action`_
* Checkout_
* `Setup Python`_
* `Setup Node.js environment`_
* Codecov_
* `Docker Login`_
* `Docker Build & Push Action`_
* `GitHub Action for DigitalOcean - doctl`_
* `Kubectl tool installer`_
* `DigitalOcean Spaces Upload Action`_

Cronjobs
----------------------------
Cronjobs are run with GitHub Actions

* Backup runs daily
* ``Update avatars`` command runs monthly

Fonts used
----------------------------
* Orbitron_ for logo.

.. |Deployment Status| image:: https://github.com/desecho/githubcontrib/actions/workflows/deployment.yaml/badge.svg
   :target: https://github.com/desecho/githubcontrib/actions/workflows/deployment.yaml

.. |Requirements Status| image:: https://requires.io/github/desecho/githubcontrib/requirements.svg?branch=master
   :target: https://requires.io/github/desecho/githubcontrib/requirements/?branch=master

.. |Codecov| image:: https://codecov.io/gh/desecho/githubcontrib/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/desecho/githubcontrib

.. _documentation: https://github.com/desecho/githubcontrib/blob/master/doc.rst
.. _Vue.js: https://vuejs.org/
.. _Bootstrap: https://getbootstrap.com/
.. _Django: https://www.djangoproject.com/
.. _ubuntu-vm: https://github.com/desecho/ubuntu-vm
.. _mysql-docker: https://github.com/desecho/mysql-docker
.. _Orbitron: https://fonts.google.com/specimen/Orbitron
.. _GitHub Actions: https://github.com/features/actions
.. _Cancel Workflow Action: https://github.com/marketplace/actions/cancel-workflow-action
.. _Checkout: https://github.com/marketplace/actions/checkout
.. _Setup Python: https://github.com/marketplace/actions/setup-python
.. _Setup Node.js environment: https://github.com/marketplace/actions/setup-node-js-environment
.. _Codecov: https://github.com/marketplace/actions/codecov
.. _Docker Login: https://github.com/marketplace/actions/docker-login
.. _Docker Build & Push Action: https://github.com/marketplace/actions/docker-build-push-action
.. _GitHub Action for DigitalOcean - doctl: https://github.com/marketplace/actions/github-action-for-digitalocean-doctl
.. _Kubectl tool installer: https://github.com/marketplace/actions/kubectl-tool-installer
.. _DigitalOcean Spaces Upload Action: https://github.com/marketplace/actions/digitalocean-spaces-upload-action
