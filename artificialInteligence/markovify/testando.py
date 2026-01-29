import markovify  # type: ignore
import os

"""
markovify doesn't ahve a stub for combine, so we need to ignore the type checking for that line.
"""

combined_model = None
for dirpath, _, filenames in os.walk("path/to/my/huge/corpus"):
    for filename in filenames:
        with open(os.path.join(dirpath, filename)) as f:
            model = markovify.Text(f, retain_original=False)
            if combined_model:
                combined_model = markovify.combine(models=[combined_model, model])  # type: ignore
            else:
                combined_model = model

print(combined_model.make_sentence())  # type: ignore
