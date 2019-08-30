"""Module for monitor results API"""

import inspect
import logging
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

from .base import JSONDict, handle_response, rate_limited
from .models import TrainCollection
from .session import HexpySession

DateOrDates = Union[Tuple[str, str], Sequence[Tuple[str, str]]]
MonitorOrMonitors = Union[Sequence[int], int]
MetricOrMetrics = Union[Sequence[str], str]

logger = logging.getLogger(__name__)


class MonitorAPI:
    """Class for working with Crimson Hexagon Monitor API.

    # Example usage.

    ```python
    >>> from hexpy import HexpySession, MonitorAPI
    >>> session = HexpySession.load_auth_from_file()
    >>> monitor_client = MonitorAPI(session)
    >>> details = monitor_client.details(monitor_id)
    >>> start = details["resultsStart"]
    >>> end = details["resultsEnd"]
    >>> monitor_client.posts(monitor_id, start, end)
    ```
    """

    def __init__(self, session: HexpySession) -> None:
        self.session = session.session
        self.TEMPLATE = session.ROOT + "monitor/"
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name not in [
                "__init__",
                "_aggregate_metrics",
                "_aggregate_dates",
                "aggregate",
            ]:
                setattr(
                    self, name, rate_limited(fn, session.MAX_CALLS, session.ONE_MINUTE)
                )
        self.METRICS: Dict[str, Callable[..., JSONDict]] = {
            "volume": self.volume,
            "word_cloud": self.word_cloud,
            "sentiment_and_categories": self.sentiment_and_categories,
            "top_sources": self.top_sources,
            "interest_affinities": self.interest_affinities,
        }

    def _aggregate_metrics(
        self, monitor_id: int, date: Sequence[str], metrics: MetricOrMetrics
    ) -> JSONDict:
        if isinstance(metrics, list):
            return {
                metric: self.METRICS[metric](monitor_id, date[0], date[1])
                for metric in metrics
            }
        elif metrics in self.METRICS:
            metric: str = str(metrics)
            return {metric: self.METRICS[metric](monitor_id, date[0], date[1])}
        else:
            raise ValueError(f"valid metrics are {self.METRICS.keys()}")

    def _aggregate_dates(
        self, monitor_id: int, dates: DateOrDates, metrics: MetricOrMetrics
    ) -> List[JSONDict]:
        if not (isinstance(dates, list) or isinstance(dates, tuple)):
            raise ValueError(
                "dates must be a start and end pair, or a list of start and end pairs"
            )
        elif isinstance(dates[0], list) or isinstance(dates[0], tuple):
            return [
                {
                    "resultsStart": date[0],
                    "resultsEnd": date[1],
                    "results": self._aggregate_metrics(monitor_id, date, metrics),
                }
                for date in dates
            ]
        else:
            return [
                {
                    "resultsStart": dates[0],
                    "resultsEnd": dates[1],
                    "results": self._aggregate_metrics(monitor_id, dates, metrics),
                }
            ]

    def aggregate(
        self,
        monitor_ids: MonitorOrMonitors,
        dates: DateOrDates,
        metrics: MetricOrMetrics,
    ) -> List[JSONDict]:
        """Return aggregated results for one or monitor ids, for one or more date pairs, for one or more metrics.

        Valid metrics
        * 'volume'
        * 'word_cloud'
        * 'top_sources'
        * 'interest_affinities'
        * 'sentiment_and_categories'

        # Arguments
            monitor_ids: Integer or list of Integers, id(s) of the monitor(s) being requested
            dates: Tuple of Strings or list of Tuples, pair(s) of 'YYYY-MM-DD' date strings
            metrics: String or list of Strings, metric(s) to aggregate upon
        """
        if isinstance(monitor_ids, list):
            return [
                {
                    "monitor_id": monitor_id,
                    "results": self._aggregate_dates(monitor_id, dates, metrics),
                }
                for monitor_id in monitor_ids
            ]

        elif isinstance(monitor_ids, int):
            return [
                {
                    "monitor_id": monitor_ids,
                    "results": self._aggregate_dates(monitor_ids, dates, metrics),
                }
            ]

        else:
            raise ValueError(
                "monitor_ids must be integer or list of integers to aggregate"
            )

    def details(self, monitor_id: int) -> JSONDict:
        """Return detailed metadata about the selected monitor, including category metadata.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "detail", params={"id": monitor_id})
        )

    def audit(self, monitor_id: int) -> JSONDict:
        """Return audit information about the selected monitor, sorted from most to least recent.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
        """
        return handle_response(
            self.session.get(self.TEMPLATE + "audit", params={"id": monitor_id})
        )

    def word_cloud(
        self, monitor_id: int, start: str, end: str, filter_string: Optional[str] = None
    ) -> JSONDict:
        """Return an alphabetized list of the top 300 words in a monitor.

        This data is generated using documents randomly selected from the pool defined by the submitted parameters.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter_string: String, pipe-separated list of field:value pairs used to filter posts
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "wordcloud",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "filter": filter_string,
                },
            )
        )

    def training_posts(
        self, monitor_id: int, category: Optional[int] = None
    ) -> JSONDict:
        """Return a list of the training posts for a given opinion monitor.

        The selected monitor must be an opinion monitor; requests for other monitor types will return an error.
        By default, all training posts for all categories in a monitor will be returned,
        however you may pass a category ID in your request to get training posts from a specific category.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            category: Integer, category id to target training posts from a specific category
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "trainingposts",
                params={"id": monitor_id, "category": category},
            )
        )

    def train_monitor(self, monitor_id: int, items: TrainCollection) -> JSONDict:
        """Upload training documents to monitor programmatically.

        Upload TrainCollection for a single category. Due to the restrictions involved in using this endpoint, unless you have a specific need to train monitors programmatically, training monitors via the user interface in ForSight will normally be the more efficient training option.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            category_id: Integer, the category this content should belong to
            items: validated instance of [TrainCollection](Data_Validation.md#traincollection) model
        """

        if len(items) > 1000:
            logger.info(
                "More than 1000 training items found.  Uploading in batches of 1000."
            )
            return self.batch_train(monitor_id=monitor_id, items=items)

        return handle_response(
            self.session.post(
                self.TEMPLATE + "train",
                params={"id": monitor_id},
                json={
                    "monitorid": monitor_id,
                    "categoryid": items[0].categoryid,
                    "documents": items.dict(),
                },
            )
        )

    def batch_train(self, monitor_id: int, items: TrainCollection) -> JSONDict:
        """Batch upload training documents to monitor programmatically for collection larger than 1000 posts.

        Batch upload TrainCollection of single category. Due to the restrictions involved in using this endpoint, unless you have a specific need to train monitors programmatically, training monitors via the user interface in ForSight will normally be the more efficient training option.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            category_id: Integer, the category this content should belong to
            items: validated instance of [TrainCollection](Data_Validation.md#traincollection) model
        """

        batch_responses = {}
        for batch_num, batch in enumerate(
            [items[i : i + 1000] for i in range(0, len(items), 1000)]
        ):
            response = self.train_monitor(monitor_id=monitor_id, items=batch)
            logger.info(f"Uploaded batch number: {batch_num}")
            batch_responses[f"Batch {batch_num}"] = response
        return batch_responses

    def interest_affinities(
        self,
        monitor_id: int,
        start: str,
        end: str,
        daily: bool = False,
        document_source: Optional[str] = None,
    ) -> JSONDict:
        """Return information about the authors in a monitor and their affinity with a range of pre-defined topics.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            daily: Boolean, if true, results returned from this endpoint will be trended daily instead of aggregated across the selected date range
            document_source: String, document source for affinities. valid params include `TWITTER` or `TUMBLR`
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "interestaffinities",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "daily": daily,
                    "documentSource": document_source,
                },
            )
        )

    def topics(
        self, monitor_id: int, start: str, end: str, filter_string: Optional[str] = None
    ) -> JSONDict:
        """Return the XML data that can be used to generate clustering visualizations using third-party software.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter_string: String, pipe-separated list of field:value pairs used to filter posts
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "topics",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "filter": filter_string,
                },
            )
        )

    def topic_waves(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return the Topic waves information for a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter_string: String, pipe-separated list of field:value pairs used to filter posts
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "topicwaves",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def top_sources(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return volume information related to the sites and content sources (e.g. Twitter, Forums, Blogs, etc.) in a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "sources",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def image_results(
        self,
        monitor_id: int,
        start: str,
        end: str,
        object_type: str = "",
        top: int = 100,
    ) -> JSONDict:
        """Return a breakdown of the top image classes within a provided monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            object_type: String, specifies type of image classes, valid values [object, scene, action, logo]
            top : Integer, if defined, only the selected number of classes will be returned
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "imageresults",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "type": object_type,
                    "top": top,
                },
            )
        )

    def volume(
        self, monitor_id: int, start: str, end: str, group_by: str = "DAILY"
    ) -> JSONDict:
        """Return volume of total posts in a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            group_by: String, specifies how the volume data over the date range will be grouped. [HOURLY, DAILY, WEEKLY, MONTHLY]
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "volume",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "groupBy": group_by,
                },
            )
        )

    def dayandtime(
        self,
        monitor_id: int,
        start: str,
        end: str,
        aggregate_by_day: bool = False,
        use_local_time: bool = False,
    ) -> JSONDict:
        """Return volume information for a monitor aggregated by time of day or day of week.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            aggregate_by_day: Boolean, if True, volume information will be aggregated by day of the week instead of time of day
            use_local_time: if True, volume aggregation will use the time local to the publishing author of a post, instead of converting that time to the timezone of the selected monitor
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "dayandtime",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "aggregatebyday": aggregate_by_day,
                    "uselocaltime": use_local_time,
                },
            )
        )

    def sentiment_and_categories(
        self, monitor_id: int, start: str, end: str, hide_excluded: bool = False
    ) -> JSONDict:
        """Return aggregate volume, sentiment, emotion and opinion category
        analysis for a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            hide_excluded: Boolean, if True, categories set as hidden will not be included in category proportion calculations.
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "results",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "hideExcluded": hide_excluded,
                },
            )
        )

    def posts(
        self,
        monitor_id: int,
        start: str,
        end: str,
        filter_string: Optional[str] = None,
        extend_limit: bool = False,
        full_contents: bool = False,
        geotagged: bool = False,
    ) -> JSONDict:
        """Return post-level information (where available) and associated analysis (sentiment, emotion) for a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter_string: String, pipe-separated list of field:value pairs used to filter posts
            extend_limit: Boolean if True increase limit of returned posts from 500 per call to 10000 per call
            full_contents: Boolean, if True, the contents field will return the original, complete posts contents instead of truncating around search terms
            geo tagged: Boolean, if True, returns only geotagged documents matching the given filter
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "posts",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "filter": filter_string,
                    "extendLimit": extend_limit,
                    "fullContents": full_contents,
                    "geotagged": geotagged,
                },
            )
        )

    ##########################################################################
    # Demographics                                                           #
    # This collection of endpoints provide demographic volume Metrics        #
    #  for users within a given monitor.                                     #
    ##########################################################################

    def age(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return volume metrics for a given monitor split by age bracket.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "demographics/age",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def ethnicity(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return volume metrics for a given monitor split by ethnicity.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "demographics/ethnicity",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def gender(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return volume metrics for a given monitor split by gender.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "demographics/gender",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    ##########################################################################
    # Geography                                                              #
    #                                                                        #
    ##########################################################################

    def cities(self, monitor_id: int, start: str, end: str, country: str) -> JSONDict:
        """Return volume metrics for a given monitor split by city.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            country: String, country code to filter cities

        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "geography/cities",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "country": country,
                },
            )
        )

    def states(self, monitor_id: int, start: str, end: str, country: str) -> JSONDict:
        """Return volume metrics for a given monitor split by state.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            country: String, country code to filter states
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "geography/states",
                params={
                    "id": monitor_id,
                    "start": start,
                    "end": end,
                    "country": country,
                },
            )
        )

    def countries(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return volume metrics for a given monitor split by country.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "geography/countries",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    ##########################################################################
    # Twitter                                                                #
    # This collection of endpoints relate provide metrics specific to        #
    # Twitter from either Social Account or Buzz monitors.                   #
    ##########################################################################

    def twitter_authors(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return information related to the Twitter authors who have posted in a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "authors",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def twitter_metrics(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return information about the top hashtags, mentions, and retweets in a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "twittermetrics",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def twitter_followers(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return the cumulative daily follower count for a targeted Twitter account in a Twitter Social Account Monitor
        as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "twittersocial/followers",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def twitter_sent_posts(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return information about posts sent by the owner of a target Twitter account in a Twitter Social Account Monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "twittersocial/sentposts",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def twitter_engagement(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return information about retweets, replies, and @mentions for a Twitter Social Account monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "twittersocial/totalengagement",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    ##########################################################################
    # Facebook                                                               #
    # This collection of endpoints relate provide metrics specific to        #
    # Facebook from either Social Account or Buzz monitors.                  #
    ##########################################################################

    def facebook_admin_posts(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return those posts made by the administrators/owners of a targeted Facebook page in a
        Facebook Social Account Monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "facebook/adminposts",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def facebook_likes(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return the cumulative daily like count for a targeted Facebook page in a
        Facebook Social Account Monitor as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "facebook/pagelikes",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def facebook_activity(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return information about actions (likes, comments, shares) made by users and admins for a given page.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "facebook/totalactivity",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    ##########################################################################
    # Instagram                                                              #
    # This collection of endpoints relate provide metrics specific           #
    # to Instagram from either Social Account or Buzz monitors.              #
    ##########################################################################

    def instagram_top_hashtags(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return the Top 50 most occurring Hashtags contained within the posts analyzed in a monitor,
        plus all explicitly targeted hashtags in a monitor's query, for which Metrics are being collected
        (i.e. for which the hashtags are being tracked explicitly in ForSight).

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "instagram/hashtags",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def instagram_followers(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return the cumulative daily follower count for a targeted Instagram account in an
        Instagram Social Account Monitor as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "instagram/followers",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def instagram_sent_media(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return media sent by admins in a targeted Instagram account.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "instagram/sentmedia",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )

    def instagram_activity(self, monitor_id: int, start: str, end: str) -> JSONDict:
        """Return information about actions (likes, comments) made by users and admins for a given account.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            self.session.get(
                self.TEMPLATE + "instagram/totalactivity",
                params={"id": monitor_id, "start": start, "end": end},
            )
        )
