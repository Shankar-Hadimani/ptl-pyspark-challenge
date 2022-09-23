from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

spark = SparkSession.builder.getOrCreate()

def addDummyColumn(df):
    df = df.withColumn("AnotherColumn", lit(0))
    return df