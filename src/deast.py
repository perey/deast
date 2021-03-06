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
    def __getattr__(self, attr):
        """Intercept a visit_* call to a simple node.

        A simple node is one that, when visited, simply adds a line of
        code to the output. This code is generated by the src_* method
        of the SourceWriter that corresponds to the visit_* method call
        that this __getattr__() call is intercepting.

        """
        # Only intercept attribute lookups that start with 'visit_'.
        visit_prefix = 'visit_'
        if attr.startswith(visit_prefix):
            src_fnname = 'src_' + attr[len(visit_prefix):]
            try:
                src_fn = getattr(self._source_writer, src_fnname)
                visit_fn = lambda node: self._source_writer.print(src_fn(node))
            except AttributeError:
                visit_fn = self.generic_visit
            return visit_fn
        else:
            # Doesn't start with 'visit_'. Fail the lookup.
            raise AttributeError('{!r} object has no attribute '
                                 '{!r}'.format(self.__class__.__name__, attr))


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

    def print(self, *args):
        """Write a complete line of code to the buffer."""
        assert self.ready

        print(self.indent, *args, sep='', file=self._buffer)

    # Node source-generating methods.
    def src_alias(self, node):
        src = node.name
        if node.asname is not None:
            src += ' as ' + node.asname
        return src

    def src_Bytes(self, node):
        return repr(node.s)

    def src_Ellipsis(self, node):
        return '...'

    def src_Import(self, node):
        return 'import ' + ', '.join(map(self.src_alias, node.names))

    def src_Name(self, node):
        return node.id

    def src_NameConstant(self, node):
        return node.value

    def src_Num(self, node):
        return repr(node.n)

    def src_Pass(self, node):
        return 'pass'

    def src_Str(self, node):
        return repr(node.s)
