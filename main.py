from urllib.parse import urlparse
import validators
from typing import List, Any
from collections import defaultdict, Counter
from itertools import zip_longest
import asyncio
from httpx import AsyncClient
from time import perf_counter
from functools import wraps


# 1

def extract_project_name_from_url(url: str) -> None:
    parsed_url = urlparse(url)
    project_name = parsed_url.path.split('/')[-1].split('.')[0]
    print(project_name)


def get_projects_names(urls: List[str]) -> None:
    for url in urls:
        suffix = '.git'
        if validators.url(url) and url.endswith(suffix):
            extract_project_name_from_url(url)
        else:
            print(f'incorrect url: {url}')


get_projects_names(['https://github.com/AniutaP/python-project-83.git',
                  'htt://github.com/AniutaP/python-project-83.git',
                  '',
                  'https://github.com/AniutaP/python-project-83'])


# 2

def merge_lists_to_dict(data1: List[str], data2: List[Any]) -> None:
    if data1:
        check_type_for_keys = all(isinstance(el, str) for el in data1)
        if check_type_for_keys:
            data1.sort()
        else:
            el_is_not_string = [el for el in data1 if not isinstance(el, str)]
            print(f'some keys not string: {el_is_not_string}')
            return

    result_dict = defaultdict(list)
    merge_lists = zip_longest(data1, data2, fillvalue='exceeding_len')
    for k, v in merge_lists:
        result_dict[k].append(v)
    print(dict(result_dict))


merge_lists_to_dict(['b', 'a'], [4, 5, 6, 7, 8])
merge_lists_to_dict([1, {1, 2}], [4, 5, 6, 7, 8])


# 3

def change_elements(data: List[int | str]) -> None:
    if data:
        changed_data = list(map(lambda el: f'abc_{el}_cba' if isinstance(el, str) else el ** 2, data))
        # used List comprehension:
        # changed_data = [f'abc_{el}_cba' if isinstance(el, str) else el ** 2 for el in data]
        print(changed_data)
    else:
        print('empty data')


change_elements([1, 'a'])
change_elements([])


# 4
# code execution time with 100 requests is 6 seconds

async def make_request(client: AsyncClient) -> int:
        response = await client.get('http://httpbin.org/delay/3', timeout=5.0)
        return response.status_code


async def check_time_exec_requests() -> None:
    start_time = perf_counter()
    check_res = Counter()
    async with AsyncClient() as client:
        requests_num = 100
        tasks = [asyncio.create_task(make_request(client)) for _ in range(requests_num)]
        for task in tasks:
            try:
                status = await task
                check_res[status] += 1
            except:
                raise
    end_time = perf_counter() - start_time
    print(end_time, check_res, sep='\n')


# asyncio.run(check_time_exec_requests())

# 6

def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = perf_counter()
        func(*args, **kwargs)
        end_time = perf_counter() - start_time
        print(end_time)
    return inner


# 5

class TextType:
    '''
    class - descriptor
    '''

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if isinstance(value, str):
            instance.__dict__[self.storage_name] = value
        else:
            raise TypeError('argument must be string')


class Text:

    text = TextType('text')

    def __init__(self, text: str):
        self.text = text

    @timer
    def longest_word(self):
        if self.text:
            print(max(self.text.split(), key=len))
        else:
            print(self.text)

    @timer
    def most_common_word(self):
        if self.text:
            count_words = {}
            for word in self.text.split():
                word = word.strip(',.;/:')
                count_words[word] = count_words.get(word, 0) + 1
            sorted_words_by_count = sorted(count_words.items(), key=lambda x: (-x[1], x[0]))
            print(sorted_words_by_count[0][0])
        else:
            print(self.text)

    @timer
    def special_symbols_count(self):
        print(len(list(el for el in self.text if el != ' ' and not el.isalnum())))

    @timer
    def palindromes(self):
        all_palindromes = [word for word in self.text.split() if word == word[::-1]]
        print(*all_palindromes, sep=', ')



text = Text('some not long words: abba, abba, klmnmlk')
text.longest_word()
text.most_common_word()
text.special_symbols_count()
text.palindromes()
text2 = Text('')
text2.longest_word()
text2.most_common_word()
text2.special_symbols_count()
text2.palindromes()