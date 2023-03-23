# -*- coding: utf-8 -*-
"""
Example FastAPI module
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello-world")
async def hello_world():
    """Retrieves hello world"""
    return "Hello, world!"


@app.get("/some-method")
async def some_method(this_is_my_long_param: str, other_query_param: str):
    """Also retrieves hello world

    :param this_is_my_long_param: some description
    :param other_query_param: some other description
    """
    return {'response': {
        'one': this_is_my_long_param,
        'two': other_query_param
    }}
