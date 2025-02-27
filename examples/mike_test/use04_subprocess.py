#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-02-27 19:35
# @Author   : mike.feng

import subprocess

subprocess.run(["python", "-c", "print('hello')"], capture_output=True,
               text=True)
