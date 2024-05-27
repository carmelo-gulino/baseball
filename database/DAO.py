from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_years():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.`year` from teams t where t.`year` >= 1980 order by t.`year` desc"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_teams_of_year(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select * from teams t where t.`year` = %s"""
        cursor.execute(query, (year,))
        result = []
        for row in cursor:
            result.append(Team(**row))
        cursor.close()
        conn.close()
        return result

