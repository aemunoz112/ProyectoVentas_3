import mysql.connector
 
def get_db_connection():
    return mysql.connector.connect(
        host="hopper.proxy.rlwy.net",
        user="root",
        password="AFnKSmajlBHrVGWucAoEzQjuusCGrxjE",
        database="railway",  
        port=55790
    )