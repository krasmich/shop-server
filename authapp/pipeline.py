import requests


def get_repos_list(backend, user, response, *args, **kwargs):
    resp = requests.get('https://api.github.com/repositories', headers={
        'Authorization': 'token %s' % response['access_token']
    })
    json = resp.json()
    repos = [r['name'] for r in json]
    user.shopuserprofile.tagline = ','.join(repos)
    user.save()
