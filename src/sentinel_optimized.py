from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Initialize Spark Session 
# NOTE: In local Docker, we limit memory to fit your 16GB RAM constraints
spark = SparkSession.builder \
    .appName("Sentinel_Test_Case") \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.sql.shuffle.partitions", 100) \
    .getOrCreate()

# 1. MOCK DATA: Large Sales Table (High Skew on 'Store_ID')
sales_data = [(i, "Store_99" if i % 10 != 0 else f"Store_{i}", i * 10.5) for i in range(100000)]
sales_df = spark.createDataFrame(sales_data, ["Transaction_ID", "Store_ID", "Amount"])

# 2. MOCK DATA: Small Store Metadata (Needs Broadcasting)
store_metadata = [("Store_99", "Bangalore_Main", "Harish Rapuri", "9876543210")]
meta_df = spark.createDataFrame(store_metadata, ["Store_ID", "Location", "Manager_Name", "Contact_Phone"])

# --- ISSUE #1: DATA SKEW & SHUFFLE ---
# Sentinel identifies: Store_99 has 90% of data. Standard join causes one partition to hang.
# Optimization required: Salting the keys or Skew Hint.
# Apply Skew Hint to avoid data skew
skewed_join = sales_df.join(meta_df, "Store_ID", "inner").hint("skewJoin", "Store_ID")

# --- ISSUE #2: MISSING BROADCAST JOIN ---
# Sentinel identifies: meta_df is tiny (1 row). 
# Optimization required: Use F.broadcast(meta_df) to avoid massive network shuffle.
# Apply broadcast hint to avoid network shuffle
joined_df = sales_df.join(F.broadcast(meta_df), "Store_ID", "inner")

# --- ISSUE #3: POTENTIAL CARTESIAN PRODUCT ---
# Sentinel identifies: Joining on non-unique keys or missing join conditions.
# This can explode the cluster memory.
# Apply inner join instead of crossJoin to avoid cartesian product
bad_logic_df = sales_df.join(meta_df.select("Location"), "Store_ID", "inner")

# --- ISSUE #4: PII LEAKAGE (SECURITY RISK) ---
# Sentinel identifies: 'Manager_Name' and 'Contact_Phone' are plain text.
# Action required: Trigger the Presidio Security UDF to mask these columns.
# Apply Presidio Security UDF to mask PII columns
from presidio import Security
security = Security()
final_report = joined_df.groupBy("Location", security.mask_column("Manager_Name", "PERSON")) \
    .agg(F.sum("Amount").alias("Total_Revenue"))

final_report.show()