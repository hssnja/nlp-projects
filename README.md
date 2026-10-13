# NLP Course Projects

Two projects I developed for my NLP course: a regex tokenizer and an n-gram
next-word predictor.

## 1. Tokenization

`tokenizer.py` splits text into tokens using a sequence of regular expressions.
It converts English letters to lowercase, separates letters from numbers, and
handles punctuation. The output lists each token and its frequency, along
with the total and unique token counts.

## 2. Next-word prediction

`next_word.py` builds unigram, bigram, trigram, and four-gram frequency tables
from a text corpus. For each order, it predicts the most frequent word following
the last `n - 1` tokens of the input. The unigram prediction is simply the most
frequent token in the corpus. When counts are tied, the first occurrence wins.

## Usage

Requires **Python 3.10+** and uses only the standard library.

Run these commands from the repository folder. On Windows, you can use `py`
instead of `python`.

```bash
# Display token frequencies
python tokenizer.py sample.txt

# Save the frequency report
python tokenizer.py sample.txt --output tokens.txt

# Predict the next word
python next_word.py sample.txt --text "من کتاب خوب"

# Start an interactive session; enter e to exit
python next_word.py sample.txt

# Run tests
python -m unittest -v
```

The prediction example returns `من` for the unigram model and `می` for the
bigram, trigram, and four-gram models.

A short Persian sample is included to try the scripts. To use another corpus,
replace `sample.txt` with the path to a UTF-8 text file. Put local corpora in
`data/` to keep them out of Git.

## Notes

- The tokenizer does not normalize Persian and Arabic character variants or
  perform morphological analysis.
- Prediction uses slightly different tokenization: standalone periods and
  Persian commas are removed, and inputs such as `.5` stay together.
- N-grams can cross sentence boundaries. The model uses raw counts without
  smoothing or backoff, so an unseen context produces no prediction.
- The sample text is for demonstration; it is too small to evaluate prediction
  quality.

