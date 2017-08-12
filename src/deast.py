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


class SourceWriter:
    """Generates Python source code."""
    def __init__(self):
        """Initialise the SourceWriter instance."""
        self._buffer = None

    @property
    def ready(self):
        """Determine whether this instance is ready to write code."""
        return self._buffer is not None

    def start(self):
        """Get this instance ready to write code."""
        self._buffer = StringIO()

    def finish(self):
        """Shut down this instance."""
        output = '5'
        self._buffer.close()
        self._buffer = None
        return output
