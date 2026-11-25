import unittest

from web import create_app


class TestWarehouseWeb(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_and_list_multiple_items(self):
        self.client.post("/items", data={"name": "Apples", "quantity": "12"})
        response = self.client.post(
            "/items", data={"name": "Oranges", "quantity": "5"}, follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Apples", response.data)
        self.assertIn(b"12.0", response.data)
        self.assertIn(b"Oranges", response.data)
        self.assertIn(b"5.0", response.data)

    def test_add_and_remove_stock(self):
        self.client.post("/items", data={"name": "Apples", "quantity": "12"})

        self.client.post("/items/add", data={"name": "Apples", "quantity": "3"})
        self.client.post("/items/remove", data={"name": "Apples", "quantity": "4"})

        response = self.client.get("/")
        self.assertIn(b"11.0", response.data)

    def test_invalid_item_is_rejected(self):
        response = self.client.post(
            "/items", data={"name": "", "quantity": "-1"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"valid non-negative quantity", response.data)

    def test_duplicate_item_name_is_rejected(self):
        self.client.post("/items", data={"name": "Apples", "quantity": "12"})

        response = self.client.post(
            "/items", data={"name": "Apples", "quantity": "3"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"already exists", response.data)


if __name__ == "__main__":
    unittest.main()
