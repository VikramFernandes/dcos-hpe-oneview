import requests
import sys
import json

#BASE_URL = 'http://master.mesos/service/hpe-oneview'
BASE_URL = 'http://10.44.193.12'
PORT = ':5000'
STATUS_URL = '/ov2mesos/status'
CAPACITY_URL = '/ov2mesos/capacity'
ADD_NODE_URL = '/ov2mesos/addnode'
REMOVE_NODE_URL = '/ov2mesos/removenode'

def get_base_service():
    url = BASE_URL+PORT
    response = requests.get(url)
    if (response.ok):
        print("get base service response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def get_status():
    url = BASE_URL+PORT+STATUS_URL
    response = requests.get(url)
    print("response in status code: ", response.status_code)
    if (response.status_code == 200):
        print("get status response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def get_capacity():
    url = BASE_URL+PORT+CAPACITY_URL
    response = requests.get(url)
    if (response.status_code == 200):
        print("get capacity response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def add_node(nos):
    url = BASE_URL+PORT+ADD_NODE_URL

    data = { "count" : nos }
    data_json = json.dumps(data)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=data_json, headers=headers)

    if (response.status_code == 200):
        print("add node response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def remove_node(nos):
    url = BASE_URL+PORT+REMOVE_NODE_URL

    data = { "count" : nos }
    data_json = json.dumps(data)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=data_json, headers=headers)

    if (response.status_code == 200):
        print("remove node response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

#if __name__ == "__main__":
#    #get_base_service()
#    #get_status()
#    get_capacity()
#    add_node("1")
#    #remove_node("1")
#    sys.exit(1)
