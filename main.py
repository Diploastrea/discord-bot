import os
from dotenv import load_dotenv
from client import Client


client = Client()


if __name__ == "__main__":
    load_dotenv()
    client.run(os.getenv('TOKEN'))
