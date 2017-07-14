import requests
from dateutil import parser


def load_commit_data(username, repo):
    url = 'https://api.github.com/search/commits?q=author:%s+repo:%s+sort:author-date-desc' % (username, repo)
    r = requests.get(url, headers={'Accept': 'application/vnd.github.cloak-preview'});
    commits = r.json()['items']
    commit_data = []
    for commit in commits:
        url = commit['html_url']
        date = commit['commit']['committer']['date']
        date = parser.parse(date)
        message = commit['commit']['message']
        commit_data.append({
            'url': url,
            'date': date,
            'message': message,
        })
    return commit_data
