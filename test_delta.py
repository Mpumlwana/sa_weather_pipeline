from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
b = SparkSession.builder.master('local[1]')
b = b.config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
b = b.config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
spark = configure_spark_with_delta_pip(b).getOrCreate()
spark.range(5).write.format('delta').mode('overwrite').save('delta_test')
spark.read.format('delta').load('delta_test').show()
spark.stop()
