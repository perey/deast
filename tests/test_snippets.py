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

# Common code for checking expected results.
def compare(code_in, code_out=None):
    """Compare code before and after an ast/deast conversion."""
    if code_out is None:
        code_out = code_in
    tree = ast.parse(code_in)
    deaster = deast.DeAST()

    deaster.visit(tree)

    assert deaster.source == code_out

# Expressions
def test_num_literal():
    """Can deast handle a simple numeric literal?"""
    compare('5\n')

def test_str_literal():
    """Can deast handle a simple string literal?"""
    compare("'Hello world'\n")
    # Other ways of writing string literals are converted to single-quoted,
    # one-line strings...
    compare('"""Hello\nworld"""\n', "'Hello\\nworld'\n")

# Import statements
def test_simple_import():
    """Can deast handle a simple import statement?"""
    compare('import sys\n')

def test_import_as():
    """Can deast handle an import statement with aliases?"""
    compare('import sys as bar\n')

def test_compound_import():
    """Can deast handle a compound import statement?"""
    compare('import re, sys as bar, math\n')

# Other simple statements
def test_pass():
    """Can deast handle the pass statement?"""
    compare('pass\n')
