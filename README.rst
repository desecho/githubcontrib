GitHubContrib
==========================================================

|Deployment Status| |Codecov|

The project is split into a Django_ API backend and a Vue.js_ 3 frontend built with Vite_ and Vuetify_.

It allows you to have a profile page with your opensource contributions.

It also shows the number of stars you have for your repositories.

The website is live at https://githubcontrib.samarchyan.me.

See more documentation_.

Development
----------------------------
| You can use ubuntu-vm_ as a development VM if needed.
| Also you can use macos-setup_ if you are on Mac.

1. Use mysql-docker_ to bring up MySQL in Docker
2. Use redis-docker_ to bring up Redis in Docker
3. Run ``make install-deps`` if necessary (only on Ubuntu)
4. Run ``make bootstrap``
5. Run ``make createsuperuser`` to create a superadmin user
6. Edit files ``env_custom.sh`` and ``env_secrets.sh``

| Run ``make run`` to run the backend on http://localhost:8000/.
| Run ``make dev`` to run the frontend on http://localhost:5173/.
| Run ``make help`` to get a list of all available commands.

| Open http://localhost:5173/ to access the web application.
| Open http://localhost:8000/admin to access the admin section.

GitHub OAuth callback URLs should point at the backend, for example:

* ``http://localhost:8000/auth/complete/github/`` for local development
* ``https://<backend-domain>/auth/complete/github/`` for production

Set ``FRONTEND_URL`` to the frontend origin so the backend can redirect OAuth users back with JWT tokens.

Run in Docker:

1. Run ``make docker-build``
2. Edit file ``docker_secrets.env``
3. Run ``make docker-run``

Production
----------------------------
To use production commands:

1. Edit file ``db_env_prod.sh``
2. Activate the kubectl context

.. |Deployment Status| image:: https://github.com/desecho/githubcontrib/actions/workflows/deployment.yaml/badge.svg
   :target: https://github.com/desecho/githubcontrib/actions/workflows/deployment.yaml

.. |Codecov| image:: https://codecov.io/gh/desecho/githubcontrib/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/desecho/githubcontrib

.. _documentation: https://github.com/desecho/githubcontrib/blob/master/doc.rst
.. _Vue.js: https://vuejs.org/
.. _Django: https://www.djangoproject.com/
.. _Vite: https://vitejs.dev/
.. _Vuetify: https://vuetifyjs.com/
.. _ubuntu-vm: https://github.com/desecho/ubuntu-vm
.. _macos-setup: https://github.com/desecho/macos-setup
.. _mysql-docker: https://github.com/desecho/mysql-docker
.. _redis-docker: https://github.com/desecho/redis-docker
