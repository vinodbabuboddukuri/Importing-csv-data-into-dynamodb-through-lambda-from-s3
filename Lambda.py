import boto3
import csv
def lambda_handler(event, context):
    region='us-east-1'
    try: 
        # get a handle on s3
        session = boto3.Session(region_name=region)
        s3 = session.resource('s3')
        dyndb = boto3.client('dynamodb', region_name=region)
        bucket = s3.Bucket('Your Bucket Name')  #Enter your s3 bucket Name
        obj = bucket.Object(key='#File Name.csv') #Object Name
        response = obj.get()
        # read the contents of the file
        lines = response['Body'].read().decode('utf-8').splitlines()
 
        firstrecord=True
        csv_reader = csv.reader(lines, delimiter=',', quotechar='"')
        for row in csv_reader:
            if (firstrecord):
                firstrecord=False
                continue
            #Based on the columes you should add
            Emp_id = row[0] #Primary key
            SecondCol = row[1]
            ThirdCol = row[2]
            ForthCol = row[3]
            response = dyndb.put_item(
                TableName='result',
                Item={
                # 'S' for type String, 'N' for Number.
                'Emp_id' : {'S':str(Emp_id)},
                'SecondCol': {'S':str(SecondCol)},
                'ThirdCol': {'S':str(ThirdCol)},
                'ForthCol': {'S':str(ForthCol)},
                }
            )
        result = 'Put succeeded:'
    except Exception as err:
        result = format(err)
    return {
            'body': result
        }