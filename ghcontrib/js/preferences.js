'use strict';

import Vue from 'vue';
import axios from 'axios';


window.vm = new Vue({
  el: '#app',
  delimiters: vars.delimiters,
  data: {
    language: vars.language,
  },
  methods: {
    savePreferences: function() {
      const vm = this;
      let params = new URLSearchParams();
      params.append('language', vm.language);
      axios.post(urls.urlSavePreferences, params).then(function() {
        location.reload();
      }).catch(function() {
        vm.flash(gettext('Error saving settings'), 'error', vars.flashOptions);
      });
    },
  },
});
