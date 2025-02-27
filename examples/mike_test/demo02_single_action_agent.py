#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-02-27 16:03
# @Author   : mike.feng
# 单一动作的智能体

import re
import asyncio

from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.actions import Action
from metagpt.schema import Message
from metagpt.context import Context


# 定义生成代码的Action类（MetaGPT框架的核心组件）
class SimpleWriteCode(Action):
    # 代码生成提示词模板，包含占位符{instruction}用于接收具体需求
    PROMPT_TEMPLATE: str = """
        Write a python function that can {instruction} and provide two runnnable test cases.
        Return ```python your_code_here ``` with NO other texts,
        your code:
        """
    name: str = "SimpleWriteCode"  # 行为名称标识

    # 异步执行代码生成的核心方法
    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)  # 构建完整提示
        rsp = await self._aask(prompt)  # 调用底层LLM接口
        return self.parse_code(rsp)  # 解析返回结果

    # 使用正则表达式提取代码块
    @staticmethod
    def parse_code(rsp):
        pattern = r"```python(.*)```"  # 匹配代码块的正则模式
        match = re.search(pattern, rsp, re.DOTALL)  # 允许跨行匹配
        code_text = match.group(1) if match else rsp
        return code_text


# 定义代码生成角色（继承自MetaGPT的Role类）
class SimpleCoder(Role):
    name: str = "Alice"  # 角色名称
    profile: str = "SimpleCoder"  # 角色描述

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SimpleWriteCode])  # 绑定代码生成行为

    # 角色执行动作的核心方法
    async def _act(self) -> Message:
        todo = self.rc.todo  # 获取待执行动作（即SimpleWriteCode）
        logger.info(f"{self._setting}: to do {todo.name}")  # 记录日志

        # 从记忆体中获取最新指令
        msg = self.get_memories(k=1)[0]
        # 执行代码生成并获取结果
        code_text = await todo.run(msg.content)

        # 构造返回消息（包含生成的代码）
        return Message(
            content=code_text,
            role=self.profile,
            cause_by=type(todo)  # 标注触发源类型
        )


async def main():
    msg = "write a function that calculates the sum of a list"
    context = Context()
    role = SimpleCoder(context=context)
    logger.info(msg)
    result = await role.run(msg)
    logger.info(result)


if __name__ == '__main__':
    asyncio.run(main())
