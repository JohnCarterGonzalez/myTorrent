import pytest
from app.main import bencode_decoder

def test_decode_string():
    bencoded_value = b"5:hello"
    result = bencode_decoder(bencoded_value)
    assert result == "hello"

def test_decode_integer_fail():
    bencoded_value = b"42e"
    result = bencode_decoder(bencoded_value)
    assert result == 42

def test_decode_bencode_string_fail():
    bencoded_value = b"6:world"
    result = bencode_decoder(bencoded_value)
    assert result == "world"

def test_decode_bencode_integer():
    bencoded_value = b"i123e"
    result = bencode_decoder(bencoded_value)
    assert result == 123

def test_bencode_decoder_list():
    bencoded_value = b"l5:helloi123ee"
    result = bencode_decoder(bencoded_value)
    asser result = ["hello", 52]

def test_bencode_decoder_dict_invalid():
    bencoded_value = b"d3:foo3:bar5:helloi52ee"
    with pytest.raises(NotImplementedError):
        bencode_decoder(bencoded_value)


if __name__ == "__main__":
    pytest.main()
