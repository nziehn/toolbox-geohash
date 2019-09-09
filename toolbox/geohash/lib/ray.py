class Ray(object):
    def __init__(self, start, end):
        self.__start = start
        self.__end = end

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def m(self):
        return self.__end - self.__start

    @property
    def b(self):
        return self.__start

    def __repr__(self):
        return 'Ray(start={}, end={})'.format(self.__start, self.__end)