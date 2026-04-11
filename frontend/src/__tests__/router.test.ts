import { describe, expect, it, vi } from "vitest";

import { router } from "../router";

vi.mock("../views/AboutView.vue", () => ({ default: {} }));
vi.mock("../views/AccountView.vue", () => ({ default: {} }));
vi.mock("../views/AuthCallbackView.vue", () => ({ default: {} }));
vi.mock("../views/ContributionsView.vue", () => ({ default: {} }));
vi.mock("../views/LoginView.vue", () => ({ default: {} }));
vi.mock("../views/LogoutView.vue", () => ({ default: {} }));
vi.mock("../views/RepositoriesView.vue", () => ({ default: {} }));
vi.mock("../views/UsersView.vue", () => ({ default: {} }));

describe("router", () => {
    it("exposes the authenticated my contributions page", () => {
        const route = router
            .getRoutes()
            .find((item) => item.path === "/my-contributions");

        expect(route).toBeDefined();
        expect(route?.props.default).toEqual({ own: true });
    });
});
