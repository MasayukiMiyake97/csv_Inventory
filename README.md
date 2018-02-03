# Ansible Dynamic Inventory サンプル（CSVファイル）
We are publishing a sample of Dynamic Inventory which loads CSV file as Inventory definition.  
This sample is realized by reading the CSV file describing the configuration information and returning a character string of JSON format to Ansible.  

---
CSVファイルをInventory定義として読み込む、Dynamic Inventoryのサンプルを公開しています。  
このサンプルは、構成情報を記述したCSVファイルを読み込み、Ansibleに対してJSON形式の文字列を返すことで実現しています。
  
## サンプルファイルの説明(Sample file description)

|sample file|description |
|:--|:--|
|playbooks/csv_inventory.py||
|playbooks/inventory.csv||
|playbooks/common_val.yml||
|playbooks/ansible.cfg||

playbooks/inventory.csv




  
Copyright Copyright (c) 2018 MasayukiMiyake  
License Apache License, Version 2.0  
