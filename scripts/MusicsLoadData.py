from decimal import Decimal
import json
import boto3


def load_movies(musics, dynamodb=None):
    if not dynamodb:
        ##dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb',region_name='us-west-1')

    table = dynamodb.Table('Musics')
    for music in musics:
        id = int(music['id'])
        name = music['name']
        print("Adding movie:", id, name)
        table.put_item(Item=music)


if __name__ == '__main__':
    with open("musicdata.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
    load_movies(music_list)
