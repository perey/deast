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
from io import StringIO

class DeAST(ast.NodeVisitor):
    """Converts an AST into Python code."""
    def __init__(self):
        """Initialise the DeAST instance."""
        super().__init__()
        self._source_writer = SourceWriter()

        self.source = None

    def visit(self, *args, **kwargs):
        """Visit an AST node and its children."""
        # As this function may be called recursively, only set up the source
        # writer at the top level.
        top_level = not self._source_writer.ready

        if top_level:
            self._source_writer.start()

        super().visit(*args, **kwargs)

        # Likewise, only get output from the source writer at the top level.
        if top_level:
            self.source = self._source_writer.finish()

    # Node visitor methods.
    def visit_Import(self, node):
        self._source_writer.print_codeline(self._source_writer.src_Import(node))

    def visit_Num(self, node):
        self._source_writer.print_codeline(self._source_writer.src_Num(node))


class SourceWriter:
    """Generates Python source code."""
    _indent_prefix = '    '

    def __init__(self):
        """Initialise the SourceWriter instance."""
        self._buffer = self._indentlvl = None

    @property
    def ready(self):
        """Determine whether this instance is ready to write code."""
        return self._buffer is not None

    @property
    def indent(self):
        """Get the leading whitespace for the current block."""
        return self._indent_prefix * self._indentlvl

    def start(self):
        """Get ready to write code."""
        assert not self.ready

        self._buffer = StringIO()
        self._indentlvl = 0

    def finish(self):
        """Stop writing code and return what has been written."""
        assert self.ready

        output = self._buffer.getvalue()
        self._buffer.close()
        self._buffer = self._indentlvl = None
        return output

    def print_codeline(self, *args):
        """Write a complete line of code to the buffer."""
        assert self.ready

        print(self.indent, *args, sep='', file=self._buffer)

    # Node source-generating methods.
    def src_alias(self, node):
        return node.name

    def src_Num(self, node):
        return repr(node.n)

    def src_Import(self, node):
        return 'import ' + ', '.join(map(self.src_alias, node.names))
