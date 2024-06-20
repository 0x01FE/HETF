# Encoding

The base question here is how can we save not only storage space when storing messages but also save bandwidth when sending them?

An idea could be to look at the top _n_ used words in the english language and give them an unique id. That way you might be able to encode a 5 letter word (or 5 byte message) into maybe 2 bytes.

So assuming we're using 16 bits per word we can shorten the most common `65536` words into 2 bytes. That's a massive space save already, but what we need to think about is when words __NOT__ contained within those top 65536 words are used. How do we signal to the machine that when decoding a part of the message it CANNOT use the heuristic. We also need to consider making this encoding variable length. Even with 16 bits most words will fall into the top 1000 or so, which is only 10 bits. For this we can pull from something like UTF-8 and perhaps make our leading bit signal if the word is 1, or 2 bytes.

```
0xxxxxxx

1xxxxxxx xxxxxxxx
```

This of course ends up wasting 1-2 bits, so rather than 2^16 combintations available we're down to 2^15 (32768).

## Plural Bit

Something else to consider is depending on how many words are just another word with `s` added to it (`word` and `words` for example), we could add a bit to declare it as some other word +`s`.

Not sure how much if any space you would save with this.

## Other Words

There's one very large flaw with this system though, how do we deal with words that aren't in the top 32768 most common words? We need to deal with random strings of characters still. The obvious solution is to have some sort of identifier that says "hey everything after this is RAW unicode characters", with some sort of terminating character.

Since we're going to be a little wasting space with words that aren't the most common, these flag characters should be
    - The same character
    - In the first byte of our variable length encoding

Because the main goal of our encoding method is to translate words to bytes, we don't need to retain compatibility with ASCII or UTF8. This means our flag character can be anything we want. Let's go with `0x01` for now.

