from dotenv import load_dotenv
import os
import subprocess
import sys


def main():
    load_dotenv()

    subprocess.run(
        [sys.executable, "extract_census.py"],
        check=True
    )

    subprocess.run(
        # single threaded to avoid race condition on index creation.
        ["dbt", "build", "--threads", "1"],
        env=os.environ.copy(),
        check=True
    )


if __name__ == "__main__":
    main()