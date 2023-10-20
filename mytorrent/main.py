import json
import sys
import hashlib

from app.decoder import bencode_decoder, bencode_encoder
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
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
