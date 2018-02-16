from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml import PipelineModel

from flask import Flask, request


# SPARK --------------------------------------------------------------------
spark = SparkSession \
    .builder \
    .master('local[*]') \
    .appName('fraud-api') \
    .getOrCreate()

model = PipelineModel.load('logmodel')

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

# API -----------------------------------------------------------------------
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    values = [(
        int(data['step']),
        data['type'],
        float(data['amount']),
        data['nameOrig'],
        float(data['oldbalanceOrg']),
        float(data['newbalanceOrig']),
        data['nameDest'],
        float(data['oldbalanceDest']),
        float(data['newbalanceDest']),
        int(data['isFraud']),
        int(data['isFlaggedFraud'])
    )]


    df = spark.createDataFrame(values, schema=schema)

    predictions = model.transform(df)
    return str(predictions.select('probability').take(1)[0][0][1])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
