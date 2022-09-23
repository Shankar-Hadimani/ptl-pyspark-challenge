import pytest
from .context import pipelines
from pipelines.jobs import power_position
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

class Test_PowerService(object):
    def mock_extract_trades():
        data_df = power_position.extract_trades("01/03/2021")
        return data_df

    def test_transform(self):
        df = Test_PowerService.mock_extract_trades()
        df = power_position.transform(df)
        assert "TimeStamp" in df.columns
        assert "Aggregated_Volume" in df.columns