import sqlite3 as sq


def sql_start(user_channel_status, channel, channels):
    global base, cur, rows
    base = sq.connect('data.db')
    cur = base.cursor()
    if not base:
        print('[+]Data base IS NOT connected!')
    base.execute('CREATE TABLE IF NOT EXISTS data(city, chat_id, user_name, user_surname, user_id)')
    base.commit()
    base.execute('INSERT INTO data VALUES(?,?,?,?,?)', (str(channel), str(channels[channel]),
                                                        str(user_channel_status['user']['first_name']),
                                                        str(user_channel_status['user']['last_name']),
                                                        str(user_channel_status['user']['id'])))
    base.commit()
    rows = cur.execute('SELECT * FROM data').fetchall()


def data_main():
    base.execute('CREATE TABLE IF NOT EXISTS data_main(city, chat_id, user_name, user_surname, user_id)')
    base.commit()
    unique_list = []
    for row in rows:
        print(row)
        if row in unique_list:
            pass
        else:
            cur.execute('INSERT INTO data_main VALUES(?,?,?,?,?)', row)
            print('added', row)
            base.commit()
            unique_list.append(row)
    print(len(unique_list))
