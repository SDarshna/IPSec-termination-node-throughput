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

def check_ipsec_term_node_bw():
    
    ipsec_node_bw_url="https://pa-us01.api.prismaaccess.com/api/sase/v2.0/resource/custom/query/remotenetworks/rn_spn_node_peak_bw_minute"

    header = {
            "prisma-tenant": tsg
        }
    sdk._session.headers.update(header)
    payload = {
        "filter":
        {
            "rules":
            [
                {"property":"event_time",
                "operator":"between",
                "values":[1673995954447,1673999553447]
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
    dataList = resp.json()["data"]
    
    df = pd.DataFrame(dataList)
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
         
        #print(valdict)

        #valdict_rec = [valdict]
        RList.append([valdict["spn"], valdict["min"],valdict["avg"],valdict["90"],valdict["max"]])
      

    table_string = tt.to_string(RList, Header, style=tt.styles.ascii_thin_double)
    print(table_string)
    
def go():
    parser = argparse.ArgumentParser(description='Checking IpSec termination node status')
    parser.add_argument('-t1', '--T1Secret', help='Input secret file in .yml format for the tenant(T1) ')
    
    args = parser.parse_args()
    T1_secret_filepath = args.T1Secret
   

    #Pass the secret of 'from tenant' to login
    sdk_login_to_controller(T1_secret_filepath)

    check_ipsec_term_node_bw()



if __name__ == "__main__":
    go()