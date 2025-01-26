import unittest
from django.test import Client

class dopc_test_cases(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()
        self.base_url = "/api/v1/delivery-order-price"

    def test_valid_request(self):
        """
		Test the valid request to the endpoint.

		This test sends a GET request to the base URL with specific query parameters
		and checks if the response status code is 200. It also verifies that the 
		response JSON contains the keys "total_price", "small_order_surcharge", 
		and "delivery".

		Query Parameters:
			venue_slug (str): The slug of the venue.
			cart_value (int): The value of the cart.
			user_lat (float): The latitude of the user.
			user_lon (float): The longitude of the user.

		Asserts:
			response.status_code == 200
			"total_price" in response.json()
			"small_order_surcharge" in response.json()
			"delivery" in response.json()
		"""
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
        """
		Test case for handling invalid cart value in the API request.

		This test sends a GET request to the base URL with a negative cart value,
		which is considered invalid. It verifies that the response status code is 400
		(Bad Request) and checks that the response contains an "error" key in the JSON body.

		Assertions:
			- The response status code should be 400.
			- The response JSON should contain an "error" key.
		"""
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
        """
		Test case for invalid coordinates.

		This test sends a GET request to the base URL with invalid latitude and longitude
		values for the user's location. It verifies that the response status code is 400
		(Bad Request) and that the response contains an "error" key in the JSON body.

		Assertions:
			- The response status code should be 400.
			- The response JSON should contain an "error" key.
		"""
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
        """
		Test case for missing query parameters in the GET request.

		This test sends a GET request to the base URL with missing query parameters.
		Specifically, it omits the 'user_lng' parameter. The expected behavior is 
		that the server responds with a 400 status code and an error message in the 
		response JSON.

		Assertions:
			- The response status code should be 400.
			- The response JSON should contain an "error" key.
		"""
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
        """
		Test case to verify that the API returns a 400 status code and an error message
		when the delivery distance is too long.

		This test simulates a scenario where the user's latitude and longitude are set
		to values that represent a far distance from the venue. The expected behavior
		is that the API should respond with a 400 status code and include an error message
		in the response JSON.

		Assertions:
			- The response status code should be 400.
			- The response JSON should contain an "error" key.
		"""
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
        """
		Test the small order surcharge for orders below the minimum order value.

		This test sends a GET request to the specified venue with a cart value below
		the minimum order value and verifies that the response status code is 200.
		It also checks that the small order surcharge in the JSON response is greater
		than 0.

		The request parameters include:
		- venue_slug: The slug identifier for the venue.
		- cart_value: The value of the cart, set below the minimum order value.
		- user_lat: The latitude of the user's location.
		- user_lon: The longitude of the user's location.

		Assertions:
		- The response status code should be 200.
		- The small order surcharge in the JSON response should be greater than 0.
		"""
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
        """
		Test case for verifying the response when the cart value is zero.

		This test sends a GET request to the base URL with the following parameters:
		- venue_slug: "home-assignment-venue-berlin"
		- cart_value: 0
		- user_lat: 52.5200
		- user_lon: 13.4050

		It asserts that the response status code is 400, indicating a bad request.
		"""
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

    def test_invalid_venue_slug(self):
        """
		Test the API endpoint with an invalid venue slug.

		This test sends a GET request to the base URL with an invalid venue slug
		and checks that the response status code is 400 (Bad Request). It also
		verifies that the response contains an "error" key in the JSON body.

		Assertions:
			- The response status code should be 400.
			- The response JSON should contain an "error" key.
		"""
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
        
    def test_floating_point_cart_value(self):
        response = self.client.get(
			self.base_url, 
			{
				"venue_slug": "home-assignment-venue-berlin",
				"cart_value": 1000.12, #Check for floating value
				"user_lat": 52.5003197,
				"user_lon": 13.4536149
			}
		)
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_price", response.json())
        self.assertIn("small_order_surcharge", response.json())
        self.assertIn("delivery", response.json())

    def test_string_cart_value(self):
        response = self.client.get(
            self.base_url, 
            {
                "venue_slug": "home-assignment-venue-berlin",
                "cart_value": "test", #Check for string value
                "user_lat": 52.5003197,
                "user_lon": 13.4536149
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("total_price", response.json())
        self.assertIn("small_order_surcharge", response.json())
        self.assertIn("delivery", response.json())

if __name__ == "__main__":
    unittest.main()
