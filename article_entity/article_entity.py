# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from collections import defaultdict
import re

if sys.version_info.major < 3:
    string_type = (str, unicode)
    def _force_text(string):
        if not isinstance(string, string_type):
            return unicode(string)
        if not isinstance(string, unicode):
            return string.decode('utf-8')
        return string
else:
    string_type = (str, bytes)
    def _force_text(string):
        if not isinstance(string, string_type):
            return str(string)
        if not isinstance(string, str):
            return string.decode('utf-8')
        return string

alpha_pattern = re.compile(r'^[a-zA-Z]+$')


def article_entity(title, content, min_word_len=2, max_word_len=10, max_count=1):
    """
    :param min_word_len: minimal entity length
    :param max_word_len: maximal entity length
    :param max_count: how many entities should we return
    """
    title = _force_text(title.strip())
    content = _force_text(content.strip())
    title_length = len(title)
    start = 0
    counter = defaultdict(int)
    while True:
        if start >= title_length:
            break

        for end in range(start+1, title_length+1):
            sub_title = title[start:end].strip()
            next_title = title[start:end+1].strip()
            if (not sub_title
                    or sub_title == title
                    or len(sub_title) > max_word_len
                    or sub_title not in content):
                break
            if len(sub_title) < min_word_len:
                continue
            # ignore duplicate word
            if sub_title in counter:
                continue
            # english word
            if (next_title != sub_title
                    and alpha_pattern.match(sub_title)
                    and alpha_pattern.match(next_title)):
                continue
            counter[sub_title] += content.count(sub_title)
        start += 1

    cleaned_counter = {k:v for k, v in counter.items() if _keep_item(k, counter)}
    sorted_counter = sorted(cleaned_counter.items(), key=lambda x: x[1], reverse=True)
    return[i[0] for i in sorted_counter[:max_count]]


def _keep_item(key, dict):
    # filter number keys(entities)
    if _force_text(key).isdigit():
        return False
    if _guess_contain(key, dict):
        return False
    return True


def _guess_contain(key, dict):
    """
    >>> guess_contain('aa', dict(abc=2, aabbcc=1, aa=1, bb=1, cc=1))
    True

    >>> guesss_contain('aa', dict(aa=2))
    False
    """
    value = dict[key]
    for k, v in dict.items():
        if key != k and key in k and value == v:
            return True
    return False
