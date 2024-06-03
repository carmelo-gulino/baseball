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

    @staticmethod
    def get_salary_of_teams(year, teams_map):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select t.teamCode , sum(s.salary) tot_salary , t.ID 
                    from salaries s , teams t , appearances a 
                    where s.`year` = t.`year` and t.`year` = a.`year` and a.`year` = %s
                    and a.teamID  = t.ID and a.playerID = a.playerID 
                    group by t.teamCode """
        cursor.execute(query, (year,))
        result = {}
        for row in cursor:
            result[teams_map[row["ID"]]] = row["tot_salary"]    # tupla (team, somma salari)
        cursor.close()
        conn.close()
        return result
