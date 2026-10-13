# NLP Course Projects

Two projects I developed for my NLP course: a regex tokenizer and an n-gram
next-word predictor.

## 1. Tokenization

`tokenizer.py` splits text into tokens using a sequence of regular expressions.
It converts English letters to lowercase, separates letters from numbers, and
handles punctuation. The output lists each token and its frequency, along
with the total and unique token counts.

## 2. Next-word prediction

The prediction method follows Experiment 5 (Section 2.2.1) of the paper by
my supervisor, Ali Reihanian, and Mohammadreza Feizi-Derakhshi [1]. This project
implements the next-word selection step; it does not reproduce the paper's
human evaluation or its other experiments.

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
python next_word.py sample.txt --text "تو به من"

# Start an interactive session; enter e to exit
python next_word.py sample.txt

# Run tests
python -m unittest -v
```

For this input, the unigram, bigram, trigram, and four-gram predictions are
`من`, `یک`, `نگاه`, and `دروغ`, respectively.

A Persian text sample is included to try the scripts. To use another corpus,
replace `sample.txt` with the path to a UTF-8 text file. Put local corpora in
`data/` to keep them out of Git.

## Notes

- Arabic `ي` and `ك` are normalized to Persian `ی` and `ک` in both the corpus
  and input text. The tokenizer does not perform morphological analysis.
- Prediction uses slightly different tokenization: standalone periods and
  Persian commas are removed, and inputs such as `.5` stay together.
- N-grams can cross sentence boundaries. The model uses raw counts without
  smoothing or backoff, so an unseen context produces no prediction.
- The included text is used for demonstration and training, not as a held-out
  evaluation set. Prediction accuracy has not been evaluated.

## Reference

[1] علی ریحانیان، محمدرضا فیضی درخشی.
«طرح آزمایش‌هایی به منظور مقایسه‌ی کارایی و قدرت پیش‌بینی مدل‌های مختلف n-gram».
اولین کنفرانس بین‌المللی دستاوردهای نوین پژوهشی در مهندسی برق و کامپیوتر.
[Paper on Civilica](https://civilica.com/doc/496991).
English translation of the title: *Designing experiments to compare the
performance and predictive power of different n-gram models.*

[2] علی ریحانیان، محمدرضا فیضی درخشی، علیرضا فیضی درخشی، میرعرفان غیبی
«ارایه ی یک جداساز کلمات با استفاده از عبارات باقاعده».

International Conference on Electrical and Computer Engineering with Emphasis on Indigenous Knowledge،Tehran
[Paper on Civilica](https://civilica.com/doc/725634).



