"""Project 2: frequency-based next-word prediction using 1–4-grams."""

import argparse
from collections import Counter
from pathlib import Path

from tokenizer import tokenize


class NGramPredictor:
    """Count continuations; break ties by first occurrence in the corpus."""

    def __init__(self, corpus: str) -> None:
        tokens = tokenize(corpus, prediction_mode=True)
        if not tokens:
            raise ValueError("The corpus contains no usable tokens.")
        self.counts: dict[int, dict[tuple[str, ...], Counter[str]]] = {}
        for order in range(1, 5):
            contexts: dict[tuple[str, ...], Counter[str]] = {}
            for start in range(len(tokens) - order + 1):
                context = tuple(tokens[start:start + order - 1])
                word = tokens[start + order - 1]
                contexts.setdefault(context, Counter())[word] += 1
            self.counts[order] = contexts

    def predict(self, text: str, order: int) -> str | None:
        """Return the most frequent continuation, or None for unseen contexts.

        Raise ValueError for unsupported orders or insufficient input context.
        Unigrams ignore the input text. No smoothing or backoff is applied.
        """
        if isinstance(order, bool) or not isinstance(order, int) or order not in range(1, 5):
            raise ValueError("order must be an integer from 1 to 4.")
        tokens = tokenize(text, prediction_mode=True)
        if len(tokens) < order - 1:
            raise ValueError(f"Enter at least {order - 1} usable tokens.")
        context = tuple(tokens[-(order - 1):]) if order > 1 else ()
        candidates = self.counts[order].get(context)
        return candidates.most_common(1)[0][0] if candidates else None


def show_predictions(model: NGramPredictor, text: str) -> None:
    for order in range(1, 5):
        try:
            result = model.predict(text, order)
            print(f"{order}-gram: {result if result is not None else 'No matching context.'}")
        except ValueError as exc:
            print(f"{order}-gram: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="UTF-8 training text")
    parser.add_argument("--text", help="Predict once instead of starting a prompt")
    args = parser.parse_args()
    try:
        model = NGramPredictor(args.corpus.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    if args.text is not None:
        show_predictions(model, args.text)
        return
    while True:
        try:
            text = input("\nEnter text (e to exit): ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.strip().lower() == "e":
            break
        show_predictions(model, text)


if __name__ == "__main__":
    main()
