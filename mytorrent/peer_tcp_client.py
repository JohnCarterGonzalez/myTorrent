import socket
from hashlib import sha1

class PeerTcpClient:
    """
    This class is responsible for the TCP client that connects to the peer server.
    establish a TCP connection with a peer and complete a handshake.
    The handshake is a message consisting of the following parts as described in the peer protocol:
    length of the protocol string (BitTorrent protocol) which is 19 (1 byte)
    the string BitTorrent protocol (19 bytes)
    eight reserved bytes, which are all set to zero (8 bytes)
    sha1 infohash (20 bytes) (NOT the hexadecimal representation, which is 40 bytes long)
    peer id (20 bytes)
    After we send a handshake to our peer, we should receive a handshake back in the same format.
    """

    def __init__(self, peer_ip, peer_port, torrent, peer_id):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.torrent = torrent
        self.peer_id = peer_id
        self.socket = None

    def connect(self):
        """Establish a TCP connection with a peer and complete a handshake."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.peer_ip, self.peer_port))
        self.__send_handshake()

    def __send_handshake(self):
        """Send handshake to peer"""
        handshake = self.__build_handshake()
        self.socket.send(handshake)
        response = self.socket.recv(68)
        self.__validate_handshake_response(response)

    def __build_handshake(self):
        pstrlen = b"\x13"
        pstr = b"BitTorrent protocol"
        reserved = b"\x00" * 8
        info_hash = self.torrent.get_info_bytes()
        peer_id = self.peer_id.encode()
        handshake = pstrlen + pstr + reserved + info_hash + peer_id
        return handshake

    def __validate_handshake_response(self, response):
        peer_id = response[48:68]
        print(f"Peer ID: {peer_id.hex()}")

    def close(self):
        """Close connection with peer"""
        self.socket.close()
