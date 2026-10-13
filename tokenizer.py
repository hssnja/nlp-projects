"""Project 1: regex tokenization and token frequencies (UTF-8 text)."""

import argparse
from collections import Counter
from pathlib import Path
import re


def tokenize(text: str, *, prediction_mode: bool = False) -> list[str]:
    """Normalize letter variants and apply the course regex rules in order.

    Prediction mode preserves Project 2's punctuation rule and removes only
    the period and Persian comma. This is not a linguistic Persian tokenizer.
    """
    # Normalize Arabic letter variants commonly found in Persian text.
    text = text.translate(str.maketrans({"ي": "ی", "ك": "ک"})).lower()
    text = re.sub('([a-z]+)(?=[0-9]+)', '\\g<0> ', text)
    text = re.sub('([0-9]+)(?=[a-z]+)', '\\g<0> ', text)
    text = re.sub('([a-z]+)(?=[^a-z\\s]+)', '\\g<0> ', text)
    text = re.sub('([^a-z\\s]+)(?=[a-z]+)', '\\g<0> ', text)
    text = re.sub('([0-9]+)(?=[^0-9\\.:\\/\\s]+)', '\\g<0> ', text)
    text = re.sub('([^0-9\\.:\\/\\s]+)(?=[0-9]+)', '\\g<0> ', text)
    text = re.sub('([0-9]+)([\\.:][0-9]+)(?=[\\.:\\/][0-9]+)', ' \\g<1> \\g<2> ', text)
    text = re.sub('([\\.:][0-9]+)([\\.:\\/][0-9]+)', ' \\g<1> \\g<2> ', text)
    text = re.sub(
        r'(?<=[^0-9\s])([.:/])' if prediction_mode else r'(?<![0-9])([.:/])',
        r' \g<0> ', text,
    )
    text = re.sub('([،,؟»؛!")\\(])', ' \\g<0> ', text)
    text = re.sub('\\\\', ' \\g<0> ', text)
    text = re.sub('(?<=[0-9])[\\.:\\/](?![0-9]+)', ' \\g<0> ', text)
    text = re.sub('(?<![0-9])[^\\w\\s](?![0-9]+)', '\\g<0> ', text)
    text = re.sub('(\\s)+', ' ', text)
    tokens = text.split(' ')
    tokens = [r for r in tokens if r != '']
    if prediction_mode:
        tokens = [token for token in tokens if token not in {'.', '،'}]
    return tokens


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 corpus file")
    parser.add_argument("-o", "--output", type=Path, help="Save the frequency report")
    args = parser.parse_args()
    try:
        counts = Counter(tokenize(args.input.read_text(encoding="utf-8")))
        lines = [f"Total tokens: {sum(counts.values())}",
                 f"Unique tokens: {len(counts)}", "", "Token\tCount"]
        lines.extend(f"{token}\t{counts[token]}" for token in sorted(counts))
        report = "\n".join(lines) + "\n"
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report, end="")
    except (OSError, UnicodeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
