def find_by_telegram_id(db, user_query, user_id):
    r = db.search(user_query.telegram_id == user_id)

    return r[0] if r else None
