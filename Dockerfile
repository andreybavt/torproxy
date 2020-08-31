FROM ubuntu
EXPOSE 9050 9052
RUN apt update
RUN apt install -y curl supervisor tor python3 python3-pip

RUN pip3 install requests flask stem pysocks

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY tor_proxy_api.py tor_proxy_api.py


RUN echo "Log notice stdout" >> /etc/tor/torrc
RUN echo "SocksPort 0.0.0.0:9050" >> /etc/tor/torrc
RUN echo "ControlPort 9051" >> /etc/tor/torrc
RUN echo "CookieAuthentication 0" >> /etc/tor/torrc

CMD ["/usr/bin/supervisord"]