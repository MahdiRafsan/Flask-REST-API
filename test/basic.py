import unittest
import json
from base64 import b64encode
from api import create_app, db
from api.models import User

class Base(unittest.TestCase):
    """
    A base class providing methods to be used for testing different routes
    """    
    def setUp(self):
        """
        execute before running a test case
        """
        self.app = create_app("testing")
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()
        self.client = self.app.test_client()
        
    def tearDown(self):
        """
        execute after running a test case
        """
        db.drop_all()
        self.app_ctx.pop()

    def get_header(self, payload):
        """
        provide header for sign-up and login
        :param payload: data to be used for sign-up and login
        :return: http header
        """
        name = bytes((json.loads(payload)['name'] + ":" + json.loads(payload)['password']).encode('utf-8'))
    
        return {"Authorization": f"Basic {b64encode(name).decode('utf-8')}",
                "Content-Type": "application/json"}
        
    def sign_up(self, username, password):
        """
        register a new user
        :param username: str
        :param password: str
        :return: http test response 
        """
        payload = json.dumps({"name": username, "password": password})
        return self.client.post("/api/sign-up", headers=self.get_header(payload), data=payload)

    def login(self, username, password):
        """
        login a registered user
        :param username: str
        :param password: str
        :return: http test response 
        """
        payload = json.dumps({"name": username, "password": password})
        return self.client.get("/api/login", headers=self.get_header(payload), data=payload)

    def get_access_token(self):
        """
        create access tokens for a admin and a non-admin user
        :return: tokens for admin and non-admin along with their public ids
        """
        self.sign_up("user1", "password1")
        self.sign_up("user2", "12345")
        pub_id1 = User.query.filter_by(name="user1").first().public_id
        pub_id2 = User.query.filter_by(name="user2").first().public_id
        
        login1 = self.login("user1", "password1")
        login2 = self.login("user2", "12345")
        return login1.json["token"], login2.json["token"], pub_id1, pub_id2

    def create_todo(self, todo):
        """
        create a todo
        :param todo: str describing the todo
        :return: http response creating a todo
        """
        token = self.get_access_token()[1]
        payload = json.dumps({"item": todo})
        item = bytes(json.loads(payload)["item"], encoding = "utf-8")
        header = {"Authorization": f"Basic {b64encode(item).decode('utf-8')}",
                  "Content-Type": "application/json", 
                  "x-access-token": token}
        return self.client.post("/api/todo", headers=header, data=payload)
