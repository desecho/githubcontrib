from datetime import datetime

from dateutil.tz import tzoffset

commits_jieter = [
    {
        "url": "https://github.com/jieter/django-tables2/commit/360b29c5948c1f9bada618c30897e380e21a4f0a",
        "date": datetime(2017, 3, 6, 13, 30, 58, tzinfo=tzoffset(None, 3600)),
        "message": "Regression fix - revert commit 05d8d1d260fe1cfe61a89ef0ae09c78513022f3c (#423)",
    }
]

commits_python_social_auth = [
    {
        "url": "https://github.com/python-social-auth/social-core/commit/ca68410f4cc6bd017919b2cf4a1b31b834b8fe6b",
        "date": datetime(2017, 4, 10, 13, 57, 41, tzinfo=tzoffset(None, -14400)),
        "message": "Fix typos in readme",
    },
    {
        "url": "https://github.com/python-social-auth/social-core/commit/ab19dc49a5366ae4f917bed2a7bfddce7e7b003f",
        "date": datetime(2017, 4, 16, 4, 39, 32, tzinfo=tzoffset(None, -14400)),
        "message": "Speed up authorization process for VKAppOAuth2\n"
        "Use first api request provided immediately instead of creating a new one.",
    },
]

repo = "username/project"

username = "username"
