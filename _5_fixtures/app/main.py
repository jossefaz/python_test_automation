def retrieve_users(db_connection) :
    if db_connection.connected :
        return "All users"
    return "Not Connected to db"