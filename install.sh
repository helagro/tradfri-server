
# look at older versions of this

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    apt-get install -f autoconf automake libtool 
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install libcoap
fi 

git clone --depth 1 --recursive -b dtls https://github.com/home-assistant/libcoap.git
cd libcoap
./autogen.sh
./configure --disable-documentation --disable-shared --without-debug CFLAGS="-D COAP_DEBUG_FD=stderr"
make
make install

pip3 install pytradfri