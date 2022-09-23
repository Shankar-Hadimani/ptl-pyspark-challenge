import pytest
from .context import pipelines
from pipelines.utils import config_control as cm
from pyspark.sql import SparkSession


spark = SparkSession.builder.getOrCreate()


class Test_ConfigControl(object):
    def test_isLocal(self):
        assert cm.isLocal() == True