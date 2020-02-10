# Copyright 2017 Palantir Technologies, Inc.
from pyls import uris
from pyls.plugins.autopep8_format import (pyls_format_document,
                                          pyls_format_range)
from pyls.workspace import Document

DOC_URI = uris.from_fs_path(__file__)
DOC = """a =    123




def func():
    pass
"""

GOOD_DOC = """A = ['hello', 'world']\n"""

INDENTED_DOC = """def foo():
    print('asdf',
    file=None
    )

bar = { 'foo': foo
}
"""

CORRECT_INDENTED_DOC = """def foo():
    print('asdf',
          file=None
          )


bar = {'foo': foo
       }
"""


def test_format(config, workspace):
    doc = Document(DOC_URI, workspace, DOC)
    res = pyls_format_document(config, doc)

    assert len(res) == 1
    assert res[0]["newText"] == "a = 123\n\n\ndef func():\n    pass\n"


def test_range_format(config, workspace):
    doc = Document(DOC_URI, workspace, DOC)

    def_range = {
        "start": {"line": 0, "character": 0},
        "end": {"line": 2, "character": 0},
    }
    res = pyls_format_range(config, doc, def_range)

    assert len(res) == 1

    # Make sure the func is still badly formatted
    assert res[0]["newText"] == "a = 123\n\n\n\n\ndef func():\n    pass\n"


def test_no_change(config, workspace):
    doc = Document(DOC_URI, workspace, GOOD_DOC)
    assert not pyls_format_document(config, doc)


def test_hanging_indentation(config, workspace):
    doc = Document(DOC_URI, workspace, INDENTED_DOC)
    res = pyls_format_document(config, doc)

    assert len(res) == 1
    assert res[0]['newText'] == CORRECT_INDENTED_DOC
