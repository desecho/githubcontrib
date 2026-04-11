import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

import { createVuetify } from "vuetify";

export default createVuetify({
    defaults: {
        VBtn: {
            rounded: 0,
        },
        VCard: {
            rounded: 0,
        },
    },
    theme: {
        defaultTheme: "light",
        themes: {
            light: {
                colors: {
                    primary: "#1f7a4d",
                    secondary: "#4a5568",
                    accent: "#0f766e",
                    error: "#c2410c",
                    info: "#256d85",
                    success: "#2f855a",
                    warning: "#b7791f",
                    background: "#f7f9fb",
                    surface: "#ffffff",
                },
            },
        },
    },
});
