"""py"""
import asyncio
import concurrent.futures
from temporalio.client import Client
from temporalio.worker import Worker
from temporal import QueryWorkflow, execute_db_query


async def main():
    """to define a worker"""
    client = await Client.connect("temporal:7233", namespace="default")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        worker = Worker(
          client,
          task_queue="task-queue",
          workflows=[QueryWorkflow],
          activities=[execute_db_query],
          activity_executor=executor,
        )
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
