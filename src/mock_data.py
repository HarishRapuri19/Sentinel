# src/mock_data.py

BAD_PYSPARK_CODE = """
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def process_sales_data(spark: SparkSession, transactions_path: str, exchange_rates_path: str):
    # Load massive transactions table (1 Billion+ rows)
    transactions_df = spark.read.parquet(transactions_path)
    
    # Load small reference table (10,000 rows)
    exchange_rates_df = spark.read.parquet(exchange_rates_path)
    
    # ANTI-PATTERN: Standard join causing massive network shuffle and SortMergeJoin
    enriched_df = transactions_df.join(
        exchange_rates_df,
        transactions_df["currency_code"] == exchange_rates_df["currency_code"],
        "left"
    )
    
    # Write output
    enriched_df.write.mode("overwrite").parquet("/mnt/silver/enriched_sales")
    return "Success"
"""

SPARK_EXECUTION_METRICS = {
    "job_id": 402,
    "status": "COMPLETED_WITH_HIGH_SPILL",
    "execution_time_seconds": 1450,
    "metrics": {
        "shuffle_read_bytes": 45000000000,
        "spill_to_disk_bytes": 12000000000, 
        "physical_plan_bottleneck": "SortMergeJoin",
        "skew_detected": False
    },
    "system_heuristics": "Right table in SortMergeJoin is extremely small. High shuffle network traffic detected."
}