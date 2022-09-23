from pipelines.jobs import power_position
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
# Use this script to test executing the pipleines locally
# planes.etl(1980, 10)
power_position.etl(trade_date='01/03/2022', file_path='/dbfs/tmp/')

df = spark.sql("SELECT * FROM trade.power_position")
df.show()