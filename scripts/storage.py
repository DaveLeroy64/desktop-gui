import sqlite3

def connect(table):
    conn = sqlite3.connect("../pcp.db")
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, Name text, Image text, Story text, Link text, Body text)")
    conn.commit()
    conn.close()

def check(source):
    print("Checking...")
    conn=sqlite3.connect("../pcp.db")
    cur = conn.cursor()

    cur.execute("SELECT * from newsitems WHERE Story=?", (source['story'],))
    result = cur.fetchall()

    if not result:
        print("First story")
        return 'first'

    elif result and (result[0][3] != source['story']):
        print(f"New story from {source['Name']} - archiving and replacing")
        connect('newsarchive')
        insert(source, 'newsarchive')
        print("Archived")
        print("Deleting from current items...")
        cur.execute('DELETE FROM newsitems WHERE Story=?', (result[0][3],))
        conn.commit()
        conn.close()
        print("Deleted")
        return 'new'

    else:
        print(f"DB up to date for {source['Name']}")

    print("Checking complete")


def insert(source, table):
    print("\n===Inserting to DB===")
    status = check(source)

    if status == 'first':
        conn=sqlite3.connect("../pcp.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?, ?)", (source['Name'], source['image'], source['story'], source['storylink'], source['body']))
        conn.commit()
        conn.close()
        print(f"===Inserted First Story from {source['Name']}===\n")
        return "first"

    elif status == 'new':
        conn=sqlite3.connect("../pcp.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?, ?)", (source['Name'], source['image'], source['story'], source['storylink'], source['body']))
        conn.commit()
        conn.close()
        print(f"===Inserted new story from {source['Name']}===\n")
        return "new"

    else:
        print(f"===Entry already exists and is up to date for: {source['Name']}===\n")
        return "existing"

def view(city):    
    conn=sqlite3.connect("property_data.db")
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM {city}")
    rows=cur.fetchall()
    conn.close()
    return rows

def search(city, date_listed="", price="", address="", beds="", bathrooms="", reception_rooms="", website="", acquire_time=""):
    conn=sqlite3.connect("property_data.db")
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM {city} WHERE date_listed=? OR price=? OR address=? OR beds=? OR bathrooms=? OR reception_rooms=? OR website=? OR acquire_time=?", (date_listed, price, address, beds, bathrooms, reception_rooms, website, acquire_time))
    rows = cur.fetchall()
    conn.close()
    return rows

def update(city, date_listed, price, address, beds, bathrooms, reception_rooms, agent_name, agent_tel, website, acquire_time):
    conn=sqlite3.connect("property_data.db")
    cur=conn.cursor()
    cur.execute(f"UPDATE {city} SET date_listed=?, price=?, beds=?, bathrooms=?, reception_rooms=?, agent_name=?, agent_tel=? WHERE address=?, WHERE website=?, WHERE acquire_time=?", (date_listed, price, beds, bathrooms, reception_rooms, agent_name, agent_tel, address, website, acquire_time)) 
    conn.commit()
    conn.close()




    #==========HOW TO CHECK ALL TABLES IN DATABASE==========
    # cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    # print(f"\nENTRY CHECK - Searching tables for: {story}")
    # for tablerow in cur.fetchall():
    #     table = tablerow[0]
    #     cur.execute(f"SELECT * FROM {table} where story=?", (story,))
    #     result = cur.fetchall()
    #     if result:
    #         print(f"Already exists in {table.upper()}")
    #         return True
