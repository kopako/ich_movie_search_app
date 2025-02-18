import logging
from sql_queries import FilmQueries, GenreQueries
from sql_connection import SqlConnection


class SqlService:
    @staticmethod
    def movies_by_genre_and_year(genre: str, year: int):
        logging.info(FilmQueries.BY_GENRE_AND_RELEASE_YEAR, (genre, year))
        SqlConnection().execute(FilmQueries.BY_GENRE_AND_RELEASE_YEAR, (genre, year))
        records = SqlConnection().cursor.fetchall()
        [print(row.get('title'), row.get('rating')) for row in records]
        return records

    @staticmethod
    def genre_names():
        SqlConnection().execute(GenreQueries.GENRES)
        return SqlConnection().cursor.fetchall()

    @staticmethod
    def movies_by_keyword(keyword: str):
        wildcard_keyword = f"%{keyword}%"
        num_placeholders = FilmQueries.BY_KEYWORD.count('%s')
        placeholders = (wildcard_keyword,) * num_placeholders
        SqlConnection().execute(FilmQueries.BY_KEYWORD,placeholders)
        records = SqlConnection().cursor.fetchall()
        [print(row.get('title'), row.get('rating')) for row in records]
        return records