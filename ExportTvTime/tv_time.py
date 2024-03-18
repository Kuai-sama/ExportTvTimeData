from itertools import product
from json import dump
from os import getenv

import pandas as pd
from stdiomask import getpass
from tvtimewrapper import TVTimeWrapper

from conf import settings


class ExportTvTimeData:
    """Class for exporting data from the TVTime website.

    This class connects to the TVTimeWrapper module, retrieves data on followed TV shows,
    and exports it to a JSON file and a CSV file. It also provides methods to change the order
    of the columns and delete specific columns from the data.

    Attributes:
        file_name_json (str): The name and path of the JSON file to be created.
        file_name_csv (str): The name and path of the CSV file to be created.
        tvtime_wrapper (TVTimeWrapper): An instance of the TVTimeWrapper class used to connect to TVTime.
        
    Methods:
        _get_credentials: Retrieves TVTime credentials.
        connect_to_tvtime: Connects to the TVTime website.
        get_list_followed_shows: Retrieves a list of followed TV shows from TVTime.
        change_columns_order: Changes the order of the columns in the data.
        delete_columns: Deletes specific columns from the data.
        create_json_file: Creates a JSON file with the provided data.
        create_csv_file: Creates a CSV file with the provided data."""

    def __init__(self):
        self.file_name_json = settings.OUTPUT_FOLDER.joinpath("data.json")
        self.file_name_csv = settings.OUTPUT_FOLDER.joinpath("dataTVTime.csv")
        self.tvtime_wrapper = None
        
    def __enter__(self):
        self.connect_to_tvtime()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception: {exc_type} - {exc_value}")
        return True

    def _get_credentials(self) -> tuple:
        """Retrieves TVTime credentials.

        Returns:
            tuple: A tuple containing the username and password."""

        if not getenv("TVTIME_CREDENTIALS"):
            # User input (username and password)
            user_name = input("Enter your username: ")
            password = getpass(prompt="Enter your password: ", mask="*")
        else:
            # Get the environment variable
            user_name, password = getenv("TVTIME_CREDENTIALS").split(";")
        return user_name, password

    def connect_to_tvtime(self):
        """Connects to the TVTime website."""
        
        user_name, password = self._get_credentials()

        self.tvtime_wrapper = TVTimeWrapper(user_name, password)
        print("Connection to TVTimeWrapper module")

    def get_list_followed_shows(self) -> list[dict]:
        """Retrieves a list of followed TV shows from TVTime.

        Returns:
            list[dictt]: A list of followed informations TV shows."""

        return self.tvtime_wrapper.show.followed()

    def change_columns_order(self, json_data: list) -> dict:
        """Changes the order of the columns in the data.

        Args:
            json_data (list): The data to be modified.

        Returns:
            dict: The modified data with columns in the desired order."""

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

    def delete_columns(self, json_data: list, columns: list, keep_one_image: bool = False) -> list:
        """Deletes specific columns from the data.

        Args:
            json_data (list): The data to be modified.
            columns (list): The columns to be deleted.
            keep_one_image (bool, optional): Whether to keep only one image. Defaults to False.

        Returns:
            list: The modified data with specified columns deleted."""

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
        """
        Creates a JSON file with the provided data.

        Args:
            json_data (list): The data to be exported."""

        with open(self.file_name_json, "w", encoding="utf_8") as my_file:
            dump(json_data, my_file)

        print("Created JSON file")

    def create_csv_file(self, json_data: list):
        """Creates a CSV file with the provided data.

        Args:
            json_data (list): The data to be exported."""

        df = pd.json_normalize(json_data)
        df.index = df.index + 1
        df.to_csv(self.file_name_csv, index=True, index_label="N°")
        print("Created CSV file")
