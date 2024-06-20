from prototype import TextEncoder

import logging
import timeit
import time

TOP_WORDS_PATH = './resources/wiki-100k.txt'
SAMPLE = "the quick brown fox jumped over the lazy dog"
SAMPLE_FILE_PATH = "./resources/utf8-wikipedia.txt"
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

# I'm not quite sure str.encode() is a fair comparison.
def test_speeds_vs_utf8():
    logging.info('<' + '-' * 5 + 'START SPEED TESTS' + '-' * 5 + '>')

    # UTF-8
    t = timeit.Timer(lambda: SAMPLE.encode)
    utf_time = t.timeit(TRIALS)
    utf_bytes_len = len(SAMPLE.encode())

    # HETF
    t = timeit.Timer(lambda: codec.encode(SAMPLE))
    hetf_time = t.timeit(TRIALS)
    hetf_bytes_len = len(codec.encode(SAMPLE))


    logging.info(f'Sample string used : "{SAMPLE}"')
    logging.info(f'Time for {TRIALS} utf-8 encodes: {utf_time} seconds')
    logging.info(f'Time for {TRIALS} HETF encodes: {hetf_time} seconds')
    logging.info(f'HETF / UTF times = {hetf_time/utf_time}')
    logging.info(f'UTF-8 size: {utf_bytes_len} bytes')
    logging.info(f'HETF size: {hetf_bytes_len} bytes')
    logging.info(f'Space Saved: {round(100 - (hetf_bytes_len / utf_bytes_len * 100), 1)}%')

    logging.info('<' + '-' * 5 + 'END SPEED TESTS' + '-' * 5 + '>')


def test_file_encode_decode():
    logging.info('<' + '-' * 5 + 'START FILE ENCODE / DECODE TESTS' + '-' * 5 + '>')

    # Encode UTF-8 file to HETF
    encoded_file_path = codec.encode_file(SAMPLE_FILE_PATH)
    t = timeit.Timer(lambda: codec.encode_file(SAMPLE_FILE_PATH))
    hetf_time = t.timeit(TRIALS)

    # Read original UTF-8 Data
    with open(SAMPLE_FILE_PATH, 'r', encoding='utf-8', newline='') as file:
        utf_data = file.read()

    utf_data_bytes_len = len(utf_data.encode())

    with open(encoded_file_path, 'rb') as file:
        hetf_data_bytes_len = len(file.read())

    # Time write UTF-8 to UTF-8
    data = utf_data.encode()

    utf_time = 0
    for i in range(0, TRIALS):
        t1 = time.time()
        with open(SAMPLE_FILE_PATH, 'wb') as file:
            file.write(utf_data.encode())
        t2 = time.time()

        utf_time += t2 - t1

    # Decode encoded file data
    hetf_data = codec.decode_file(encoded_file_path)

    logging.info("Writing decoded data to temp folder...")
    with open('./resources/temp/decoded.txt', 'w+', encoding='utf-8', newline='') as file:
        file.write(hetf_data)

    logging.info(f"Time for {TRIALS} utf-8 encodes: {utf_time / 1000} seconds")
    logging.info(f"Time for {TRIALS} HETF encodes: {hetf_time} seconds")
    logging.info(f'UTF-8 size: {utf_data_bytes_len/1000} Kilobytes')
    logging.info(f'HETF size: {hetf_data_bytes_len/1000} Kilobytes')
    logging.info(f'Space Saved: {round(100 - (hetf_data_bytes_len / utf_data_bytes_len * 100), 1)}%')

    assert utf_data == hetf_data

    logging.info('<' + '-' * 5 + 'END FILE ENCODE / DECODE TESTS' + '-' * 5 + '>')

# Run Tests
test_encode_decode()
test_speeds_vs_utf8()
test_file_encode_decode()
