import mysql.connector
 
def get_db_connection():
    return mysql.connector.connect(
        host="hopper.proxy.rlwy.net",
        user="root",
        password="AFnKSmajlBHrVGWucAoEzQjuusCGrxjE",
        database="railway",  # <- reemplaza con tu DB en Railway
        port=55790
    )