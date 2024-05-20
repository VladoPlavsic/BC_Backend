import requests as re
from requests import Session, Request
import io

class IPFSBase:

    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIzMDg1NDE0NC03MTA2LTRkNzUtOTMxZC03ZWJkYzk1OGFjNzciLCJlbWFpbCI6InBsYXZzaWN2bGFkbzk4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI0NWYxNzc1MjYyZmI0NTMxNDg0MCIsInNjb3BlZEtleVNlY3JldCI6IjZjNzEwZTRiNjBkMTkxNjJhYjIzMGExYTM0N2I0ODEzY2E3N2Q5MGFmNTVmYmZiZWI5N2MzMjEyYjBmM2U3YmEiLCJpYXQiOjE3MTI1ODk3NzR9.nQDZ8C4HCRrr6Drn1kirJU-uny3xBOau5fIhXQ5G7-w"
    api1_key = '3a6cfc8248fb0e344795'
    api1_secret = "df5d8a05e90835929717ccf6094b84cdaf51a770077b683f72f3517d521900ba"

    """
    curl --request GET 	--url https://api.pinata.cloud/data/testAuthentication 	--header 'accept: application/json' 	--header 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIzMDg1NDE0NC03MTA2LTRkNzUtOTMxZC03ZWJkYzk1OGFjNzciLCJlbWFpbCI6InBsYXZzaWN2bGFkbzk4QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI0NWYxNzc1MjYyZmI0NTMxNDg0MCIsInNjb3BlZEtleVNlY3JldCI6IjZjNzEwZTRiNjBkMTkxNjJhYjIzMGExYTM0N2I0ODEzY2E3N2Q5MGFmNTVmYmZiZWI5N2MzMjEyYjBmM2U3YmEiLCJpYXQiOjE3MTI1ODk3NzR9.nQDZ8C4HCRrr6Drn1kirJU-uny3xBOau5fIhXQ5G7-w'
    """

    def __init__(self):
        self.url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    def upload(self, content, filename): 
        # directory is the abs path of dir
        content = io.BytesIO(content)
        files = []
        files.append(('pinataMetadata', (None, '{"name":"' + filename + '"}')))
        ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
            'pinata_api_key': f"{self.api1_key}",
            'pinata_secret_api_key': f"{self.api1_secret}"
        }
        files.append(('file', ("f1", content)))
        request = Request(
            'POST',
            ipfs_url,
            headers=headers,
            files=files
        ).prepare()
        response = Session().send(request)
        return response.json()

    # def upload(self, content, filename):
    #     content = io.BytesIO(content)
    #     response = re.post(self.url, files={filename: content}, headers={
    #         'Content-Type': "multipart/form-data;",
    #         'Authorization': f"Bearer {self.api_key}"}
    #     )
    #     return response.content

    def download(self, hash):
        print("hello")
        # url = "http://localhost:5001/api/v0"
        url = f"https://aquamarine-hollow-beetle-189.mypinata.cloud/ipfs/{hash}?pinataGatewayToken=H3RbK1tZmDFpW2twLHDkiBlUKm8MFyN74zXRcX1KgP2hoX-fU9r4y9eSIrngO-J9"
        # url = url + f'/cat?arg={hash}'
        response = re.get(url)
        print(response)
        return response.content