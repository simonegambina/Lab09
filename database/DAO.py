from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_edges(distanza_minima):
        conn = DBConnect.get_connection()

        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)

        query = """
                           SELECT 
                               a1.ID AS id1,
                               a1.IATA_CODE AS iata1,
                               a1.AIRPORT AS airport1,
                               a2.ID AS id2,
                               a2.IATA_CODE AS iata2,
                               a2.AIRPORT AS airport2,
                               AVG(f.DISTANCE) AS avg_distance
                           FROM flights f
                           JOIN airports a1 
                               ON a1.ID = LEAST(f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID)
                           JOIN airports a2 
                               ON a2.ID = GREATEST(f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID)
                           GROUP BY 
                               a1.ID, a1.IATA_CODE, a1.AIRPORT,
                               a2.ID, a2.IATA_CODE, a2.AIRPORT
                           HAVING AVG(f.DISTANCE) >= %s
                           ORDER BY avg_distance DESC
                           """

        cursor.execute(query, (distanza_minima,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result
