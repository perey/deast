#!/usr/bin/env python3

"""Test the deast module on short snippets of code."""

# Copyright © 2017 Timothy Pederick
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard library imports.
import ast

# The module being tested.
import deast

def test_simple_expr():
    """Can deast handle a simple expression?"""
    code_in = code_out = '5\n'
    tree = ast.parse(code_in)
    deaster = deast.DeAST()

    deaster.visit(tree)

    assert deaster.source == code_out

def test_simple_import():
    """Can deast handle a simple import statement?"""
    code_in = code_out = 'import sys\n'
    tree = ast.parse(code_in)
    deaster = deast.DeAST()

    deaster.visit(tree)

    assert deaster.source == code_out

def test_import_as():
    """Can deast handle an import statement with aliases?"""
    code_in = code_out = 'import sys as bar\n'
    tree = ast.parse(code_in)
    deaster = deast.DeAST()

    deaster.visit(tree)

    assert deaster.source == code_out

def test_compound_import():
    """Can deast handle a compound import statement?"""
    code_in = code_out = 'import re, sys as bar, math\n'
    tree = ast.parse(code_in)
    deaster = deast.DeAST()

    deaster.visit(tree)

    assert deaster.source == code_out

def test_pass():
    """Can deast handle the pass statement?"""
    code_in = code_out = 'pass\n'
    tree = ast.parse(code_in)
    deaster = deast.DeAST()

    deaster.visit(tree)

    assert deaster.source == code_out
