path: blob/master/src/hexpy
source: analysis.py

# Analysis API

Class for working with Crimson Hexagon Analysis API.

## Example Usage
<div class="termy">

```python
>>> from hexpy import HexpySession, AnalysisAPI
>>> session = HexpySession.load_auth_from_file()
>>> analysis_client = AnalysisAPI(session)
>>> analysis_client.results(request_id)
```
</div>

## Methods

### analysis_request
```python
analysis_request(request: AnaysisRequest) -> JSONDict
```
Submit a query task against 24 hours of social data.

#### Arguments
* request: validated [AnalysisRequest](Data_Validation.md#analysisrequest).

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
