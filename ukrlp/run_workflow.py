import asyncio
import json
import os
import time
from datetime import datetime

from temporalio.client import Client

WORKFLOW_NAME = "ProviderExportWorkflow"


def build_stats(providers):
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


async def main():
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    task_queue = os.getenv("TEMPORAL_TASK_QUEUE", "ukrlp-task-queue")

    updated_since = os.getenv("UKRLP_UPDATED_SINCE", "2026-07-03")
    page_size = int(os.getenv("DEFAULT_PAGE_SIZE", "100"))
    output_json = os.getenv("UKRLP_OUTPUT_JSON", "ukrlp_providers_all.json")

    client = await Client.connect(temporal_address, namespace=temporal_namespace)
    workflow_id = f"ukrlp-export-all-{int(time.time())}"

    print("Starting workflow full export")
    print(f"WorkflowName: {WORKFLOW_NAME}")
    print(f"WorkflowID: {workflow_id}")
    print(f"UpdatedSince: {updated_since}")
    print(f"PageSize: {page_size}")
    print("Running workflow...")

    result = await client.execute_workflow(
        WORKFLOW_NAME,
        args=[page_size, updated_since],
        id=workflow_id,
        task_queue=task_queue,
    )

    if isinstance(result, dict):
        providers = result.get("providers", [])
        stats = result.get("stats") or build_stats(providers)
    else:
        providers = result
        stats = build_stats(providers)

    output = {
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "workflow_name": WORKFLOW_NAME,
        "workflow_id": workflow_id,
        "updated_since": updated_since,
        "page_size": page_size,
        "stats": stats,
        "providers": providers,
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("Workflow complete")
    print(f"Output file: {output_json}")
    print(f"Total providers: {stats['total_providers']}")
    print(f"Unique UKPRNs: {stats['unique_ukprn_count']}")
    print(f"Oldest LastUpdated: {stats['oldest_last_updated']}")
    print(f"Newest LastUpdated: {stats['newest_last_updated']}")
    print(f"Status counts: {stats['status_counts']}")


if __name__ == "__main__":
    asyncio.run(main())
