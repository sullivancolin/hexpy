# -*- coding: utf-8 -*-
"""Module for monitor results API"""

import requests
from halo import Halo
from .base import ROOT, response_handler


class MonitorAPI(object):
    """Class for working with Crimson Hexagon Monitor API.

    # Example usage.

    ```python
    >>> from hexpy import HexpyAuthorization, MonitorAPI
    >>> auth = HexpyAuthorization.load_auth_from_file()
    >>> monitor_client = MonitorAPI(auth)
    >>> details = monitor_client.details(monitor_id)
    >>> start = details["resultsStart"]
    >>> end = details["resultsEnd"]
    >>> monitor_client.posts(monitor_id, start, end)
    ```
    """

    TEMPLATE = ROOT + "monitor/"

    def __init__(self, authorization):
        super(MonitorAPI, self).__init__()
        self.authorization = authorization
        self.METRICS = {
            "volume": self.volume,
            "word_cloud": self.word_cloud,
            "sentiment_and_categories": self.sentiment_and_categories,
            "top_sources": self.top_sources,
            "interest_affinities": self.interest_affinities
        }

    def _aggregate_metrics(self, monitor_id, date, metrics):
        if isinstance(metrics, list):
            return {
                metric: self.METRICS[metric](monitor_id, date[0], date[1])
                for metric in metrics
            }
        elif metrics in self.METRICS:
            return {
                metrics: self.METRICS[metrics](monitor_id, date[0], date[1])
            }
        else:
            raise ValueError(
                'valid metrics are {}'.format(self.METRICS.keys()))

    def _aggregate_dates(self, monitor_id, dates, metrics):
        if not (isinstance(dates, list) or isinstance(dates, tuple)):
            raise ValueError(
                "dates must be a start and end pair, or a list of start and end pairs"
            )
        elif isinstance(dates[0], list) or isinstance(dates[0], tuple):
            return [{
                "resultsStart":
                date[0],
                "resultsEnd":
                date[1],
                "results":
                self._aggregate_metrics(monitor_id, date, metrics)
            } for date in dates]
        else:
            return [{
                "resultsStart":
                dates[0],
                "resultsEnd":
                dates[1],
                "results":
                self._aggregate_metrics(monitor_id, dates, metrics)
            }]

    def aggregate(self, monitor_ids, dates, metrics):
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
            return [{
                "monitor_id":
                monitor_id,
                "results":
                self._aggregate_dates(monitor_id, dates, metrics)
            } for monitor_id in monitor_ids]

        elif isinstance(monitor_ids, int):
            return [{
                "monitor_id":
                monitor_ids,
                "results":
                self._aggregate_dates(monitor_ids, dates, metrics)
            }]

        else:
            raise ValueError(
                "monitor_ids must be integer or list of integers to aggregate")

    @response_handler
    def details(self, monitor_id):
        """Return detailed metadata about the selected monitor, including category metadata.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
        """
        return requests.get(
            self.TEMPLATE + "detail",
            params={"auth": self.authorization.token,
                    "id": monitor_id})

    @response_handler
    def audit(self, monitor_id):
        """Return audit information about the selected monitor, sorted from most to least recent.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
        """
        return requests.get(
            self.TEMPLATE + "audit",
            params={"auth": self.authorization.token,
                    "id": monitor_id})

    @response_handler
    def word_cloud(self, monitor_id, start, end, filter_string=None):
        """Return an alphabetized list of the top 300 words in a monitor.

        This data is generated using documents randomly selected from the pool defined by the submitted parameters.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter_string: String, pipe-separated list of field:value pairs used to filter posts
        """
        return requests.get(
            self.TEMPLATE + "wordcloud",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "filter": filter_string
            })

    @response_handler
    def trained_posts(self, monitor_id, category=None):
        """Return a list of the training posts for a given opinion monitor.

        The selected monitor must be an opinion monitor; requests for other monitor types will return an error.
        By default, all training posts for all categories in a monitor will be returned,
        however you may pass a category ID in your request to get training posts from a specific category.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            category: Integer, category id to target training posts from a specific category
        """
        return requests.get(
            self.TEMPLATE + "trainingposts",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "category": category
            })

    @response_handler
    def train_monitor(self, monitor_id, category_id, data):
        """Upload individual training document monitors programmatically.

        You may only upload one document per request. Due to the restrictions involved in using this endpoint,
        unless you have a specific need to train monitors programmatically,
        training monitors via the user interface in ForSight will normally be the more efficient training option.
        [Reference](https://apidocs.crimsonhexagon.com/reference#training-document-upload)

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            category_id: Integer, the category this content should belong to
            data: Dictionary, document item with required fields
        """
        return requests.post(
            self.TEMPLATE + "train",
            json={
                "monitorID": monitor_id,
                "categoryID": category_id,
                "document": data
            },
            params={"auth": self.authorization.token})

    @response_handler
    def interest_affinities(self,
                            monitor_id,
                            start,
                            end,
                            daily=False,
                            document_source=None):
        """Return information about the authors in a monitor and their affinity with a range of pre-defined topics.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            daily: Boolean, if true, results returned from this endpoint will be trended daily instead of aggregated across the selected date range
            document_source: String, document source for affinities. valid params include `TWITTER` or `TUMBLR`
        """
        return requests.get(
            self.TEMPLATE + "interestaffinities",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "daily": daily,
                "documentSource": document_source
            })

    @response_handler
    def top_sources(self, monitor_id, start, end):
        """Return volume information related to the sites and content sources (e.g. Twitter, Forums, Blogs, etc.) in a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "sources",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def image_analysis(self, monitor_id, start, end, object_type="", top=100):
        """Return a breakdown of the top image classes within a provided monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            object_type: String, specifies type of image classes, valid values [object, scene, action, logo]
            top : Integer, if defined, only the selected number of classes will be returned
        """
        return requests.get(
            self.TEMPLATE + "imageresults",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "type": object_type,
                "top": top
            })

    @response_handler
    def volume(self,
               monitor_id,
               start,
               end,
               aggregate_by_day=False,
               use_local_time=False):
        """Return volume metrics for a given monitor split by date.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            aggregate_by_day: Boolean, if True, volume information will be aggregated by day of the week instead of time of day
            use_local_time: if True, volume aggregation will use the time local to the publishing author of a post, instead of converting that time to the timezone of the selected monitor
        """
        return requests.get(
            self.TEMPLATE + "dayandtime",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "aggregatebyday": aggregate_by_day,
                "uselocaltime": use_local_time
            })

    @response_handler
    def sentiment_and_categories(self,
                                 monitor_id,
                                 start,
                                 end,
                                 hide_excluded=False):
        """Return aggregate volume, sentiment, emotion and opinion category
        analysis for a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            hide_excluded: Boolean, if True, categories set as hidden will not be included in category proportion calculations.
        """
        return requests.get(
            self.TEMPLATE + "results",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "hideExcluded": hide_excluded
            })

    @response_handler
    def posts(self,
              monitor_id,
              start,
              end,
              filter_string=None,
              extend_limit=False,
              full_contents=False,
              geotagged=False):
        """Return post-level information (where available)
        and associated analysis (sentiment, emotion) for a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter_string: String, pipe-separated list of field:value pairs used to filter posts
            extend_limit: Boolean if True increase limit of returned posts from 500 per call to 10000 per call
            full_contents: Boolean, if True, the contents field will return the original, complete posts contents instead of truncating around search terms
            geotagged: Boolean, if True, returns only geotagged documents matching the given filter
        """
        return requests.get(
            self.TEMPLATE + "posts",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "filter": filter_string,
                "extendLimit": extend_limit,
                "fullContents": full_contents,
                "geotagged": geotagged
            })

    #################################################################################
    # Demographics                                                                  #
    # This collection of endpoints provide demographic volume metrics for users     #
    # within a given monitor.                                                       #
    #################################################################################

    @response_handler
    def age(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by age bracket.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "demographics/age",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def ethnicity(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by ethnicity.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "demographics/ethnicity",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def gender(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by gender.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "demographics/gender",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    #################################################################################
    # Geography                                                                     #
    #                                                                               #
    #################################################################################

    @response_handler
    def cities(self, monitor_id, start, end, country):
        """Return volume metrics for a given monitor split by city.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            country: String, country code to filter cities

        """
        return requests.get(
            self.TEMPLATE + "geography/cities",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "country": country
            })

    @response_handler
    def states(self, monitor_id, start, end, country):
        """Return volume metrics for a given monitor split by state.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            country: String, country code to filter states
        """
        return requests.get(
            self.TEMPLATE + "geography/states",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end,
                "country": country
            })

    @response_handler
    def countries(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by country.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "geography/countries",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    #################################################################################
    # Twitter                                                                       #
    # This collection of endpoints relate provide metrics specific to Twitter from  #
    # either Social Account or Buzz monitors.                                       #
    #################################################################################

    @response_handler
    def twitter_authors(self, monitor_id, start, end):
        """Return information related to the Twitter authors who have posted in a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "authors",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def twitter_metrics(self, monitor_id, start, end):
        """Return information about the top hashtags, mentions, and retweets in a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "twittermetrics",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def twitter_followers(self, monitor_id, start, end):
        """Return the cumulative daily follower count for a targeted Twitter account in a Twitter Social Account Monitor
        as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "twittersocial/followers",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def twitter_sent_posts(self, monitor_id, start, end):
        """Return information about posts sent by the owner of a target Twitter account in a Twitter Social Account Monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "twittersocial/sentposts",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def twitter_engagement(self, monitor_id, start, end):
        """Return information about retweets, replies, and @mentions for a Twitter Social Account monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "twittersocial/totalengagement",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    #################################################################################
    # Facebook                                                                      #
    # This collection of endpoints relate provide metrics specific to Facebook from #
    # either Social Account or Buzz monitors.                                       #
    #################################################################################

    @response_handler
    def facebook_admin_posts(self, monitor_id, start, end):
        """Return those posts made by the administrators/owners of a targeted Facebook page in a
        Facebook Social Account Monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "facebook/adminposts",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def facebook_likes(self, monitor_id, start, end):
        """Return the cumulative daily like count for a targeted Facebook page in a
        Facebook Social Account Monitor as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "facebook/pagelikes",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def facebook_activity(self, monitor_id, start, end):
        """Return information about actions (likes, comments, shares) made by users and admins for a given page.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "facebook/totalactivity",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    #################################################################################
    # Instagram                                                                     #
    # This collection of endpoints relate provide metrics specific to Instagram     #
    # from either Social Account or Buzz monitors.                                  #
    #################################################################################

    @response_handler
    def instagram_top_hashtags(self, monitor_id, start, end):
        """Return the Top 50 most occurring Hashtags contained within the posts analyzed in a monitor,
        plus all explicitly targeted hashtags in a monitor's query, for which Metrics are being collected
        (i.e. for which the hashtags are being tracked explicitly in ForSight).

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "instagram/hashtags",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def instagram_followers(self, monitor_id, start, end):
        """Return the cumulative daily follower count for a targeted Instagram account in an
        Instagram Social Account Monitor as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "instagram/followers",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def instagram_sent_media(self, monitor_id, start, end):
        """Return media sent by admins in a targeted Instagram account.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "instagram/sentmedia",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })

    @response_handler
    def instagram_activity(self, monitor_id, start, end):
        """Return information about actions (likes, comments) made by users and admins for a given account.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return requests.get(
            self.TEMPLATE + "instagram/totalactivity",
            params={
                "auth": self.authorization.token,
                "id": monitor_id,
                "start": start,
                "end": end
            })
