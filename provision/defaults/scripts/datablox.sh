set -ex
apt-get update
# engage dependencies
apt-get -y install git-core g++ ocaml zlib1g-dev python-dev python-crypto \
    python-virtualenv make libzmq-dev libzmq1 curl
pip install pyzmq
git clone git://github.com/mpi-sws-rse/datablox.git ~/datablox
cd ~/datablox && make all
#cd ~/datablox/engage/engage-dist && ./install_datablox.py ~/apps
