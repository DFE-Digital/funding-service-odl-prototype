import os

from dotenv import load_dotenv

from client.ukrlp_client import stream_providers


def main():
    load_dotenv(override=True)

    updated_since = os.getenv("UKRLP_UPDATED_SINCE", "2026-07-03T00:00:00.000")
    page_size = int(os.getenv("DEFAULT_PAGE_SIZE", "100"))

    print("Starting UKRLP export")
    print(f"UpdatedSince: {updated_since}")
    print(f"PageSize: {page_size}")

    total_rows = 0
    page_number = 1

    while True:
        page_rows = 0

        for payload in stream_providers(
            page_number=page_number,
            page_size=page_size,
            updated_since=updated_since,
        ):
            page_rows += len(payload.MatchingProviderRecords)

        total_rows += page_rows
        print(f"Page {page_number}: {page_rows} rows")

        if page_rows < page_size:
            break

        page_number += 1

    print(f"Total rows: {total_rows}")


if __name__ == "__main__":
    main()
