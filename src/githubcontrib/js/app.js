import VueToast from 'vue-toast-notification';
import VueCookie from 'vue-cookies';
import {createApp} from 'vue';

import {library} from '@fortawesome/fontawesome-svg-core';
/* import font awesome icon component */
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';


/* import specific icons */
import {faGear, faSignIn, faSignOut, faExternalLinkSquare, faStar, faTrash} from '@fortawesome/free-solid-svg-icons';
import {faGithub} from '@fortawesome/free-brands-svg-icons';


/* add icons to the library */
library.add(faGear, faSignIn, faSignOut, faExternalLinkSquare, faGithub, faStar, faTrash);

export function newApp(options) {
  const app = createApp(options);
  app.config.compilerOptions.delimiters = ['[[', ']]'];
  app.use(VueToast, {
    position: 'top-right',
    duration: 1500,
  },
  );
  app.use(VueCookie);

  /* add font awesome icon component */
  app.component('FontAwesomeIcon', FontAwesomeIcon);

  return app;
}
