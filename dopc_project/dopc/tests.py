import unittest
from django.test import Client

class dopc_test_cases(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()
        self.base_url = "/api/v1/delivery-order-price"

    def test_valid_request(self):
        """Test valid request with all correct parameters."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "cart_value": 1000,
                "user_lat": 52.5003197,
                "user_lon": 13.4536149
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_price", response.json())
        self.assertIn("small_order_surcharge", response.json())
        self.assertIn("delivery", response.json())

    def test_invalid_cart_value(self):
        """Test request with invalid cart value."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "cart_value": -1000,
                "user_lat": 52.5200,
                "user_lon": 13.4050
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_invalid_coordinates(self):
        """Test request with invalid latitude and longitude values."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "cart_value": 1000,
                "user_lat": 1000,
                "user_lon": 2000
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_missing_query_parameters(self):
        """Test request with missing query parameters."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "user_lat": 52.5200
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_delivery_distance_too_long(self):
        """Test request where the delivery distance exceeds the maximum range."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "cart_value": 1000,
                "user_lat": 85.0000,  # Far latitude value to simulate large distance
                "user_lon": 179.0000
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_small_order_surcharge(self):
        """Test request where a small order surcharge is applied."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "cart_value": 800,  # Below the minimum order value
                "user_lat": 52.5012207,
                "user_lon": 13.4536149
            }
        )
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertGreater(json_response["small_order_surcharge"], 0)

    def test_zero_cart_value(self):
        """Test request with zero cart value."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "cart_value": 0,
                "user_lat": 52.5200,
                "user_lon": 13.4050
            }
        )
        self.assertEqual(response.status_code, 400)
        # json_response = response.json()
        # self.assertGreater(json_response["small_order_surcharge"], 0)

    def test_invalid_venue_slug(self):
        """Test request with an invalid venue slug."""
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "invalid-venue-slug",
                "cart_value": 1000,
                "user_lat": 52.5200,
                "user_lon": 13.4050
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

if __name__ == "__main__":
    unittest.main()
