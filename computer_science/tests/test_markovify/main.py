import markovify  # type: ignore
from pathlib import Path

"""
markovify doesn't have a stub for combine, so we need to ignore the type checking for that line.
"""


def main() -> None:
    combined_model = None
    for file in Path().rglob("*"):
        if not file.is_file():
            continue
        with file.open(encoding="utf-8", errors="ignore") as f:
            model = markovify.Text(f, retain_original=False)
            if combined_model is None:
                combined_model = model
            else:
                combined_model = markovify.combine(models=[combined_model, model])  # type: ignore
    if combined_model is not None:
        print(combined_model.make_sentence())  # type: ignore


if __name__ == "__main__":
    main()
