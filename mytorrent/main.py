import json
import sys
import hashlib

from app.decoder import bencode_decoder, bencode_encoder

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
            decoded_value = bencode_decoder(bencoded_value)
            if isinstance(decoded_value, dict):
                print(f"Tracker URL: {decoded_value['announce'].decode()}")
                info = decoded_value["info"]
                print(f"Length: {info['length']}")
                # TODO: implement bencode_encoder in decoder.py!!
                info_hash = hashlib.sha1(bencode_encoder(info)).hexdigest()
                print(f"Info Hash: {info_hash}")
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
