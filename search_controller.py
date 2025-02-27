import logging

from mongo_service import MongoService
from sql_service import SqlService


class SearchController:
    def __init__(self):
        self.exit_flag = False

    def exit(self):
        self.exit_flag = True

    @staticmethod
    def search_by_keyword():
        print("Search by keyword:")
        keyword = input('Enter keyword: ')
        print(*SqlService().movies_by_keyword(keyword), sep='\n')

    @staticmethod
    def search_by_genre_and_year():
        genre = ''
        print("Search by genre and year:")
        genre_names = [row.get('name') for row in SqlService().genre_names()]
        for index, genre_name in enumerate(genre_names):
            print(f"{index}. {genre_name}")
        genre_choice = input("Select genre: ")
        if genre_choice.isnumeric() and len(genre_names) > int(genre_choice) > 0:
            genre = genre_names[int(genre_choice)]
        elif genre_choice in genre_names:
            genre = genre_choice
        else:
            logging.warning("Invalid genre")
            SearchController.search_by_genre_and_year()
        year = int(input("Select year: "))
        print(*SqlService().movies_by_genre_and_year(genre=genre, year=year), sep='\n')

    @staticmethod
    def top_searches():
        print("Top searches:")
        for doc in MongoService().top_three():
            print(*doc['top_searches'], sep='\n')
