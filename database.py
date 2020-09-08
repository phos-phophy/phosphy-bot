import sqlite3


class Database:

    def __init__(self, database):
        """connect to database"""

        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_chat_info(self, chat_id, filter_state=1, nerd_id=0, nerd_name='', nerd_date=0):
        """add into 'chat_info' table information about chat"""

        with self.connection:
            return self.cursor.execute("INSERT INTO 'chat_info' ('id', 'filter_state', "
                                       "'nerd_id', 'nerd_name', 'nerd_date') VALUES (?, ?, ?, ?, ?)",
                                       (chat_id, filter_state, nerd_id, nerd_name, nerd_date,))

    def update_filter_state(self, chat_id, filter_state=1):
        """update chat`s filter_state in the 'chat_info' table"""

        with self.connection:
            return self.cursor.execute("UPDATE 'chat_info' SET filter_state = ? "
                                       "WHERE id = ?", (filter_state, chat_id,))

    def update_nerd_info(self, chat_id, nerd_id=0, nerd_name='', nerd_date=0):
        """update chat`s information about nerd in the 'chat_info' table"""

        with self.connection:
            return self.cursor.execute("UPDATE 'chat_info' SET nerd_id = ?, nerd_name = ?, "
                                       "nerd_date = ? WHERE id = ?",
                                       (nerd_id, nerd_name, nerd_date, chat_id,))

    def get_chat_info(self, chat_id):
        """return information about chat saved in the 'chat_info' table"""

        with self.connection:
            return self.cursor.execute("SELECT * FROM 'chat_info' WHERE id = ?", (chat_id,)).fetchall()

    def delete_chat_info(self, chat_id):
        """delete information about chat in the 'chat_info' table"""
        with self.connection:
            return self.cursor.execute("DELETE FROM 'chat_info' WHERE id = ?", (chat_id,))

    def create_chat_members_table(self, chat_id):
        """create 'chat_members?' table with information about chat members (id, count of warnings)"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("CREATE TABLE " + chat_name + " ('user_id' INTEGER NOT NULL UNIQUE, "
                                       "'warning_count' INTEGER NOT NULL DEFAULT 0, "
                                       "'nerd_count' INTEGER NOT NULL DEFAULT 0, "
                                       "PRIMARY KEY('user_id'))")

    def add_chat_member(self, chat_id, user_id, warning_count=0, nerd_count=0):
        """add information about chat member into 'chat_members?' table"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("INSERT INTO " + chat_name + " ('user_id', "
                                       "'warning_count', 'nerd_count') VALUES (?, ?, ?)",
                                       (user_id, warning_count, nerd_count,))

    def update_warning_count(self, chat_id, user_id, warning_count=0):
        """update member`s warning_count in the 'chat_members?' table"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("UPDATE " + chat_name + " SET warning_count = ? "
                                       "WHERE user_id = ?", (warning_count, user_id,))

    def update_nerd_count(self, chat_id, user_id, nerd_count=0):
        """update member`s nerd_count in the 'chat_members?' table"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("UPDATE " + chat_name + " SET nerd_count = ? "
                                       "WHERE user_id = ?", (nerd_count, user_id,))

    def get_all_chat_members(self, chat_id):
        """return information about all chat members saved in the 'chat_members?' table"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("SELECT * FROM " + chat_name).fetchall()

    def get_chat_member(self, chat_id, user_id):
        """return information about chat member saved in the 'chat_members?' table"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("SELECT * FROM " + chat_name + " WHERE user_id = ?", (user_id,)).fetchall()

    def delete_chat_member(self, chat_id, user_id):
        """delete information about chat member from 'chat_members?' table"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("DELETE FROM " + chat_name + " WHERE user_id = ?", (user_id,))

    def delete_chat_members_table(self, chat_id):
        """delete 'chat_members?' table"""

        with self.connection:
            chat_name = "'chat_members" + str(chat_id) + "'"
            return self.cursor.execute("DROP TABLE " + chat_name)

    def increase_warning_count(self, chat_id, user_id):
        """increase user`s warning_count
            return 1 - user has 1 warning
            return 2 - user has 2 warnings
            return 3 - user has 3 warnings (update user`s warning_count to 0)"""

        member_info = self.get_chat_member(chat_id, user_id)

        if len(member_info) == 0:
            self.add_chat_member(chat_id, user_id, 1)
            return 1
        elif member_info[0][1] == 0:
            self.update_warning_count(chat_id, user_id, 1)
            return 1
        elif member_info[0][1] == 1:
            self.update_warning_count(chat_id, user_id, 2)
            return 2
        else:
            self.update_warning_count(chat_id, user_id, 0)
            return 3

    def close(self):
        """close database connection"""

        self.connection.close()
