import logging

from mongo_connection import MongoService
from sql_service import SqlService


class SearchController:
    def __init__(self):
        self.sql_service = SqlService()
        self.exit_flag = False

    def exit(self):
        self.exit_flag = True

    def search_by_keyword(self):
        print("Search by keyword:")
        keyword = input('Enter keyword: ')
        self.sql_service.movies_by_keyword(keyword)

    def search_by_genre_and_year(self):
        print("Search by genre and year:")
        genre_names = [row.get('name') for row in self.sql_service.genre_names()]
        for index, genre_name in enumerate(genre_names):
            print(f"{index}. {genre_name}")
        genre_choice = input("Select genre: ")
        if genre_choice.isnumeric() and len(genre_names) > int(genre_choice) > 0:
            genre = genre_names[int(genre_choice)]
        elif genre_choice in genre_names:
            genre = genre_choice
        else:
            logging.warning("Invalid genre")
            self.search_by_genre_and_year()
        year = int(input("Select year: "))

        return self.sql_service.movies_by_genre_and_year(genre=genre, year=year)

    def top_searches(self, limit: int=3):
        print("Top searches:")
        MongoService().list_collections()
