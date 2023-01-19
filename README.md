# IPSec-termination-node-throughput
To check the min,max,avg,90th percentils of all the IPSec termination nodes. Gives output in stdout,csv and json file formats.


Help:
(base) dsubashchand@M-JY4VCQYQ64 IPSec node BW % ./ipsec_node.py --help
usage: ipsec_node.py [-h] [-t1 T1SECRET] [-timerange TIMERANGE]

Checking IpSec termination node status

optional arguments:
  -h, --help            show this help message and exit
  -t1 T1SECRET, --T1Secret T1SECRET
                        Input secret file in .yml format for the tenant(T1)
  -timerange TIMERANGE, --TimeRange TIMERANGE
                        Time range in hours for which data needs to be fetched
(base) dsubashchand@M-JY4VCQYQ64 IPSec node BW % ./ipsec_node.py       
--------------------------------
Script Execution Progress: 
--------------------------------
Login to TSG ID 1228584868 successful
+--------------------+----------------+--------------------+----------------------------+----------------+
| SPN Name           | Min Throughput | Average Throughput | 90th percentile Throughput | Max Throughput |
+====================+================+====================+============================+================+
| us-southwest-pecan | 1.23           | 386.66             | 846.36                     | 1148.03        |
+--------------------+----------------+--------------------+----------------------------+----------------+
| us-east-cottonwood | 313.66         | 537.84             | 732.17                     | 763.25         |
+--------------------+----------------+--------------------+----------------------------+----------------+
| us-central-kiwi    | 0.0            | 0.0                | 0.0                        | 0.0            |
+--------------------+----------------+--------------------+----------------------------+----------------+
(base) dsubashchand@M-JY4VCQYQ64 IPSec node BW % ./ipsec_node.py -t1 T1-secret.yml -timerange 2
--------------------------------
Script Execution Progress: 
--------------------------------
Login to TSG ID 1228584868 successful
+--------------------+----------------+--------------------+----------------------------+----------------+
| SPN Name           | Min Throughput | Average Throughput | 90th percentile Throughput | Max Throughput |
+====================+================+====================+============================+================+
| us-southwest-pecan | 1.23           | 296.31             | 802.32                     | 1148.03        |
+--------------------+----------------+--------------------+----------------------------+----------------+
| us-east-cottonwood | 22.33          | 386.72             | 709.78                     | 763.25         |
+--------------------+----------------+--------------------+----------------------------+----------------+
| us-central-kiwi    | 0.0            | 0.0                | 0.0                        | 0.0            |
+--------------------+----------------+--------------------+----------------------------+----------------+
(base) dsubashchand@M-JY4VCQYQ64 IPSec node BW % cat spn.csv 
SPN Name,Min Throughput,Average Throughput,90th percentile Throughput,Max Throughput
us-southwest-pecan,1.23,296.31,802.32,1148.03
us-east-cottonwood,22.33,386.72,709.78,763.25
us-central-kiwi,0.0,0.0,0.0,0.0
(base) dsubashchand@M-JY4VCQYQ64 IPSec node BW % cat spn.json
{
    "0": {
        "SPN Name": "us-southwest-pecan",
        "Min Throughput": "1.23",
        "Average Throughput": "296.31",
        "90th percentile Throughput": "802.32",
        "Max Throughput": "1148.03"
    },
    "1": {
        "SPN Name": "us-east-cottonwood",
        "Min Throughput": "22.33",
        "Average Throughput": "386.72",
        "90th percentile Throughput": "709.78",
        "Max Throughput": "763.25"
    },
    "2": {
        "SPN Name": "us-central-kiwi",
        "Min Throughput": "0.0",
        "Average Throughput": "0.0",
        "90th percentile Throughput": "0.0",
        "Max Throughput": "0.0"
    }
}%                                                                                                                                                                                           
(base) dsubashchand@M-JY4VCQYQ64 IPSec node BW % 
