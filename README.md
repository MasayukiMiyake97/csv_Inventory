# Ansible Dynamic Inventory サンプル（CSVファイル）
We are publishing a sample of Dynamic Inventory which loads CSV file as Inventory definition.  
This sample is realized by reading the CSV file describing the configuration information and returning a character string of JSON format to Ansible.  

---
CSVファイルをInventory定義として読み込む、Dynamic Inventoryのサンプルを公開しています。  
このサンプルは、構成情報を記述したCSVファイルを読み込み、Ansibleに対してJSON形式の文字列を返すことで実現しています。
  
## サンプルファイルの説明(Sample file description)

|sample file|description |
|:--|:--|
|playbooks/csv_inventory.py| Dynamic Inventory file|
|playbooks/inventory.csv| Inventory file in CSV format.|
|playbooks/common_val.yml| This file defines common settings.  Define common data for ALL group and group to which the node belongs.|
|playbooks/ansible.cfg|Ansible configuration file. |

### playbooks/csv_inventory.py  
Read CSV file, convert it to Ansible into JSON format configuration information and return it.  
CSVファイルを読み込んで、Ansibleに対してJSON形式の構成情報に変換して返します。  

### playbooks/inventory.csv

|S.group|S.host_name|S.ansible_host|S.backend_ip|S.frontend_ip|B.is_active|I.port_no|I.weight|F.sample|
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
|web_server|web001|10.0.2.10|192.168.0.10||true|8080|1|20.1|
|web_server|web002|10.0.2.11|192.168.0.11||true||2|0.22|
|web_server|web003|10.0.2.12|192.168.0.12||true||5|0.1|
|web_server|web004|10.0.2.13|192.168.0.13||true||4|2.6|
|ha_proxy|proxy01|10.0.2.20|192.168.0.20|192.168.10.20|true|||1.2|
    
### playbooks/common_val.yml  

    common_data: specific_val
    
    all_vars:
      all_test1: 123234
      all_test2: 2.13
      all_test3: True
      all_test4: test_data
    
    group_vars:
      ha_proxy:
        ha_proxy_conf_path: /etc/haproxy/haproxy.cfg
        http_port_no: 80
    
      web_server:
        web_conf_path: /etc/httpd/conf/httpd.conf
        port_no: 80

## csv_inventory.pyの出力例(Sample output from csv_inventory.py)

    $ ./csv_inventory.py | python -m json.tool
    {
        "_meta": {
            "hostvars": {
                "proxy01": {
                    "ansible_host": "10.0.2.20",
                    "backend_ip": "192.168.0.20",
                    "frontend_ip": "192.168.10.20",
                    "is_active": true,
                    "sample": 1.2
                },
                "web001": {
                    "ansible_host": "10.0.2.10",
                    "backend_ip": "192.168.0.10",
                    "is_active": true,
                    "port_no": 8080,
                    "sample": 20.1,
                    "weight": 1
                },
                "web002": {
                    "ansible_host": "10.0.2.11",
                    "backend_ip": "192.168.0.11",
                    "is_active": true,
                    "sample": 0.22,
                    "weight": 2
                },
                "web003": {
                    "ansible_host": "10.0.2.12",
                    "backend_ip": "192.168.0.12",
                    "is_active": true,
                    "sample": 0.1,
                    "weight": 5
                },
                "web004": {
                    "ansible_host": "10.0.2.13",
                    "backend_ip": "192.168.0.13",
                    "is_active": true,
                    "sample": 2.6,
                    "weight": 4
                }
            }
        },
        "all": {
            "vars": {
                "all_test1": 123234,
                "all_test2": 2.13,
                "all_test3": true,
                "all_test4": "test_data"
            }
        },
        "ha_proxy": {
            "hosts": [
                "proxy01"
            ],
            "vars": {
                "ha_proxy_conf_path": "/etc/haproxy/haproxy.cfg",
                "http_port_no": 80,
                "web_backend": [
                    {
                        "backend_ip": "192.168.0.10",
                        "host_name": "web001",
                        "port_no": 8080,
                        "weight": 1
                    },
                    {
                        "backend_ip": "192.168.0.11",
                        "host_name": "web002",
                        "port_no": 80,
                        "weight": 2
                    },
                    {
                        "backend_ip": "192.168.0.12",
                        "host_name": "web003",
                        "port_no": 80,
                        "weight": 5
                    },
                    {
                        "backend_ip": "192.168.0.13",
                        "host_name": "web004",
                        "port_no": 80,
                        "weight": 4
                    }
                ]
            }
        },
        "web_server": {
            "hosts": [
                "web001",
                "web002",
                "web003",
                "web004"
            ],
            "vars": {
                "port_no": 80,
                "web_conf_path": "/etc/httpd/conf/httpd.conf"
            }
        }
    }

## ansibleの出力例(Sample output from ansible)

### ansible_host
    $ ansible all -m debug -a "msg={{ ansible_host }}"
    proxy01 | SUCCESS => {
        "changed": false,
        "msg": "10.0.2.20"
    }
    web001 | SUCCESS => {
        "changed": false,
        "msg": "10.0.2.10"
    }
    web002 | SUCCESS => {
        "changed": false,
        "msg": "10.0.2.11"
    }
    web003 | SUCCESS => {
        "changed": false,
        "msg": "10.0.2.12"
    }
    web004 | SUCCESS => {
        "changed": false,
        "msg": "10.0.2.13"
    }

### web_backend
web_backendの値は、csv_inventory.pyの処理の中で、読み込んだ構成情報から生成します。  
The value of web_backend is generated from the read configuration information in the processing of csv_inventory.py.  

    $ ansible ha_proxy -m debug -a "msg={{ web_backend }}"
    proxy01 | SUCCESS => {
        "changed": false,
        "msg": [
            {
                "backend_ip": "192.168.0.10",
                "host_name": "web001",
                "port_no": 8080,
                "weight": 1
            },
            {
                "backend_ip": "192.168.0.11",
                "host_name": "web002",
                "port_no": 80,
                "weight": 2
            },
            {
                "backend_ip": "192.168.0.12",
                "host_name": "web003",
                "port_no": 80,
                "weight": 5
            },
            {
                "backend_ip": "192.168.0.13",
                "host_name": "web004",
                "port_no": 80,
                "weight": 4
            }
        ]
    }


  
Copyright Copyright (c) 2018 MasayukiMiyake  
License Apache License, Version 2.0  
