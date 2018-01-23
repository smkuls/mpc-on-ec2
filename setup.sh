#!/bin/bash
sudo yum -y update
sudo yum -y install git gcc gmp-devel
sudo pip install twisted[tls]
sudo pip install gmpy
sudo pip uninstall -y pyasn1
sudo easy_install pyasn1
wget http://hg.viff.dk/viff/archive/tip.zip
unzip tip.zip
mv viff-f1d477e94d0b/ /home/ec2-user
cd /home/ec2-user/viff-f1d477e94d0b
python setup.py install --home=/home/ec2-user/opt