'use strict';

import Vue from 'vue';
import VueFlashMessage from 'vue-flash-message';
import VueCookie from 'vue-cookies';


window.vars = {
  flashOptions: {
    timeout: 1500,
    important: true,
  },
  delimiters: ['[[', ']]'],
};
window.urls = {};

Vue.use(VueFlashMessage);
Vue.use(VueCookie);
