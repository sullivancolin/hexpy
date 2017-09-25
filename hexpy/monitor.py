import requests
from response import handle_response
from ratelimiter import RateLimiter
from timestamp import Timestamp

ONE_MINUTE = 60


class MonitorAPI(object):
    """docstring for MonitorAPI"""

    def __init__(self, authorization):
        super(MonitorAPI, self).__init__()
        self.authorization = authorization

    TEMPLATE = "https://api.crimsonhexagon.com/api/monitor/"

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def word_cloud(self, monitor_id, start, end, filter=None):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "wordcloud?auth={token}&id={monitor_id}&start={start}&end={end}&filter={filter}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start.to_string(),
                    end=end.to_string(),
                    filter=filter)))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def details(self, monitor_id):
        return handle_response(
            requests.get(
                self.TEMPLATE + "detail?auth={token}&id={monitor_id}".format(
                    token=self.authorization.token, monitor_id=monitor_id)))

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
                }),
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
                "interestaffinities?auth={token}&id={monitor_id}&start={start}&end={end}&daily={daily}&documentSource={document_source}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start.to_string(),
                    end=end.to_string()),
                daily=str(daily).lower(),
                document_source=document_source))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def top_sources(self, monitor_id, start, end):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "sources?auth={token}&id={monitor_id}&start={start}&end={end}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start.to_string(),
                    end=end.to_string())))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def image_analysis(self, monitor_id, start, end, type=None, top=None):
        return handle_response(
            requests.get(
                self.TEMPLATE +
                "imageresults?auth={token}&id={monitor_id}&start={start}&end={end}&type={type}&top={top}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start.to_string(),
                    end=end.to_string(),
                    type=type,
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
                "dayandtime?auth={token}&id={monitor_id}&start={start}&end={end}&aggregatebyday={aggregate_by_day}&uselocaltime={use_local_time}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start.to_string(),
                    end=end.to_string(),
                    aggregate_by_day=str(aggregate_by_day).lower(),
                    use_local_time=str(use_local_time).lower())))

    @RateLimiter(max_calls=120, period=ONE_MINUTE)
    def sentiment_and_categories(self,
                                 monitor_id,
                                 start,
                                 end,
                                 hide_excluded=False):
        requests.get(
            self.TEMPLATE +
            "results?auth={token}&id={monitor_id}&start={start}&end={end}&hideExcluded={hide_excluded}".format(
                token=self.authorization.token,
                monitor_id=monitor_id,
                start=start.to_string(),
                end=end.to_string(),
                hide_excluded=str(hide_excluded).lower()))

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
                "posts?auth={token}&id={monitor_id}&start={start}&end={end}&filter={filter}&extendLimit={extend_limit}&fullContents={full_contents}&geotagged={geotagged}".format(
                    token=self.authorization.token,
                    monitor_id=monitor_id,
                    start=start.to_string(),
                    end=end.to_string(),
                    filter=filter,
                    extend_limit=str(extend_limit).lower(),
                    full_contents=str(full_contents).lower(),
                    geotagged=str(geotagged).lower())))


if __name__ == '__main__':
    from auth import CrimsonAuthorization

    auth = CrimsonAuthorization()

    client = MonitorAPI(auth)
    results = client.details(3770323157)
    start = Timestamp.from_string(results["resultsStart"])
    end = Timestamp.from_string(results["resultsEnd"])

    cloud = client.posts(3770323157, start, end, extend_limit=False)

    import json

    print(json.dumps(cloud, indent=4))
