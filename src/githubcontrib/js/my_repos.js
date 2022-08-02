'use strict';

import axios from 'axios';
import {newApp} from './app';
import {initAxios} from './helpers';

newApp({
  data() {
    const vars = window.vars;
    return {
      repos: vars.repos,
      reposOriginal: vars.repos,
      name: '',
      urls: window.urls,
    };
  },
  methods: {
    deleteRepo(id, index) {
      function success(response) {
        if (response.data.status === 'success') {
          vm.repos.splice(index, 1);
        } else {
          vm.$toast.error(response.data.message);
        }
      }

      function fail() {
        vm.$toast.error(gettext('Error deleting repository'));
      }

      const vm = this;
      const url = vm.urls.repo + id + '/';
      axios.delete(url).then(success).catch(fail);
    },
    addRepo() {
      function success(response) {
        if (response.data.status === 'success') {
          vm.repos.unshift({
            id: response.data.id,
            name: vm.name,
          });
          vm.name = '';
        } else {
          vm.$toast.open({
            message: response.data.message,
            type: response.data.messageType});
        }
      }

      function fail() {
        vm.$toast.error(gettext('Error adding repository'));
      }

      const vm = this;
      const data = {
        name: vm.name,
      };
      axios.post(vm.urls.repo, data).then(success).catch(fail);
    },
    loadCommitData() {
      function success(response) {
        if (response.data.status === 'success') {
          vm.$toast.success(gettext('Commit data has been updated'));
        } else {
          vm.$toast.error(response.data.message);
        }
      }

      function fail() {
        vm.$toast.error(gettext('Error loading commit data'));
      }

      const vm = this;
      axios.post(vm.urls.loadCommitData).then(success).catch(fail);
    },
    loadCommitDataForRepo(repoId) {
      function success(response) {
        if (response.data.status === 'success') {
          vm.$toast.success(gettext('Commit data has been updated'));
        } else {
          vm.$toast.error(response.data.message);
        }
      }

      function fail() {
        vm.$toast.error(gettext('Error loading commit data'));
      }

      const vm = this;
      const url = vm.urls.repo + repoId + '/load-commit-data/';
      axios.post(url).then(success).catch(fail);
    },
    saveReposOrder() {
      function getSortData() {
        const data = [];
        vm.repos.forEach((repo, index) => {
          const sortData = {'id': repo.id, 'order': index + 1};
          data.push(sortData);
        });
        return data;
      }

      function success() {
        vm.reposOriginal = vm.repos;
      }

      function fail() {
        vm.repos = vm.reposOriginal;
        vm.$toast.error(gettext('Error saving repositories order'));
      }

      const vm = this; // eslint-disable-line no-invalid-this
      axios.put(vm.urls.saveReposOrder, {'repos': getSortData()}).then(success).catch(fail);
    },
  },
  mounted() {
    initAxios(this);
  },
}).mount('#app');
