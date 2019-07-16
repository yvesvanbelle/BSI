import urllib.request
import socket


def set_proxy(ip, port):
    try:
        socket.gethostbyaddr(ip)
        proxy = urllib.request.ProxyHandler({'http': r'http://'+ip+':'+port})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
    except Exception as e:
        pass


def get_ip_address():
    ip = urllib.request.urlopen('http://ipv4bot.whatismyipaddress.com')
    ip = ip.read().decode()
    return ip


def get_provider():
    url = 'http://xml.utrace.de/?query=' + get_ip_address()
    provider = urllib.request.urlopen(url)
    provider = provider.read().decode()
    provider_start = provider.find(r'<isp>')
    provider_end = provider.find(r'</isp>')
    provider = provider[provider_start + 5: provider_end]
    return provider


def get_smtp():
    smtp_server = {'Belgacom': 'relay.skynet.be',
                   'Proximus': 'relay.skynet.be',
                   'Dommel': 'relay.dommel.be',
                   'Edpnet': 'relay.belgacom.be',
                   'Numericable': 'smtp.numericable.be',
                   'Scarlet': 'smtp.scarlet.be',
                   'Skynet': 'relay.skynet.be',
                   'Telenet': 'uit.telenet.be',
                   'united telecom': 'smtp.unitedtelecom.be',
                   'Base': 'mail.internetmail.be',
                   'Billi': 'relay.alphanetworks.be',
                   'Euphony': 'out.euphonynet.be',
                   'Mobistar': 'smtp.mobistar.be',
                   'Online': 'smtp.antw.online.be',
                   'Télé': 'out.tel2allin.be',
                   'Télésat': 'smtp.telesat.lu',
                   'Versatel': 'out.versateladsl.be',
                   'Voo': 'smtp.voo.be',
                   'Xs4all': 'smtp.xs4all.be'
                   }
    provider = get_provider().split()[0]

    if provider in smtp_server.keys():
        return smtp_server[provider]
    else:
        return'smtp.provider.net'


if __name__ == '__main__':
    set_proxy('10.10.129.129','8080')
    print(get_smtp())
