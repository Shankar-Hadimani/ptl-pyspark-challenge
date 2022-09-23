from pyspark.sql import SparkSession
from pipelines.utils import config_control as cm
from pipelines.utils.trading import get_trades
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import StringType, DoubleType
from pyspark.sql.functions import coalesce, concat, to_timestamp, unix_timestamp
from pyspark.sql.functions import lit, monotonically_increasing_id, row_number, max
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import StringType, DoubleType
from pyspark.sql.window import Window
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from dependencies.run_spark import run_spark
from pytz import timezone 
from datetime import datetime
import pandas as pd


### set spark session
app_name = "power_position_app"
spark, log = run_spark(app_name)

### define schema
trade_schema = StructType(
    [StructField("date", StringType(), True),
     StructField("time", StringType(), True),
     StructField("volume", DoubleType(), True),
     StructField("id", StringType(), True)
    ])

### constant filename
file_date = datetime.now(timezone('Europe/London')).strftime("%Y%m%d_%H%M")
out_filename = "PowerPosition_"+ file_date +".csv"

def extract_trades(trade_date, schema=trade_schema) -> DataFrame:
  try:
    trades = get_trades(date=trade_date)
  except Exception as e:
    log.error(f'ERROR: Unable to extract Volumes for Trade Date. Trade date seems "{trade_date}" incorrect : ==> ' + str(e))
  pdf = pd.DataFrame(trades[0])
  df = spark.createDataFrame(pdf, schema)
  return df


def transform(df: DataFrame) -> DataFrame :
  try:
    sdf = df.withColumn("timestamp", to_timestamp(concat(df["date"],lit(' '),df["time"]),"dd/MM/yyyy HH:mm"))
    sdf1 = sdf.withColumn("idx1", monotonically_increasing_id())

    # Create the window specification
    w1 = Window.orderBy("idx1")
    w2 = Window.orderBy("idx2")

    # Use row number with the window specification
    sdf1 = sdf1.withColumn("id", row_number().over(w1)).drop("idx1")

    ### generate minute-wise data ranges between MIN and MAX Date Values
    dates_range = (sdf.groupBy("date")
                .agg(F.max(F.col("timestamp")).alias("max_timestamp"),F.min(F.col("timestamp")).alias("min_timestamp"))
                .select("date",F.expr("sequence(min_timestamp, max_timestamp, interval 5 minutes)").alias("new_timestamp"))
                .withColumn("new_timestamp", F.explode("new_timestamp"))
                .withColumn("idx2", monotonically_increasing_id())
                )
    # Add row number to data ranges           
    dates_range = dates_range.withColumn("id", row_number().over(w2)).drop("idx2")

    """
    # Join date ranges with orignal dataframe. 
    # Replace missing dates with date range values
    # and, replace missing volumes with zero's
    """
    w = Window.partitionBy("date").orderBy("id")
    result = (dates_range
            .join(sdf1, ["id", "date"], "left")
            .select("id","date","new_timestamp",
                    *[F.last(F.col(c), ignorenulls=True).over(w).alias(c)
                for c in sdf.columns if c not in ("id", "date", "time","volume","new_timestamp")],"volume")
            .fillna(0, subset=['volume'])
            .withColumn("hour", F.date_trunc('hour',"new_timestamp"))
            .groupby("hour").sum("volume")
          )
    result = result.select(F.col('hour').alias("TimeStamp"), F.col('sum(volume)').alias("Aggregated_Volume"))
  except Exception as e:
    log.error(f'ERROR: There are one or more errors while transforming and aggregating data : ==> ' + str(e))

  return result



def write_data(df: DataFrame, file_path:str):

  try:
    ### create database from config file
    cm.setDatabase()

    ### create delta table 
    spark.sql("DROP TABLE IF EXISTS power_position")
    df.write.format("delta").mode("overwrite").saveAsTable("power_position")

    (df.coalesce(1).write.mode("overwrite")
    .option("header", "true")
    .option("treatEmptyValuesAsNulls", "true")
    .option("nullValue", " ")
    .csv(file_path)
    )
  except Exception as e:
    log.error(f'ERROR: There are one or more errors while writinng data to  DELTA/CSV file: ==> ' + str(e))

  return None


def etl(trade_date:str, file_path:str) -> None:
  try:
    file_path = file_path.rstrip('/')+'/'+ out_filename
  except Exception as e:
    log.error(f'ERROR: Incorrect input file path -  "{file_path}": ==> ' + str(e))
  pdf = extract_trades(trade_date, trade_schema)
  df = transform(pdf)
  write_data(df, file_path)

