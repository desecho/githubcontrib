'use strict';

import axios from 'axios';
import {newApp} from './app';

window.vm = newApp({
  data() {
    return {
      language: vars.language,
    };
  },
  methods: {
    savePreferences() {
      const vm = this;
      axios.post(urls.savePreferences, {
        language: vm.language,
      }).then(function() {
        location.reload();
      }).catch(function() {
        vm.$toast.error(gettext('Error saving settings'));
      });
    },
  },
});
window.vm.mount('#app');
