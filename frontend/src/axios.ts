import axios from "axios";

import type { AxiosError, InternalAxiosRequestConfig } from "axios";
import type { ApiErrorData } from "./types";

import { getBackendUrl } from "./helpers";
import { router } from "./router";
import { useAuthStore } from "./stores/auth";

let responseInterceptor: number | null = null;

interface RetryConfig extends InternalAxiosRequestConfig {
    _retry?: boolean;
}

export function initAxios(): void {
    axios.defaults.baseURL = getBackendUrl();
    axios.defaults.headers.common["Content-Type"] =
        "application/json; charset=UTF-8";
    axios.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";

    const { user } = useAuthStore();
    if (user.isLoggedIn && user.accessToken !== undefined) {
        axios.defaults.headers.common.Authorization = `Bearer ${user.accessToken}`;
    } else {
        delete axios.defaults.headers.common.Authorization;
    }

    if (responseInterceptor !== null) {
        axios.interceptors.response.eject(responseInterceptor);
    }

    responseInterceptor = axios.interceptors.response.use(
        (response) => response,
        async (error: AxiosError<ApiErrorData>) => {
            if (error.response?.status === 401) {
                const auth = useAuthStore();
                const config = error.config as RetryConfig | undefined;
                if (
                    auth.user.isLoggedIn &&
                    config !== undefined &&
                    config._retry !== true
                ) {
                    config._retry = true;
                    await auth.refreshToken();
                    if (auth.user.accessToken !== undefined) {
                        config.headers.Authorization = `Bearer ${auth.user.accessToken}`;
                    }
                    return axios(config);
                }
                auth.logout(false);
                void router.push("/login");
            }
            return Promise.reject(error);
        },
    );
}
