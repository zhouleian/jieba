# import pytest

import os
import flaskr
import tempfile
import unittest


# @pytest.fixture
class FlaskrTestCase(unittest.TestCase):
    def client(request):
        db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        client = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

        def teardown():
            os.close(db_fd)
            os.unlink(flaskr.app.config['DATABASE'])

        request.addfinalizer(teardown)

        return client
    def login(self, username, password):
        return self.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


def logout(self):
    return self.get('/logout', follow_redirects=True)


def test_empty_db(self):
    """Start with a blank database."""
    rv = self.get('/')
    assert b'No entries here so far' in rv.data


def test_login_logout(self):
    """Make sure login and logout works"""
    rv = login(self, flaskr.app.config['USERNAME'],
               flaskr.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(self)
    assert b'You were logged out' in rv.data
    rv = login(self, flaskr.app.config['USERNAME'] + 'x',
               flaskr.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(self, flaskr.app.config['USERNAME'],
               flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


def test_messages(self):
    """Test that messages work"""
    login(self, flaskr.app.config['USERNAME'],
          flaskr.app.config['PASSWORD'])
    rv = self.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
