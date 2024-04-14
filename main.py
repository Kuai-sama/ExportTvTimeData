from ExportTvTime.generic import Generic
from ExportTvTime.tv_time import ExportTvTimeData


def main():
    username, passwd = Generic().get_credentials
    with ExportTvTimeData(username=username, passwd=passwd) as my_tvtime:
        shows = my_tvtime.get_list_followed_shows()

        sorted_shows = my_tvtime.change_columns_order(shows)

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


if __name__ == "__main__":
    main()
    