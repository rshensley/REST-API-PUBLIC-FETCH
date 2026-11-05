# REST API Public Fetch

## Project Overview

This project is a Flask REST API that retrieves vehicle data from the National Highway Traffic Safety Administration (NHTSA) public API.

The application requests JSON data from an external endpoint and filters the results to include only vehicle variables where `GroupName` equals `"Active Safety System"`.

The application is based on the class example, modified to use the NHTSA API and its JSON response structure.

## Technologies Used

- Python - 3.14
- Flask - 3.1.3
- Requests - 2.34.2
- JSON

## Installation and Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

The application runs locally on:

`http://127.0.0.1:5000`

## External API

**Provider:** National Highway Traffic Safety Administration (NHTSA)

**Endpoint:**

https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json

The API returns a JSON object containing vehicle specification variables in a `Results` array.

Each record includes fields:

- `ID` - Vehicle ID
- `Name` - Vehicle name
- `GroupName` - Category
- `DataType` - Data type
- `Description` - Description

## Application Endpoint

| Method | Endpoint | Description |
|---|---|---|
| GET | `/items` | Retrieve vehicle variables filtered by Active Safety System |

### Filtering Logic

The application retrieves the external JSON response and accesses it's `Results` array.

```python
filtered = [
    item for item in data["Results"]
    if item.get("GroupName") == "Active Safety System"
]
```

The filter uses string comparison, excluding records that belong to other categories.

## Testing and Results

### Test 1: GET Request

```bash
curl -i http://127.0.0.1:5000/items
```

**Result: HTTP 200 OK**

The endpoint successfully retrieved and filtered data from external NHTSA API.

A total of **11 matching records** were returned during testing.

Examples include:

| ID | Name |
|---|---|
| 86 | Antilock Braking System (ABS) |
| 99 | Electronic Stability Control (ESC) |
| 100 | Traction Control |
| 168 | Tire Pressure Monitoring System (TPMS) Type |
| 175 | Event Data Recorder (EDR) |
| 181 | SAE Automation Level From |
| 182 | SAE Automation Level To |

Each returned record contained `"GroupName": "Active Safety System"`.

### Test 2: JSON Formatting

```bash
curl -s http://127.0.0.1:5000/items | python -m json.tool
```

**Result:** The response was parsed and displayed as formatted JSON.

### Test 3: Filter Validation

The following test shows that the returned JSON array is not empty and that every record matches the required category.

```bash
curl -s http://127.0.0.1:5000/items | python -c '
import json
import sys

records = json.load(sys.stdin)

assert records, "No records returned"
assert all(
    r.get("GroupName") == "Active Safety System"
    for r in records
), "Unexpected GroupName found"

print(f"All {len(records)} records match the required filter.")
'
```

**Actual output:**

```text
All 11 records match the required filter.
```

### Test 4: External API Error Handling

The external API URL was modified to an invalid endpoint:

```text
https://vpic.nhtsa.dot.gov/api/vehicles/ThisEndPointDoesNotExist
```

The application was tested using:

```bash
curl -i http://127.0.0.1:5000/items
```

**Result: HTTP 502 Bad Gateway**

```json
{
  "detail": "404 Client Error: Not Found for url: https://vpic.nhtsa.dot.gov/api/vehicles/ThisEndPointDoesNotExist",
  "error": "External API returned an HTTP error"
}
```

This shows that the application handled an HTTP error and returned appropriate JSON error response.

## Error Handling

The application uses exception handling to manage external API failures:

- **HTTP 502:** External HTTP errors or invalid JSON response data.
- **HTTP 503:** Network-related failures, including connection errors and timeouts.

## Reflection

This assignment is an example of how a Flask application can pull structured data from a public API and filter it through a local endpoint. I modified the example to use the NHTSA Vehicle Variable List API. Unlike the original example, its response is a JSON object containing a `Results` array, so I had to access the array before filtering records by `GroupName`.

Testing with `curl` shows successful HTTP 200 response and 11 matching records. I also used a Python assertion to verify that every returned record contained the required `GroupName` value.

To test error handling, I used an invalid NHTSA endpoint. The application detected the HTTP 404 error and returned a JSON error response with HTTP 502.

This assignment demonstrated an external API's response structure, applying filtering to the result, and handling failures when accessing external services.
