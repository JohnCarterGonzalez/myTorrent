import json
import sys
import hashlib


from app.decoder import bencode_decoder, bencode_encoder
from app.peer_tcp_client import PeerTcpClient
from app.torrent_service import TorrentService
from app.torrent_data import TorrentData
from app.tracker_service_api import TrackerService

def bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode()
    raise TypeError(f"Type not serializable: {type(data)}")

def main():
    command = sys.argv[1]
    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # convert to strings for printing to console
        print(json.dumps(bencode_decoder(bencoded_value), default=bytes_to_str))
    elif command == "info":
        file_name = sys.argv[2]
        with open(file_name, "rb") as f:
            bencoded_value = f.read()
            torrent = TorrentData(bencoded_value)

            print(f"Tracker URL: {torrent.announce}")
            print(f"Length: {torrent.info.length}")
            print(f"Info Hash: {torrent.get_info_hash()}")
            print(f"Piece Length: {torrent.info.piece_length}")

            print(f"Pieces Hash: ")
            pieces_hash = torrent.get_pieces_hash()
            for hash in pieces_hash:
                print(hash)
    elif command == "peers":
        file_name = sys.argv[2]
        with open(file_name, "rb") as f:
            bencoded_value = f.read()
            torrent = TorrentData(bencoded_value)

            tracker_service_api = TrackerService(torrent, "12345678901234567890")
            peers = tracker_service_api.get_peers()
            print(peers)
    elif command == "handshake":
        file_name = sys.argv[2]
        peer_info = sys.argv[3]
        with open(file_name, "rb") as f:
            peer_ip = peer_info.split(":")[0]
            peer_port = peer_info.split(":")[1]
            bencoded_value = f.read()
            torrent = TorrentData(bencoded_value)
            peer_client = PeerTcpClient(peer_ip, int(peer_port), torrent, "12345678901234567890")
            peer_client.connect() # establish TCP connection and perform handshake with the peer
            peer_client.close() # close the handshake
    elif command == "download_piece":
        output_file = sys.argv[3]
        file_name = sys.argv[4]
        piece_index = int(sys.argv[5])
        with open(file_name, "rb") as f:
            bencoded_value = f.read()
            torrent = TorrentData(bencoded_value)
            torrent_service = TorrentService(torrent, "12345678901234567890")
            torrent_service.setup_connection_for_download()
            piece = torrent_service.download_piece(piece_index)
            with open(output_file, "wb") as file:
            with open(output_file, "wb") as file:
                file.write(piece)
            torrent_service.close()
            print(f"Piece {piece_index} downloaded to {output_file}")
    elif command == "download":
        output_file = sys.argv[3]
        file_name = sys.argv[4]
        with open(file_name, "rb") as f:
            bencoded_value = f.read()
            torrent = TorrentData(bencoded_value)
            torrent_service = TorrentService(torrent, "12345678901234567890")
            torrent_service.setup_connection_for_download()
            pieces_count = torrent.info.length // torrent.info.piece_length
            pieces = b""
            for i in range(pieces_count + 1):
                piece = torrent_service.download_piece(i)
                pieces += piece
                print(f"Piece {i} downloaded")
            torrent_service.close()
            with open(output_file, "wb") as file:
                file.write(pieces)
            print(f"Downloaded {file_name} to {output_file}")
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
