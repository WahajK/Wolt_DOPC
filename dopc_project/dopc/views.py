import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_distance
from .utils import fetch_venue_data
BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/"

@csrf_exempt
def calculate_price(request):
    if request.method == 'GET':
        try:
            # Get query parameters
            venue_slug = request.GET.get('venue_slug')
            cart_value = int(request.GET.get('cart_value'))
            user_lat = float(request.GET.get('user_lat'))
            user_lon = float(request.GET.get('user_lon'))

            # Fetch venue data
            static_data, dynamic_data = fetch_venue_data(venue_slug)
            if not static_data or not dynamic_data:
                return JsonResponse({'error': 'Unable to fetch venue data'}, status=400)

            # Extract relevant data
            venue_coordinates = tuple(static_data['venue_raw']['location']['coordinates'][::-1])
            order_minimum = dynamic_data['venue_raw']['delivery_specs']['order_minimum_no_surcharge']
            base_price = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['base_price']
            distance_ranges = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['distance_ranges']

            # Calculate distance
            delivery_distance = calculate_distance((user_lat, user_lon), venue_coordinates)

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

            # Construct response
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

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
