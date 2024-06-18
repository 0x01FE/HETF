import logging
import timeit

FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(encoding="utf-8", level=logging.DEBUG, format=FORMAT)

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

            self.word_indexes[line] = index
            self.words.append(line)
            self.avg_len += len(line)

            index += 1

            if index >= (2**14) - RESERVED_WORDS:
                break

        self.avg_len /= index - RESERVED_WORDS

    def encode_word(self, word: str) -> bytes:
        if word == ' ':
            return SPACE_BYTE
        elif word == '\n':
            return NEWLINE_BYTE

        # logging.debug(f"Encoding word \"{word}\"")

        if ' ' in word:
            # logging.debug("Space found in word while encoding")
            return
        elif word not in self.word_indexes:
            output = FLAG_BYTE

            output += word.encode('utf-8')

            output += FLAG_BYTE

            # logging.debug("Word not found in common words, converting to raw utf8")
            # logging.debug(f'Bytes: {output}, Length: {len(output)}')

            return output

        # Ok now we encode
        b = ""
        index: int = self.word_indexes[word]
        num: str = bin(index)[2:]

        if len(num) > 7:
            b += '1'
            b += '0' * (15 - len(num))
            b += num

        else:
            b += '0' * (8 - len(num))
            b += num

        logging.debug(f'Bytes: {b}, Length: {len(b)}')

        return int(b, 2).to_bytes(len(b) // 8, byteorder='big')

    def encode(self, raw: str) -> bytes:
        out = bytes()

        space_index: int = raw.find(' ')
        while (space_index != -1):

            out += self.encode_word(raw[:space_index])

            out += SPACE_BYTE
            raw = raw[space_index+1:]
            logging.debug(raw)

            space_index = raw.find(' ')

        out += self.encode_word(raw) # Encode the last word

        return out

    def decode_word(self, word: bytes) -> str:
        offset = len(word) == 2

        logging.debug(f"Decoding word \"{word}\"")

        if not word:
            logging.error("Word was None.")
            return ''

        if word[0] == 1:
            unicode = word[1:-1]
            return unicode.decode()

        index = int.from_bytes(word, "big")

        # This needs to be done because 2 bytes words have a 1 at the start, which will offset the index. By A LOT
        if offset:
            index -= MAGIC_NUMBER

        return self.words[index]

    """
    Works much like the inverse of encoding for some reason...
    """
    def decode(self, raw: bytes) -> str:
        out = ""

        space_index: int = raw.find(SPACE_BYTE)
        while (space_index != -1):
            out += self.decode_word(raw[:space_index])

            out += ' '
            raw = raw[space_index+1:]

            space_index = raw.find(SPACE_BYTE)

        out += self.decode_word(raw)

        return out

    def encode_file(self, file_path: str) -> str:
        write_bytes = bytes()
        with open(file_path, 'r') as file:
            for line in file.readlines():
                write_bytes += self.encode(line)

        new_file_path = 'encoded-' + file_path
        with open(new_file_path, 'wb+') as file:
            file.write(write_bytes)

        return new_file_path

    def decode_file(self, file_path: str) -> str:

        t = ""
        with open(file_path, 'rb') as file:
            for line in file.readlines():
                t += foo.decode(line)

        return t


foo = TextEncoder('./wiki-100k.txt')

# sample = "The quick brown fox jumped over the lazy dog"

# print('My Encoding')
# print(x := foo.encode(sample))
# print(len(x))
# print(foo.decode(x))

# print()

# print("UTF-8")
# print(len(sample.encode('utf-8')))

x = foo.encode_file('test.txt')
print(foo.decode_file(x))




# print(len(x))
# i = int.from_bytes(x, "big")
# i -= MAGIC_NUMBER
# print(i)
# print(foo.words[i])


exit()



utf = sample.encode()
trials = 100

t = timeit.Timer(sample.encode)
utf_time = t.timeit(trials)


output = foo.encode(sample)

t = timeit.Timer(lambda: foo.encode(sample))
mine_time = t.timeit(trials)

print("My Text Encoder")
print(output)
print(len(output))
print(f"My time: {mine_time}")
print("UTF-8")
print(utf)
print(len(utf))
print(f"UTF Time: {utf_time}")

percent_gain = round(len(output) * 100/len(utf), 3)

print(f'\nGain: {percent_gain}%')

# with open('out', 'wb+') as file:
#     file.write(output)
