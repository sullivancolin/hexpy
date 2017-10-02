# Timestamp 

## Class for working with dates and times.

## Example Usage

```python
>>> from hexpy import Timestamp
>>> stamp = Timestamp(2017, 9, 26)
>>> stamp.to_string()
'2017-09-29T00:00:00'
```
## Methods

### to_string
```python
to_string()
```
Convert timestamp object to ISO format string.

### from_string
```python
from_string(timestamp)
```
Instantiate Timestamp object from ISO format String.

#### Arguments
* timestamp: String, isoformatted timestamp

