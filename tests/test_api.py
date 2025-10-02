import json

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200


def test_count(client):
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json['length'] == 20


def test_data_contains_10_songs(client):
    res = client.get("/song")
    assert len(res.json) == 20


def test_get_song(client):
    res = client.get("/song")
    assert res.status_code == 200
    assert len(res.json) == 20


def test_get_songs_check_content_type_equals_json(client):
    res = client.get("/song")
    assert res.headers["Content-Type"] == "application/json"


def test_get_song_by_id(client):
    id_delete = 2
    res = client.get(f'/song/{id_delete}')
    assert res.status_code == 200
    assert res.json['id'] == id_delete

    res = client.get('/song/404')
    assert res.status_code == 404


def test_songs_json_is_not_empty(client):
    res = client.get("/song")
    assert len(res.json) > 0


def test_post_song(song, client):
    # create a brand new song to upload
    res = client.post("/song", data=json.dumps(song),
                      content_type="application/json")
    assert res.status_code == 201
    assert res.json['id'] == song['id']
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json['length'] == 21

def test_post_song_duplicate(song, client):
    # create a brand new song to upload
    res = client.post("/song", data=json.dumps(song),
                      content_type="application/json")
    assert res.status_code == 302
    assert res.json['Message'] == f"song with id {song['id']} already present"

def test_update_song_by_id(client, song):
    id = '2'
    res = client.get(f'/song/{id}')
    res_song = res.json
    assert res_song['id'] == 2
    res_state = res_song["title"]
    new_state = "*" + res_state
    res_song["title"] = new_state
    res = client.put(f'/song/{id}', data=json.dumps(res_song),
                     content_type="application/json")
    res.status_code == 200
    res = client.get(f'/song/{id}')
    assert res.json['title'] == new_state

def test_delete_song_by_id(client):
    res = client.get("/count")
    assert res.json['length'] == 21
    res = client.delete("/song/1")
    assert res.status_code == 204
    res = client.get("/count")
    assert res.json['length'] == 20
    res = client.delete("/song/100")
    assert res.status_code == 404



