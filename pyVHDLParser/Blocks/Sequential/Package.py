# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python functions:   A streaming VHDL parser
#
# Description:
# ------------------------------------
#		TODO:
#
# License:
# ==============================================================================
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
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
# ==============================================================================
#
# load dependencies
from pydecor.decorators             import export

from pyVHDLParser.Token             import LinebreakToken, WordToken, SpaceToken, CommentToken, MultiLineCommentToken
from pyVHDLParser.Token.Keywords    import PackageKeyword, IsKeyword, EndKeyword, GenericKeyword, BodyKeyword, UseKeyword, VariableKeyword, SignalKeyword
from pyVHDLParser.Token.Keywords    import BoundaryToken, IdentifierToken
from pyVHDLParser.Token.Keywords    import ConstantKeyword, SharedKeyword, ProcedureKeyword, FunctionKeyword, PureKeyword, ImpureKeyword
from pyVHDLParser.Blocks            import BlockParserException, Block, CommentBlock, ParserState
from pyVHDLParser.Blocks.Common     import LinebreakBlock, IndentationBlock, WhitespaceBlock
from pyVHDLParser.Blocks.Generic    import SequentialDeclarativeRegion
from pyVHDLParser.Blocks.Generic1   import EndBlock as EndBlockBase
from pyVHDLParser.Blocks.Sequential import PackageBody
from pyVHDLParser.Blocks.List       import GenericList

__all__ = []
__api__ = __all__


@export
class EndBlock(EndBlockBase):
	KEYWORD =             PackageKeyword
	KEYWORD_IS_OPTIONAL = True
	EXPECTED_NAME =       KEYWORD.__KEYWORD__


@export
class DeclarativeRegion(SequentialDeclarativeRegion):
	END_BLOCK = EndBlock

	@classmethod
	def __cls_init__(cls):
		super().__cls_init__()

		# TODO: use key assignment: a[b] = c
		cls.KEYWORDS.update({
			# Keyword         Transition
			GenericKeyword:  GenericList.OpenBlock.stateGenericKeyword
		})

@export
class NameBlock(Block):
	@classmethod
	def statePackageKeyword(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace1
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace1
			return

		raise BlockParserException("Expected whitespace after keyword PACKAGE.", token)

	@classmethod
	def stateWhitespace1(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, WordToken):
			if (token <= "body"):
				parserState.NewToken =    BodyKeyword(token)
				parserState.NextState =   PackageBody.NameBlock.stateBodyKeyword
				return
			else:
				parserState.NewToken =    IdentifierToken(token)
				parserState.NextState =   cls.statePackageName
				return
		elif isinstance(token, LinebreakToken):
			if (not (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				_ =                       LinebreakBlock(parserState.NewBlock, token)
			else:
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected package name (identifier).", token)

	@classmethod
	def statePackageName(cls, parserState: ParserState):
		token = parserState.Token
		if isinstance(token, SpaceToken):
			parserState.NewToken =    BoundaryToken(token)
			parserState.NextState =   cls.stateWhitespace2
			return
		elif isinstance(token, (LinebreakToken, CommentToken)):
			block =                   LinebreakBlock if isinstance(token, LinebreakToken) else CommentBlock
			parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                       block(parserState.NewBlock, token)
			parserState.TokenMarker = None
			parserState.NextState =   cls.stateWhitespace2
			return

		raise BlockParserException("Expected whitespace after package name.", token)

	@classmethod
	def stateWhitespace2(cls, parserState: ParserState):
		token = parserState.Token
		if (isinstance(token, WordToken) and (token <= "is")):
			parserState.NewToken =      IsKeyword(token)
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=parserState.NewToken)
			parserState.TokenMarker =   None
			parserState.NextState =     DeclarativeRegion.stateDeclarativeRegion
			return
		elif isinstance(token, LinebreakToken):
			if (not (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
				parserState.NewBlock =    cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
				_ =                       LinebreakBlock(parserState.NewBlock, token)
			else:
				parserState.NewBlock =    LinebreakBlock(parserState.LastBlock, token)
			parserState.TokenMarker =   None
			return
		elif isinstance(token, CommentToken):
			parserState.NewBlock =      cls(parserState.LastBlock, parserState.TokenMarker, endToken=token.PreviousToken, multiPart=True)
			_ =                         CommentBlock(parserState.NewBlock, token)
			parserState.TokenMarker =   None
			return
		elif (isinstance(token, SpaceToken) and (isinstance(parserState.LastBlock, CommentBlock) and isinstance(parserState.LastBlock.StartToken, MultiLineCommentToken))):
			parserState.NewToken =      BoundaryToken(token)
			parserState.NewBlock =      WhitespaceBlock(parserState.LastBlock, parserState.NewToken)
			parserState.TokenMarker =   None
			return

		raise BlockParserException("Expected keyword IS after package name.", token)
