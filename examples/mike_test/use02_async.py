#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-02-27 17:24
# @Author   : mike.feng
# 并行执行多个协程

import asyncio


async def task(name, delay):
    print(f"{name} start")
    await asyncio.sleep(delay)
    print(f"{name} end")


async def main():
    await asyncio.gather(
        task("Task1", 2),
        task("Task2", 1),
        task("Task3", 3)
    )


if __name__ == '__main__':
    asyncio.run(main())
