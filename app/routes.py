from flask import request, jsonify
from app import app, executor
import asyncio
import aiohttp
from datetime import datetime
import time
import json
from bson import json_util

# Function to collect weather data for a specific city by city_id using aiohttp
async def get_weather_by_city_id(session, city_id):
    base_url = app.config['OPENWEATHER_BASE_URL']
    params = {
        'id': city_id,
        'appid': app.config['API_KEY'],
        'units': 'metric'
    }
    async with session.get(base_url, params=params) as response:
        return await response.json()

def initialize_city_records(user_id):
    city_ids = [3439525, 3439781, 3440645, 3442098, 3442778, 3443341, 3442233, 3440781,
                3441572, 3441575, 3443207, 3442546, 3441287, 3441242, 3441686, 3440639,
                3441354, 3442057, 3442585, 3442727, 3439705, 3441890, 3443411, 3440054,
                3441684, 3440711, 3440714, 3440696, 3441894, 3443173, 3441702, 3442007,
                3441665, 3440963, 3443413, 3440033, 3440034, 3440571, 3443025, 3441243,
                3440789, 3442568, 3443737, 3440771, 3440777, 3442597, 3442587, 3439749,
                3441358, 3442980, 3442750, 3443352, 3442051, 3441442, 3442398, 3442163,
                3443533, 3440942, 3442720, 3441273, 3442071, 3442105, 3442683, 3443030,
                3441011, 3440925, 3440021, 3441292, 3480823, 3440379, 3442106, 3439696,
                3440063, 3442231, 3442926, 3442050, 3440698, 3480819, 3442450, 3442584,
                3443632, 3441122, 3441475, 3440791, 3480818, 3439780, 3443861, 3440780,
                3442805, 7838849, 3440581, 3440830, 3443756, 3443758, 3443013, 3439590,
                3439598, 3439619, 3439622, 3439652, 3439659, 3439661, 3439725, 3439748,
                3439787, 3439831, 3439838, 3439902, 3440055, 3440076, 3440394, 3440400,
                3440541, 3440554, 3440577, 3440580, 3440596, 3440653, 3440654, 3440684,
                3440705, 3440747, 3440762, 3440879, 3440939, 3440985, 3441074, 3441114,
                3441377, 3441476, 3441481, 3441483, 3441577, 3441659, 3441674, 3441803,
                3441954, 3441988, 3442058, 3442138, 3442206, 3442221, 3442236, 3442238,
                3442299, 3442716, 3442766, 3442803, 3442939, 3443061, 3443183, 3443256,
                3443280, 3443289, 3443342, 3443356, 3443588, 3443631, 3443644, 3443697,
                3443909, 3443928, 3443952, 3480812, 3480820, 3480822, 3480825
            ]


    for city_id in city_ids:
        # Check if the city is already recorded for this user_id
        existing_record = app.cities_collection.find_one({"user_id": user_id, "city_id": city_id})
        
        if not existing_record:
            # Insert the record with collected = false
            app.cities_collection.insert_one({
                "user_id": user_id,
                "city_id": city_id,
                "collected": False
            })
            print(f"city: {city_id} inserted.")

async def collect_and_store_weather_data(user_id):
    # Get all uncollected records for this user_id
    uncollected_cities = list(app.cities_collection.find({"user_id": user_id, "collected": False}))

    city_count = 0
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
         for city in uncollected_cities:
            city_id = city["city_id"]
            # Make the HTTP request and get the weather data
            weather_data = await get_weather_by_city_id(session, city_id)
            weather_data = {
                            "temperature": weather_data["main"]["temp"],
                            "humidity": weather_data["main"]["humidity"]
                        }

            if weather_data:
                # Add the date and mark as collected
                weather_data["datetime"] = datetime.now()
                weather_data["collected"] = True

                # Update the record with weather data and mark collected as true
                app.cities_collection.update_one(
                    {"user_id": user_id, "city_id": city_id},
                    {"$set": weather_data}
                )
                print(f"weather data for city {city_id} of user {user_id} inserted.")

            city_count += 1

            # Check if the limit of 60 cities has been reached
            if city_count >= 60:
                print('city limit per minute reached. waiting for timeout.')
                elapsed_time = time.time() - start_time
                if elapsed_time < 60:
                    # Wait until 1 minute is complete
                    await asyncio.sleep(60 - elapsed_time)
                # Reset the counter and time
                city_count = 0
                start_time = time.time()

            # 1-second interval to space out the requests
            await asyncio.sleep(1)

# POST route to store weather data
@app.route('/weather', methods=['POST'])
async def store_weather_data():
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    # Initialize the city records
    initialize_city_records(user_id)
    
    print('cities registered.')

    # Start asynchronous data collection
    executor.submit(asyncio.run, collect_and_store_weather_data(user_id))
    
    return jsonify({"message": "Data collection started"}), 202

# GET route to get progress
@app.route('/weather/<user_id>', methods=['GET'])
def get_progress(user_id):
    # Total cities associated with this user_id
    total_cities = app.cities_collection.count_documents({"user_id": user_id})
    
    # Collected cities associated with this user_id
    collected_cities = app.cities_collection.count_documents({"user_id": user_id, "collected": True})

    # Progress calculation
    progress = (collected_cities / total_cities) * 100 if total_cities > 0 else 0

    return jsonify({"user_id": user_id, "progress": progress, "collected": collected_cities})

# GET route to get all user records
@app.route('/city/<user_id>', methods=['GET'])
def get_cities(user_id):

    projection = {
        '_id': 0,           
        'city_id': 1,       
            'datetime': {
                '$dateToString': {
                    'format': '%Y-%m-%d %H:%M:%S',  
                    'date': '$datetime',
                    'timezone': 'UTC'   
                }
            },
        'humidity': 1,      # Include the humidity field
        'temperature': 1,   # Include the temperature field
        'user_id': 1        # Include the user_id field
    }
    cities = app.cities_collection.find({"user_id": user_id}, projection)

    cities = list(cities)

    if(not cities):
        return jsonify({"message": f"No city registered with the user_id {user_id}"}), 202
    else:
        results = json_util.dumps(cities)

    return jsonify(json.loads(results))