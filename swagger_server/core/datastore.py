from redis import Redis


class Datastore(object):
    def __init__(self, **kwargs):
        self._redis = Redis(**kwargs)
