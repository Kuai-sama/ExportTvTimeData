# coding: utf-8
from tvtimewrapper import TVTimeWrapper
import pandas
import json
import os

"""
    Author : Kuaï
    Github : Kuai-sama
    Created date project : 18/02/2022
    Last update : 03/04/2022
    Current version : v1.1
    Python interpreter : 3.8.7 64 bit
    Goals of the Project : Exporting accurately data from TvTime to cvs file
"""

dir_path = os.path.dirname(os.path.realpath(__file__))  # Current directory project

file_name_json = dir_path + os.sep + r"data.json"
file_name_csv = dir_path + os.sep + r"dataTVTime.csv"

# Connection
tvtime = TVTimeWrapper(r"YourUserName", r"YourPassword")
print("Connection to TVTimeWrapper module")

# Get all the shows that the user have followed
ShowFollowed = tvtime.show.followed()

list = ["1", "1,3", "1,5", "2", "2,6", "3", "4"]
# Keep only one image for all shows
for element in ShowFollowed:
    del element["all_images"]["banner"]
    del element["all_images"]["fanart"]
    for i in list:
        del element["all_images"]["poster"][i]

print("Get selected data of all the shows that you have followed")

# Send the modified data in to a real json file
with open(file_name_json, "w") as my_file:
    json.dump(ShowFollowed, my_file)

# Convert json to csv data
pandas.read_json(file_name_json).to_csv(file_name_csv)

# Read the file
data = pandas.read_csv(file_name_csv)

# List of all columns to be deleted
columns_To_Be_Deleted = [
    "last_seen",
    "last_aired",
    "next_aired",
    "followed",
    "archived",
    "diffusion",
    "folder",
    "notification_type",
    "is_web_serie",
    "hashtag",
    "number_of_seasons",
    "favorite",
]

# Drop useless columns from the CSV data
for column in columns_To_Be_Deleted:
    data.pop(column)

# Remove shows already seen
index = data[data["up_to_date"] == True].index
data.drop(index, inplace=True)

"""
    By default, when converting json data to csv, it creates a column named "Unnamed: 0", which refers to the iteration number of your show. so we have rename the column to "N°"
"""
data.rename(columns={"Unnamed: 0": "N°"}, inplace=True)
data.columns

# Remove {'poster': {'0':  in all_images column
for incremented_value, (key, value) in enumerate(data.iterrows(), start=1):
    NewString = f'{value["all_images"]}'.lstrip("{'poster': {'0': '")
    data.loc[key, "all_images"] = NewString[:-3]
    data.loc[key, "N°"] = incremented_value

print(data)  # display

# Saving file
data.to_csv(file_name_csv, index=None)
print("Saved file")
