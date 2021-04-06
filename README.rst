GitHubContrib
==========================================================

|Build Status| |Requirements Status| |Codecov|

The web application on Django_ 2, Vue.js_ 2, Bootstrap_ 4. It allows you to have a profile page with your opensource contributions.

See more documentation_.

Development
----------------------------
1. Use ubuntu-vm_ as a development VM
2. Use mysql-docker_ to bring up MySQL in Docker
3. Run ``make bootstrap``
4. Run ``make createsuperuser`` to create a superadmin user
5. Edit file ``env.sh``

Run ``make build`` and ``make runserver`` to run the server for development.

| Open http://localhost:8000/ to access the web application.
| Open http://localhost:8000/admin to access the admin section.

Run ``make format`` to format all the code.

Run ``make help`` to get a list of all available commands.

Production
----------------------------
To use production commands edit ``db_env_prod.sh``.


.. |Requirements Status| image:: https://requires.io/github/desecho/githubcontrib/requirements.svg?branch=master
   :target: https://requires.io/github/desecho/githubcontrib/requirements/?branch=master

.. |Codecov| image:: https://codecov.io/gh/desecho/githubcontrib/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/desecho/githubcontrib

.. |Build Status| image:: https://travis-ci.org/desecho/githubcontrib.svg?branch=master
   :target: https://travis-ci.org/desecho/githubcontrib

.. _documentation: https://github.com/desecho/githubcontrib/blob/master/doc.rst
.. _Vue.js: https://vuejs.org/
.. _Bootstrap: https://getbootstrap.com/
.. _Django: https://www.djangoproject.com/
.. _ubuntu-vm: https://github.com/desecho/ubuntu-vm
.. _mysql-docker: https://github.com/desecho/mysql-docker
