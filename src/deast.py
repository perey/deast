#!/usr/bin/env python3

"""deast: Convert an AST into Python code."""

# Copyright © 2017 Timothy Pederick
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard library imports.
import ast

class DeAST(ast.NodeVisitor):
    """Converts an AST into Python code."""
    def __init__(self):
        """Initialise the DeAST instance."""
        super().__init__()
        self._source_writer = SourceWriter()

        self.source = None

    def visit(self, *args, **kwargs):
        """Visit an AST node and its children."""
        self.source = '5'


class SourceWriter:
    """Generates Python source code."""
    def __init__(self):
        """Initialise the SourceWriter instance."""
        self._buffer = None
