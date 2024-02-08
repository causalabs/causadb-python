import os
from dotenv import load_dotenv
load_dotenv()


CAUSADB_URL = os.getenv("CAUSADB_URL", "https://api.causadb.com/v1")
