# NLP Course Projects

Two small Python projects by Hasan Jafari: a rule-based tokenizer and a
frequency-based next-word predictor. Developed as coursework and cleaned up
for reproducible command-line use.

## Run

Requires **Python 3.10+**. No third-party packages or downloads are needed.
Open a terminal in this folder. On Windows, use `py` instead of `python` if needed.

```bash
# Project 1: print token frequencies, or save them
python tokenizer.py sample.txt
python tokenizer.py sample.txt --output tokens.txt

# Project 2: predict using each of the four n-gram orders
python next_word.py sample.txt --text "من کتاب خوب"

# Interactive mode (enter e to exit)
python next_word.py sample.txt

# Run tests
python -m unittest -v
```

Replace `sample.txt` with your own UTF-8 text file; quote paths containing spaces.
The included text is a tiny illustrative example, not an evaluation dataset.
The original `Book Sample.txt` corpus was not supplied and is not included.
Keep personal or unlicensed corpora in the ignored `data/` directory.

## Projects

- **`tokenizer.py`** lowercases text, applies the original ordered regex rules,
  and reports token frequencies in sorted token order. Punctuation is counted.
- **`next_word.py`** counts unigrams through four-grams. It uses the final
  `n - 1` input tokens as context and returns the most frequent continuation.
  Ties are resolved by first occurrence in the training corpus, as before.
  Unigrams return the most frequent corpus token regardless of the input.

For the sample query above, the predictions are `من`, `می`, `می`, and `می`
for orders 1 through 4, respectively.

## Method and limitations

The regex tokenizer is a course exercise, not a full Persian language
preprocessor: it does not normalize Persian/Arabic character variants or
handle morphology and zero-width joiners linguistically.

Project 2 retains its original preprocessing: standalone `.` and `،` tokens
are removed, and its punctuation rule differs slightly from Project 1
(for example, `.5` stays together). These differences are explicit in the
shared tokenizer's `prediction_mode` option.

N-grams span the whole token stream, including sentence boundaries after
punctuation removal. There is no smoothing, backoff, or sentence-boundary
modeling. Unseen contexts produce no prediction. This preserves the original
method; it is not a modern language model, and no accuracy claims are made.

## Cleanup

Shared tokenization replaces duplicate functions while retaining both original
behaviors. Standard-library counters replace NumPy and NLTK frequency counting.
The predictor stores context counts instead of repeatedly scanning every n-gram.
Scripts now have explicit input paths, safe imports, command-line options,
and clear errors for unreadable files, empty corpora, and invalid orders.

The unfinished `AAI_Project2_code_playground.py` was a duplicate prototype with
a syntax error; it is intentionally excluded. The runnable Project 2 is the
basis of `next_word.py`. Tests cover tokenization, prediction, ties, and edge cases.
