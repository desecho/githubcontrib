import { jwtDecode } from "jwt-decode";
import { createRouter, createWebHistory } from "vue-router";

import type { JWTDecoded } from "./types";

import { useAuthStore } from "./stores/auth";
import AboutView from "./views/AboutView.vue";
import AccountView from "./views/AccountView.vue";
import AuthCallbackView from "./views/AuthCallbackView.vue";
import ContributionsView from "./views/ContributionsView.vue";
import LoginView from "./views/LoginView.vue";
import LogoutView from "./views/LogoutView.vue";
import RepositoriesView from "./views/RepositoriesView.vue";
import UsersView from "./views/UsersView.vue";

export const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: "active",
    routes: [
        { path: "/", component: UsersView },
        { path: "/users/:username", component: ContributionsView, props: true },
        {
            path: "/my-contributions",
            component: ContributionsView,
            props: { own: true },
        },
        { path: "/repositories", component: RepositoriesView },
        { path: "/account", component: AccountView },
        { path: "/about", component: AboutView },
        { path: "/login", component: LoginView },
        { path: "/logout", component: LogoutView },
        { path: "/auth/callback", component: AuthCallbackView },
    ],
});

router.beforeEach(async (to) => {
    const privatePages = ["/my-contributions", "/repositories", "/account"];
    const authRequired = privatePages.includes(to.path);
    const auth = useAuthStore();

    if (authRequired && !auth.user.isLoggedIn) {
        return "/login";
    }

    if (auth.user.isLoggedIn && auth.user.accessToken !== undefined) {
        const decodedToken = jwtDecode<JWTDecoded>(auth.user.accessToken);
        if (decodedToken.exp - Date.now() / 1000 < 30 * 60) {
            await auth.refreshToken();
        }
    }
});
