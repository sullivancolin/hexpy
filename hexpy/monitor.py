# -*- coding: utf-8 -*-
"""Module for Monitor results API"""

import requests
from .response import handle_response
from ratelimiter import RateLimiter

ONE_MINUTE = 60


class MonitorAPI(object):
    """docstring for MonitorAPI"""

    TEMPLATE = "https://api.crimsonhexagon.com/api/monitor/"

    def __init__(self, authorization):
        super(MonitorAPI, self).__init__()
        self.authorization = authorization

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def details(self, monitor_id):
        return handle_response(
            requests.get(
                self.TEMPLATE + "detail?auth={token}&id={monitor_id}".format(
                    token=self.authorization.token, monitor_id=monitor_id)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def audit(self, monitor_id):
        return handle_response(
            requests.get(
                self.TEMPLATE + "audit?auth={token}&id={monitor_id}".format(
                    token=self.authorization.token, monitor_id=monitor_id)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def word_cloud(self, monitor_id, start, end, filter=None):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "wordcloud?auth={token}&id={monitor_id}&start={start}&end={end}&filter={filter}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    filter=filter)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def trained_posts(self, monitor_id, category=None):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "trainingposts?auth={token}&id={monitor_id}&category={category}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    category=category)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def train_monitor(self, monitor_id, category_id, data):
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

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def interest_affinities(self,
                            monitor_id,
                            start,
                            end,
                            daily=False,
                            document_source=None):
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

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def top_sources(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "sources?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def image_analysis(self,
                       monitor_id,
                       start,
                       end,
                       object_type="object",
                       top=100):
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

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def volume(self,
               monitor_id,
               start,
               end,
               aggregate_by_day=False,
               use_local_time=False):
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

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def sentiment_and_categories(self,
                                 monitor_id,
                                 start,
                                 end,
                                 hide_excluded=False):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "results?auth={token}&id={monitor_id}&start={start}&end={end}&hideExcluded={hide_excluded}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    hide_excluded=str(hide_excluded).lower())))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def posts(self,
              monitor_id,
              start,
              end,
              filter=None,
              extend_limit=False,
              full_contents=True,
              geotagged=True):
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
    #################################################################################

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def age(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "demographics/age?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def ethnicity(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "demographics/ethnicity?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def gender(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "demographics/gender?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    #################################################################################
    # Geography                                                                  #
    #################################################################################

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def cities(self, monitor_id, start, end, country):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "geography/cities?auth={token}&id={monitor_id}&start={start}&end={end}&country={country}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    country=country)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def states(self, monitor_id, start, end, country):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "geography/states?auth={token}&id={monitor_id}&start={start}&end={end}&country={country}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end,
                    country=country)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def countries(self, monitor_id, start, end):
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
    #################################################################################

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def twitter_authors(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "authors?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def twitter_metrics(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "twittermetrics?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def twitter_followers(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "twittersocial/followers?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def twitter_sent_posts(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "twittersocial/sentposts?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def twitter_engagement(self, monitor_id, start, end):
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
    #################################################################################

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def facebook_admin_posts(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "facebook/adminposts?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def facebook_likes(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "facebook/pagelikes?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def facebook_activity(self, monitor_id, start, end):
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
    #################################################################################

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def instagram_top_hashtags(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/hashtags?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def instagram_followers(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/followers?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def instagram_sent_media(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/sentmedia?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def instagram_activity(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "instagram/totalactivity?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start,
                    end=end)))