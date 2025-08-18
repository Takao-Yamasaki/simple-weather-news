import json
import boto3
import random

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):

    if 'cityId' in event:
        city_id = int(event['cityId'])
    else:
        city_id = random.choice([1, 13, 23, 27, 40])
    
    city_name = findCityName(city_id)
    if city_name == 'ERROR':
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid cityId')
        }

    random_number = random.randrange(11)

    rainfall_probability = random_number * 10

    if random_number <= 2:
        weather_id = 2
        weather_name = "晴れ"
    elif random_number <= 7:
        weather_id = 4
        weather_name = "くもり"
    else:
        weather_id = 12
        weather_name = "雨"
    
    response = dynamodb_client.put_item(
        TableName='simple-weather-news-table',
        Item={
            "CityId": {
                "N": str(city_id)
            },
            "CityName": {
                "S": city_name
            },
            "WeaterId": {
                "N": str(weather_id)
            },
            "WeaterName": {
                "S": weather_name
            },
            "RainfallProbability": {
                "N": str(rainfall_probability)
            }
        }
    )

    print('Update: ' + city_name + ' to ' + weather_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Update: ' + str(city_id))
    }

def findCityName(city_id):
    city_map = {
        1: "札幌",
        13: "東京",
        23: "名古屋",
        27: "大阪",
        40: "博多"
    }
    return city_map.get(city_id, "ERROR")
