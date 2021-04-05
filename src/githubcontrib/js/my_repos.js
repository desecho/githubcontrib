'use strict';

import Vue from 'vue';
import axios from 'axios';
import {
  param,
} from './helpers';


window.vm = new Vue({
  el: '#app',
  data: {
    repos: vars.repos,
    name: '',
  },
  methods: {
    deleteRepo: function(id) {
      function success(response) {
        if (response.data.status === 'success') {
          vm.repos = vm.repos.filter((repo) => repo.id != id);
        } else {
          vm.flash(response.data.message, 'error', vars.flashOptions);
        }
      }

      function fail() {
        vm.flash(gettext('Error deleting repository'), 'error', vars.flashOptions);
      }

      const vm = this;
      const url = urls.repo + id + '/';
      axios.delete(url).then(success).catch(fail);
    },
    addRepo: function() {
      function success(response) {
        if (response.data.status === 'success') {
          vm.repos.push({
            id: response.data.id,
            name: vm.name,
          });
          vm.name = '';
        } else {
          vm.flash(response.data.message, response.data.messageType, vars.flashOptions);
        }
      }

      function fail() {
        vm.flash(gettext('Error adding repository'), 'error', vars.flashOptions);
      }

      const vm = this;
      const data = param({
        name: vm.name,
      });
      axios.post(urls.repo, data).then(success).catch(fail);
    },
    loadCommitData: function() {
      function success(response) {
        if (response.data.status === 'success') {
          vm.flash(gettext('Commit data has been updated'), 'success', vars.flashOptions);
        } else {
          vm.flash(response.data.message, 'error', vars.flashOptions);
        }
      }

      function fail() {
        vm.flash(gettext('Error loading commit data'), 'error', vars.flashOptions);
      }

      const vm = this;
      axios.post(urls.loadCommitData, param({
        name: vm.name,
      })).then(success).catch(fail);
    },
  },
});
