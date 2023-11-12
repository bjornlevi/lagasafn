import os
import requests

CACHE_DIRECTORY: list[str] = ['data']

def prepare_dir(path: list[str]) -> None:
    if len(path) == 0:
        return
    for i in range(len(path)):
        tmppathlist = path[:i+1]
        tmppath = os.path.join(*tmppathlist)
        if not os.path.exists(tmppath):
            os.mkdir(tmppath)

def touch_path(path: list | tuple) -> None:
    if path is None:
        return None
    for i in range(len(path)):
        pathstr = path[0] if i == 0 else os.path.join(*path[:i], path[i])
        if i != len(path) - 1:
            if not os.path.exists(pathstr):
                os.mkdir(pathstr)
        elif not os.path.exists(pathstr):
            with open(pathstr, 'x') as file:
                pass

def save_cache(path: list[str], data: str, encoding: str = 'utf-8') -> None:
    cache_path = os.path.join(*CACHE_DIRECTORY, *path)

    # If directory does not exists, then create it
    #if len(path) > 1:
    #   prepare_dir(CACHE_DIRECTORY + path[:-1])

    touch_path(CACHE_DIRECTORY + path)

    # Save cache
    with open(cache_path, 'w', encoding=encoding) as file:
        file.write(data)

def load_cache(path: list[str], encoding: str = 'utf-8') -> str | None:
    cache_path = os.path.join(*CACHE_DIRECTORY, *path)
    if not os.path.exists(cache_path):
        return None
    with open(cache_path, 'r', encoding=encoding) as file:
        if not file:
            return None
        return file.read()

def read_web_or_cache(url: str):
     respo