from tv_time import ExportTvTimeData


if __name__ == "__main__":
    my_tvtime = ExportTvTimeData()
    username, password = my_tvtime.get_credentials()
    my_tvtime.connect_to_tvtime(username, password)
    shows = my_tvtime.get_list_followed_shows()

    sorted_shows = my_tvtime.change_columns_order(shows)
    print(type(sorted_shows))

    keep_columns = my_tvtime.delete_columns(
        sorted_shows,
        [
            "followed",
            "last_seen",
            "next_aired",
            "diffusion",
            "folder",
            "notification_type",
            "is_web_serie",
            "hashtag",
            "number_of_seasons",
            "favorite",
            "last_aired",
            "all_images",
        ],
        True
    )

    my_tvtime.create_csv_file(keep_columns)
else:
    print("This file is not meant to be imported")