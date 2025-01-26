from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_distance
from .utils import fetch_venue_data
BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/"

@csrf_exempt
def calculate_price(request):
    """
    Calculate the total price for a delivery order based on the cart value, user location, and venue data.
    Args:
        request (HttpRequest): The HTTP request object containing query parameters:
            - venue_slug (str): The slug identifier for the venue.
            - cart_value (int): The value of the items in the cart.
            - user_lat (float): The latitude of the user's location.
            - user_lon (float): The longitude of the user's location.
    Returns:
        JsonResponse: A JSON response containing:
            - total_price (int): The total price including cart value, small order surcharge, and delivery fee.
            - small_order_surcharge (int): The surcharge applied if the cart value is below the minimum order value.
            - cart_value (int): The value of the items in the cart.
            - delivery (dict): A dictionary containing:
                - fee (int): The delivery fee based on the distance.
                - distance (int): The calculated delivery distance.
    Raises:
        JsonResponse: A JSON response with an error message and appropriate HTTP status code in case of:
            - Invalid parameter data type (400)
            - Invalid cart value (400)
            - Unable to fetch venue data (400)
            - Delivery distance exceeds the allowed range (400)
            - Delivery not available for this distance (400)
            - Invalid request method (405)
    """
    if request.method == 'GET':
        try:
            # Get query parameters
            venue_slug = request.GET.get('venue_slug')
            cart_value = int(float(request.GET.get('cart_value')))
            user_lat = float(request.GET.get('user_lat'))
            user_lon = float(request.GET.get('user_lon'))
        except Exception as e:
            return JsonResponse({'error': 'Invalid parameter data type'}, status=400)

        try:
            cart_value = int(cart_value)
            if cart_value <= 0:
                raise ValueError("Cart value must be a positive integer")
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid cart value'}, status=400)

        # Fetch venue data
        static_data, dynamic_data = fetch_venue_data(venue_slug)
        if not static_data or not dynamic_data:
            return JsonResponse({'error': 'Unable to fetch venue data'}, status=400)

        # Extract relevant data
        venue_coordinates = tuple(static_data['venue_raw']['location']['coordinates'][::-1])
        order_minimum = dynamic_data['venue_raw']['delivery_specs']['order_minimum_no_surcharge']
        base_price = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['base_price']
        distance_ranges = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['distance_ranges']
        max_distance = distance_ranges[-1]['min']
        # Calculate distance
        delivery_distance = calculate_distance((user_lat, user_lon), venue_coordinates)
        if delivery_distance > max_distance:
            return JsonResponse({'error': 'Delivery distance exceeds the allowed range.'}, status=400)

        # Find the applicable range for the delivery fee
        for range_ in distance_ranges:
            if range_['min'] <= delivery_distance < range_['max'] or range_['max'] == 0:
                delivery_fee = base_price + range_['a'] + round(range_['b'] * delivery_distance / 10)
                break
        else:
            return JsonResponse({'error': 'Delivery not available for this distance'}, status=400)

        # Calculate small order surcharge
        small_order_surcharge = max(0, order_minimum - cart_value)

        # Calculate total price
        total_price = cart_value + small_order_surcharge + delivery_fee

        response = {
            'total_price': total_price,
            'small_order_surcharge': small_order_surcharge,
            'cart_value': cart_value,
            'delivery': {
                'fee': delivery_fee,
                'distance': delivery_distance
            }
        }
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
