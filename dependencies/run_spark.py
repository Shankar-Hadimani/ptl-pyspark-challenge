from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils 
from dependencies import logging



def run_spark(app_name: str):
    """create spark session and attach spark logger object
    Args:
        app_name (str): set spark session and configuration
    Returns:
        _type_: Spark session and logger
    """
    spark_session = SparkSession.builder.appName(app_name).getOrCreate()
    spark_logger = logging.Log4j(spark_session)
    return spark_session, spark_logger