
import json


class RTTM:
    def __init__(self, start, end, label, **args):
        self.start = start
        self.end = end
        self.label = label


def parse_to_rttm_list(items):
    # items = json.load(text)
    rttm_list = []
    for item in items:
        rttm_list.append(RTTM(**item))
    return rttm_list