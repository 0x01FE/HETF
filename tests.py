from prototype import TextEncoder

import timeit

# Set up encoder
codec = TextEncoder('./wiki-100k.txt')

SAMPLE = "the quick brown fox jumped over the lazy dog"
TRIALS = 100

def test_encode_decode():
    encoded_text = codec.encode(SAMPLE)
    decoded_text = codec.decode(encoded_text)


    assert SAMPLE == decoded_text


def test_speeds_vs_utf8():
    pass

    # UTF-8
    t = timeit.Timer(SAMPLE.encode)
    utf_time = t.timeit(TRIALS)
    utf_bytes_len = len(SAMPLE.encode())

    # HETF
    t = timeit.Timer(lambda: codec.encode(SAMPLE))
    hetf_time = t.timeit(TRIALS)
    hetf_bytes_len = len(codec.encode(SAMPLE))


    print(f'Sample string used : "{SAMPLE}"')
    print(f'Time for {TRIALS} utf-8 encodes: {utf_time} seconds')
    print(f'Time for {TRIALS} HETF encodes: {hetf_time} seconds')
    print(f'HETF / UTF times = {hetf_time/utf_time}')
    print(f'UTF-8 byte size: {utf_bytes_len}')
    print(f'HETF byte size: {hetf_bytes_len}')





# test_encode_decode()
test_speeds_vs_utf8()

