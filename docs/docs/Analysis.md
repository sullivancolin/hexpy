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
analysis_request(data: Dict[str, Any]) -> JSONDict
```
Submit a query task against 24 hours of social data.

#### Arguments
* data: Dictionary, query and filter parameters

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
