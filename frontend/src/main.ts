import "x-axios-progress-bar/dist/nprogress.css";
import "vue-toast-notification/dist/theme-sugar.css";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "./styles/styles.scss";

import { createPinia } from "pinia";
import piniaPersist from "pinia-plugin-persist";
import { createApp } from "vue";
import { createGtag } from "vue-gtag";
import VueToast from "vue-toast-notification";
import { loadProgressBar } from "x-axios-progress-bar";

import App from "./App.vue";
import { initAxios } from "./axios";
import vuetify from "./plugins/vuetify";
import { router } from "./router";

loadProgressBar();

const pinia = createPinia();
pinia.use(piniaPersist);

const app = createApp(App);
const googleAnalyticsId = import.meta.env.VITE_GOOGLE_ANALYTICS_ID as
    | string
    | undefined;

app.use(vuetify).use(pinia).use(router).use(VueToast, {
    position: "top-right",
    duration: 1800,
});

if (googleAnalyticsId !== undefined && googleAnalyticsId !== "") {
    app.use(
        createGtag({
            tagId: googleAnalyticsId,
            pageTracker: {
                router,
            },
        }),
    );
}

app.mount("#app");
initAxios();
