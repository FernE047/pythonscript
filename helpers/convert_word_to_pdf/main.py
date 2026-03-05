# type: ignore

## win32com doesn't have stubs for its methods
import win32com.client as client
from pathlib import Path

PDF_FILE_FORMAT = 17


def convert_to_pdf(filepath: Path) -> None:
    """Save a pdf of a docx file."""
    try:
        word = client.DispatchEx("Word.Application")
        target_path = filepath.with_suffix(".pdf")
        with word.Documents.Open(str(filepath)) as word_doc:
            word_doc.SaveAs(str(target_path), FileFormat=PDF_FILE_FORMAT)
    except Exception as e:
        raise e 
    finally:
        word.Quit()


def main() -> None:
    pass


if __name__ == "__main__":
    main()
