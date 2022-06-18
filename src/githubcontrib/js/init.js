'use strict';

import VueFlashMessage from 'vue-flash-message';
import VueCookie from 'vue-cookies';
import {library} from '@fortawesome/fontawesome-svg-core';

/* import font awesome icon component */
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

/* import specific icons */
import {faGear, faSignIn, faSignOut, faExternalLinkSquare, faStar, faTrash} from '@fortawesome/free-solid-svg-icons';
import {faGithub} from '@fortawesome/free-brands-svg-icons';


Vue.options.delimiters = ['[[', ']]'];
Vue.use(VueFlashMessage, {
  messageOptions: {
    timeout: 1500,
    important: true,
  },
});
Vue.use(VueCookie);

/* add icons to the library */
library.add(faGear, faSignIn, faSignOut, faExternalLinkSquare, faGithub, faStar, faTrash);

/* add font awesome icon component */
Vue.component('FontAwesomeIcon', FontAwesomeIcon);
new Vue({
  el: '#menu',
  methods: {
    changeLanguage: function() {
      document.getElementById('language-form').submit();
    },
  },
});
