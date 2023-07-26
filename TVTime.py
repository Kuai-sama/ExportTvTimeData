import os
from itertools import product
from json import dump
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from stdiomask import getpass
from tvtimewrapper import TVTimeWrapper


class ExportTvTimeData:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.file_name_json = Path(self.dir_path, "data.json")
        self.file_name_csv = Path(self.dir_path, "dataTVTime.csv")
        self.tvtime_wrapper = None
        load_dotenv(Path(self.dir_path, "env", "tvtime.env"))

    def get_credentials(self) -> tuple:
        if not os.getenv("TVTIME_CREDENTIALS"):
            # User input (username and password)
            user_name = input("Enter your username: ")
            password = getpass(prompt="Enter your password: ", mask="*")
        else:
            # Get the environment variable
            credentials = os.getenv("TVTIME_CREDENTIALS").split(";")
            user_name = credentials[0]
            password = credentials[1]
        return user_name, password

    def connect_to_tvtime(self, user_name, password):
        self.tvtime_wrapper = TVTimeWrapper(user_name, password)
        print("Connection to TVTimeWrapper module")

    def get_list_followed_shows(self) -> list:
        return self.tvtime_wrapper.show.followed()

    def change_columns_order(self, json_data: list):
        # Change the order of the columns
        columns = [
            "id",
            "name",
            "last_seen",
            "last_aired",
            "next_aired",
            "up_to_date",
            "followed",
            "archived",
            "favorite",
            "diffusion",
            "folder",
            "status",
            "notification_type",
            "is_web_serie",
            "hashtag",
            "number_of_seasons",
            "aired_episodes",
            "seen_episodes",
            "runtime",
            "all_images",
        ]
        # new dataframe with the columns in the order that we want
        df = pd.DataFrame(columns=columns)

        # Convert dataframe to dictionary
        data = list(json_data)
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

        return df.to_dict(orient="records")

    def delete_columns(self, json_data: list, columns: list, keep_one_image: bool = False):
        for item, column in product(json_data, columns):
            if keep_one_image and column == "all_images":
                # Keep only the first image (posters), delete the rest
                del item[column]["banner"]
                del item[column]["fanart"]
                item[column]["poster"] = item[column]["poster"]["0"]
            else:
                del item[column]
        return json_data

    def create_json_file(self, json_data: list):
        with open(self.file_name_json, "w") as my_file:
            dump(json_data, my_file)
        print("Created JSON file")

    def create_csv_file(self, json_data: list):
        df = pd.json_normalize(json_data)
        df.index = df.index + 1
        df.to_csv(self.file_name_csv, index=True, index_label="N°")
        print("Created CSV file")
