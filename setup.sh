#!/bin/bash

# Viff setup
sudo yum -y update
sudo yum -y install git gcc gmp-devel git
sudo pip install twisted[tls]
sudo pip install gmpy
sudo pip uninstall -y pyasn1
sudo easy_install pyasn1
git clone -b asyncmix https://github.com/amiller/viff/
mv viff/ /home/ec2-user
pushd /home/ec2-user/viff
python setup.py install --home=/home/ec2-user/opt
echo 'export PYTHONPATH=$PYTHONPATH:/home/ec2-user/opt/lib/python' \
	>> /home/ec2-user/.bashrc
source /home/ec2-user/.bashrc
popd

# SPDZ-2 setup
sudo yum -y update
sudo yum -y install yasm gcc-c++ m4 git
wget http://mpir.org/mpir-3.0.0.zip
unzip mpir-3.0.0.zip
cd mpir-3.0.0
./configure --enable-cxx
sudo make install
cd ..
wget https://download.libsodium.org/libsodium/releases/LATEST.tar.gz
tar -xvzf LATEST.tar.gz
cd libsodium-stable/
./configure
sudo make install
echo 'export LD_LIBRARY_PATH=/usr/local/lib' >> /home/ec2-user/.bashrc
source /home/ec2-user/.bashrc
cd ..
git clone -b insecure https://github.com/smkuls/SPDZ-2 spdz-2
mv spdz-2/ /home/ec2-user
cd /home/ec2-user/spdz-2
make
sudo chown -R ec2-user /home/ec2-user/spdz-2
