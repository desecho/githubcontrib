GitHubContrib
==========================================================

|Build Status| |Requirements Status| |Codecov|

The web application on Django_ 2, Vue.js_ 2, Bootstrap_ 4. It allows you to have a profile page with your opensource contributions.

The website is live at https://githubcontrib.desecho.org.

See more documentation_.

Development
----------------------------
1. Use ubuntu-vm_ as a development VM
2. Use mysql-docker_ to bring up MySQL in Docker
3. Run ``make bootstrap``
4. Run ``make createsuperuser`` to create a superadmin user
5. Edit file ``env.sh``

Run ``make build`` and ``make run`` to run the server for development.

| Open http://localhost:8000/ to access the web application.
| Open http://localhost:8000/admin to access the admin section.

Run ``make format-all`` to format all the code.

Run ``make help`` to get a list of all available commands.

Run in Docker:

1. Edit ``env_docker.sh``

Note: static files are not served in docker so you will need to put a URL to your static files there in ``STATIC_URL`` variable.

2. Run ``make docker-build``
3. Run ``make docker-run``

Production
----------------------------
To use production commands edit ``db_env_prod.sh``.

Fonts used
----------------------------
* Orbitron_ for logo

.. |Requirements Status| image:: https://requires.io/github/desecho/githubcontrib/requirements.svg?branch=master
   :target: https://requires.io/github/desecho/githubcontrib/requirements/?branch=master

.. |Codecov| image:: https://codecov.io/gh/desecho/githubcontrib/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/desecho/githubcontrib

.. |Build Status| image:: https://github.com/desecho/githubcontrib/actions/workflows/deployment.yaml/badge.svg
   :target: https://github.com/desecho/githubcontrib/actions/workflows/deployment.yaml

.. _documentation: https://github.com/desecho/githubcontrib/blob/master/doc.rst
.. _Vue.js: https://vuejs.org/
.. _Bootstrap: https://getbootstrap.com/
.. _Django: https://www.djangoproject.com/
.. _ubuntu-vm: https://github.com/desecho/ubuntu-vm
.. _mysql-docker: https://github.com/desecho/mysql-docker
.. _Orbitron: https://fonts.google.com/specimen/Orbitron
