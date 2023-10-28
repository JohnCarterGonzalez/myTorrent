import socket

class PeerTcpClient:
    def __init__(self, peer_ip, peer_port, peer_id):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.peer_id = peer_id
        self.socket = None

    def connect(self):
        """Establish a TCP connection with a peer and complete a handshake."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.peer_ip, self.peer_port))
        print(f"Connected to peer {self.peer_ip}:{self.peer_port}")
    def send_handshake(self, info_hash_bytes):
        """Send handshake message to peer"""
        handshake = self.__build_handshake(info_hash_bytes)
        self.socket.send(handshake)
        response = self.socket.recv(len(handshake))
        print(f"Peer ID: {response[48:68].hex()}")

    def wait_for_bitfield(self):
        """Wait for bitfield message from peer"""
        while True:
            length, msg_id, _ = self.__receive_message()
            if msg_id == 5:
                print(f"Bitfield message received")
                return True
            else:
                raise RuntimeError("Wrong message id")

    def send_interested(self):
        """Send interested message to peer"""
        msg_length = 5
        # Interested msg id
        msg_id = 2
        message = msg_length.to_bytes(4, byteorder="big") + msg_id.to_bytes(
            1, byteorder="big"
        )
        self.socket.send(message)

    def wait_until_unchoke(self):
        """Wait until peer unchoke message"""
        while True:
            length, msg_id, _ = self.__receive_message()
            if msg_id == 1:
                print(f"Unchoke message received")
                return True

    def request_piece(self, piece_index, block_offset, block_length) -> bytes:
        """Send request message to peer"""
        msg_length = 13
        msg_id = 6
        request_message = (
            msg_length.to_bytes(4, byteorder="big")
            + msg_id.to_bytes(1, byteorder="big")
            + piece_index.to_bytes(4, byteorder="big")
            + block_offset.to_bytes(4, byteorder="big")
            + block_length.to_bytes(4, byteorder="big")
        )
        self.socket.send(request_message)
        while True:
            length, msg_id, payload = self.__receive_message()
            if msg_id == 7:
                return payload

    def wait_for_piece(self) -> bytes:
        """Wait for piece message from peer
        The message id for piece is 7.
        The payload for this message consists of:
        index: the zero-based piece index
        begin: the zero-based byte offset within the piece
        block: the data for the piece, usually 2^14 bytes long
        """
        while True:
            length, msg_id = self.__receive_message()
            if length > 4 and msg_id == 7:
                msg = self.socket.recv(length - 1)
                msg_id = msg[0]
                if msg_id == 7:
                    print(f"Piece message received")
                    return msg[9:]

    def __build_handshake(self, info_hash_bytes: bytes) -> bytes:
        pstr = b"BitTorrent protocol"
        pstrlen = len(pstr).to_bytes(1, byteorder="big")
        reserved = b"\x00" * 8
        peer_id = self.peer_id.encode()
        handshake = pstrlen + pstr + reserved + info_hash_bytes + peer_id
        return handshake

    def __receive_message(self) -> (int, int, bytes):
        length, msg_id = (
            int.from_bytes(self.socket.recv(4), byteorder="big"),
            int.from_bytes(self.socket.recv(1), byteorder="big"),
        )

        payload = b""
        if length > 1:
            payload_length = length - 1

            while payload_length > 0:
                payload_response = self.socket.recv(payload_length)
                payload += payload_response
                payload_length -= len(payload_response)

        print(
            f"Message received, length: {length}, msg_id: {msg_id}, payload length: {len(payload)}"
        )
        return length, msg_id, payload

    def close(self):
        """Close connection with peer"""
        self.socket.close()
