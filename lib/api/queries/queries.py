import base64
from ariadne import QueryType

from lib.smart_contracts.image_metadata import ImageMetadata
from lib.ipfs.base import IPFSBase

queries = QueryType()

def resolve_get_images(_obj, _info):
    client = ImageMetadata()
    return client.get_all()

def resolve_get_image(_obj, _info, filename):
    client = ImageMetadata()
    ipfs = IPFSBase()
    ipfs_hash, _size = client.get(filename)
    response = base64.b64encode(ipfs.download(ipfs_hash)).decode("utf-8")
    return {"image": response}


