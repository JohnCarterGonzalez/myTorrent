from typing import List

import requests

from app.decoder import bencode_decoder
from app.torrent_data import TorrentData

class TrackerService:
    """
    Tracker GET request

        info_hash: the info hash of the torrent
            - 20 bytes long, will need to be URL encoded
            NOTE: this is NOT the hexadecimal representation, which is 40 bytes long
        peer_id: a unique identifier for your client
            - A string of length 20 that you get to pick. You can use something like 00112233445566778899.
        port: the port your client is listening on
            - set to 6881 for simplicity
        uploaded: the total amount uploaded so far
            - Since your client hasn't uploaded anything yet, you can set this to 0.
        downloaded: the total amount downloaded so far
            - Since your client hasn't downloaded anything yet, you can set this to 0.
        left: the number of bytes left to download
            - Since you client hasn't downloaded anything yet, this'll be the total length of the file (you've extracted this value from the torrent file in previous stages)
        compact: whether the peer list should use the compact representation
            - For the purposes of this challenge, set this to 1.
            - The compact representation is more commonly used in the wild, the non-compact representation is mostly supported for backward-compatibility.

    Read the BitTorrent Protocol Specification (https://www.bittorrent.org/beps/bep_0003.html#trackers) for more information about these query parameters.
    """

    def __init__(self, torrent: TorrentData, peer_id: str):
        self.torrent = torrent
        self.peer_id = peer_id

    def get_peers(self):
        info_hash = self.torrent.get_info_bytes()
        print(f"Info Hash: {info_hash}")

        port = 6881
        uploaded = 0
        downloaded = 0
        left = self.torrent.info.length
        compact = 1

        query_params = {
            "info_hash": info_hash,
            "peer_id": self.peer_id,
            "port": port,
            "uploaded": uploaded,
            "downloaded": downloaded,
            "left": left,
            "compact": compact,
        }

        response = requests.get(self.torrent.announce, params=query_params)
        if response.status_code != 200:
            raise RuntimeError(f"Tracker returned status code {response.status_code}")

        return self.__decode_response(response.content)

    def __decode_response(self, response_data: bytes) -> List[str]:
        """
        The tracker's response will be a bencoded dictionary with two keys:

        interval:
        An integer, indicating how often your client should make a request to the tracker.

        peers:
        A string, which contains list of peers that your client can connect to.
        Each peer is represented using 6 bytes. The first 4 bytes are the peer's IP address
        and the last 2 bytes are the peer's port number.
        """

        decoded_response = bencode_decoder(response_data)
        decoded_peers = decoded_response["peers"]

        peers = []

        for i in range(0, len(decoded_peers), 6):
            ip_addr = ".".join(map(str, decoded_peers[i : i + 4]))
            port = int.from_bytes(decoded_peers[i + 4 : i + 6], byteorder="big")
            peers.append(f"{ip_addr}:{port}")

        return peers
