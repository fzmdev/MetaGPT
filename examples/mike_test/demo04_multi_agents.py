# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-02-27 19:46
# @Author   : mike.feng
# 多智能体

import re
import asyncio

import fire
from metagpt.team import Team
from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.schema import Message
from metagpt.actions import Action, UserRequirement


class SimpleWriteCode(Action):
    PROMPT_TEMPLATE: str = """
        Write a python function that can {instruction}.
        Return ```python your_code_here ``` with NO other texts,
        your code:
        """
    name: str = "SimpleWriteCode"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)
        return SimpleWriteCode.parse_code(rsp)

    @staticmethod
    def parse_code(rsp: str):
        pattern = r"```python(.*) ```"
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text


class SimpleWriteTest(Action):
    PROMPT_TEMPLATE: str = """
        Context: {context}
        Write {k} unit tests using pytest for the given function, assuming you have imported it.
        Return ```python your_code_here ``` with NO other texts,
        your code:
        """

    name: str = "SimpleWriteTest"

    async def run(self, context: str, k: int = 3):
        prompt = self.PROMPT_TEMPLATE.format(context=context, k=k)
        rsp = await self._aask(prompt)
        return SimpleWriteTest.parse_code(rsp)

    @staticmethod
    def parse_code(rsp: str):
        pattern = r"```python(.*) ```"
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text


class SimpleWriteReview(Action):
    PROMPT_TEMPLATE: str = """
        Context: {context}
        Review the test cases and provide one critical comments:
        """

    name: str = "SimpleWriteReview"

    async def run(self, context: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context)
        rsp = await self._aask(prompt)
        return rsp


class SimpleCoder(Role):
    name: str = "Alice"
    profile: str = "SimpleCoder"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self.set_actions([SimpleWriteCode])


class SimpleTester(Role):
    name: str = "Bob"
    profile: str = "SimpleTester"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SimpleWriteTest])
        self._watch([SimpleWriteCode, SimpleWriteReview])

    async def _act(self) -> Message:
        todo = self.rc.todo
        logger.info(f"{self._setting}: to do {todo} (self.rc.todo.name)")

        context = self.get_memories()

        code_text = await todo.run(context, k=5)
        msg = Message(content=code_text, role=self.profile, cause_by=type(todo))

        # self.rc.memory.add(msg)
        return msg


class SimpleReviewer(Role):
    name: str = "Charlie"
    profile: str = "SimpleReviewer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([SimpleWriteReview])
        self._watch([SimpleWriteTest])


async def main(
        idea: str = "write a function that calculates the prdocut of a list",
        investment: float = 3.0,
        n_round: int = 5,
):
    logger.info(idea)
    team = Team()
    team.hire([
        SimpleCoder(),
        SimpleTester(),
        SimpleReviewer()
    ])

    team.invest(investment=investment)
    team.run_project(idea)
    await team.run(n_round=n_round)


if __name__ == '__main__':
    fire.Fire(main)
