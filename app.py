from flask import Flask, jsonify
import requests

app = Flask(__name__)

# NHTSA public vehicle variables API
API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json"


@app.route("/items", methods=["GET"])
def get_items():
    """Retrieve vehicle variables filtered by Active Safety System."""

    try:
        # Retrieve data from the external API
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Filter for Active Safety System
        filtered = [
            item
            for item in data["Results"]
            if item.get("GroupName") == "Active Safety System"
        ]

        return jsonify(filtered), 200

    except requests.exceptions.HTTPError as exc:
        return (
            jsonify(
                {"error": "External API returned an HTTP error", "detail": str(exc)}
            ),
            502,
        )

    except requests.exceptions.RequestException as exc:
        return (
            jsonify(
                {"error": "Unable to retrieve external API data", "detail": str(exc)}
            ),
            503,
        )

    except (ValueError, KeyError, TypeError) as exc:
        return (
            jsonify(
                {"error": "Invalid response from external API", "detail": str(exc)}
            ),
            502,
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
