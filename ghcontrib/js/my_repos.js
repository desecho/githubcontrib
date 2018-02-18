'use strict';

import Vue from 'vue';
import axios from 'axios';
import param from './helpers';


window.vm = new Vue({
  el: '#app',
  data: {
    repos: vars.repos,
    name: '',
  },
  methods: {
    deleteRepo: function(id) {
      const vm = this;
      const url = urls.urlRepo + id + '/';
      axios.delete(url).then(function(response) {
        if (response.data.status === 'success') {
          vm.repos = vm.repos.filter(repo => repo.id != id);
        } else {
          vm.flash(response.data.message, 'error', vars.flashOptions);
        }
      }).catch(function() {
        vm.flash(gettext('Error deleting repository'), 'error', vars.flashOptions);
      });
    },
    addRepo: function() {
      const vm = this;
      axios.post(urls.urlRepo, param({
        name: vm.name
      })).then(function(response) {
        if (response.data.status === 'success') {
          vm.repos.push({
            id: response.data.id,
            name: vm.name,
          });
          vm.name = '';
        } else {
          vm.flash(response.data.message, response.data.messageType, vars.flashOptions);
        }
      }).catch(function() {
        vm.flash(gettext('Error adding repository'), 'error', vars.flashOptions);
      });
    },
    loadCommitData: function() {
      const vm = this;
      axios.post(urls.urlLoadCommitData, param({name: vm.name})).then(function(response) {
        if (response.data.status === 'success') {
          vm.flash(gettext('Commit data has been updated'), 'success', vars.flashOptions);
        } else {
          vm.flash(response.data.message, 'error', vars.flashOptions);
        }
      }).catch(function() {
        vm.flash(gettext('Error loading commit data'), 'error', vars.flashOptions);
      });
    },
  },
});
