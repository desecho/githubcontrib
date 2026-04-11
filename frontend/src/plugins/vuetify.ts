import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

import { createVuetify } from "vuetify";

export default createVuetify({
    defaults: {
        VBtn: {
            rounded: "sm",
        },
        VCard: {
            rounded: "sm",
        },
        VExpansionPanel: {
            elevation: 0,
        },
        VTextField: {
            color: "primary",
        },
        VList: {
            density: "comfortable",
        },
    },
    theme: {
        defaultTheme: "light",
        themes: {
            light: {
                colors: {
                    primary: "#1a7f37",
                    secondary: "#57606a",
                    accent: "#0969da",
                    error: "#cf222e",
                    info: "#0969da",
                    success: "#1a7f37",
                    warning: "#9a6700",
                    background: "#f6f8fa",
                    surface: "#ffffff",
                    "on-background": "#24292f",
                    "on-surface": "#24292f",
                },
            },
        },
    },
});
