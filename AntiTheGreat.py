# import json
# import requests
import json
from time import sleep
import jsonpath
import aiohttp
import asyncio
import warnings

sleep(0.5)
print("Powered By UnderTides")
sleep(1)

warnings.filterwarnings("ignore", category=Warning)

Characters = json.load(open('Characters.json' , 'r' , encoding='utf-8'))
url_base = "https://ak.hypergryph.com/activity/cypher-challenge/api/act/questions/"

cookie = input("请输入cookie(最好使用小号的cookie),仅输入AKa3_5Anniv项即可,完整输入也可:")

headers = {
    "content-type": "application/json",
    "cookie": cookie,
    "Host": "ak.hypergryph.com"
}

body = {
    "answer": "",
    "attemptCnt": 1,
    "advanced": True
}


# # 同步/阻塞io

# def try_sync(url: str, body: dict, headers: dict):
#     response = requests.post(url=url, data=str(body).replace(
#         "'", '"').replace("True", 'true').encode('utf-8'), headers=headers)
#     result = jsonpath.jsonpath(json.loads(response.text), '$..result')[0]
#     return result


# def answer_sync(Character: list, question: str, url_base: str, body: dict, headers: dict):
#     url = url_base + question
#     for i in Character:
#         body["answer"] = i
#         if try_sync(url, body, headers):
#             print("{} is the answer".format(i))
#             return i
#         else:
#             print("{} is not the answer".format(i))
#     return -1


# 异步/非阻塞io

async def fetch_async(session, url: str, data: dict, headers: dict):
    async with session.post(url=url, data=data, headers=headers) as response:
        return await response.json()


async def try_async(url: str,answer:str, body: dict, headers: dict):
    body["answer"] = answer
    async with aiohttp.ClientSession() as session:
        response_json = await fetch_async(session, url, str(body).replace("'", '"').replace("True", 'true').encode('utf-8'), headers)
        result = jsonpath.jsonpath(response_json, '$..result')[0]
        if result:
            print("答案是:{}".format(answer))
        return jsonpath.jsonpath(response_json, '$..result')[0]


def answer_async(Character: list, question: str, url_base: str, body: dict, headers: dict):
    url = url_base + question

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(try_async(url,i,body,headers)) for i in Character]
    tasks = asyncio.gather(*tasks)

    return loop.run_until_complete(tasks)

def getTAG():
    tag_range = input("请输入第一个线索所属范围(势力/出生地/种族/职业/TAG/all):")
    if tag_range != all:
        tag = input("请输入第一个线索内容:")

    if tag_range == all:
        return [i for i in Characters]
    else:
        Characters_range = []
        for i in Characters:
            if tag in Characters[i][tag_range]:
                Characters_range.append(i)
        return Characters_range


while True:
    question = input("请输入问题id:")

    Characters_range = getTAG()

    answer_async(Characters_range, question, url_base, body, headers)
