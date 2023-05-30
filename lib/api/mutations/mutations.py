import base64
import json

from ariadne import MutationType

from lib.ipfs.base import IPFSBase
from lib.smart_contracts.image_metadata import ImageMetadata

mutations = MutationType()

def resolve_upload_image(_obj, _info, image, filename):
    b64file = image.split(',')[1]
    ipfs_response = upload_file(b64file, filename)
    key, metadata = prepare_metadata(ipfs_response)
    save_metadata(key, metadata)
    return  {"filename": filename}

def upload_file(b64file, filename):
    client = IPFSBase()
    file = base64.b64decode(b64file)
    return client.upload(file, filename)

def prepare_metadata(ipfs_response):
    response = json.loads(ipfs_response)
    print(response)
    return [response["Name"], {
        "ipfs_address": f'{response["Hash"]}',
        "size": int(response["Size"])
    }]

def save_metadata(key, metadata):
    client = ImageMetadata()
    client.set(key, metadata)
