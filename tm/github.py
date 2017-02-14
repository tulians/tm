# Implemented using:
# --> http://docs.python-requests.org/
# --> https://developer.github.com/v3/
# --> https://developer.github.com/v3/repos/contents/

import json
import requests

api_url = "https://api.github.com/"
api_content_url = api_url + "repos/{0}/{1}/contents/{2}"


class Github(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.req = requests.get(api_url + "user",
                                auth=(username, password))

    def get_file(self, repository, path, payload=None):
        url = api_content_url.format(self.username, repository, path)
        return requests.get(url, params=payload)

    def create_file(self, repository, path, commit_message, content, file_name,
                    branch=None, name=None, email=None):
        payload = {
            "message": commit_message,
            "commiter": {
                "name": name,
                "email": email
            },
            "content": content
        }
        url = (api_content_url.format(self.username, repository, path) +
               file_name)
        print url
        return requests.put(url, json=payload, auth=(self.username,
                                                     self.password))
