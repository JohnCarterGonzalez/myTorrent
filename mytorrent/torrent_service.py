import hashlib

from app.peer_tcp_client import PeerTcpClient
from app.torrent_data import TorrentData
from app.tracker_info_service import TrackerInfoService

class TorrentService:
    torrent: TorrentData
    tcp_client: PeerTcpClient
    tracker_service: TrackerInfoService
    peer_id: str
    connected: bool = False

    def __init__(
        self,
        torrent: TorrentData,
        peer_id: str,
        peer_ip: str = None,
        peer_port: int = None,
    ):

        self.torrent = torrent
        self.tracker_service = TrackerInfoService(torrent, peer_id)
        if peer_ip is None or peer_port is None:
            print("Getting peers from tracker")
            peer_info = self.tracker_service.get_peers()[0].split(":")
            peer_ip = peer_info[0]
            peer_port = int(peer_info[1])
        self.tcp_client = PeerTcpClient(peer_ip, peer_port, peer_id)
        self.peer_id = peer_id

    def connect_and_print_peer_id(self):
        self.tcp_client.connect()
        self.tcp_client.send_handshake(self.torrent.get_info_bytes())
        self.connected = True


    def setup_connection_for_download(self):
        if not self.connected:
            self.connect_and_print_peer_id()
        self.tcp_client.wait_for_bitfield()
        self.tcp_client.send_interested()
        self.tcp_client.wait_until_unchoke()

    def download_piece(self, piece_index: int) -> bytes:
        piece_length = self.torrent.info.piece_length
        file_length = self.torrent.info.length
        count = file_length // piece_length
        if piece_index == count:
            piece_length = file_length % piece_length
        print(f"Piece length: {piece_length}")
        block_size = 16 * 1024
        i = 0
        piece = b""

        while piece_length > block_size:
            requested_block = self.tcp_client.request_piece(
                piece_index, i * block_size, block_size
            )

            print(f"Block {i} received from peer with length {len(requested_block)}")
            piece += requested_block[8:]
            piece_length -= block_size
            print(f"Lasting piece length: {piece_length}")
            i += 1

        if piece_length > 0:
            piece += self.tcp_client.request_piece(
                piece_index, i * block_size, piece_length
            )[8:]
        stored_hash = self.torrent.get_pieces_hashes()[piece_index]
        print(f"Piece hash: {hashlib.sha1(piece).hexdigest()}")
        print(f"Stored hash: {stored_hash}")
        assert hashlib.sha1(piece).hexdigest() == stored_hash
        return piece

    def close(self):
        self.tcp_client.close()
