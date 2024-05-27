from typing import Iterable

from mopyx import action


@action
def set_list(dist: list, source: Iterable):
    dist.clear()
    dist.extend(source)
