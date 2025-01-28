import sys
import os


def main():
    try:
        from fastapi_admin.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import FastAPI-Admin. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv[1:])

if __name__ == "__main__":
    main()
