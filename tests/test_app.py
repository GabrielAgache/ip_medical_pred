import sys
import json
sys.path.append('..')


def test_root(test_client):
    response = test_client.get('/')
    assert response.data == b'Hello from flask'


def test_get(test_client):
    rv = test_client.get('/get?up=100&down=30&info=weight')
    data_dic = json.loads(rv.data, encoding='UTF-8')
    assert isinstance(data_dic, list)
    rv = test_client.get('/get?up=7&down=3&info=water')
    data_dic = json.loads(rv.data, encoding='UTF-8')
    assert isinstance(data_dic, list)
    rv = test_client.get('/get?up=2500&down=1500&info=calories')
    data_dic = json.loads(rv.data, encoding='UTF-8')
    assert isinstance(data_dic, list)
    rv = test_client.get('/get?max=190&min=60&info=pulse')
    data_dic = json.loads(rv.data, encoding='UTF-8')
    assert isinstance(data_dic, list)
    rv = test_client.get('/get?day=07-05-2016&info=day')
    assert rv is not None
    rv = test_client.get('/get?day=07-05-2016&id=45910&info=all')
    assert rv is not None


# def test_predict(test_client):
#     data = {
#         "patient_id": 45666,
#         "pulse": 82,
#         "temperature": 40,
#         "today": "19-11-2016",
#         "weight": 80,
#         "water": 3
#     }
#     response = test_client.post('/predict_hd', json=data)
#     json = response.get_json()
#     assert json is not None


def test_send(test_client):
    data = {
        "patient_id": 45666,
        "pulse": 82,
        "temperature": 40,
        "today": "19-11-2016",
        "weight": 80,
        "water": 3
    }
    response = test_client.post('/send_data', json=data)
    data_dic = json.loads(response.data, encoding='UTF-8')

    assert data_dic.get(
        'today') is not None or 'Error!' in data_dic.get('message')
    assert data_dic.get(
        'patient_id') is not None or 'Error!' in data_dic.get('message')


def test_anomaly(test_client):
    data = {
        "patient_id": 45666,
        "pulse": 82,
        "temperature": 40,
        "today": "19-11-2016",
        "weight": 80,
        "water": 3
    }
    response = test_client.post('/verify_anomaly', json=data)
    data_dic = json.loads(response.data, encoding='UTF-8')

    for i in data_dic:
        assert isinstance(data_dic[i], str)
