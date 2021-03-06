# HandsOn DynamoDB Local

Command line script and other.


## Requirements

- MacOS
- AWS CLI
- Java 11 or major
- Python 3

### Checking Requirements

```
sw_vers
aws --version
java --version
python3 --version
```

## Enviroment Result

### OS

> ProductName:	macOS
> 
> ProductVersion:	11.6
> 
> BuildVersion:	20G165


#### AWS

> aws-cli/2.2.46 Python/3.8.8 Darwin/20.6.0 exe/x86_64 prompt/off


#### Java

> java 11.0.11 2021-04-20 LTS
>
> Java(TM) SE Runtime Environment 18.9 (build 11.0.11+9-LTS-194)
>
> Java HotSpot(TM) 64-Bit Server VM 18.9 (build 11.0.11+9-LTS-194, mixed mode)

#### Python

> Python 3.8.9

## Step-by-step

### 1. Download Package DynamoDB

```
mkdir dynamodb
cd dynamodb
wget https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz
```

### 2. Extract Package DynamoDB

```
tar -xvzf dynamodb_local_latest.tar.gz
```

### 3. Run DynamoDB

```
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```

### 4. Check Tables

```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

### 5. Create Script Python - CREATE TABLE

#### 5.1. Create File -- CREATE TABLE

```
code MoviesCreateTable.py
```

#### 5.2. Write Code - CREATE TABLE

```python

import boto3

def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    movie_table = create_movie_table()
    print("Table status:", movie_table.table_status)
```

#### 5.3. Test Script - CREATE TABLE

```
sudo pip3 install boto3
python3 MoviesCreateTable.py
```

### 6. Create Script Python - LOAD DATA 

#### 6.1. Create File -- LOAD DATA

```
code MoviesLoadData.py
```

#### 6.1. Write Code -- LOAD DATA

```python

from decimal import Decimal
import json
import boto3

def load_movies(movies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print("Adding movie:", year, title)
        table.put_item(Item=movie)


if __name__ == '__main__':
    with open("moviedata.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    load_movies(movie_list)
```


### 7. Example Using Table 

#### 7.1. Check Table Detail

```
aws dynamodb describe-table --table-name Movies --endpoint-url http://localhost:8000
```

#### 7.2. Check Table: ItemCount

```
aws dynamodb describe-table --table-name Movies --endpoint-url http://localhost:8000 | grep ItemCount
```

#### 7.9. Write Shell Script - Delete All Items

```shell
#!/bin/bash

TABLE_NAME=TableName
KEY=id

aws dynamodb scan --table-name $TABLE_NAME --attributes-to-get "$KEY" \
  --query "Items[].$KEY.S" --output text | \
  tr "\t" "\n" | \
  xargs -t -I keyvalue aws dynamodb delete-item --table-name $TABLE_NAME \
  --key "{\"$KEY\": {\"S\": \"keyvalue\"}}"
```

## Files

- [moviedata.zip](https://github.com/andersonbraz/hands-on-dynamodb/raw/main/moviedata.zip)

- [musicdata.zip](https://github.com/andersonbraz/hands-on-dynamodb/raw/main/musicdata.zip)

## References

[Developer Guide - DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)

[Developer Guide - Getting Started - Python](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html)

[Boto3 Project - The AWS SDK for Python](https://pypi.org/project/boto3/)

[Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
