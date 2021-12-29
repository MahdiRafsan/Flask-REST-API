import unittest
from test.basic import Base

class TestTodo(Base):
    """
    test todo functionalities 
    """
    def test_create_todo(self):
        """
        test create a todo route
        """
        response = super().create_todo("Create a todo")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "New todo created!")

    def test_get_todos(self): 
        """
        test route for getting all todos
        """       
        super().create_todo("Create a todo")
        super().create_todo("Get all todos")

        token = super().get_access_token()[1]

        response = self.client.get("/api/todo", headers={"x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json["todos"]), list)
        self.assertEqual(len(response.json["todos"]), 2)
        self.assertEqual(response.json["todos"][1]["item"], "Get all todos")

    def test_get_todo(self):
        """
        test route for getting a todo
        """
        super().create_todo("Create a todo")
        super().create_todo("Get a todo")

        token = super().get_access_token()[1]

        response = self.client.get("/api/todo/2", headers={"x-access-token": token})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["todo"]), 1)
        self.assertEqual(response.json["todo"][0]["item"], "Get a todo" )

    def test_complete_todo(self):
        """
        test complete todo route
        """        
        super().create_todo("Create a todo")
        super().create_todo("Complete a todo")
        
        token = super().get_access_token()[1]

        response = self.client.put("/api/todo/2", 
            headers={"Content-Tyep":"application/json", "x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Todo item has been updated as complete!")
        
        response = self.client.get("/api/todo/2", headers={"x-access-token": token})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["todo"][0]["complete"] == 1)

        response = self.client.get("/api/todo/1", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json["todo"][0]["complete"] == 1)

    def test_delete_todo(self):        
        """
        test delete todo route
        """
        super().create_todo("Create a todo")
        super().create_todo("Delete a todo")
        
        token = super().get_access_token()[1]

        response = self.client.delete("/api/todo/2", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Todo item deleted!")

        response = self.client.delete("/api/todo/2", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Todo does not exist!")

    def test_inaccessible_todo(self): 
        """
        test routes for non-existing todos
        """
        token = super().get_access_token()[1]
        
        # get a todo
        response = self.client.get("/api/todo/1", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Todo does not exist!")

        # mark todo as complete
        response = self.client.put("/api/todo/2", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Todo does not exist!")

        # delete todo
        response = self.client.delete("/api/todo/3", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Todo does not exist!")

    def test_unauthorized_todo(self):
        """
        test routes for todos with unauthorized user (not owner of todo)
        """
        super().create_todo("First todo")
        token = super().get_access_token()[0]
        
        # get a todo
        response = self.client.get("/api/todo/1", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")

        # mark todo as complete
        response = self.client.put("/api/todo/1", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")

        # delete todo
        response = self.client.delete("/api/todo/1", headers={"x-access-token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "You don't have permission to perform that function!")

if __name__ == "__main__":
    unittest.main()