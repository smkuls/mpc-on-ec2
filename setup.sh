#!/bin/bash
sudo yum -y update
sudo yum -y install git gcc gmp-devel git
sudo pip install twisted[tls]
sudo pip install gmpy
sudo pip uninstall -y pyasn1
sudo easy_install pyasn1
git clone -b asyncmix https://github.com/amiller/viff/
mv viff/ /home/ec2-user
cd /home/ec2-user/viff
python setup.py install --home=/home/ec2-user/opt
echo 'export PYTHONPATH=$PYTHONPATH:/home/ec2-user/opt/lib/python' >> /home/ec2-user/.bashrc
source /home/ec2-user/.bashrc