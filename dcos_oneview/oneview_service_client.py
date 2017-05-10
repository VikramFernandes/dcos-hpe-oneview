###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

import requests, json, sys, os, subprocess

master_uri = ''
service_endpoint = '/service/hpe-oneview'
status_uri = '/ov2mesos/status'
capacity_uri = '/ov2mesos/capacity'
addnode_uri = '/ov2mesos/addnode'
removenode_uri = '/ov2mesos/removenode'

dcos_auth_token = ''

def get_master_url():
    proc = subprocess.Popen('dcos config show core.dcos_url', stdout=subprocess.PIPE)
    uri = proc.stdout.read()
    uri_str = uri.decode('utf-8')
    global master_uri
    master_uri=uri_str.rstrip()
    # get the auth token
    get_auth_token()

def get_auth_token():
    proc = subprocess.Popen('dcos config show core.dcos_acs_token', stdout=subprocess.PIPE)
    token = proc.stdout.read()
    token_str = token.decode('utf-8')
    global dcos_auth_token
    dcos_auth_token = token_str.rstrip()

def get_base_service():
    get_master_url()
    url = master_uri+service_endpoint
    response = requests.get(url)
    if (response.ok):
        sys.stdout("get base service response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def get_status():
    get_master_url()
    url = master_uri+service_endpoint+status_uri
    response = requests.get(url, verify=False, headers={'Authorization': 'token='+dcos_auth_token})
    sys.stdout("response in status code: ", response.status_code)
    if (response.status_code == 200):
        sys.stdout("get status response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def get_capacity():
    get_master_url()
    url = master_uri+service_endpoint+capacity_uri

    response = requests.get(url, verify=False, headers={'Authorization': 'token='+dcos_auth_token})
    if (response.status_code == 200):
        sys.stdout("get capacity response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def add_node(nos):
    get_master_url()
    url = master_uri+service_endpoint+addnode_uri

    data = { "count" : nos }
    data_json = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data_json, headers=headers)

    if (response.status_code == 200):
        sys.stdout("addnode response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

def remove_node(nos):
    get_master_url()
    url = master_uri+service_endpoint+removenode_uri

    data = { "count" : nos }
    data_json = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data_json, headers=headers)

    if (response.status_code == 200):
        sys.stdout("removenode response: ", response.json())
        return response.json()
    else:
        response.raise_for_status()

if __name__ == '__main__':
    get_capacity()