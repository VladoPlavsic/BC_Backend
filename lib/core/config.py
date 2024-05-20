from dotenv import load_dotenv
import os

load_dotenv()

CHAIN_ID = os.getenv("CHAIN_ID")
ROOT_ACCOUNT = os.getenv("ROOT_ACCOUNT")
PORT = os.getenv("PORT")
