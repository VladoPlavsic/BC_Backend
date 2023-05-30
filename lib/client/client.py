from lib.smart_contracts.image_metadata import ImageMetadata


def main():
    client = ImageMetadata()
    client.deploy_contract()