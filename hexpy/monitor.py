# -*- coding: utf-8 -*-
"""Module for monitor results API"""

import requests
from .response import handle_response
from ratelimiter import RateLimiter
from .base import ROOT, ONE_MINUTE, MAX_CALLS, sleep_message


class MonitorAPI(object):
    """Class for working with Crimson Hexagon Monitor API.

    # Example usage.

    ```python
    >>> from hexpy import CrimsonAuthorization, MonitorAPI
    >>> auth = CrimsonAuthorization.load_auth_from_file()
    >>> monitor_client = MonitorAPI(auth)
    >>> details = monitor_client.details(monitor_id)
    >>> start = details["resultsStart"]
    >>> end = details["resultsEnd"]
    >>> monitor_client.posts(monitor_id, start, end)
    {
      "posts": [
        {
          "url": "http://twitter.com/username/status/status_id",
          "date": "2016-05-28T00:00:00",
    ...
    ```
    """

    TEMPLATE = ROOT + "monitor/"

    def __init__(self, authorization):
        super(MonitorAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def details(self, monitor_id):
        """Return detailed metadata about the selected monitor, including category metadata.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
        """
        return handle_response(
            requests.get(
                self.TEMPLATE + "detail?auth={token}&id={monitor_id}".format(
                    token=self.authorization.token, monitor_id=monitor_id)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def audit(self, monitor_id):
        """Return audit information about the selected monitor, sorted from most to least recent.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
        """
        return handle_response(
            requests.get(
                self.TEMPLATE + "audit?auth={token}&id={monitor_id}".format(
                    token=self.authorization.token, monitor_id=monitor_id)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def word_cloud(self, monitor_id, start, end, filter=None):
        """Return an alphabetized list of the top 300 words in a monitor.

        This data is generated using documents randomly selected from the pool defined by the submitted parameters.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter: String, pipe-separated list of field:value pairs used to filter posts
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "wordcloud?auth={token}&id={monitor_id}&start={start}&end={end}&filter={filter}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    filter=filter)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def trained_posts(self, monitor_id, category=None):
        """Return a list of the training posts for a given opinion monitor.

        The selected monitor must be an opinion monitor; requests for other monitor types will return an error.
        By default, all training posts for all categories in a monitor will be returned,
        however you may pass a category ID in your request to get training posts from a specific category.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            category: Integer, category id to target training posts from a specific category
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "trainingposts?auth={token}&id={monitor_id}&category={category}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    category=category)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
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
        return handle_response(
            requests.post(
                self.TEMPLATE + "train",
                json={
                    "monitorID": monitor_id,
                    "categoryID": category_id,
                    "document": data
                },
                params={"auth": self.authorization.token}),
            check_text=True)

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
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
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "interestaffinities?auth={token}&id={monitor_id}&start={start}&end={end}&daily={daily}\
                &documentSource={document_source}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    daily=str(daily).lower(),
                    document_source=document_source)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def top_sources(self, monitor_id, start, end):
        """Return volume information related to the sites and content sources (e.g. Twitter, Forums, Blogs, etc.) in a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "sources?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def image_analysis(self, monitor_id, start, end, object_type="", top=100):
        """Return a breakdown of the top image classes within a provided monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            object_type: String, specifies type of image classes, valid values [object, scene, action, logo]
            top : Integer, if defined, only the selected number of classes will be returned
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "imageresults?auth={token}&id={monitor_id}&start={start}&end={end}&type={type}&top={top}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    type=object_type,
                    top=top)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
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
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "dayandtime?auth={token}&id={monitor_id}&start={start}&end={end}&aggregatebyday={aggregate_by_day}\
                &uselocaltime={use_local_time}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    aggregate_by_day=str(aggregate_by_day).lower(),
                    use_local_time=str(use_local_time).lower())))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
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
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "results?auth={token}&id={monitor_id}&start={start}&end={end}&hideExcluded={hide_excluded}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    hide_excluded=str(hide_excluded).lower())))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def posts(self,
              monitor_id,
              start,
              end,
              filter=None,
              extend_limit=False,
              full_contents=False,
              geotagged=False):
        """Return post-level information (where available)
        and associated analysis (sentiment, emotion) for a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            filter: String, pipe-separated list of field:value pairs used to filter posts
            extend_limit: Boolean if True increase limit of returned posts from 500 per call to 10000 per call
            full_contents: Boolean, if True, the contents field will return the original, complete posts contents instead of truncating around search terms
            geotagged: Boolean, if True, returns only geotagged documents matching the given filter
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "posts?auth={token}&id={monitor_id}&start={start}&end={end}&filter={filter}&extendLimit={extend_limit}\
                &fullContents={full_contents}&geotagged={geotagged}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    filter=filter,
                    extend_limit=str(extend_limit).lower(),
                    full_contents=str(full_contents).lower(),
                    geotagged=str(geotagged).lower())))

    #################################################################################
    # Demographics                                                                  #
    # This collection of endpoints provide demographic volume metrics for users     #
    # within a given monitor.                                                       #
    #################################################################################

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def age(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by age bracket.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "demographics/age?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def ethnicity(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by ethnicity.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "demographics/ethnicity?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def gender(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by gender.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "demographics/gender?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    #################################################################################
    # Geography                                                                     #
    #                                                                               #
    #################################################################################

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def cities(self, monitor_id, start, end, country):
        """Return volume metrics for a given monitor split by city.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            country: String, country code to filter cities

        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "geography/cities?auth={token}&id={monitor_id}&start={start}&end={end}&country={country}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    country=country)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def states(self, monitor_id, start, end, country):
        """Return volume metrics for a given monitor split by state.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
            country: String, country code to filter states
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "geography/states?auth={token}&id={monitor_id}&start={start}&end={end}&country={country}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    country=country)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def countries(self, monitor_id, start, end):
        """Return volume metrics for a given monitor split by country.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "geography/countries?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    #################################################################################
    # Twitter                                                                       #
    # This collection of endpoints relate provide metrics specific to Twitter from  #
    # either Social Account or Buzz monitors.                                       #
    #################################################################################

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def twitter_authors(self, monitor_id, start, end):
        """Return information related to the Twitter authors who have posted in a given monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "authors?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def twitter_metrics(self, monitor_id, start, end):
        """Return information about the top hashtags, mentions, and retweets in a monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "twittermetrics?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def twitter_followers(self, monitor_id, start, end):
        """Return the cumulative daily follower count for a targeted Twitter account in a Twitter Social Account Monitor
        as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "twittersocial/followers?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def twitter_sent_posts(self, monitor_id, start, end):
        """Return information about posts sent by the owner of a target Twitter account in a Twitter Social Account Monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "twittersocial/sentposts?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def twitter_engagement(self, monitor_id, start, end):
        """Return information about retweets, replies, and @mentions for a Twitter Social Account monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "twittersocial/totalengagement?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    #################################################################################
    # Facebook                                                                      #
    # This collection of endpoints relate provide metrics specific to Facebook from #
    # either Social Account or Buzz monitors.                                       #
    #################################################################################

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def facebook_admin_posts(self, monitor_id, start, end):
        """Return those posts made by the administrators/owners of a targeted Facebook page in a
        Facebook Social Account Monitor.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "facebook/adminposts?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def facebook_likes(self, monitor_id, start, end):
        """Return the cumulative daily like count for a targeted Facebook page in a
        Facebook Social Account Monitor as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "facebook/pagelikes?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def facebook_activity(self, monitor_id, start, end):
        """Return information about actions (likes, comments, shares) made by users and admins for a given page.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "facebook/totalactivity?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    #################################################################################
    # Instagram                                                                     #
    # This collection of endpoints relate provide metrics specific to Instagram     #
    # from either Social Account or Buzz monitors.                                  #
    #################################################################################

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def instagram_top_hashtags(self, monitor_id, start, end):
        """Return the Top 50 most occurring Hashtags contained within the posts analyzed in a monitor,
        plus all explicitly targeted hashtags in a monitor's query, for which Metrics are being collected
        (i.e. for which the hashtags are being tracked explicitly in ForSight).

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/hashtags?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def instagram_followers(self, monitor_id, start, end):
        """Return the cumulative daily follower count for a targeted Instagram account in an
        Instagram Social Account Monitor as of the selected dates.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/followers?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def instagram_sent_media(self, monitor_id, start, end):
        """Return media sent by admins in a targeted Instagram account.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/sentmedia?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(
        max_calls=MAX_CALLS, period=ONE_MINUTE, callback=sleep_message)
    def instagram_activity(self, monitor_id, start, end):
        """Return information about actions (likes, comments) made by users and admins for a given account.

        # Arguments
            monitor_id: Integer, id of the monitor or monitor filter being requested
            start: String, inclusive start date in YYYY-MM-DD
            end: String, exclusive end date in YYYY-MM-DD
        """
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/totalactivity?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))
