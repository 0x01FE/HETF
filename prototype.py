import logging

FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(encoding="utf-8", level=logging.INFO, format=FORMAT)

SPACE_BYTE = (0).to_bytes(1, byteorder='big')
FLAG_BYTE = (1).to_bytes(1, byteorder='big')
NEWLINE_BYTE = (2).to_bytes(1, byteorder='big')
MAGIC_NUMBER = 32768
RESERVED_WORDS = 3

class TextEncoder:
    word_indexes: dict
    words: list
    avg_len: float

    def __init__(self, file_path: str):
        self.word_indexes = {}
        self.avg_len = 0
        self.words = [' ', None, '\n']

        self.read_file(file_path)

    def read_file(self, file_path: str) -> None:

        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()

        index = RESERVED_WORDS
        for line in data:

            # Skip Comments
            if line[0] == '#':
                continue

            if line in self.word_indexes:
                continue

            line = line.strip()

            self.word_indexes[line.encode()] = index
            self.words.append(line)
            self.avg_len += len(line)

            index += 1

            if index >= (2**15) - RESERVED_WORDS:
                break

        self.avg_len /= index - RESERVED_WORDS

    def encode_word(self, word: bytes) -> bytes:
        if word == b' ':
            return SPACE_BYTE
        elif word == b'\n':
            return NEWLINE_BYTE

        logging.debug(f"Encoding word \"{word}\"")

        if b' ' in word:
            logging.error("Space found in word while encoding")
            return
        elif word not in self.word_indexes:
            output = FLAG_BYTE

            output += word

            output += FLAG_BYTE

            return output

        # Ok now we encode
        b = ""
        index: int = self.word_indexes[word]
        num: str = bin(index)[2:]
        if len(num) > 15:
            logging.error(f'Length of word "{word} is over 15 bits."')

        if len(num) > 7:
            b += '1'
            b += '0' * (15 - len(num))
            b += num

        else:
            b += '0' * (8 - len(num))
            b += num

        logging.debug(f'Bytes: {b}, Length: {len(b)}')

        return int(b, 2).to_bytes(len(b) // 8, byteorder='big')

    def encode(self, raw: bytes | str) -> bytes:
        if type(raw) == str:
            raw = raw.encode()

        out = bytes()

        space_index: int = raw.find(b' ')
        while (space_index != -1):

            out += self.encode_word(raw[:space_index])

            out += SPACE_BYTE
            raw = raw[space_index+1:]

            space_index = raw.find(b' ')

        if raw:
            out += self.encode_word(raw) # Encode the last word

        return out

    def decode_word(self, word: bytes) -> str:
        offset: bool = len(word) == 2

        logging.debug(f"Decoding word \"{word}\"")

        if not word:
            logging.error("Word was None.")
            return ''

        index = int.from_bytes(word, "big")

        logging.debug(f"Index found for word is {index}")
        # This needs to be done because 2 bytes words have a 1 at the start, which will offset the index. By A LOT
        if offset:
            index -= MAGIC_NUMBER
            logging.debug(f"Word is 2 bytes, offsetting index... Result: {index}")

        return self.words[index]

    """
    Works much like the inverse of encoding for some reason...
    """
    def decode(self, raw: bytes) -> str:
        out = ""

        while raw:
            double = 1
            byte = raw[0]

            # 1 signals the start of a raw UTf-8 string
            if byte == 1:
                end_utf_index = raw[1:].find(FLAG_BYTE)

                out += raw[1:end_utf_index + 1].decode()
                raw = raw[end_utf_index + 2:]

            else:

                # The best way to check if a word is over 1 byte i think
                if byte >= 128:
                    double = 2

                out += self.decode_word(raw[0:double])
                raw = raw[double:]

        return out

    def encode_file(self, file_path: str) -> str:
        write_bytes = bytes()
        with open(file_path, 'rb') as file:
            line = file.read()
            write_bytes = self.encode(line)

        new_file_path = file_path[:len(file_path) - len(file_path.split('.')[-1]) - 1] + '-encoded.' + file_path.split('.')[-1]
        with open(new_file_path, 'wb+') as file:
            file.write(write_bytes)

        return new_file_path

    def decode_file(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            line = file.read()
            return self.decode(line)
