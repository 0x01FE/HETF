from prototype import TextEncoder

import logging
import timeit

TOP_WORDS_PATH = './resources/wiki-100k.txt'
SAMPLE = "the quick brown fox jumped over the lazy dog"
SAMPLE_FILE_PATH = "./resources/utf8-wikipedia.txt"
# SAMPLE_FILE_PATH = "./resources/small-sample.txt"
TRIALS = 100

# Set up encoder
codec = TextEncoder(TOP_WORDS_PATH)

def test_encode_decode():
    logging.info('<' + '-' * 5 + 'START ENCODE / DECODE TEST' + '-' * 5 + '>')

    encoded_text = codec.encode(SAMPLE)
    decoded_text = codec.decode(encoded_text)

    logging.info(f'Sample: "{SAMPLE}"')
    logging.info(f'Encoded Text: {encoded_text}')
    logging.info(f'Decoded Text: {decoded_text}')

    assert SAMPLE == decoded_text

    logging.info('<' + '-' * 5 + 'END ENCODE / DECODE TESTS' + '-' * 5 + '>')

def test_speeds_vs_utf8():
    logging.info('<' + '-' * 5 + 'START SPEED TESTS' + '-' * 5 + '>')

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

    logging.info('<' + '-' * 5 + 'END SPEED TESTS' + '-' * 5 + '>')


def test_file_encode_decode():
    logging.info('<' + '-' * 5 + 'START FILE ENCODE / DECODE TESTS' + '-' * 5 + '>')

    # Encode UTF-8 file to HETF
    encoded_file_path = codec.encode_file(SAMPLE_FILE_PATH)

    # Read original UTF-8 Data
    with open(SAMPLE_FILE_PATH, 'r') as file:
        utf_data = file.read()

    # Decode encoded file data
    hetf_data = codec.decode_file(encoded_file_path)

    logging.info(hetf_data)

    assert utf_data == hetf_data

    logging.info('<' + '-' * 5 + 'END FILE ENCODE / DECODE TESTS' + '-' * 5 + '>')




test_encode_decode()
# test_speeds_vs_utf8()
test_file_encode_decode()
