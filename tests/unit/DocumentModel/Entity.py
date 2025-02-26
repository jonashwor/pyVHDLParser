from textwrap import dedent
from unittest import TestCase, skip

from pyVHDLParser.DocumentModel import Document
from tests.unit.Common import Initializer


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


def setUpModule():
	Initializer()


class Entity(TestCase):
	@skip("Not working yet")
	def test_Entity(self):
		code = dedent("""\
			package p is
			end package;
			""")

		document = Document("Entity.vhdl")
		document.Parse(code)

		self.assertTrue(len(document.Architectures) == 0,   "Document contains unexpected architectures.")
		self.assertTrue(len(document.Configurations) == 0,  "Document contains unexpected configurations.")
		self.assertTrue(len(document.Contexts) == 0,        "Document contains unexpected contexts.")
		self.assertTrue(len(document.Entities) == 1,        "Document doesn't contain the expected entity.")
		self.assertTrue(len(document.Libraries) == 0,       "Document contains unexpected libraries.")
		self.assertTrue(len(document.PackageBodies) == 0,   "Document contains unexpected package bodies.")
		self.assertTrue(len(document.Packages) == 0,        "Document contains unexpected packages.")
		self.assertTrue(len(document.Uses) == 0,            "Document contains unexpected uses.")
