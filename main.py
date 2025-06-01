import os
from dotenv import load_dotenv
from bot import Bot


client = Bot()


if __name__ == "__main__":
    load_dotenv()
    client.run(os.getenv('TOKEN'))
