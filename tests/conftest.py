import pytest

# First charge the .env file to get the environment variables
from dotenv import load_dotenv
load_dotenv()

from backend import app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def song():
    song = {
        "id": 200,
        "title": "Bohemian Rhapsody",
        "lyrics": "Bohemian Rhapsody is a song by the British rock band Queen. It was written by Freddie Mercury for the band's debut studio album, A Night at the Opera (1975). The song is a six-minute suite that combines elements of rock, opera, and ballad."
    }
    return dict(song)