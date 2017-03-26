# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
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
# Copyright 2007-2017 Patrick Lehmann - Dresden, Germany
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
from pyVHDLParser.Blocks      import TokenParserException
from pyVHDLParser.Token       import StringToken, VHDLToken


class BoundaryToken(VHDLToken):
	def __init__(self, spaceToken):
		super().__init__(spaceToken.PreviousToken, spaceToken.Value, spaceToken.Start, spaceToken.End)

	def __str__(self):
		return "<BoundaryToken '{value}' at {pos!r}>".format(value=self.Value, pos=self.Start)

class BracketToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)

	def __str__(self):
		return "<{name} '{value}' at {pos!r}>".format(name=self.__class__.__name__, value=self.Value, pos=self.Start)

# Round bracket / parenthesis / ()
class RoundBracketToken(BracketToken): pass
class OpeningRoundBracketToken(RoundBracketToken): pass
class ClosingRoundBracketToken(RoundBracketToken): pass
# Square bracket / []
class SquareBracketToken(BracketToken): pass
class OpeningSquareBracketToken(SquareBracketToken): pass
class ClosingSquareBracketToken(SquareBracketToken): pass
# Curly bracket / brace / curved bracket / {}
class CurlyBracketToken(BracketToken): pass
class OpeningCurlyBracketToken(CurlyBracketToken): pass
class ClosingCurlyBracketToken(CurlyBracketToken): pass
# Angle bracket / arrow bracket / <>
class AngleBracketToken(BracketToken): pass
class OpeningAngleBracketToken(AngleBracketToken): pass
class ClosingAngleBracketToken(AngleBracketToken): pass


class OperatorToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)

	def __str__(self):
		return "<{name} '{value}' at {pos!r}>".format(name=self.__class__.__name__, value=self.Value, pos=self.Start)


class PlusOperatorToken(OperatorToken): pass
class MinusOperatorToken(OperatorToken): pass
class MultiplyOperatorToken(OperatorToken): pass
class DivideOperatorToken(OperatorToken): pass
class PowerOperatorToken(OperatorToken): pass
class ConcatOperatorToken(OperatorToken): pass


class DelimiterToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)

	def __str__(self):
		return "<DelimiterToken '{value}' at {pos!r}>".format(value=self.Value, pos=self.Start)

class EndToken(VHDLToken):
	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, characterToken.Value, characterToken.Start, characterToken.End)

	def __str__(self):
		return "<EndToken ';' at {pos!r}>".format(pos=self.Start)


class IdentifierToken(VHDLToken):
	def __init__(self, stringToken):
		super().__init__(stringToken.PreviousToken, stringToken.Value, stringToken.Start, stringToken.End)

	def __str__(self):
		return "<Identifier '{value}' at {pos!r}>".format(value=self.Value, pos=self.Start)

class RepeatedIdentifierToken(IdentifierToken):
	def __str__(self):
		return "<RepeatedIdentifier '{value}' at {pos!r}>".format(value=self.Value, pos=self.Start)


class SimpleNameToken(VHDLToken):
	def __init__(self, stringToken):
		super().__init__(stringToken.PreviousToken, stringToken.Value, stringToken.Start, stringToken.End)

	def __str__(self):
		return "<SimpleName '{value}' at {pos!r}>".format(value=self.Value, pos=self.Start)


class LabelToken(VHDLToken):
	def __init__(self, stringToken):
		super().__init__(stringToken.PreviousToken, stringToken.Value, stringToken.Start, stringToken.End)

	def __str__(self):
		return "<Label '{value}' at {pos!r}>".format(value=self.Value, pos=self.Start)


class RepeatedLabelToken(LabelToken):
	def __str__(self):
		return "<RepeatedLabel '{value}' at {pos!r}>".format(value=self.Value, pos=self.Start)


class TwoCharKeyword(VHDLToken):
	__KEYWORD__ = None

	def __init__(self, characterToken):
		super().__init__(characterToken.PreviousToken, self.__KEYWORD__, characterToken.Start, characterToken.End)

	def __str__(self):
		return "<{className} '{value}' at {pos!r}>".format(
			className=self.__class__.__name__[:-7],
			value=self.__KEYWORD__,
			pos=self.Start
		)


class CommentKeyword(TwoCharKeyword):                         pass
class SingleLineCommentKeyword(CommentKeyword):               __KEYWORD__ = "--"
class MultiLineCommentKeyword(CommentKeyword):                pass
class MultiLineCommentStartKeyword(MultiLineCommentKeyword):  __KEYWORD__ = "/*"
class MultiLineCommentEndKeyword(MultiLineCommentKeyword):    __KEYWORD__ = "*/"

class AssignmentKeyword(TwoCharKeyword):                      pass
class VariableAssignmentKeyword(AssignmentKeyword):           __KEYWORD__ = ":="
class SignalAssignmentKeyword(AssignmentKeyword):             __KEYWORD__ = "<="

class RelationalOperator: pass
class EqualOperatorKeyword(VHDLToken):                        __KEYWORD__ = "="
class UnequalOperatorKeyword(VHDLToken):                      __KEYWORD__ = "/="
class LessThanOperatorKeyword(VHDLToken):                     __KEYWORD__ = "<"
class LessThanOrEqualOperatorKeyword(VHDLToken):              __KEYWORD__ = "<="
class GreaterThanOperatorKeyword(VHDLToken):                  __KEYWORD__ = ">"
class GreaterThanOrEqualOperatorKeyword(VHDLToken):           __KEYWORD__ = ">="
class MatchingEqualOperatorKeyword(VHDLToken):                __KEYWORD__ = "?="
class MatchingUnequalOperatorKeyword(VHDLToken):              __KEYWORD__ = "?/="
class MatchingLessThanOperatorKeyword(VHDLToken):             __KEYWORD__ = "?<"
class MatchingLessThanOrEqualOperatorKeyword(VHDLToken):      __KEYWORD__ = "?<="
class MatchingGreaterThanOperatorKeyword(VHDLToken):          __KEYWORD__ = "?>"
class MatchingGreaterThanOrEqualOperatorKeyword(VHDLToken):   __KEYWORD__ = "?>="


class KeywordToken(VHDLToken):
	__KEYWORD__ = None

	def __init__(self, stringToken):
		if (not (isinstance(stringToken, StringToken) and (stringToken <= self.__KEYWORD__))):
			raise TokenParserException("Expected keyword {0}.".format(self.__KEYWORD__.upper()), stringToken)
		super().__init__(stringToken.PreviousToken, self.__KEYWORD__, stringToken.Start, stringToken.End)

	def __str__(self):
		return "<Keyword: {0}>".format(self.__KEYWORD__.upper())

class DirectionKeyword(KeywordToken): pass

class OperatorKeyword(KeywordToken): pass
class LogicalOperatorKeyword(OperatorKeyword): pass
class MiscellaneousOperatorKeyword(OperatorKeyword): pass
class ShiftOperatorKeyword(OperatorKeyword): pass

class AbsKeyword(KeywordToken):             __KEYWORD__ = "abs"
class AccessKeyword(KeywordToken):          __KEYWORD__ = "access"
class AfterKeyword(KeywordToken):           __KEYWORD__ = "after"
class AliasKeyword(KeywordToken):           __KEYWORD__ = "alias"
class AllKeyword(KeywordToken):             __KEYWORD__ = "all"
class AndKeyword(LogicalOperatorKeyword):   __KEYWORD__ = "and"
class ArchitectureKeyword(KeywordToken):    __KEYWORD__ = "architecture"
class ArrayKeyword(KeywordToken):           __KEYWORD__ = "array"
class AssertKeyword(KeywordToken):          __KEYWORD__ = "assert"
class AttributeKeyword(KeywordToken):       __KEYWORD__ = "attribute"
class BeginKeyword(KeywordToken):           __KEYWORD__ = "begin"
class BlockKeyword(KeywordToken):           __KEYWORD__ = "block"
class BodyKeyword(KeywordToken):            __KEYWORD__ = "body"
class BufferKeyword(KeywordToken):          __KEYWORD__ = "buffer"
class BusKeyword(KeywordToken):             __KEYWORD__ = "bus"
class CaseKeyword(KeywordToken):            __KEYWORD__ = "case"
class ComponentKeyword(KeywordToken):       __KEYWORD__ = "component"
class ConfigurationKeyword(KeywordToken):   __KEYWORD__ = "configuration"
class ConstantKeyword(KeywordToken):        __KEYWORD__ = "constant"
class ContextKeyword(KeywordToken):         __KEYWORD__ = "context"
class DefaultKeyword(KeywordToken):         __KEYWORD__ = "default"
class DisconnectKeyword(KeywordToken):      __KEYWORD__ = "disconnect"
class DowntoKeyword(DirectionKeyword):      __KEYWORD__ = "downto"
class ElseKeyword(KeywordToken):            __KEYWORD__ = "else"
class ElsIfKeyword(KeywordToken):           __KEYWORD__ = "elsif"
class EndKeyword(KeywordToken):             __KEYWORD__ = "end"
class EntityKeyword(KeywordToken):          __KEYWORD__ = "entity"
class ExitKeyword(KeywordToken):            __KEYWORD__ = "exit"
class FileKeyword(KeywordToken):            __KEYWORD__ = "file"
class ForKeyword(KeywordToken):             __KEYWORD__ = "for"
class ForceKeyword(KeywordToken):           __KEYWORD__ = "force"
class FunctionKeyword(KeywordToken):        __KEYWORD__ = "function"
class GenerateKeyword(KeywordToken):        __KEYWORD__ = "generate"
class GenericKeyword(KeywordToken):         __KEYWORD__ = "generic"
class GroupKeyword(KeywordToken):           __KEYWORD__ = "group"
class GuardedKeyword(KeywordToken):         __KEYWORD__ = "guarded"
class IfKeyword(KeywordToken):              __KEYWORD__ = "if"
class IsKeyword(KeywordToken):              __KEYWORD__ = "is"
class InKeyword(KeywordToken):              __KEYWORD__ = "in"
class InoutKeyword(KeywordToken):           __KEYWORD__ = "inout"
class ImpureKeyword(KeywordToken):          __KEYWORD__ = "impure"
class InertialKeyword(KeywordToken):        __KEYWORD__ = "inertial"
class LableKeyword(KeywordToken):           __KEYWORD__ = "lable"
class LibraryKeyword(KeywordToken):         __KEYWORD__ = "library"
class LinkageKeyword(KeywordToken):         __KEYWORD__ = "linkage"
class LiteralKeyword(KeywordToken):         __KEYWORD__ = "literal"
class LoopKeyword(KeywordToken):            __KEYWORD__ = "loop"
class MapKeyword(KeywordToken):             __KEYWORD__ = "map"
class NandKeyword(LogicalOperatorKeyword):  __KEYWORD__ = "nand"
class NewKeyword(KeywordToken):             __KEYWORD__ = "new"
class NextKeyword(KeywordToken):            __KEYWORD__ = "next"
class NorKeyword(LogicalOperatorKeyword):   __KEYWORD__ = "nor"
class NotKeyword(KeywordToken):             __KEYWORD__ = "not"
class NullKeyword(KeywordToken):            __KEYWORD__ = "null"
class OfKeyword(KeywordToken):              __KEYWORD__ = "of"
class OnKeyword(KeywordToken):              __KEYWORD__ = "on"
class OpenKeyword(KeywordToken):            __KEYWORD__ = "open"
class OrKeyword(LogicalOperatorKeyword):    __KEYWORD__ = "or"
class OthersKeyword(KeywordToken):          __KEYWORD__ = "others"
class OutKeyword(KeywordToken):             __KEYWORD__ = "out"
class PackageKeyword(KeywordToken):         __KEYWORD__ = "package"
class ParameterKeyword(KeywordToken):       __KEYWORD__ = "parameter"
class PortKeyword(KeywordToken):            __KEYWORD__ = "port"
class PostponendKeyword(KeywordToken):      __KEYWORD__ = "postponend"
class ProcedureKeyword(KeywordToken):       __KEYWORD__ = "procedure"
class ProcessKeyword(KeywordToken):         __KEYWORD__ = "process"
class PropertyKeyword(KeywordToken):        __KEYWORD__ = "property"
class ProtectedKeyword(KeywordToken):       __KEYWORD__ = "protected"
class PureKeyword(KeywordToken):            __KEYWORD__ = "pure"
class RangeKeyword(KeywordToken):           __KEYWORD__ = "range"
class RecordKeyword(KeywordToken):          __KEYWORD__ = "record"
class RegisterKeyword(KeywordToken):        __KEYWORD__ = "register"
class RejectKeyword(KeywordToken):          __KEYWORD__ = "reject"
class ReleaseKeyword(KeywordToken):         __KEYWORD__ = "release"
class ReportKeyword(KeywordToken):          __KEYWORD__ = "report"
class ReturnKeyword(KeywordToken):          __KEYWORD__ = "return"
class RolKeyword(ShiftOperatorKeyword):     __KEYWORD__ = "rol"
class RorKeyword(ShiftOperatorKeyword):     __KEYWORD__ = "ror"
class SelectKeyword(KeywordToken):          __KEYWORD__ = "select"
class SequenceKeyword(KeywordToken):        __KEYWORD__ = "sequence"
class SeverityKeyword(KeywordToken):        __KEYWORD__ = "severity"
class SharedKeyword(KeywordToken):          __KEYWORD__ = "shared"
class SignalKeyword(KeywordToken):          __KEYWORD__ = "signal"
class SlaKeyword(ShiftOperatorKeyword):     __KEYWORD__ = "sla"
class SllKeyword(ShiftOperatorKeyword):     __KEYWORD__ = "sll"
class SraKeyword(ShiftOperatorKeyword):     __KEYWORD__ = "sra"
class SrlKeyword(ShiftOperatorKeyword):     __KEYWORD__ = "srl"
class SubtypeKeyword(KeywordToken):         __KEYWORD__ = "subtype"
class ThenKeyword(KeywordToken):            __KEYWORD__ = "then"
class ToKeyword(DirectionKeyword):          __KEYWORD__ = "to"
class TransportKeyword(KeywordToken):       __KEYWORD__ = "transport"
class TypeKeyword(KeywordToken):            __KEYWORD__ = "type"
class UnitsKeyword(KeywordToken):           __KEYWORD__ = "units"
class UntilKeyword(KeywordToken):           __KEYWORD__ = "until"
class UseKeyword(KeywordToken):             __KEYWORD__ = "use"
class UnbufferedKeyword(KeywordToken):      __KEYWORD__ = "unbuffered"
class VariableKeyword(KeywordToken):        __KEYWORD__ = "variable"
class VunitKeyword(KeywordToken):           __KEYWORD__ = "vunit"
class WaitKeyword(KeywordToken):            __KEYWORD__ = "wait"
class WhenKeyword(KeywordToken):            __KEYWORD__ = "when"
class WhileKeyword(KeywordToken):           __KEYWORD__ = "while"
class WithKeyword(KeywordToken):            __KEYWORD__ = "with"
class XorKeyword(LogicalOperatorKeyword):   __KEYWORD__ = "xor"
class XnorKeyword(LogicalOperatorKeyword):  __KEYWORD__ = "xnor"
