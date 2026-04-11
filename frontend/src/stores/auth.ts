import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { defineStore } from "pinia";

import type {
    AuthCallbackTokens,
    AuthUser,
    JWTDecoded,
    TokenRefreshData,
} from "../types";

import { initAxios } from "../axios";

function defaultUser(): AuthUser {
    return {
        isLoggedIn: false,
    };
}

export const useAuthStore = defineStore("auth", {
    state: () => ({
        user: defaultUser(),
    }),
    persist: {
        enabled: true,
        strategies: [
            {
                key: "user",
                storage: localStorage,
            },
        ],
    },
    actions: {
        setTokens(tokens: AuthCallbackTokens): void {
            this.user = {
                accessToken: tokens.access,
                refreshToken: tokens.refresh,
                username: tokens.username,
                isLoggedIn: true,
            };
            initAxios();
        },
        async refreshToken(): Promise<void> {
            if (this.user.refreshToken === undefined) {
                this.logout(false);
                return;
            }

            const decodedToken = jwtDecode<JWTDecoded>(this.user.refreshToken);
            if (decodedToken.exp < Date.now() / 1000) {
                this.logout(false);
                return;
            }

            const response = await axios.post<TokenRefreshData>(
                "token/refresh/",
                { refresh: this.user.refreshToken },
            );
            this.user.accessToken = response.data.access;
            initAxios();
        },
        logout(resetAxios = true): void {
            this.user = defaultUser();
            localStorage.removeItem("user");
            if (resetAxios) {
                initAxios();
            }
        },
    },
});
