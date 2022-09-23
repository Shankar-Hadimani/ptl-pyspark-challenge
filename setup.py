from setuptools import setup

setup(name='power_service_pipelines',
      version='0.0.1',
      description='Azure databricks- PySpark App aligned with Databricks-Connect',
      url='https://github.com/Shankar-Hadimani',
      author='Shankar-Hadimani',
      author_email='Shankar.Hadimani@gmail.com',
      packages=['pipelines', 'pipelines.utils', 'pipelines.jobs','dependencies'],
      zip_safe=False)