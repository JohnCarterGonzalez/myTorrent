import pytest
from app.main import bencode_decoder

def test_bencode_decoder_string():
    bencoded_value = b"5:hello"
    result = bencode_decoder(bencoded_value)
    assert result == "hello"

def test_bencode_decoder_integer():
    bencoded_value = b"i123e"
    result = bencode_decoder(bencoded_value)
    assert result == 123

def test_bencode_decoder_integer_fail():
    bencoded_value = b"42e"
    result = bencode_decoder(bencoded_value)
    assert result == 42

def test_bencode_decoder_string_fail():
    bencoded_value = b"6:world"
    result = bencode_decoder(bencoded_value)
    assert result == "world"

def test_bencode_decoder_list():
    bencoded_value = b"l5:helloi123ee"
    result = bencode_decoder(bencoded_value)
    assert result = ["hello", 52]

def test_bencode_decoder_dict():
    bencoded_value = b"d3:foo3:bar5:helloi123ee"
    result = bencode_decoder(bencoded_value)
    assert result = {"hello": 123, "foo": "bar"}

def test_bencode_encoder_str():
    value = "hello"
    result = bencode_encoder(value)
    assert result = "5:hello"

def test_bencode_encoder_int():
    value = 5
    result = bencode_encoder(value)
    assert result = "i5e"

def test_bencode_encoder_list():
    value = [ "hello", 52 ]
    result = bencode_encoder(value)
    assert result = "l5:helloi52ee"

def test_bencode_encoder_dict():
    value = { "foo": "bar", "hello": 52 }
    result = bencode_encoder(value)
    assert result = "d3:foo3:bar5:helloi52ee"


if __name__ == "__main__":
    pytest.main()
