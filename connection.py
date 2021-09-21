from datetime import datetime
import mysql.connector
import random


class Connection:
    db = mysql.connector.connect(
        host='11.111.11.111',
        user='youcantseethis',
        passwd='sorry',
        database='faith'
    )

    cursor = db.cursor()

    date = datetime.now()
    current_month = date.strftime('%B')

    def get_latest_main_service(self):
        self.cursor.execute(f'SELECT * FROM main_service WHERE month="{self.current_month}"')
        fetched_details = self.cursor.fetchall()

        schedule_num = len(fetched_details)

        fetched_month = []
        fetched_sched_num = []
        fetched_date = []
        fetched_time = []
        fetched_year = []
        fetched_preacher = []
        fetched_sub_preacher = []
        fetched_topic = []
        fetched_topic_details = []
        fetched_event = []
        fetched_event_details = []
        fetched_opening_prayer = []
        fetched_scripture_reading = []
        fetched_offertory = []
        fetched_closing_prayer = []
        fetched_status = []

        for i in range(schedule_num):
            fetched_month.append(fetched_details[i][0])
            fetched_sched_num.append(fetched_details[i][1])
            fetched_date.append(fetched_details[i][2])
            fetched_time.append(fetched_details[i][3])
            fetched_year.append(fetched_details[i][4])
            fetched_preacher.append(fetched_details[i][5])
            fetched_sub_preacher.append(fetched_details[i][6])
            fetched_topic.append(fetched_details[i][7])
            fetched_topic_details.append(fetched_details[i][8])
            fetched_event.append(fetched_details[i][9])
            fetched_event_details.append(fetched_details[i][10])
            fetched_opening_prayer.append(fetched_details[i][11])
            fetched_scripture_reading.append(fetched_details[i][12])
            fetched_offertory.append(fetched_details[i][13])
            fetched_closing_prayer.append(fetched_details[i][14])
            fetched_status.append(fetched_details[i][15])

        return schedule_num, fetched_month, fetched_sched_num, fetched_date, fetched_time, fetched_year, fetched_preacher, \
               fetched_sub_preacher, fetched_topic, fetched_topic_details, fetched_event, fetched_event_details, \
               fetched_opening_prayer, fetched_scripture_reading, fetched_offertory, fetched_closing_prayer, fetched_status

    def get_outreach_names(self):
        self.cursor.execute(f'SELECT DISTINCT outreach_name FROM outreach_service WHERE month="{self.current_month}"')
        fetched_details = self.cursor.fetchall()

        fetched_outreach_names = []

        for i in range(len(fetched_details)):
            fetched_outreach_names.append(fetched_details[i][0])

        return fetched_outreach_names

    def get_latest_outreach_service(self, outreach):
        self.cursor.execute(
            f'SELECT * FROM outreach_service WHERE month="{self.current_month}" AND outreach_name = "{outreach}"')
        fetched_details = self.cursor.fetchall()

        schedule_num = len(fetched_details)

        fetched_month = []
        fetched_outreach = []
        fetched_sched_num = []
        fetched_date = []
        fetched_time = []
        fetched_year = []
        fetched_preacher = []
        fetched_sub_preacher = []
        fetched_topic = []
        fetched_topic_details = []
        fetched_event = []
        fetched_event_details = []
        fetched_opening_prayer = []
        fetched_scripture_reading = []
        fetched_offertory = []
        fetched_closing_prayer = []
        fetched_status = []

        for i in range(schedule_num):
            fetched_month.append(fetched_details[i][0])
            fetched_outreach.append(fetched_details[i][1])
            fetched_sched_num.append(fetched_details[i][2])
            fetched_date.append(fetched_details[i][3])
            fetched_time.append(fetched_details[i][4])
            fetched_year.append(fetched_details[i][5])
            fetched_preacher.append(fetched_details[i][6])
            fetched_sub_preacher.append(fetched_details[i][7])
            fetched_topic.append(fetched_details[i][8])
            fetched_topic_details.append(fetched_details[i][9])
            fetched_event.append(fetched_details[i][10])
            fetched_event_details.append(fetched_details[i][11])
            fetched_opening_prayer.append(fetched_details[i][12])
            fetched_scripture_reading.append(fetched_details[i][13])
            fetched_offertory.append(fetched_details[i][14])
            fetched_closing_prayer.append(fetched_details[i][15])
            fetched_status.append(fetched_details[i][16])

        return schedule_num, fetched_month, fetched_outreach, fetched_sched_num, fetched_date, fetched_time, fetched_year, fetched_preacher, \
               fetched_sub_preacher, fetched_topic, fetched_topic_details, fetched_event, fetched_event_details, \
               fetched_opening_prayer, fetched_scripture_reading, fetched_offertory, fetched_closing_prayer, fetched_status

    def get_latest_events(self):
        self.cursor.execute(f'SELECT * FROM events WHERE month="{self.current_month}"')
        fetched_details = self.cursor.fetchall()

        schedule_num = len(fetched_details)

        fetched_month = []
        fetched_event_name = []
        fetched_sched_num = []
        fetched_date = []
        fetched_time = []
        fetched_year = []
        fetched_preacher = []
        fetched_sub_preacher = []
        fetched_topic = []
        fetched_topic_details = []
        fetched_event_details = []
        fetched_opening_prayer = []
        fetched_scripture_reading = []
        fetched_offertory = []
        fetched_closing_prayer = []
        fetched_event_organizer = []
        fetched_contact_details = []
        fetched_status = []

        for i in range(schedule_num):
            fetched_month.append(fetched_details[i][0])
            fetched_event_name.append(fetched_details[i][1])
            fetched_sched_num.append(fetched_details[i][2])
            fetched_date.append(fetched_details[i][3])
            fetched_time.append(fetched_details[i][4])
            fetched_year.append(fetched_details[i][5])
            fetched_preacher.append(fetched_details[i][6])
            fetched_sub_preacher.append(fetched_details[i][7])
            fetched_topic.append(fetched_details[i][8])
            fetched_topic_details.append(fetched_details[i][9])
            fetched_event_details.append(fetched_details[i][10])
            fetched_opening_prayer.append(fetched_details[i][11])
            fetched_scripture_reading.append(fetched_details[i][12])
            fetched_offertory.append(fetched_details[i][13])
            fetched_closing_prayer.append(fetched_details[i][14])
            fetched_event_organizer.append(fetched_details[i][15])
            fetched_contact_details.append(fetched_details[i][16])
            fetched_status.append(fetched_details[i][17])

        return schedule_num, fetched_month, fetched_event_name, fetched_sched_num, fetched_date, fetched_time, fetched_year, fetched_preacher, \
               fetched_sub_preacher, fetched_topic, fetched_topic_details, fetched_event_details, \
               fetched_opening_prayer, fetched_scripture_reading, fetched_offertory, fetched_closing_prayer, fetched_event_organizer, fetched_contact_details, fetched_status

    def on_main_send(self, send):
        self.cursor.executemany('INSERT INTO main_service VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                send)

        self.db.commit()

    def on_outreach_send(self, send):
        self.cursor.executemany(
            'INSERT INTO outreach_service VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', send)

        self.db.commit()

    def on_events_send(self, send):
        self.cursor.executemany('INSERT INTO events VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                send)

        self.db.commit()

    def on_goal_send(self, title, body, date):
        self.cursor.execute('INSERT INTO goal VALUES(%s,%s,%s)', (title, body, date))

        self.db.commit()

    def on_announcement_send(self, title, body, date):
        self.cursor.execute('INSERT INTO announcement(title, body, date) VALUES(%s,%s,%s)', (title, body, date))

        self.db.commit()

    def announcements(self):
        title = ''
        body = ''
        date_now = ''

        self.cursor.execute('SELECT * FROM announcement ORDER BY id DESC LIMIT 1')
        fetched_details = self.cursor.fetchall()

        for i in range(len(fetched_details)):
            title = fetched_details[i][1]
            body = fetched_details[i][2]
            date_now = fetched_details[i][3]

        processed_date = datetime.strptime(str(date_now), '%Y-%m-%d')
        new_date = processed_date.strftime('%d %b, %Y')

        return title, body, new_date

    def memory_verse(self):
        title = ''
        body = ''

        self.cursor.execute('SELECT num FROM memory_verse ORDER BY num DESC LIMIT 1')
        fetched_number = self.cursor.fetchone()

        generated_num = random.randint(1, fetched_number[0])

        self.cursor.execute(f'SELECT * FROM memory_verse WHERE num = {generated_num}')
        fetched_details = self.cursor.fetchall()

        for detail in range(len(fetched_details)):
            title = fetched_details[detail][1]
            body = fetched_details[detail][2]

        return title, body

    def goal(self):
        title = ''
        body = ''

        self.cursor.execute(f'SELECT * FROM goal ORDER BY id DESC LIMIT 1')
        fetched_details = self.cursor.fetchall()

        for detail in range(len(fetched_details)):
            title = fetched_details[detail][1]
            body = fetched_details[detail][2]

        return title, body


connect = Connection()

if __name__ == '__main__':
    Connection()
