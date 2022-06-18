GitHubContrib
==========================================================

|Deployment Status| |Requirements Status| |Codecov|

The web application on Django_ 4, Vue.js_ 3, Bootstrap_ 4, `Font Awesome`_ 6.

It allows you to have a profile page with your opensource contributions.

It also shows the number of stars you have for your repositories.

The website is live at https://githubcontrib.samarchyan.me.

See more documentation_.

Development
----------------------------
1. Use ubuntu-vm_ as a development VM
2. Use mysql-docker_ to bring up MySQL in Docker
3. Run ``make bootstrap``
4. Run ``make createsuperuser`` to create a superadmin user
5. Edit files ``env_custom.sh`` and ``env_secrets.sh``

| Run ``make build`` and ``make run`` to run the server for development.
| Run ``make help`` to get a list of all available commands.

| Open http://localhost:8000/ to access the web application.
| Open http://localhost:8000/admin to access the admin section.
| Open http://localhost:8000/rosetta to access Rosetta.

Run in Docker:

1. Run ``make docker-build``
2. Edit file ``docker_secrets.env``
3. Run ``make docker-run``

Production
----------------------------
To use production commands:

1. Edit file ``db_env_prod.sh``
2. Activate the kubectl context

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
.. _Font Awesome: https://fontawesome.com/
