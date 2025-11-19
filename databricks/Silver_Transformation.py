# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC Data Understanding

# COMMAND ----------

df_silver = spark.read.format("csv")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load("abfss://bronze@adlssmart1211.dfs.core.windows.net/amazon_prime_titles.csv")
df_silver.limit(50).display()



# COMMAND ----------

df_silver.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC Data Cleaning

# COMMAND ----------

df_silver_without_empty = df_silver.na.fill({"rating": "Unrated", "country": "Unknown"})
df_silver_without_empty.display()

# COMMAND ----------

df_silver_without_duplicates = df_silver_without_empty.dropDuplicates()

df_silver_without_duplicates.display()

# COMMAND ----------

df_silver_clean = df_silver_without_duplicates.na.fill({"rating": "Unrated", "country": "Unknown", "cast": "Unknown", "director": "Unknown", "description": "Unknown","date_added": "01/01/2025", "release_year": "2020"})
df_silver_clean.display()

# COMMAND ----------

df_silver_clean = df_silver_clean.dropna("any")
df_silver_clean.display()

# COMMAND ----------

df_silver_clean = df_silver_clean.withColumnRenamed("title","content_title")
df_silver_clean.display()

# COMMAND ----------

df_silver_clean = df_silver_clean.withColumn("is_country", when(col("country") == "Unknown", 0).otherwise(1))
df_silver_clean.display()

# COMMAND ----------

df_silver_clean.write.mode("overwrite").format("parquet").save("abfss://silver@adlssmart1211.dfs.core.windows.net/amazon_prime_titles_silver")

# COMMAND ----------



# COMMAND ----------

