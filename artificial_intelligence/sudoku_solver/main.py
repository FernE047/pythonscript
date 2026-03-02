from solver_no_ui import solver_no_ui
from solver_with_ui import solver_ui

USE_UI_FLAG = False

def main() -> None:
    if USE_UI_FLAG:
        solver_ui()
    else:
        solver_no_ui()

if __name__ == "__main__":
    main()