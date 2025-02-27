#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-02-27 10:52
# @Author   : mike.feng
# 使用现成的智能体

import asyncio
from metagpt.context import Context
from metagpt.roles.product_manager import ProductManager
from metagpt.logs import logger


async def main():
    msg = "write a PRD for a simple snake game"
    context = Context()
    role = ProductManager(context=context)
    while msg:
        msg = await role.run(msg)
        logger.info(str(msg))


if __name__ == '__main__':
    asyncio.run(main())
