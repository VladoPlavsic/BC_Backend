import base64
from ariadne import QueryType

from lib.ipfs.base import IPFSBase

from lib.client.contracts.image_metadata import ImageMetadata
from lib.client.contracts.student_info import StudentInfo
from lib.client.contracts.sticks import Sticks
from lib.client.contracts.semaphore import Semaphore

from lib.client.accounts.account import Account


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

def resolve_get_students(_obj, _info):
    client = StudentInfo()
    return client.list()

def resolve_can_join(_obj, _info):
    client = Sticks()
    return client.can_join()

def resolve_get_accounts(_obj, _info):
    account = Account()
    return account.get_accounts()

def resolve_get_balance(_obj, _info, address):
    account = Account()
    return account.get_balance(address)

def resolve_check_transaction(_obj, _info, transactionHash):
    account = Account()
    return account.check_transaction(transactionHash)

def resolve_change_light(_obj, _info):
    semaphore = Semaphore("0x2eE4B180678Ee32A88E10BBE7C4Efe4a6F9b70De")
    return semaphore.change_light()

def resolve_get_current_light_state(_obj, _info):
    semaphore = Semaphore()
    return semaphore.get_current_state()