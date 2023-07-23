import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="kw5",
    user="myuser",
    password="mypass"
)