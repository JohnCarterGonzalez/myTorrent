def bencode_decoder(bencoded_value):
    return bencode_transforms(bencoded_value)[1]

def bencode_encoder(bencoded_value):
    if isinstance(value, bytes):
        return str(len(value)).encode() + b":" + value
    elif isinstance(value, str):
        return encode_str(value)
    elif isinstance(value, int):
        return encode_int(value)
    elif isinstance(value, list):
        return encode_list(value)
    elif isinstance(value, dict):
        return encode_dict(value)
    else:
        raise NotImplementedError(f"Type not supported: {type(value)}")

def bencode_transforms(bencoded_value) -> (int, object):
    if is_string(bencoded_value):
        return decode_string(bencoded)
    elif is_int(bencoded_value):
        return decode_integer(bencoded_value)
    elif is_list(bencoded_value):
        body = bencoded_value[1:-1]
        body_length = len(body)
        decoded_list = []

        while len(body) > 0:
            decoded_element = bencode_transforms(body)
            decoded_list.append(decoded_element[1])
            body = body[decoded_element[0] :]
        return body_length + 2, decoded_list
    elif is_dict(bencoded_value):
        body = bencoded_value[1:-1]
        body_length = len(body)
        decoded_dict = {}

        while len(body) > 0:
            # decode the key and value
            decoded_key = decoding_transforms(body)
            decoded_value = decoding_transforms(body[len(decoded_key[0]) :])

            decoded_dict[decoded_key[1].decode("utf-8")] = decoded_value[1]
            body = body[len(decoded_key[0]) + len(decoded_value[0]) :] # remove the parts that have been decoded
        return body_length + 2, decoded_dict
    else:
        raise NotImplementedError("Only strings are supported at the moment")

""" Helper Functions """
def is_string(bencoded_value):
    return chr(bencoded_value[0].isdigit())


def is_int(bencoded_value):
    return bencoded_value.startswith(b"i")


def is_list(bencoded_value):
    return bencoded_value.startswith(b"l") and bencoded_value.endswith(b"e")

def is_dict(bencoded_value):
    return bencoded_value.startswith(b"d") and bencoded_value.endswith(b"e")


""" Decoder Functions"""
def decode_integer(bencoded_value):
    end_str = bencoded_value.index(b"e")
    str_num = bencoded_value[1:end_str]
    return int(str_num)

def decode_string(bencoded_value):
    split_value = bencoded_value.split(b":", 1)
    length = int(split_value[0])
    decoded_str = split[1][:length]
    return len(str(length)) + len(decoded_str) + 1, decoded_str
# TODO: implement list and dict helper functions
def decode_list(bencoded_value):
    pass

def decode_dict(bencoded_value):
    pass

"""Encoder Functions"""
def encode_str(value):
    pass

def encode_int(value):
    pass

def encode_list(value):
    pass

def encode_dict(value):
    pass
