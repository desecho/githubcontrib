'use strict';

import axios from 'axios';
import {newApp} from './app';
import {initAxios} from './helpers';

newApp({
  data() {
    const vars = window.vars;
    return {
      language: vars.language,
      urls: window.urls,
    };
  },
  methods: {
    savePreferences() {
      const vm = this;

      axios.post(vm.urls.savePreferences, {
        language: vm.language,
      }).then(function() {
        location.reload();
      }).catch(function() {
        vm.$toast.error(gettext('Error saving settings'));
      });
    },
  },
  mounted() {
    initAxios(this);
  },
}).mount('#app');
