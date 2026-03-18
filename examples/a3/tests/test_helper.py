import ast
import inspect
import typing
from inspect import Signature
from modulefinder import Module
from types import ModuleType
from typing import Callable
import math


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


def hex_area(a):
    """Helper to avoid repeating code"""
    return (3 / 2) * math.sqrt(3) * (a**2)


WEEKS_PER_YEAR: int = 52
CONCENTRATION_THRESHOLD = 0.05

TAX_BRACKET_LOW = 53_255
TAX_BRACKET_MED = 106_495
TAX_BRACKET_HIGH = 129_590

TAX_RATE_LOW = 0.14
TAX_RATE_MED = 0.19
TAX_RATE_HIGH = 0.24
TAX_RATE_ULTRA = 0.2575


def net_income(hourly_rate, hours_per_week):
    gross_income = hourly_rate * hours_per_week * WEEKS_PER_YEAR
    if gross_income <= TAX_BRACKET_LOW:
        tax_rate = TAX_RATE_LOW
    elif gross_income <= TAX_BRACKET_MED:
        tax_rate = TAX_RATE_MED
    elif gross_income <= TAX_BRACKET_HIGH:
        tax_rate = TAX_RATE_HIGH
    else:
        tax_rate = TAX_RATE_ULTRA
    return gross_income * (1 - tax_rate)


def actual_net_income(hourly_rate: float, hours_per_week: float) -> float:
    """Function calculating the actual salary of a Quebec resident"""
    taxable_gross_income = hourly_rate * hours_per_week * WEEKS_PER_YEAR
    accumulated_net_income = 0
    if taxable_gross_income > TAX_BRACKET_HIGH:
        tax_rate = TAX_RATE_ULTRA
        accumulated_net_income += (taxable_gross_income - TAX_BRACKET_HIGH) * (
            1 - tax_rate
        )
        taxable_gross_income = TAX_BRACKET_HIGH
    if taxable_gross_income > TAX_BRACKET_MED:
        tax_rate = TAX_RATE_HIGH
        accumulated_net_income += (taxable_gross_income - TAX_BRACKET_MED) * (
            1 - tax_rate
        )
        taxable_gross_income = TAX_BRACKET_MED
    if taxable_gross_income > TAX_BRACKET_LOW:
        tax_rate = TAX_RATE_MED
        accumulated_net_income += (taxable_gross_income - TAX_BRACKET_LOW) * (
            1 - tax_rate
        )
        taxable_gross_income = TAX_BRACKET_LOW
    if taxable_gross_income <= TAX_BRACKET_LOW:
        tax_rate = TAX_RATE_LOW
        accumulated_net_income += (taxable_gross_income) * (1 - tax_rate)
    return accumulated_net_income
