import json

def get_simulated_response(scenario):
    """
    Simulates an HTTP response for different scenarios.
    Returns (status_code, body_string).
    """
    if scenario == "good_data":
        data = {
            "status": "success",
            "data": {
                "id": 123,
                "name": "Product A",
                "price": 99.99,
                "available": True,
                "tags": ["electronics", "gadget"]
            },
            "message": "Product data retrieved successfully."
        }
        return 200, json.dumps(data)
    elif scenario == "bad_data_missing_field":
        data = {
            "status": "success", # API still reports success
            "data": {
                "id": 456,
                "name": "Product B",
                # 'price' field is missing, but 200 OK is returned
                "available": True
            },
            "message": "Product data retrieved successfully (but might be incomplete)."
        }
        return 200, json.dumps(data)
    elif scenario == "bad_data_invalid_value":
        data = {
            "status": "success",
            "data": {
                "id": 789,
                "name": "Product C",
                "price": -10.00, # Price is negative, logically invalid
                "available": True
            },
            "message": "Product data retrieved successfully (but contains invalid values)."
        }
        return 200, json.dumps(data)
    elif scenario == "not_found":
        data = {
            "status": "error",
            "message": "Resource not found."
        }
        return 404, json.dumps(data)
    else:
        return 500, json.dumps({"status": "error", "message": "Internal server error."})

def process_product_response(status_code, response_body):
    """
    Processes a product API response, validating content even if 200 OK.
    """
    print(f"\n--- Processing Response (Status: {status_code}) ---")

    if status_code == 200:
        print("HTTP Status: 200 OK. Proceeding to content validation...")
        try:
            data = json.loads(response_body)

            # --- ARTICLE'S CORE CONCEPT ILLUSTRATED HERE ---
            # Even if the HTTP status is 200 OK, we must validate the *content* of the response body
            if data.get("status") == "success":
                product_data = data.get("data")
                if product_data is None:
                    print("Content Validation FAILED: 'data' field is missing or null.")
                    return False

                # Check for essential fields
                required_fields = ["id", "name", "price", "available"]
                missing_fields = [field for field in required_fields if field not in product_data]
                if missing_fields:
                    print(f"Content Validation FAILED: Missing required fields: {', '.join(missing_fields)}")
                    return False

                # Validate field values for logical correctness
                if not isinstance(product_data.get("id"), int):
                    print("Content Validation FAILED: 'id' is not an integer.")
                    return False
                if not isinstance(product_data.get("name"), str) or not product_data.get("name"): # Ensure not empty string
                    print("Content Validation FAILED: 'name' is missing or not a string.")
                    return False
                if not isinstance(product_data.get("price"), (int, float)) or product_data.get("price") < 0: # Price cannot be negative
                    print("Content Validation FAILED: 'price' is invalid (not a number or negative).")
                    return False
                if not isinstance(product_data.get("available"), bool):
                    print("Content Validation FAILED: 'available' is not a boolean.")
                    return False

                print("Content Validation PASSED: Data is complete and valid.")
                return True
            else:
                print(f"Content Validation FAILED: API reported internal status: '{data.get('status')}'")
                return False
        except json.JSONDecodeError:
            print("Content Validation FAILED: Response body is not valid JSON.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during content validation: {e}")
            return False
    else:
        print(f"HTTP Status: {status_code}. Not a 200 OK. Content validation skipped.")
        return False

# --- Main execution ---
if __name__ == "__main__":
    # Scenario 1: Truly successful response with valid content
    status, body = get_simulated_response("good_data")
    process_product_response(status, body)

    # Scenario 2: 200 OK but missing a required field in the data
    status, body = get_simulated_response("bad_data_missing_field")
    process_product_response(status, body)

    # Scenario 3: 200 OK but an invalid value in the data (e.g., negative price)
    status, body = get_simulated_response("bad_data_invalid_value")
    process_product_response(status, body)

    # Scenario 4: Non-200 OK response (e.g., 404 Not Found)
    status, body = get_simulated_response("not_found")
    process_product_response(status, body)

    print("\n--- Demonstration Complete ---")
