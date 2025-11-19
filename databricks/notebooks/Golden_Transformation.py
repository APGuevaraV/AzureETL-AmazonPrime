# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df_golden = spark.read.format("parquet")\
            .option("header", "true")\
            .option("inferSchema", "true")\
            .load("abfss://silver@adlssmart1211.dfs.core.windows.net/amazon_prime_titles_silver")
df_golden.display()

# COMMAND ----------

df_golden_renamed = df_golden.withColumn("date_added", to_date(col("date_added"), "MM/dd/yyyy"))
df_golden_with_year= df_golden_renamed.withColumn("year_added", year(col("date_added")))

df_golden_with_year.display()

# COMMAND ----------

df_golden_with_year = df_golden_with_year.withColumn("category_1",split(df_golden_with_year["listed_in"],",")[0])
df_golden_with_year = df_golden_with_year.withColumn("category_2",split(df_golden_with_year["listed_in"],",")[1])


df_golden_with_year.display()

# COMMAND ----------

df_golden_final = df_golden_with_year.withColumn("category_2", when(col("category_2").isNull(),"Unknown").otherwise(col("category_2")))

# COMMAND ----------

df_golden_final.display()
df_golden_final.write.mode("overwrite").format("delta").option("header", "true").save("abfss://golden@adlssmart1211.dfs.core.windows.net/amazon_prime_titles_gold")

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG main;
# MAGIC create database golden_layer;

# COMMAND ----------

df_golden_final.write.mode("overwrite").format("delta").option("header", "true").option("path","abfss://golden@adlssmart1211.dfs.core.windows.net/amazon_prime_titles_gold").saveAsTable("golden_layer.prime_golden")

# COMMAND ----------

