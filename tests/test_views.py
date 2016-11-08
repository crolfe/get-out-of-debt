from rest_framework import status


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == status.HTTP_200_OK
