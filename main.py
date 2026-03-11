import sys
import os

# Add src to path if needed for relative imports when running as script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.ui.app import App

def main():
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
