import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "ukrlp-task-queue")
ACTIVITY_EXECUTOR = ThreadPoolExecutor(max_workers=4)


@activity.defn
def validate_auth_access():
    from client.auth import fetch_access_token_from_env

    access_token, _ = fetch_access_token_from_env()

    return {
        "authenticated": bool(access_token),
    }


@activity.defn
def fetch_provider_summaries(
    page_number=1,
    page_size=5,
    updated_since=None,
):
    from client.ukrlp_client import stream_provider_records

    summaries = []
    for record in stream_provider_records(
        page_number=page_number,
        page_size=page_size,
        updated_since=updated_since,
    ):
        summaries.append(
            {
                "UKPRN": record.UKPRN,
                "ProviderName": record.ProviderName,
                "ProviderStatus": record.ProviderStatus,
                "LastUpdated": record.LastUpdated,
            }
        )
        if len(summaries) >= page_size:
            return summaries

    return summaries


@activity.defn
def summarize_provider_export(providers):
    status_counts = {}
    unique_ukprns = set()
    missing_provider_name_count = 0
    missing_last_updated_count = 0
    oldest_last_updated = None
    newest_last_updated = None

    for row in providers:
        status = str(row.get("ProviderStatus") or "UNKNOWN")
        status_counts[status] = status_counts.get(status, 0) + 1

        ukprn = row.get("UKPRN")
        if ukprn:
            unique_ukprns.add(str(ukprn))

        if not row.get("ProviderName"):
            missing_provider_name_count += 1

        last_updated = row.get("LastUpdated")
        if not last_updated:
            missing_last_updated_count += 1
            continue

        text_value = str(last_updated)
        compare_value = text_value.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(compare_value)
        except ValueError:
            continue

        if oldest_last_updated is None or parsed < oldest_last_updated[0]:
            oldest_last_updated = (parsed, text_value)
        if newest_last_updated is None or parsed > newest_last_updated[0]:
            newest_last_updated = (parsed, text_value)

    return {
        "total_providers": len(providers),
        "unique_ukprn_count": len(unique_ukprns),
        "status_counts": status_counts,
        "missing_provider_name_count": missing_provider_name_count,
        "missing_last_updated_count": missing_last_updated_count,
        "oldest_last_updated": oldest_last_updated[1] if oldest_last_updated else None,
        "newest_last_updated": newest_last_updated[1] if newest_last_updated else None,
    }


@workflow.defn
class ProviderExportWorkflow:
    @workflow.run
    async def run(self, page_size=100, updated_since="1800-01-01"):
        all_rows = []
        page_number = 1

        await workflow.execute_activity(
            validate_auth_access,
            start_to_close_timeout=timedelta(minutes=2),
        )

        while True:
            page_rows = await workflow.execute_activity(
                fetch_provider_summaries,
                args=[page_number, page_size, updated_since],
                start_to_close_timeout=timedelta(minutes=2),
            )

            all_rows.extend(page_rows)

            if len(page_rows) < page_size:
                break

            page_number += 1

        summary = await workflow.execute_activity(
            summarize_provider_export,
            args=[all_rows],
            start_to_close_timeout=timedelta(minutes=2),
        )

        return {
            "providers": all_rows,
            "stats": summary,
        }


async def main():
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

    client = await Client.connect(temporal_address, namespace=temporal_namespace)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ProviderExportWorkflow],
        activities=[
            validate_auth_access,
            fetch_provider_summaries,
            summarize_provider_export,
        ],
        activity_executor=ACTIVITY_EXECUTOR,
    )

    print(
        f"Worker connected to {temporal_address} (namespace={temporal_namespace}, task_queue={TASK_QUEUE})"
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
