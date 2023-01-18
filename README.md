# IPSec-termination-node-throughput
To check the min,max,avg of all the IPSec termination nodes


Help:
./ipsec_node.py --help
usage: ipsec_node.py [-h] [-t1 T1SECRET]

Checking IpSec termination node status

optional arguments:
  -h, --help            show this help message and exit
  -t1 T1SECRET, --T1Secret T1SECRET
                        Input secret file in .yml format for the tenant(T1)
(base) dsubashchand@M-JY4VCQYQ64 IPSec node BW % 

Input CLI:
./ipsec_node.py -t1 T1-secret.yml

Output:
+--------------------+----------------+--------------------+----------------------------+----------------+
| SPN Name           | Min Throughput | Average Throughput | 90th percentile Throughput | Max Throughput |
+====================+================+====================+============================+================+
| us-southwest-pecan | 1.2            | 131.42             | 312.81                     | 474.8          |
+--------------------+----------------+--------------------+----------------------------+----------------+
| us-east-cottonwood | 5.57           | 79.84              | 159.54                     | 319.98         |
+--------------------+----------------+--------------------+----------------------------+----------------+
| us-central-kiwi    | 0.03           | 0.05               | 0.08                       | 0.12           |
+--------------------+----------------+--------------------+----------------------------+----------------+
