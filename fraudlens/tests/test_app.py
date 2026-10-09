import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from app import create_app
from ml import Engine

@pytest.fixture
def client(tmp_path):
    return create_app(str(tmp_path/'test.db')).test_client()

NORMAL=dict(amount=350,hour=14,distance_km=3,transactions_1h=1,account_age_days=800,device_new=0)

def test_prediction_persistence_feedback(client):
    r=client.post('/api/predict',json=NORMAL)
    assert r.status_code==200
    d=r.get_json(); assert 0<=d['fraud_probability']<=1
    assert len(d['reasons'])==3
    assert client.post(f"/api/transactions/{d['id']}/feedback",json={'label':'fraud'}).status_code==200
    assert client.get('/api/transactions').get_json()[0]['feedback']=='fraud'

@pytest.mark.parametrize('body',[{},[],None,{**NORMAL,'amount':-1},{**NORMAL,'hour':24},{**NORMAL,'device_new':.5},{**NORMAL,'amount':'nan'}])
def test_invalid(client,body):
    assert client.post('/api/predict',json=body).status_code==400
    assert client.get('/api/transactions').get_json()==[]

def test_batch_atomic(client):
    import io
    header='amount,hour,distance_km,transactions_1h,account_age_days,device_new\n'
    valid=header+'350,14,3,1,800,0\n'
    bad=valid+'-5,14,3,1,800,0\n'
    assert client.post('/api/batch',data={'file':(io.BytesIO(bad.encode()),'test.csv')}).status_code==400
    assert client.get('/api/transactions').get_json()==[]
    assert client.post('/api/batch',data={'file':(io.BytesIO(valid.encode()),'test.csv')}).get_json()['count']==1

def test_pages(client):
    assert client.get('/').status_code==200
    assert client.get('/static/app.js').status_code==200
    assert client.get('/api/health').get_json()['status']=='ok'
    assert client.post('/api/transactions/999/feedback',json={'label':'fraud'}).status_code==404

def test_repeatable_and_sensitive():
    e=Engine(); a=e.score(NORMAL)
    assert a==e.score(NORMAL)
    b=e.score(dict(amount=12000,hour=2,distance_km=700,transactions_1h=9,account_age_days=12,device_new=1))
    assert b['fraud_probability']>a['fraud_probability']
