import mongoengine

# Connect to the db, initialize the client.
mongoengine.connect(
    'project 0',
    host='mongodb+srv://justin-yum:sTj9slycmNQ0cVDy@fanspot.yuudu.azure.mongodb.net/<dbname>?retryWrites=true&w=majority'
)


# Load the artists data.
with open(file=r'samples/responses/artists_data.jsonc', mode='r') as artists_data_file:
    artists = json.load(fp=artists_data_file)