"""temporal"""
import os
from datetime import timedelta
import aiopg
from temporalio import workflow, activity


@activity.defn
async def execute_db_query(query):
    """Activity to execute a database query."""
    database_url = os.getenv('DATABASE_URL')
    try:
        pool = await aiopg.create_pool(dsn=database_url)
        async with pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    if cur.description:
                        columns = [desc[0] for desc in cur.description]
                        data = await cur.fetchall()
                        result = [dict(zip(columns, row)) for row in data]
                        return {"data": result}, 201
                    return {"status": "sucess"}, 201
            except Exception as e:
                return {"status": "Error executing query", "message": str(e)}

    except Exception as e:
        return {"status": "Error connecting to database", "message": str(e)}


@workflow.defn
class QueryWorkflow:
    """workflow class"""
    @workflow.run
    async def run(self, query):
        """workflow.run"""
        result = await workflow.execute_activity(
            execute_db_query,
            query,
            start_to_close_timeout=timedelta(seconds=10)
        )
        return result
