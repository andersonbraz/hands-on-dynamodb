import boto3

def create_movie_table(dynamodb=None):
    if not dynamodb:
        ##dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb',region_name='us-west-1')

    table = dynamodb.create_table(
        TableName='Musics',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'name',
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