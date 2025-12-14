import ast
import inspect
import typing
from inspect import Signature
from modulefinder import Module
from types import ModuleType
from typing import Callable


def get_inner_func(student_code: ModuleType) -> dict[str, list[str]]:
    source = inspect.getsource(student_code)
    nodes = ast.walk(ast.parse(source))

    func_nodes = [node for node in nodes if isinstance(node, ast.FunctionDef)]

    inner_func_dict = {}
    for outer_func in func_nodes:
        inner_func_dict[outer_func.name] = [
            inner_func.name
            for inner_func in ast.walk(outer_func)
            if isinstance(inner_func, ast.FunctionDef)
            and inner_func.name != outer_func.name
        ]

    return inner_func_dict


def uses_loop(function: Callable):
    nodes = ast.walk(ast.parse(inspect.getsource(function)))
    return any(isinstance(node, (ast.For, ast.While)) for node in nodes)


def uses_condition(function: Callable):
    nodes = ast.walk(ast.parse(inspect.getsource(function)))
    return any(isinstance(node, ast.If) for node in nodes)


def get_signature(function: Callable) -> Signature:
    return inspect.signature(function)


def get_func_calls(caller: Callable) -> list[str]:
    nodes = ast.walk(ast.parse(inspect.getsource(caller)))
    func_calls = (call for call in nodes if isinstance(call, ast.Call))
    call_names = [
        call.func.id for call in func_calls if isinstance(call.func, ast.Name)
    ]
    return call_names


def contains_func(student_code: Module, func_name: str) -> bool:
    return hasattr(student_code, func_name)
