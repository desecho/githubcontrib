import { describe, expect, it } from "vitest";

import { formatDate, getUrl, githubAvatarUrl } from "../helpers";

describe("helpers", () => {
    it("builds backend urls", () => {
        expect(getUrl("users/")).toBe("http://localhost:8000/users/");
    });

    it("formats dates", () => {
        expect(formatDate("2017-04-10T13:57:41-04:00")).toContain("2017");
    });

    it("builds GitHub avatar urls", () => {
        expect(githubAvatarUrl("neo")).toBe(
            "https://github.com/neo.png?size=160",
        );
    });
});
