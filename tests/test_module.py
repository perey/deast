#!/usr/bin/env python3

"""Test the basic properties of the deast module."""

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

def test_import():
    """Can the deast module be imported?"""
    import deast

def test_DeAST_class():
    """Can the DeAST class be instantiated?"""
    from ast import NodeVisitor
    from deast import DeAST
    deaster = DeAST()

    assert isinstance(deaster, DeAST)
    assert isinstance(deaster, NodeVisitor)

def test_SourceWriter_class():
    """Can the SourceWriter class be instantiated?"""
    from deast import SourceWriter
    source_writer = SourceWriter()

    assert isinstance(source_writer, SourceWriter)

def test_DeAST_has_source():
    """Is a DeAST's source attribute filled when visit() is called?"""
    from ast import AST
    from deast import DeAST
    deaster = DeAST()

    assert hasattr(deaster, 'source')
    assert deaster.source is None

    deaster.visit(AST())

    assert deaster.source is not None

def test_DeAST_has_SourceWriter():
    """Does a DeAST instance have a SourceWriter instance?"""
    import deast
    deaster = deast.DeAST()

    assert isinstance(deaster._source_writer, deast.SourceWriter)

def test_SourceWriter_has_no_buffer():
    """Does a SourceWriter's _buffer attribute appear to be None?"""
    from deast import SourceWriter
    source_writer = SourceWriter()

    assert source_writer._buffer is None
