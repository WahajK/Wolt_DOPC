# Delivery Order Price Calculator (DOPC)

## **Overview**

The Delivery Order Price Calculator (DOPC) is a Django-based API service that calculates the total price for an order, including a delivery fee and a small order surcharge, based on the following inputs:

- **Venue slug**: Identifies the venue from which the order is placed.
- **Cart value**: The total value of items in the cart.
- **User's latitude and longitude**: To calculate the delivery distance from the venue.

The API fetches static and dynamic venue data from external endpoints, calculates the delivery fee based on distance, and applies a small order surcharge if the cart value is below a threshold.

---

## **Features**

- **Delivery Fee Calculation**: Based on configurable distance ranges and pricing rules.
- **Small Order Surcharge**: Applied if the cart value is below the venue-defined minimum.
- **Dynamic Data Fetching**: Uses external APIs for venue location and pricing specifications.
- **REST API**: Accessible via a single endpoint, following best practices for request and response handling.

---

## **Requirements**

### **Prerequisites**

Ensure the following tools are installed on your machine:
- Python 3.8+
- pip (Python package installer)

### **Dependencies**

The project uses the following Python packages:
- `Django`
- `requests`
- `geopy`

Install all dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

---

## **Setup Instructions**

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/WahajK/Wolt_DOPC.git
cd dopc
```

### **Step 2: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 3: Start the Django Project**

Run the following command to start the development server:
```bash
python manage.py runserver
```

The API will be accessible at: `http://127.0.0.1:8000/`

---

## **API Documentation**

### **Endpoint**

#### **GET** `/api/v1/delivery-order-price`

**Description**: Calculates the total delivery order price based on venue data and user inputs.

#### **Query Parameters**

| Parameter       | Type    | Description                                | Required |
|-----------------|---------|--------------------------------------------|----------|
| `venue_slug`    | string  | Unique identifier for the venue            | Yes      |
| `cart_value`    | integer | Total value of items in the cart (in cents)| Yes      |
| `user_lat`      | float   | Latitude of the user’s location            | Yes      |
| `user_lon`      | float   | Longitude of the user’s location           | Yes      |

#### **Sample Request**

```bash
curl "http://127.0.0.1:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-berlin&cart_value=1000&user_lat=52.5200&user_lon=13.4050"
```

#### **Sample Response**

```json
{
    "total_price": 1125,
    "small_order_surcharge": 0,
    "cart_value": 1000,
    "delivery": {
        "fee": 125,
        "distance": 1523
    }
}
```

#### **Error Responses**

| Status Code | Message                             | Reason                                       |
|-------------|-------------------------------------|----------------------------------------------|
| 400         | `Unable to fetch venue data`       | Venue slug is invalid or API request failed. |
| 400         | `Invalid or missing parameters`    | One or more query parameters are missing.    |
| 405         | `Invalid request method`           | Only GET method is supported.                |

---

## **Project Structure**

```
dopc_project/
├── dopc_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── dopc/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── utils.py
├── manage.py
└── requirements.txt
```

### **Key Files**

- **`views.py`**: Contains the `calculate_price` view function with the main API logic.
- **`utils.py`**: Helper functions for calculating distances and fetching external data.
- **`urls.py`**: Defines URL routing for the app and its endpoint.

---

## **How It Works**

1. **Query Parameters**:
   - User provides the venue slug, cart value, and their geolocation via query parameters.

2. **Venue Data Fetching**:
   - The API retrieves static and dynamic data for the venue from the external Wolt API.

3. **Distance Calculation**:
   - The user’s geolocation is compared with the venue’s coordinates to calculate the delivery distance using `geopy`.

4. **Fee Calculation**:
   - A small order surcharge is applied if the cart value is below the minimum.
   - The delivery fee is calculated based on distance ranges and pricing rules.

5. **Response**:
   - Returns the total price, including the cart value, small order surcharge, and delivery fee.

---

## **Testing**

### **Run Tests**
Automated tests ensure the functionality of the API:
```bash
python manage.py test
```

### **Test Scenarios**

1. Valid request with all parameters.
2. Missing or invalid query parameters.
3. Invalid venue slug.

---

## **Future Improvements**

- Add authentication for secure API access.
- Cache venue data to reduce external API calls.
- Handle more complex pricing rules.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.
