FROM alpine:3.17.7

# ------------------------- SETUP OS ------------------------- #

RUN apk update && apk upgrade

# --------------------- INSTALL PACKAGES --------------------- #

RUN apk add -q \
    autoconf \
    automake \ 
    libtool \
    git \
    build-base \
    gcc \
    make

# --------------------- GET SOURCE FILES --------------------- #

COPY src $HOME/src
WORKDIR $HOME/src
RUN git clone --depth 1 --recursive -b dtls https://github.com/home-assistant/libcoap.git

# ----------------------- SETUP ---------------------- #

WORKDIR $HOME/src/libcoap

RUN ./autogen.sh && \
    ./configure --disable-documentation --disable-shared --without-debug CFLAGS="-D COAP_DEBUG_FD=stderr" && \
    make && \
    make install