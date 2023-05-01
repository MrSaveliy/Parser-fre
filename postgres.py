import psycopg2
from config_postgres import host, user, password, db_name


# Connect to the database

def record_db(list_name: list):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
             cursor.execute(
            """CREATE TABLE vyacheslav_kim (
            id_article bigserial PRIMARY KEY,
            url_article varchar(255) NOT NULL,
            date_article date NOT NULL,
            name_article varchar(255) NOT NULL,
            txt_article text NOT NULL,
            web_site varchar(255) NOT NULL,
            asset varchar(255) NOT NULL);"""
              )
        with connection.cursor() as cursor:
            for i in range(len(list_name)):
                cursor.execute(
                """INSERT INTO vyacheslav_kim(
                url_article, date_article, name_article, txt_article, web_site, asset )
                VALUES ( %s, %s, %s, %s, %s, %s)""",
                (list_name[i][0], list_name[i][2], list_name[i][1],
                        list_name[i][3], list_name[i][4], list_name[i][5])
                           )
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()
def update_db(list_name, name_table: str):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            for i in range(len(list_name)):
                cursor.execute(
                f"""INSERT INTO {name_table}(
                url_article, date_article, name_article, txt_article, web_site, asset )
                VALUES ( %s, %s, %s, %s, %s, %s)""",
                (list_name[i][0], list_name[i][2], list_name[i][1],
                        list_name[i][3], list_name[i][4], list_name[i][5])
                           )
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()