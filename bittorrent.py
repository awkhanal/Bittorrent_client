from collections import OrderedDict
import bencoder
import random
import aiohttp
from hashlib import sha1
from urllib.parse import urlencode
import logging
import asyncio
from collections import namedtuple
import socket
from struct import unpack




with open('/home/sunil/Desktop/a2/86983F50E8781CADD98579199BEE2665.torrent', 'rb') as f:
    meta_info = f.read()
    torrent = OrderedDict(bencoder.decode(meta_info))

TorrentFile = namedtuple('TorrentFile', ['name', 'length'])

files = [TorrentFile(torrent[b'info'][b'name'].decode('utf-8'), torrent[b'info'][b'length'])]

torrent_total_size = files[0].length

peer_id = '-PC0001-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])


async def connect(first : bool = None, uploaded : int = 0, downloaded : int = 0):

        http_client = aiohttp.ClientSession()
        
        params = {
            'info_hash': sha1(bencoder.encode(torrent[b'info'])).digest(),
            'peer_id': peer_id,
            'port': 6889,
            'uploaded': uploaded,
            'downloaded': downloaded,
            'left': torrent_total_size - downloaded,
            'compact': 1
        }

        if first:
            params['event'] = 'started'
        
        url = torrent[b'announce'].decode('utf-8') + '?' + urlencode(params)
        print(url)
        logging.info('Connecting to tracker at: ' + url)
        print("hi")

        
        async with http_client.get(url) as response:
            if not response.status == 200:
                raise ConnectionError('Unable to connect to tracker: status code {}'.format(response.status))
            print("hi")
            data = await response.read()
            return bencoder.decode(data)



response = asyncio.run(connect())


peers = response[b'peers']
peers = [peers[i:i+6] for i in range(0, len(peers), 6)]
peers = [(socket.inet_ntoa(p[:4]), unpack(">H", p[4:])[0])for p in peers]

print(peers)









