#####################################
#####################################
# How many random data to generate?
how_many_users = 4
how_many_books = 50
how_many_logs = how_many_books * 4
#####################################
#####################################

from util.db import db_config
import pytz
import psycopg2
from faker import Faker
import time
from datetime import datetime



fake = Faker()
params = db_config()
conn = psycopg2.connect(**params)
cur = conn.cursor()


# Find all table names
cur.execute(
    "SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
tables = cur.fetchall()

# Truncate all tables
for table in tables:
    cur.execute(f"TRUNCATE TABLE {table[0]} CASCADE;")
    conn.commit()


# Restart IDs and add default users
cur.execute("""
    ALTER SEQUENCE users_user_id_seq RESTART WITH 1;
    ALTER SEQUENCE books_book_id_seq RESTART WITH 100;
    ALTER SEQUENCE logs_log_id_seq RESTART WITH 1;

    INSERT INTO users (user_name, user_password) VALUES('Tabali', '123');
    INSERT INTO users (user_name, user_password) VALUES('Kursad', '123');
    INSERT INTO users (user_name, user_password) VALUES('Ramy', '123');
    INSERT INTO users (user_name, user_password) VALUES('Ziad', '123');

""")
conn.commit()

# # Close the cursor and the connection
# cur.close()
# conn.close()
print("all data from all tables deleted!")


time.sleep(2)


print('Generating & inserting fake data into the 3 tables...')

# insert data into users table
for i in range(how_many_users):
    user_name = fake.first_name()
    user_password = fake.password()
    query = f"INSERT INTO public.users (user_name, user_password) VALUES ('{user_name}', '{user_password}')"
    cur.execute(query)

# insert data into books table
for i in range(how_many_books):

    book_name = fake.sentence(nb_words=4, variable_nb_words=True)
    # remove the dot and capitalize each word
    book_name = ' '.join(word.capitalize() for word in book_name[:-1].split())

    book_author = fake.name()

    book_number_of_pages = fake.random_int(min=50, max=1000)

    genres = ['Romance', 'Mystery', 'Thriller', 'Fiction',
              'Fantasy', 'Horror', 'History']
    book_genre = fake.random_element(elements=genres)
    book_count = fake.random_int(min=1, max=10)
    query = f"INSERT INTO public.books (book_name, book_author, book_number_of_pages, book_genre, book_count) VALUES ('{book_name}', '{book_author}', {book_number_of_pages}, '{book_genre}', {book_count})"
    cur.execute(query)

# insert data into logs table
# this is because we have forigen key restrains!
cur.execute("SELECT user_id FROM public.users")
user_ids = [r[0] for r in cur.fetchall()]
cur.execute("SELECT book_id FROM public.books")
book_ids = [r[0] for r in cur.fetchall()]


for i in range(how_many_logs):
    # choose from the fetched user_id list above!
    user_id = fake.random_element(elements=user_ids)
    book_id = fake.random_element(elements=book_ids)  # same for book_id list

    borrowed = fake.boolean()
    read = fake.boolean()
    favorited = fake.boolean()
    added = fake.boolean()

    # check if this combination already exists for this book_id
    cur.execute(
        f"SELECT * FROM public.logs WHERE book_id={book_id} AND borrowed={borrowed} AND read={read} AND favorited={favorited} AND added={added}")
    result = cur.fetchone()
    if result:
        print(
            f"data for book_id={book_id} with the combination borrowed={borrowed}, read={read}, favorited={favorited}, added={added} already exists")
        continue

    if sum([borrowed, read, favorited, added]) != 1:
        # if more than one value is True, set all to False
        borrowed, read, favorited, added = False, False, False, False
        # choose one value to set as True
        choice = fake.random_element(
            elements=['borrowed', 'read', 'favorited', 'added'])
        if choice == 'borrowed':
            borrowed = True
        elif choice == 'read':
            read = True
        elif choice == 'favorited':
            favorited = True
        elif choice == 'added':
            added = True

    start_date = datetime(2010, 1, 1, tzinfo=pytz.UTC)
    end_date = datetime.now(tz=pytz.UTC)
    timestamp = fake.date_time_between(
        start_date=start_date, end_date=end_date).strftime("%Y-%m-%d %H:%M:%S%z")

    query = f"INSERT INTO public.logs (user_id, book_id, borrowed, read, favorited, added, timestamp) VALUES ({user_id}, {book_id}, {borrowed}, {read}, {favorited}, {added}, '{timestamp}')"
    cur.execute(query)


conn.commit()

cur.close()
conn.close()
print ('ALL DONE!')