from db import Database


def test_db():
    db = Database(path_to_db='test.db')

    db.create_table_users()

    db.add_user(1, "TEst USer", 123123, "Tashkent")
    db.add_user(2, "TEst USer1", 12312, "Tashkent")
    db.add_user(3, "TEst USer2", 12313, "Tashkent")
    db.add_user(4, "TEst USer3", 1123, "Tashkent")
    db.add_user(5, "TEst USer4", 123123123, "Tashkent")
    db.add_user(6, "TEst USer5", 123112321323, "Tashkent")
    db.add_user(7, "TEst USer6", 123121233, "Tashkent")

    a = db.select_user(1)
    print(a)
    b = db.select_user(2)
    print(b)

    print(db.count_users())


test_db()
