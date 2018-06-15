Monitor API
===========

## Class for working with Crimson Hexagon Monitor API.

## Example usage.

```python
>>> from hexpy import HexpySession, MonitorAPI
>>> session = HexpySession.load_auth_from_file()
>>> monitor_client = MonitorAPI(session)
>>> details = monitor_client.details(monitor_id)
>>> start = details["resultsStart"]
>>> end = details["resultsEnd"]
>>> monitor_client.posts(monitor_id, start, end)
>>> session.close()
```

## Methods

### details

```python
details(monitor_id: int) -> Dict[str, Any]
```

Return detailed metadata about the selected monitor, including category metadata.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested

### audit
```python
audit(monitor_id: int) -> Dict[str, Any]
```

Return audit information about the selected monitor, sorted from most to least recent.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested

### word_cloud
```python
word_cloud(monitor_id: int, start: str, end: str, filter_string: str = None) -> Dict[str, Any]
```

Return an alphabetized list of the top 300 words in a monitor. This data is generated using documents randomly selected from the pool defined by the submitted parameters.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* filter_string: String, pipe-separated list of field:value pairs used to filter posts


### training_posts
```python
training_posts(monitor_id: int, category: int = None) -> Dict[str, Any]
```

Return a list of the training posts for a given opinion monitor. The selected monitor must be an opinion monitor; requests for other monitor types will return an error. By default, all training posts for all categories in a monitor will be returned, however you may pass a category ID in your request to get training posts from a specific category.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* category: Integer, category id to target training posts from a specific category

### train_monitor
```python
train_monitor(monitor_id: int, category_id: int, data: List[Dict[str, Any]]) -> Dict[str, Any]
```

Upload individual training document monitors programmatically.

Upload a list documents of one category per request. Due to the restrictions involved in using this endpoint, unless you have a specific need to train monitors programmatically, training monitors via the user interface in ForSight will normally be the more efficient training option. [Reference](https://apidocs.crimsonhexagon.com/reference#training-document-upload)

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* category_id: Integer, the category this content should belong to
* data: List of document dictionaries with required fields

### interest_affinities
```python
interest_affinities(monitor_id: int, start: str, end: str, daily: bool = False, document_source: str = None) -> Dict[str, Any]
```

Return information about the authors in a monitor and their affinity with a range of pre-defined topics.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* daily: Boolean, if true, results returned from this endpoint will be trended daily instead of aggregated across the selected date range
* document_source: String, document source for affinities. valid params include `TWITTER` or `TUMBLR`

### top_sources
```python
top_sources(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```

Return volume information related to the sites and content sources (e.g. Twitter, Forums, Blogs, etc.) in a monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### image_results
```python
image_results(monitor_id: int, start: str, end: str, object_type: str = "", top: int = 100) -> Dict[str, Any]
```

Return a breakdown of the top image classes within a provided monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* object_type: String, specifies type of image classes, valid values [object, scene, action, logo]
* top : Integer, if defined, only the selected number of classes will be returned

### volume
```python
volume(monitor_id: int, start: str, end: str, group_by: str = "DAILY") -> Dict[str, Any]
```

Return volume of total posts in a monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* group_by: String, specifies how the volume data over the date range will be grouped. [HOURLY, DAILY, WEEKLY, MONTHLY]

### dayandtime
```python
dayandtime(monitor_id: int, start: str, end: str, aggregate_by_day: bool = False, use_local_time: bool = False) -> Dict[str, Any]
```

Return volume metrics for a given monitor split by date.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* aggregate_by_day: Boolean, if True, volume information will be aggregated by day of the week instead of time of day
* use_local_time: if True, volume aggregation will use the time local to the publishing author of a post, instead of converting that time to the timezone of the selected monitor

### sentiment_and_categories
```python
sentiment_and_categories(monitor_id: int, start: str, end: str, hide_excluded: bool = False) -> Dict[str, Any]
```

Return aggregate volume, sentiment, emotion and opinion category analysis for a given monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* hide_excluded: Boolean, if True, categories set as hidden will not be included in category proportion calculations.


### aggregate
```python
aggregate(monitor_ids: Union[Sequence[int], int], dates: Union[Sequence[str], Sequence[Sequence[str]]], metrics: Union[Sequence[str], str]) -> Sequence[Dict[str, Any]]
```
Return aggregated results for one or monitor ids, for one or more date pairs, for one or more metrics.

#### Valid metrics
* 'volume'
* 'word_cloud'
* 'top_sources'
* 'interest_affinities'
* 'sentiment_and_categories'

#### Arguments
* monitor_ids: Integer or list of Integers, id(s) of the monitor(s) being requested
* dates: Tuple of Strings or list of Tuples, pair(s) of 'YYYY-MM-DD' date strings
* metrics: String or list of Strings, metric(s) to aggregate upon


### posts
```python
posts(monitor_id: int, start: str, end: str, filter_string: str = None, extend_limit: bool = False, full_contents: bool = False, geotagged: bool = False) -> Dict[str, Any]
```

Return post-level information (where available) and associated analysis (sentiment, emotion) for a given monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* filter_string: String, pipe-separated list of field:value pairs used to filter posts
* extend_limit: Boolean if True increase limit of returned posts from 500 per call to 10000 per call
* full_contents: Boolean, if True, the contents field will return the original, complete posts contents instead of truncating around search terms
* geotagged: Boolean, if True, returns only geotagged documents matching the given filter

Demographics
-------------
This collection of endpoints provide demographic volume metrics for users within a given monitor.

### age
```python
age(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return volume metrics for a given monitor split by age bracket.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD


### ethnicity
```python
ethnicity(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return volume metrics for a given monitor split by ethnicity.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### gender
```python
gender(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return volume metrics for a given monitor split by gender.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

Geography
---------

### cities
```python
cities(monitor_id: int, start: str, end: str, country: str) -> Dict[str, Any]
```
Return volume metrics for a given monitor split by city.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* country: String, country code to filter cities

### states
```python
states(monitor_id: int, start: str, end: str, country: str) -> Dict[str, Any]
```
Return volume metrics for a given monitor split by state.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD
* country: String, country code to filter states

### countries
```python
countries(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```

Return volume metrics for a given monitor split by country.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

Twitter
------------

This collection of endpoints relate provide metrics specific to Twitter from either Social Account or Buzz monitors. 

### twitter_authors
```python
twitter_authors(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return information related to the Twitter authors who have posted in a given monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### twitter_metrics
```python
twitter_metrics(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return information about the top hashtags, mentions, and retweets in a monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### twitter_followers
```python
twitter_followers(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return the cumulative daily follower count for a targeted Twitter account in a Twitter Social Account Monitor as of the selected dates.
#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### twitter_sent_posts
```python
twitter_sent_posts(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return information about posts sent by the owner of a target Twitter account in a Twitter Social Account Monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### twitter_engagement
```python
twitter_engagement(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return information about retweets, replies, and @mentions for a Twitter Social Account monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

Facebook
------------

### facebook_admin_posts
```python
facebook_admin_posts(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return those posts made by the administrators/owners of a targeted Facebook page in a Facebook Social Account Monitor.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### facebook_likes
```python
facebook_likes(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return the cumulative daily like count for a targeted Facebook page in a Facebook Social Account Monitor as of the selected dates.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### facebook_activity
```python
facebook_activity(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return information about actions (likes, comments, shares) made by users and admins for a given page.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

Instagram
-------------

### instagram_top_hashtags
```python
instagram_top_hashtags(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return the Top 50 most occurring Hashtags contained within the posts analyzed in a monitor, plus all explicitly targeted hashtags in a monitor's query, for which Metrics are being collected (i.e. for which the hashtags are being tracked explicitly in ForSight).

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### instagram_followers
```python
instagram_followers(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return the cumulative daily follower count for a targeted Instagram account in an Instagram Social Account Monitor as of the selected dates.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### instagram_sent_media
```python
instagram_sent_media(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return media sent by admins in a targeted Instagram account.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

### instagram_activity
```python
instagram_activity(monitor_id: int, start: str, end: str) -> Dict[str, Any]
```
Return information about actions (likes, comments) made by users and admins for a given account.

#### Arguments
* monitor_id: Integer, id of the monitor or monitor filter being requested
* start: String, inclusive start date in YYYY-MM-DD
* end: String, exclusive end date in YYYY-MM-DD

