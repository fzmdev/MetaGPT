#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-02-27 17:10
# @Author   : mike.feng

import re

if __name__ == '__main__':
    prompt = """
            Write a python function that can {instruction} and provide two runnnable test cases.
            Return ```python aaa
             bbb
             cccc
             dddd``` with NO other texts,
            your code:
            """

    pattern = r"```python(.*)```"  # 匹配代码块的正则模式
    match = re.search(pattern, prompt, re.DOTALL)  # 允许跨行匹配
    res = match.group(1) if match else None
    print(res)
