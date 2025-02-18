class FilmQueries:
    BY_GENRE_AND_RELEASE_YEAR = """
                SELECT
                    *
                FROM
                    film f
                JOIN film_category fc
                    ON f.film_id = fc.film_id
                JOIN category c
                    ON fc.category_id = c.category_id
                    AND c.name = %s
                WHERE
                    f.release_year = %s
                ORDER BY f.rating
            """
    BY_KEYWORD = """
                    SELECT * FROM film f
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
                    ORDER BY f.rating
                """
class GenreQueries:
    GENRES = "SELECT DISTINCT name FROM category"