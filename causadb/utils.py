import os
from dotenv import load_dotenv
load_dotenv()


def get_causadb_url():
    return os.getenv("CAUSADB_URL", "https://api.causadb.com/v1")


def set_causadb_url(url: str):
    os.environ["CAUSADB_URL"] = url
