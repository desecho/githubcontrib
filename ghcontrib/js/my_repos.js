'use strict';

import Vue from 'vue';
import VueFlashMessage from 'vue-flash-message';
import VueCookie from 'vue-cookies';
import axios from 'axios';

Vue.use(VueFlashMessage);
Vue.use(VueCookie);

window.vm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
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
          vm.repos = vm.repos.filter(function(repo) {
            if (repo.id != id) {
              return repo;
            }
          });
        } else {
          vm.flash(response.data.message, 'error', vars.flashOptions);
        }
      }).catch(function(r) {
        vm.flash(gettext('Error deleting repository'), 'error', vars.flashOptions);
      });
    },
    addRepo: function() {
      const vm = this;
      let params = new URLSearchParams();
      params.append('name', vm.name);
      axios.post(urls.urlRepo, params).then(function(response) {
        if (response.data.status === 'success') {
          vm.repos.push({
            id: response.data.id,
            name: vm.name,
          });
          vm.name = '';
        } else {
          vm.flash(response.data.message, response.data.messageType, vars.flashOptions);
        }
      }).catch(function(response) {
        vm.flash(gettext('Error adding repository'), 'error', vars.flashOptions);
      });
    },
    loadCommitData: function() {
      const vm = this;
      let params = new URLSearchParams();
      params.append('name', vm.name);
      axios.post(urls.urlLoadCommitData, params).then(function(response) {
        if (response.data.status === 'success') {
          vm.flash(gettext('Commit data has been updated'), 'success');
        } else {
          vm.flash(response.data.message, 'error', vars.flashOptions);
        }
      }).catch(function(response) {
        vm.flash(gettext('Error loading commit data'), 'error', vars.flashOptions);
      });
    },
  },
});
