import requests as re
import io

class IPFSBase:
    def __init__(self):
        self.url = "http://localhost:5001/api/v0"

    def upload(self, content, filename):
        url = self.url + '/add'
        content = io.BytesIO(content)
        response = re.post(url, files={filename: content})
        return response.content

    def download(self, hash):
        url = self.url + f'/cat?arg={hash}'
        response = re.post(url)
        return response.content