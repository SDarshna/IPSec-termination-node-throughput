#!/usr/bin/env python3

import prisma_sase
import io
import requests
import json
import os
import termtables as tt
import yaml
import argparse
import pandas as pd
import time
import csv
import numpy as np


def sdk_login_to_controller(filepath):
    with open(filepath) as f:
        client_secret_dict = yaml.safe_load(f)
        client_id = client_secret_dict["client_id"]
        client_secret = client_secret_dict["client_secret"]
        tsg_id_str = client_secret_dict["scope"]
        global tsg
        tsg = tsg_id_str.split(":")[1]
        #print(client_id, client_secret, tsg)

    global sdk 
    sdk = prisma_sase.API(controller="https://sase.paloaltonetworks.com/", ssl_verify=False)
   
    sdk.interactive.login_secret(client_id, client_secret, tsg)
    print("--------------------------------")
    print("Script Execution Progress: ")
    print("--------------------------------")
    print("Login to TSG ID {} successful".format(tsg))

def create_csv_output_file(Header, RList):
    with open('spn.csv', mode='w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(Header)
        for Rec in RList:
            csvwriter.writerow(Rec)

def create_json_output_file():
    #create a dictionary
    data_dict = {}
 
    with open('spn.csv', encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        i=0
        for rows in csv_reader:
            key = i
            data_dict[key] = rows
            i += 1

    with open('spn.json', 'w', encoding = 'utf-8') as json_file_handler:
       json_file_handler.write(json.dumps(data_dict, indent = 4))
    

def get_epoch_time_range(t):
    now = time.time() * 1000 #milliseconds
    then = now - t*60*60*1000 #milliseconds
    return int(then),int(now)

def check_ipsec_term_node_bw(time_range):
    
    ipsec_node_bw_url="https://pa-us01.api.prismaaccess.com/api/sase/v2.0/resource/custom/query/remotenetworks/rn_spn_node_peak_bw_minute"

    header = {
            "prisma-tenant": tsg
        }
    sdk._session.headers.update(header)
    t1,t2 = get_epoch_time_range(time_range)
    #print(t1,t2)
    payload = {
        "filter":
        {
            "rules":
            [
                {"property":"event_time",
                "operator":"between",
                "values":[t1,t2]
                }
            ]
        },
        "histogram":
        {"property":"event_time",
        "enableEmptyInterval":True,
        "range":"minute",
        "value":"3"}
    }
    resp = sdk.rest_call(url=ipsec_node_bw_url, data=payload, method="POST")
    #print(resp.json())

    try:
        dataList = resp.json()["data"]
    except:
        print("No data found")
        exit(0)

    df1 = pd.DataFrame(dataList)
    df = df1.dropna()
   
    spns = df.spn_name.unique()
    RList = []
    Header = ["SPN Name", "Min Throughput", "Average Throughput","90th percentile Throughput", "Max Throughput"]
   
    for spn in spns:
        tmp = df[df.spn_name == spn]
        
        valdict = {}
        valdict["spn"] = spn
        #valdict["count"] = tmp.tunnel_throughput_greatest.count()
        valdict["min"] = round(tmp.tunnel_throughput_greatest.min(),2)
        valdict["avg"] = round(tmp.tunnel_throughput_greatest.mean(),2)
        valdict["90"] = round(tmp.tunnel_throughput_greatest.quantile(.9),2)
        valdict["max"] = round(tmp.tunnel_throughput_greatest.max(),2)
       
        valdict_rec = [valdict["spn"], valdict["min"],valdict["avg"],valdict["90"],valdict["max"]]
     
        
        RList.append(valdict_rec)
        #print(RList)
    
    create_csv_output_file(Header,RList)
    create_json_output_file()

    table_string = tt.to_string(RList, Header, style=tt.styles.ascii_thin_double)


    print(table_string)
    
def go():
    parser = argparse.ArgumentParser(description='Checking IpSec termination node status')
    parser.add_argument('-t1', '--T1Secret', help='Input secret file in .yml format for the tenant(T1) ',default="T1-secret.yml")
    parser.add_argument('-timerange', '--TimeRange', help='Time range in hours for which data needs to be fetched ',default=1)

    args = parser.parse_args()
    T1_secret_filepath = args.T1Secret
    time_range = int(args.TimeRange)
   

    #Pass the secret of 'from tenant' to login
    sdk_login_to_controller(T1_secret_filepath)

    check_ipsec_term_node_bw(time_range)



if __name__ == "__main__":
    go()