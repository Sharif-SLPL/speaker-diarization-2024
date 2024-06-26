
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


def _parse_rttm_line(line):
    line = line.decode('utf-8').strip()
    fields = line.split()
    if len(fields) < 9:
        raise IOError('Number of fields < 9. LINE: "%s"' % line)
    file_id = fields[1]
    speaker_id = fields[7]

    # Check valid turn onset.
    try:
        onset = float(fields[3])
    except ValueError:
        raise IOError('Turn onset not FLOAT. LINE: "%s"' % line)
    if onset < 0:
        raise IOError('Turn onset < 0 seconds. LINE: "%s"' % line)

    # Check valid turn duration.
    try:
        dur = float(fields[4])
    except ValueError:
        raise IOError('Turn duration not FLOAT. LINE: "%s"' % line)
    if dur <= 0:
        raise IOError('Turn duration <= 0 seconds. LINE: "%s"' % line)
    
    end = onset + dur

    return RTTM(start=onset, end=end, label=speaker_id)


def parse_from_rttm_list(f):
    rttm_list = []
    for line in f:
        if line.startswith(b'SPKR-INFO'):
            continue
        turn = _parse_rttm_line(line)
        rttm_list.append(turn)
    return rttm_list