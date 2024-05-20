import base64
import json

from ariadne import MutationType

from lib.ipfs.base import IPFSBase

from lib.client.contracts.image_metadata import ImageMetadata
from lib.client.contracts.student_info import StudentInfo
from lib.client.contracts.semaphore import Semaphore

from lib.client.accounts.account import Account


CONTRACTS = {
    "studentInfo": StudentInfo,
    "semaphore": Semaphore,
    "imageMetadata": ImageMetadata
}

mutations = MutationType()

def resolve_upload_image(_obj, _info, image, filename, account, password):
    b64file = image.split(',')[1]
    ipfs_response = upload_file(b64file, filename)
    key, metadata = prepare_metadata(ipfs_response, filename)
    save_metadata(key, metadata, account, password)
    return  {"filename": filename}

def upload_file(b64file, filename):
    client = IPFSBase()
    file = base64.b64decode(b64file)
    return client.upload(file, filename)

def prepare_metadata(response, filename):
    return [filename, {
        "ipfs_address": f'{response["IpfsHash"]}',
        "size": int(response["PinSize"])
    }]

def save_metadata(key, metadata, account_address, password):
    client = ImageMetadata(account_address)
    client.set(key, metadata, password)

# Student info (LAB-2)
def resolve_add_student(_obj, _info, firstName, lastName, birthday, account, password):
    client = StudentInfo(account)
    client.set({
         "student_first_name": firstName,
         "student_last_name": lastName,
         "birthday": birthday 
        }, password)
    return True

# 
# Account administrating
def resolve_create_account(_obj, _info, password):
    account = Account()
    return account.create_account(password)

def resolve_send_wei(_obj, _info, from_, to, amount, password):
    account = Account()
    return account.send_wei(from_, to, amount, password)

def resolve_deploy_contract(_obj, _info, contract, accountAddress, password):
    contract = CONTRACTS[contract]
    contract = contract(accountAddress)
    return contract.deploy_contract(password)



