'use strict';

import Vue from 'vue';
import VueFlashMessage from 'vue-flash-message';
import VueCookie from 'vue-cookies';
import axios from 'axios';
import VueAxios from 'vue-axios';

Vue.use(VueAxios, axios);
Vue.use(VueFlashMessage);
Vue.use(VueCookie);

window.vm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    language: vars.language,
  },
  methods: {
    savePreferences: function() {
      const vm = this;
      let params = new URLSearchParams();
      params.append('language', vm.language);
      vm.axios.post(urls.urlSavePreferences, params).then(function() {
        location.reload();
      }).catch(function() {
        vm.flash(gettext('Error saving settings'), 'error', vars.flashOptions);
      });
    },
  },
});
