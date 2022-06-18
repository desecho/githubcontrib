'use strict';

import axios from 'axios';

window.vm = new Vue({
  el: '#app',
  data: {
    language: vars.language,
  },
  methods: {
    savePreferences: function() {
      const vm = this;
      axios.post(urls.savePreferences, {
        language: vm.language,
      }).then(function() {
        location.reload();
      }).catch(function() {
        vm.flashError(gettext('Error saving settings'));
      });
    },
  },
});
