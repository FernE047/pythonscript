# type: ignore

## win32com doesn't have stubs for its methods
import win32com.client as client

PDF_FILE_FORMAT = 17


def convert_to_pdf(filepath: str) -> None:
    """Save a pdf of a docx file."""
    try:
        word = client.DispatchEx("Word.Application")
        target_path = filepath.replace(".docx", ".pdf")
        word_doc = word.Documents.Open(filepath)
        word_doc.SaveAs(target_path, FileFormat=PDF_FILE_FORMAT)
        word_doc.Close()
    except Exception as e:
        raise e
    finally:
        word.Quit()


def main() -> None:
    pass


if __name__ == "__main__":
    main()
