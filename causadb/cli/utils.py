import os
import dotenv
dotenv.load_dotenv()


CAUSADB_API_URL = os.getenv("CAUSADB_API_URL", "https://api.causadb.com")
