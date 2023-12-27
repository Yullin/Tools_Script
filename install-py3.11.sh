#!/bin/bash
echo "--- Preparing install ---"
yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel -y

echo "--- Downloading packages ---"
wget http://URL/openssl-1.1.1n.tar.gz -O /usr/local/src/openssl-1.1.1n.tar.gz
wget http://URL/Python-3.11.4.tar.xz -O /usr/local/src/Python-3.11.4.tar.xz

echo "--- Building OpenSSL ---"
if test -d "/usr/local/openssl";
then
    echo "Already exist directory: /usr/local/openssl"
    echo -n "Do you want to OVERWRITE it? (yes|no):"
    read input
    if [ "$input" == "no" ]
    then
        echo "Exit installing"
        exit 1
    fi
fi
cd /usr/local/src/
tar xzf openssl-1.1.1n.tar.gz
cd openssl-1.1.1n
./config --prefix=/usr/local/openssl
make && make install

echo "/usr/local/openssl/lib" >> /etc/ld.so.conf
ldconfig -v

echo "--- Building Python3.10 ---"
if test -d "/usr/local/python3";
then
    echo "Already exist directory: /usr/local/python3"
    echo -n "Do you want to OVERWRITE it? (yes|no):"
    read input
    if [ "$input" == "no" ]
    then
        echo "Exit installing"
        exit 1
    fi
fi
cd /usr/local/src/
tar xf Python-3.11.4.tar.xz
cd Python-3.11.4
./configure prefix=/usr/local/python3 --with-openssl=/usr/local/openssl
make && make install

echo "--- Set Sys Path ---"
ln -s /usr/local/python3/bin/python3 /bin/python3.11
