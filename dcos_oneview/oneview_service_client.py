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

import requests
import json
import subprocess
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# supress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

master_uri = ''
service_endpoint = '/service/hpe-oneview'
status_uri = '/ov2mesos/status'
capacity_uri = '/ov2mesos/capacity'
addnode_uri = '/ov2mesos/addnode'
removenode_uri = '/ov2mesos/removenode'

dcos_auth_token = ''

def get_master_url():
    proc = subprocess.Popen('dcos config show core.dcos_url',shell=True, stdout=subprocess.PIPE)
    uri = proc.stdout.read()
    uri_str = uri.decode('utf-8')
    global master_uri
    master_uri=uri_str.rstrip()
    # get the auth token
    get_auth_token()

def get_auth_token():
    proc = subprocess.Popen('dcos config show core.dcos_acs_token', shell=True, stdout=subprocess.PIPE)
    token = proc.stdout.read()
    token_str = token.decode('utf-8')
    global dcos_auth_token
    dcos_auth_token = token_str.rstrip()

def get_base_service():
    get_master_url()
    url = master_uri+service_endpoint
    response = requests.get(url, verify=False, headers={'Authorization': 'token='+dcos_auth_token})
    if (response.ok):
        format_response(response.json(),'endpoint')
        return
    else:
        response.raise_for_status()

def get_status():
    get_master_url()
    url = master_uri+service_endpoint+status_uri
    response = requests.get(url, verify=False, headers={'Authorization': 'token='+dcos_auth_token})
    if (response.status_code == 200):
        format_response(response.json(), 'status')
        return
    else:
        response.raise_for_status()

def format_response(resp_json, method):
    if method == 'endpoint':
        print("I am {:<10}".format(resp_json['status']))

    if method == 'capacity':
        print("Available Capacity : ",len(resp_json['available']))
        print("{:<25} {:<35}".format('Name', 'Model'))
        for row in resp_json['available']:
            print("{:<25} {:<35}".format(row['name'], row['model']))

    if method == 'add_node':
        print(resp_json['status'])
        if 'requested' in resp_json:
            print('Building %d servers'%(resp_json['requested']))
            print("{:<20} {:<15} {:<40}".format('Status', 'Complete %', 'ServerProfile URI'))
            for row in resp_json['profileList']:
                print("{:<20} {:<15} {:<40}".format(row['status'], row['percentComplete'], row['serverProfileUri']))

    if method == 'remove_node':
        print(resp_json['status'])
        if 'requested' in resp_json:
            print('Removing %d servers'%(resp_json['requested']))
            print("{:<20} {:<30} {:<40}".format('Name', 'URI', 'ServerHW URI'))
            for row in resp_json['profiles']:
                print("{:<20} {:<30} {:<40}".format(row['name'], row['uri'], row['serverHardwareUri']))

    if method == 'status':
        if int(resp_json['Count']) == 0:
            print("All tasks complete")
        else:
            print("Outstanding actions # ", resp_json['Count'])
            print("{:<20} {:<15} {:<45}".format('Status', 'Complete %', 'ServerProfile URI'))
            for row in resp_json['profile']:
                print("{:<20} {:<15} {:<45}".format(row['status'], row['percentComplete'], row['serverProfileUri']))

def get_capacity():
    get_master_url()
    url = master_uri+service_endpoint+capacity_uri

    response = requests.get(url, verify=False, headers={'Authorization': 'token='+dcos_auth_token})
    if (response.status_code == 200):
        format_response(response.json(),'capacity')
        return
    else:
        response.raise_for_status()

def add_node(nos):
    get_master_url()
    url = master_uri+service_endpoint+addnode_uri

    data = { "count" : nos }
    data_json = json.dumps(data)
    response = requests.post(url, verify=False, data=data_json, headers={'Content-Type': 'application/json','Authorization': 'token='+dcos_auth_token})

    if (response.status_code == 200):
        format_response(response.json(),'add_node')
        return
    else:
        response.raise_for_status()

def remove_node(nos):
    get_master_url()
    url = master_uri+service_endpoint+removenode_uri

    data = { "count" : nos }
    data_json = json.dumps(data)
    response = requests.post(url, verify=False, data=data_json, headers={'Content-Type': 'application/json','Authorization': 'token='+dcos_auth_token})

    if (response.status_code == 200):
        format_response(response.json(), 'remove_node')
        return
    else:
        response.raise_for_status()
