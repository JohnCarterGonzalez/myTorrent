import hashlib
from typing import List

from app.decoder import bencode_decoder, bencode_encoder

class TorrentInfo:
    """
    Stores info on Torrent
    length: size of the file in bytes, for single file torrents
    name: suggested name to save the file / directory as
    piece: concatenated SHA-1 hashes of each piece
    piece_length: number of bytes in each piece

    NOTE: the info dict looks slightly different for multi file torrents

    In a torrent, a file is split into equally-sized parts called 'pieces'. A piece is usually 256 KB or 1 MB in size.
    Each piece is assigned a SHA-1 hash value. On public networks, there may be malicious peers that send fake data.
    These hash values allow us to verify the integrity of each piece that we'll download.
    """

    length: int
    name: str
    piece_length: int
    pieces: str
    __raw_value: dict

    def __init__(self, value: dict):
        self.__raw_value = value
        self.length = value["length"]
        self.name = value["name"]
        self.pieces = value["pieces"]
        self.piece_length = value["piece length"]

    def get_dict(self) -> dict:
        return self.__raw_value

class TorrentData:
    """
    Stores Torrent data

    An example output:
    Tracker URL: http://bittorrent-test-tracker.johncarter.io/announce -- dummy URL
    Length: 92063
    Info Hash: d69f91e6b2ae4c542468d1073a71d4ea13879a7f
    Piece Length: 32768
    Piece Hashes:
    e876f67a2a8886e8f36b136726c30fa29703022d
    6e2275e604a0766656736e81ff10b55204ad8d35
    f00d937a0213df1982bc8d097227ad9e909acc17
    """

    announce: str # URL to a "tracker" which is a central server that keeps track of peers
    info: TorrentInfo # a dict

    def __init__(self, bencoded_value: bytes):
        decoded_value = bencode_decoder(bencoded_value)
        if isinstance(decoded_value, dict):
            self.announce = decoded_value["announce"].decode()
            self.info = TorrentInfo(decoded_value["info"])

        else:
            raise NotImplementedError(f"Type not supported: {type(decoded_value)}")

    def get_info_bytes(self) -> bytes:
        return hashlib.sha1(bencode_encoder(self.info.get_dict())).digest()

    def get_info_hash(self) -> str:
        return self.get_info_bytes().hex()

    def get_pieces_hash(self) -> List[str]:
        pieces = self.info.pieces
        pieces_hash = []
        for i in range(0, len(pieces), 20):
            pieces_hash.append(pieces[i : i + 20].hex())
        return pieces_hash
