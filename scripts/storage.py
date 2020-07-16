import sqlite3

def connect(table):
    conn = sqlite3.connect("./pcp.db")
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, Name text, Image text, Story text, Link text, Body text)")
    conn.commit()
    conn.close()
def connect_property(city):
    city = city.replace(" ", "_")
    print("connect property")
    conn = sqlite3.connect("./pcp.db")
    cur = conn.cursor()
    print(city)
    cur.execute(f"CREATE TABLE IF NOT EXISTS {city} (id INTEGER PRIMARY KEY, date_listed text, price integer, address text, beds integer, bathrooms integer, reception_rooms integer, agent_name text, agent_tel text, website text, acquire_time text)")
    
    conn.commit()
    conn.close()

# LATER ON REFACTOR THIS TO USE THE SAME FUNCTIONS FOR PROPERTIES AND NEWSITEMS IF POSSIBLE

#==========NEWSITEMS==========

def check_newsitem(source):
    print("Checking..." + source['story'])
    conn=sqlite3.connect("./pcp.db")
    cur = conn.cursor()

    cur.execute("SELECT * from newsitems WHERE Story=?", (source['story'],))
    result = cur.fetchall()
    # print(result)
    # print(result[0])

    if result:
        print("story DOES exist...let's have a look at it")
        print(result[0][4])
        print("new story")
        print(source['storylink'])
        print(str(result[0][4] != str(source['storylink']))) # True if not the same

        if str(result[0][4]) != str(source['storylink']):
            print(f"{source['Name']} has a new story!") # wait to see if this works before putting in archival

            print(f"New story from {source['Name']} - archiving and replacing")
            connect('newsarchive')
            insert_newsitem(source, 'newsarchive')
            print("Archived")
            print("Deleting from current items...")
            cur.execute('DELETE FROM newsitems WHERE Link=?', (str(result[0][4]),))
            conn.commit()
            conn.close()
            print("Deleted")

            return "new"

        else:
            print(f"{source['Name']} no new story")

        print(f"DB up to date for {source['Name']}")

    else:
        print("First story")
        return 'first'

    # elif result and (result[0][3] != source['story']):
    #     print(f"New story from {source['Name']} - archiving and replacing")
    #     connect('newsarchive')
    #     insert_newsitem(source, 'newsarchive')
    #     print("Archived")
    #     print("Deleting from current items...")
    #     cur.execute('DELETE FROM newsitems WHERE Story=?', (result[0][3],))
    #     conn.commit()
    #     conn.close()
    #     print("Deleted")
    #     return 'new'



    print("Checking complete")


def insert_newsitem(source, table):
    print("\n===Inserting to DB===")
    status = check_newsitem(source)

    if status == 'first':
        conn=sqlite3.connect("./pcp.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?, ?)", (source['Name'], source['image'], source['story'], source['storylink'], source['body']))
        conn.commit()
        conn.close()
        print(f"===Inserted First Story from {source['Name']}===\n")
        return "first"

    elif status == 'new':
        conn=sqlite3.connect("./pcp.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?, ?)", (source['Name'], source['image'], source['story'], source['storylink'], source['body']))
        conn.commit()
        conn.close()
        print(f"===Inserted new story from {source['Name']}===\n")
        return "new"

    elif status == "test":
        print("test status")
        return "test"

    else:
        print(f"===Entry already exists and is up to date for: {source['Name']}===\n")
        return "existing"


#==========PROPERTIES==========

def check_property(city, address):
    conn=sqlite3.connect("./pcp.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

    print(f"\nENTRY CHECK - Searching tables for: {address}")
    for tablerow in cur.fetchall():
        table = tablerow[0]
        if table != 'newsitems':
            cur.execute(f"SELECT * FROM {table} WHERE address=?", (address,))
            result = cur.fetchall()
            if result:
                print(f"Already exists in {table.upper()}")
                return True

    if not result:
        print("Does not exist")
        return False
    else:
        return True


def insert_property(city, date_listed, price, address, beds, bathrooms, reception_rooms, agent_name, agent_tel, website, acquire_time):
    city = city.replace(" ", "_")
    status = check_property(city, address)
    if status == False:
        conn=sqlite3.connect("./pcp.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {city} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date_listed, price, address, beds, bathrooms, reception_rooms, agent_name, agent_tel, website, acquire_time))
        conn.commit()
        conn.close()
        print("saved")
        return "new"
    else:
        # print(f"Entry already exists for: {address}")
        print("not saved")
        return "existing"

def view_properties(city):    
    conn=sqlite3.connect("./pcp.db")
    cur=conn.cursor()
    if " " in str(city):
        city = city.replace(" ", "_")
    try:
        cur.execute(f"SELECT * FROM {city}")
        properties=cur.fetchall()
        conn.close()
        print("found!!")
        return properties
    except:
        print("not found...")
        return "not found"

def search_property(city, date_listed="", price="", address="", beds="", bathrooms="", reception_rooms="", website="", acquire_time=""):
    conn=sqlite3.connect("./pcp.db")
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM {city} WHERE date_listed=? OR price=? OR address=? OR beds=? OR bathrooms=? OR reception_rooms=? OR website=? OR acquire_time=?", (date_listed, price, address, beds, bathrooms, reception_rooms, website, acquire_time))
    prop = cur.fetchall()
    conn.close()
    return prop

def update_property(city, date_listed, price, address, beds, bathrooms, reception_rooms, agent_name, agent_tel, website, acquire_time):
    conn=sqlite3.connect("./pcp.db")
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
