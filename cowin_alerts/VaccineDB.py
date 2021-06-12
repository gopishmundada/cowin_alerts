from os import environ, path
import psycopg2
from urllib.parse import urlparse

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class VaccineDB:
    users_table = 'users'
    pincodes_table = 'pincodes'
    preference_table = 'preference'
    subscriptions_table = 'subscriptions'

    def __init__(self, testing=False):
        self.testing = testing

        db_url = ''

        if not testing:
            db_url = urlparse(environ.get('DATABASE_URL'))
        else:
            db_url = urlparse(environ.get('TEST_DATABASE_URL_2'))

        print('=====>', db_url.path[1:])

        self.conn = psycopg2.connect(
            database=db_url.path[1:],
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port
        )
        self.cur = self.conn.cursor()

    def _commit(self):
        self.conn.commit()

    def get_all_pincodes(self):
        self.cur.execute(f'SELECT pincode FROM {self.pincodes_table};')
        all_pincodes = list(map(lambda p: p[0], self.cur.fetchall()))

        return all_pincodes

    def get_subscribers_list(self, pincode: int, sub_18: bool = None, sub_45: bool = None) -> list:
        '''
        Returns list of username and email e.g [('John','john@wick.com'), ('Tony', 'tony@stark.com')]

            :param pincode: Integer pincode of the district the user is subscribed to.
            :param sub_18: Boolean indicating if the user subscribed to 18+ slots. Can be `None`
            :param sub_45: Boolean indicating if the user subscribed to 45+ slots. Can be `None`

            :returns: List of tuple of username and their email.
        '''
        pass

    def populate_test_db(self):
        if not self.testing:
            return

        # Populating Users table
        self.cur.execute(f'''INSERT INTO {self.users_table}
                             (id, name, email) values
                             (1,'John Wick','john@wick.com'),
                             (2,'Tony Stark','tony@stark.com'),
                             (3,'Needle','arya@stark.com');''')

        # Populating pincodes table
        self.cur.execute(f'''INSERT INTO {self.pincodes_table}
                             (id, pincode) values
                             (1, 431203),
                             (2, 431204), 
                             (3, 410507);''')

        # Populating Preference table
        self.cur.execute(f'''INSERT INTO {self.preference_table}
                             (id, sub_18, sub_45) values
                             (1,True,True),
                             (2,True,False),
                             (3,False,True);''')

        # Populating Subscriptions table
        self.cur.execute(f'''INSERT INTO {self.subscriptions_table}
                             (id, subscriber_id, pincode_id, preference_id) values
                             (1,1,1,1),
                             (2,1,2,3),
                             (3,3,1,3),
                             (4,2,3,1),
                             (5,3,3,2),
                             (6,2,1,1);''')

        self._commit()

    def drop_all(self):
        self.cur.execute(f'TRUNCATE {self.pincodes_table} CASCADE')
        self.cur.execute(f'TRUNCATE {self.users_table} CASCADE')
        self.cur.execute(f'TRUNCATE {self.preference_table} CASCADE')

        self._commit()