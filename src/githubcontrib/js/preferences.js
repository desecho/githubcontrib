'use strict';

import Vue from 'vue';
import axios from 'axios';
import {
  param,
} from './helpers';


window.vm = new Vue({
  el: '#app',
  data: {
    language: vars.language,
  },
  methods: {
    savePreferences: function() {
      const vm = this;
      axios.post(urls.savePreferences, param({
        language: vm.language,
      })).then(function() {
        location.reload();
      }).catch(function() {
        vm.flashError(gettext('Error saving settings'));
      });
    },
  },
});
