from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoder

spark = SparkSession \
    .builder \
    .master('local[*]') \
    # .config("spark.driver.memory", "6g") \
    .appName('fraud') \
    .getOrCreate()

schema = StructType([
    StructField('step', IntegerType(), True),
    StructField('type', StringType(), True),
    StructField('amount', DoubleType(), True),
    StructField('nameOrig', StringType(), True),
    StructField('oldbalanceOrg', DoubleType(), True),
    StructField('newbalanceOrig', DoubleType(), True),
    StructField('nameDest', StringType(), True),
    StructField('oldbalanceDest', DoubleType(), True),
    StructField('newbalanceDest', DoubleType(), True),
    StructField('isFraud', IntegerType(), True),
    StructField('isFlaggedFraud', IntegerType(), True)
])

features = 'amount oldbalanceOrg newbalanceOrig oldbalanceDest'.split()

df = spark.read.csv('../data/train.csv', schema=schema)

lr = LogisticRegression(labelCol="isFraud", featuresCol="features")

savepipeline = Pipeline(stages=[
    StringIndexer().setInputCol('type').setOutputCol('typeIndexed'),
    OneHotEncoder(inputCol='typeIndexed', outputCol='typeEncoded'),
    VectorAssembler(inputCols=features + ['typeEncoded'], outputCol='features'),
    lr
])

model = savepipeline.fit(df)
model.save('logmodel')
