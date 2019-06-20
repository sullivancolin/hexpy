path: blob/master/src/hexpy
source: analysis.py

# Analysis API

Class for working with Crimson Hexagon Analysis API.

## Example Usage

```python
>>> from hexpy import HexpySession, AnalysisAPI
>>> session = HexpySession.load_auth_from_file()
>>> analysis_client = AnalysisAPI(session)
>>> analysis_client.results(request_id)
```

## Methods

### analysis_request
```python
analysis_request(request: JSONDict) -> JSONDict
```
Submit a query task against 24 hours of social data.

#### Arguments
* request: Dictionary, query and filter parameters

Example Request
```python
{
    "analysis": [
        "volume",
        "sentiment",
        "emotion",
        "affinity",
        "gender",
        "age",
        "location",
        "source",
        "reach"
    ],
    "keywords": "iPhone",
    "languages": {
        "type": "include",
        "values": [
        "EN"
        ]
    },
    "gender": {
            "type": "include",
            "values": ["M"]
    },
    "locations": {
        "type": "exclude",
        "values": [
            "JPN"
        ]
    },
    "sources": [
        "TWITTER",
        "TUMBLR",
        "INSTAGRAM",
        "BLOGS",
        "REVIEWS",
        "GOOGLE_PLUS",
        "NEWS",
        "YOUTUBE",
        "FORUMS"
    ],
    "startDate": "2016-09-20T00:00:00",
    "endDate": "2016-09-21T00:00:00",
    "timezone": "America/New_York",
    "requestUsage": true
}
```

### results
```python
results(request_id: int) -> JSONDict
```
Retrieve the status of the analysis request and the results.

#### Arguments
* request_id: Integer, the identifier given for the analysis, generated via the Analysis Request endpoints


### image_analysis
```python
image_analysis(url: str) -> JSONDict
```
Get object, scene, activity predictions for image from public url.

#### Arguments
* url: String, the url of the image to analyze
