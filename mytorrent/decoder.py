def bencode_decoder(bencoded_value):
    return bencode_transforms(bencoded_value)[1]

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

def decode_string(bencoded_value):
    length = int(bencoded_value.split(b":")[0])
    return bencoded_value.split(b":")[1][:length]

def is_int(bencoded_value):
    return bencoded_value.startswith(b"i")

def decode_integer(bencoded_value):
    end_str = bencoded_value.index(b"e")
    str_num = bencoded_value[1:end_str]
    return int(str_num)

def is_list(bencoded_value):
    return bencoded_value.startswith(b"l") and bencoded_value.endswith(b"e")

def is_dict(bencoded_value):
    return bencoded_value.startswith(b"d") and bencoded_value.endswith(b"e")
