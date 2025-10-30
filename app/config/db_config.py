import mysql.connector
 
def get_db_connection():
    return mysql.connector.connect(
        host="bp0llqonc2zbeikjoktk-mysql.services.clever-cloud.com",
        user="uwybvvz9lfismmzd",
        password="6M7anx74lTGiOrM3u9Rf",
        database="bp0llqonc2zbeikjoktk"
    )