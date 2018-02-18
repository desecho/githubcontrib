'use strict';

import {
  loadProgressBar,
} from 'axios-progress-bar';
import axios from 'axios';

(function() {
  loadProgressBar();

  if (window.vm == null) {
    return;
  }
  const headers = {
    'X-CSRFToken': vm.$cookies.get('csrftoken'),
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
  };
  axios.defaults.headers.common = headers;
})();
