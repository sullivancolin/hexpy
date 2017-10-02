# Analysis API

## Class for working with Crimson Hexagon Analysis API.

## Example Usage

```python
>>> from hexpy import CrimsonAuthorization, AnalysisAPI
>>> auth = CrimsonAuthorization.load_auth_from_file()
>>> analysis_client = AnalysisAPI(auth)
>>> analysis_client.results(request_id)
```

## Methods

### anaysis_requests
```python
analysis_request(data)
```
Submit a query task against 24 hours of social data.

#### Arguments
* data: Dictionary, query and filter parameters

### results
```python
results(request_id)
```
Retrieve the status of the analysis request and the results.

#### Arguments
* request_id: Integer, the identifier given for the analysis, generated via the Analysis Request endpoints
