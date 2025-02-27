class FilmQueries:
    BY_GENRE_AND_RELEASE_YEAR = """
                SELECT DISTINCT
                        f.film_id,
                        f.title,
                        f.description
                FROM
                    film f
                JOIN film_category fc
                    ON f.film_id = fc.film_id
                JOIN category c
                    ON fc.category_id = c.category_id
                    AND c.name = %s
                WHERE
                    f.release_year = %s
                ORDER BY f.film_id
            """
    BY_KEYWORD = """
                    SELECT DISTINCT
                        f.film_id,
                        f.title,
                        f.description
                    FROM film f
                    JOIN film_category fc ON f.film_id = fc.film_id
                    JOIN category c ON fc.category_id = c.category_id
                    JOIN film_actor fa ON f.film_id = fa.film_id
                    JOIN actor a ON fa.actor_id = a.actor_id
                    WHERE
                        f.title LIKE %s
                        OR f.description LIKE %s
                        OR a.first_name LIKE %s
                        OR a.last_name LIKE %s
                        OR c.name LIKE %s
                    ORDER BY f.film_id
                """
class GenreQueries:
    GENRES = "SELECT DISTINCT name FROM category"

class MongoQueries:
    TOP_PIPELINES = [
      { "$addFields": { "params": { "$setUnion": ["$params", []] } } },
      { "$unwind": { "path": "$params", "preserveNullAndEmptyArrays": False } },
      { "$group": { "_id": "$params", "count": { "$sum": 1 } } },
      { "$sort": { "count": -1 } },
      { "$limit": 3 },
      { "$group": { "_id": None, "top_searches": { "$push": "$_id" } } }
    ]
