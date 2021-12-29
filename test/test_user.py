import json
import unittest
from test.basic import Base

class TestUser(Base):
    """
    test user functionalities
    """    
    def test_get_users(self):
        """
        test get all users route with admin
        """
        token = super().get_access_token()[0]
        response = self.client.get("/api/user", headers = {"x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.json["users"]))
        self.assertEqual("user1", response.json["users"][0]["name"])
        self.assertEqual(str, type(response.json["users"][0]["public_id"]))
        
    def test_get_user(self):
        """
        test get a user route with admin
        """
        token, _, pub_id1, pub_id2 = super().get_access_token()

        response = self.client.get(f"/api/user/{pub_id1}", headers = {"x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.json["user"]))
        self.assertTrue(response.json["user"][0]["admin"] == True)
        self.assertEqual("user1", response.json["user"][0]["name"])
        self.assertEqual(str, type(response.json["user"][0]["public_id"]))

        response = self.client.get(f"/api/user/{pub_id2}", headers = {"x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.json["user"]))
        self.assertEqual(str, type(response.json["user"][0]["public_id"]))
        self.assertFalse(response.json["user"][0]["admin"] == True)
        self.assertEqual("user2", response.json["user"][0]["name"])
        
    def test_promote_user(self):
        """
        test promote user route with admin
        """
        token, _, pub_id1, pub_id2 = super().get_access_token()

        response = self.client.get(f"/api/user/{pub_id1}", headers = {"x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["user"][0]["admin"] == True)

        response = self.client.put(f"/api/user/{pub_id2}/promote",
            headers = {"Content-Type": "application/json", "x-access-token": token})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User has been promoted to admin!")

        response = self.client.get(f"/api/user/{pub_id2}", headers = {"x-access-token": token})
        
        self.assertTrue(response.json["user"][0]["admin"] == True)
        self.assertEqual("user2", response.json["user"][0]["name"])
    
    def test_update_user(self):
        """
        test update user route with admin
        """
        token, _, pub_id1, pub_id2 = super().get_access_token()
    
        response = self.client.get(f"/api/user/{pub_id1}", headers = {"x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["user"][0]["admin"] == True)

        payload = {"name":"updated_user1", "password":"password1"}
        response = self.client.put(f"/api/user/{pub_id1}/update",
            headers = {"Content-Type": "application/json", "x-access-token": token}, 
            data = json.dumps(payload))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User info has been updated!")

        payload = {"name":"updated_user2", "password":"password1"}
        response = self.client.put(f"/api/user/{pub_id2}/update",
            headers = {"Content-Type": "application/json", "x-access-token": token},
            data = json.dumps(payload))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User info has been updated!")
        
        response = self.client.get(f"/api/user", headers = {"x-access-token": token})

        self.assertEqual("updated_user1", response.json["users"][0]["name"])
        self.assertEqual("updated_user2", response.json["users"][1]["name"])
    
    def test_delete_user(self):
        """
        test delete user route with admin
        """
        token, _, pub_id1, pub_id2 = super().get_access_token()

        response = self.client.get(f"/api/user/{pub_id1}",
            headers = {"Content-Type": "application/json", "x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["user"][0]["admin"] == True)

        response = self.client.delete(f"/api/user/{pub_id2}",
            headers = {"Content-Type": "application/json", "x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User has been deleted!")

        response = self.client.get(f"/api/user/{pub_id2}", headers = {"x-access-token": token})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User does not exist!")
    
    def test_inaccessible_user(self):
            """
            test routes for non exisiting user 
            """
            token = super().get_access_token()[0]

            # get user
            response = self.client.get("/api/user/akjdhslsa", headers = {"x-access-token": token})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["message"], "User does not exist!")
            
            # promote user
            response = self.client.put("/api/user/akjdhslsa/promote", headers = {"x-access-token": token})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["message"], "User does not exist!")

            # update user
            response = self.client.put("/api/user/akjdhslsa/update", headers = {"x-access-token": token})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["message"], "User does not exist!")

            # delete user
            response = self.client.delete("/api/user/akjdhslsa", headers = {"x-access-token": token})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["message"], "User does not exist!")

    def test_unauthorized_user(self):
        """
        test routes with unauthorized login (not admin)
        """
        _, token, _, pub_id2 = super().get_access_token()

        # get all users
        response = self.client.get("/api/user", headers = {"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")

        # get a user
        response = self.client.get(f"/api/user/{pub_id2}", headers = {"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")

        # promote a user
        response = self.client.put(f"/api/user/{pub_id2}/promote", headers = {"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")

        # update a user
        response = self.client.put(f"/api/user/{pub_id2}/update", headers = {"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")

        # delete a user
        response = self.client.delete(f"/api/user/{pub_id2}", headers = {"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")
        
       
if __name__ == "__main__":
    unittest.main()