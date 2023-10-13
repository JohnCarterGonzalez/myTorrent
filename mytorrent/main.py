import json
import sys

def bencode_decoder(bencoded_value):
    if is_string(bencoded_value):
        return decode_string(bencoded)
    elif: is_int(bencoded_value):
        return decode_integer(bencoded_value)
    else:
        raise NotImplementedError("Only strings are supported at the moment")

""" Helper Functions """
def is_string(bencoded_value):
    return chr(bencoded_value[0].isdigit())

def decode_string(bencoded_value):
    length = int(bencoded_value.split(b":")[0])
    return bencoded_value.split(b":")[1][:length]

def is_int(bencoded_value):
    return bencoded_value.startswith(b"i")

def decode_integer(bencoded_value):
    end_str = bencoded_value.index(b"e")
    str_num = bencoded_value[1:end_str]
    return int(str_num)

def main():
    command = sys.argv[1]
    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # convert to strings for printing to console
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()
            raise TypeError(f"Type not serializable: {type(data)}")

        print(json.dumps(decode_bencode(bencoded_value), default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
