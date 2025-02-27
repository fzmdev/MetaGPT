#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-02-27 17:33
# @Author   : mike.feng

import asyncio


async def fetch_data():
    print("Start fetching")
    await asyncio.sleep(2)  # 模拟网络请求
    print("Data received")
    return {"data": 100}


async def main():
    task = asyncio.create_task(fetch_data())
    print("do other task")
    await task
    print("do other task2")
    print(f"Result: {task.result()}")


if __name__ == '__main__':
    asyncio.run(main())
