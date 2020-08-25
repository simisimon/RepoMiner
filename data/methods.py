from data.modificationTypes import ModificationType
from utils.parsing import ParseMethod, ParseTestMethod
from typing import List, Tuple
import difflib
import re

java_test_annotations = ["@BeforeClass", "@AfterClass", "@Before", "@After", "@Test", "@Parameters",
                         "@ParameterizedTest", "@MethodSource"]

qualifiers = ["public", "static", "final", "protected"]


class Method:
    """
    This class represents a method that contains various informations.
    """
    def __init__(self, func, sourceCode, commitInfo):
        self.name = func.name
        self.long_name = func.long_name
        self.parameters = func.parameters
        self.start_line = func.start_line
        self.end_line = func.end_line
        self.length = func.length
        self.source_code = sourceCode
        self.file_name = func.name.split("::")[0] + ".java"
        self.test_method = self.__IsTestMethod(self.source_code)
        self.commit = commitInfo

    @staticmethod
    def __IsTestMethod(source_code) -> bool:
        lines = source_code.splitlines()
        for line in lines:
            if any(annotation in line for annotation in java_test_annotations):
                return True

        return False

    @property
    def code_lines(self) -> List[Tuple[int, str]]:
        """Returns a list of code lines corresponding to (line number, actual line)."""
        code_lines = self.__CalculateCodeLines()
        return code_lines

    def __CalculateCodeLines(self) -> List[Tuple[int, str]]:
        lines = self.source_code.splitlines()
        lineNumber = self.start_line
        code_lines = []

        for line in lines:
            line = line.rstrip()
            if any(x in line for x in java_test_annotations):
                if any(y in line for y in qualifiers):
                    code_lines.append((lineNumber, line))
                    lineNumber = lineNumber + 1
            else:
                code_lines.append((lineNumber, line))
                lineNumber = lineNumber + 1

        return code_lines

    @property
    def signature(self) -> str:
        """Returns the signature of a method."""
        lines = self.source_code.splitlines()
        signature = lines[0] if not any(annotation in lines[0] for annotation in java_test_annotations) else \
            lines[1]
        return signature

    @property
    def method_body(self) -> str:
        """Returns the body of a method."""
        method_body = ""
        match = re.findall(r'{(.+)}', self.source_code, re.S)
        for x in match:
            method_body += x

        return method_body


class ModifiedMethod(Method):
    """
    This class represents a modified methods that contains various information about the modifications
    """
    def __init__(self, methodBefore=None, methodAfter=None, modificationType=None, ratio=None, lines=None):
        if methodAfter is not None and methodBefore is not None:
            super().__init__(methodAfter, methodAfter.source_code, methodAfter.commit)
            self.__source_code_after = methodAfter.source_code
            self.__source_code_before = methodBefore.source_code
        elif methodAfter is not None and methodBefore is None:
            super().__init__(methodAfter, methodAfter.source_code, methodAfter.commit)
            self.__source_code_after = methodAfter.source_code
            self.__source_code_before = ""
        elif methodAfter is None and methodBefore is not None:
            super().__init__(methodBefore, methodBefore.source_code, methodBefore.commit)
            self.__source_code_after = ""
            self.__source_code_before = methodBefore.source_code
        elif methodAfter is None and methodBefore is None:
            raise SystemExit("methodAfter and methodBefore are none")

        self._type = modificationType

        if lines is not None:
            self.__added_lines_from_diff = lines[0]
            self.__deleted_lines_from_diff = lines[1]

        # TODO: summarize to properties?
        if modificationType == ModificationType.RENAMED.name:
            self.old_name = methodBefore.name
            self.old_long_name = methodBefore.long_name
            self.old_signature = methodBefore.signature
            self.multiple_renamed = False
            self.renamed_methods = []

        if ratio is not None:
            self.ratio_signature = ratio[0]
            self.ratio_method_body = ratio[1]

        self.__change_frequency = 0
        self.__added, self.__added_lines = self.__CalculateLines(methodAfter, self.__added_lines_from_diff)
        self.__deleted, self.__deletedLines = self.__CalculateLines(methodBefore, self.__deleted_lines_from_diff)
        self.__code_churn = self.__added + self.__deleted

    def __GetDiffLines(self, methodBefore, methodAfter):
        sourceCodeBefore = methodBefore.strip().splitlines()
        sourceCodeAfter = methodAfter.strip().splitlines()

        diff = difflib.unified_diff(sourceCodeBefore, sourceCodeAfter, fromfile=self.file_name, tofile=self.file_name,
                                    lineterm='')
        lines = list(diff)[2:]
        return lines

    @property
    def source_code_before(self) -> str:
        return self.__source_code_before

    @property
    def change_frequency(self) -> int:
        """Returns the change frequency."""
        return self.__change_frequency

    @change_frequency.setter
    def change_frequency(self, value):
        """Sets the change frequency."""
        self.__change_frequency = value

    @property
    def type(self) -> str:
        """Returns the change type."""
        if self._type is not None:
            return self._type
        else:
            return ModificationType.UNKOWN.name

    @property
    def diff(self) -> str:
        diff = ""
        lines = self.__GetDiffLines(self.__source_code_before, self.__source_code_after)
        for line in lines:
            if not line.startswith('@@'):
                diff = diff + line + "\n"
        return diff

    @property
    def added_lines(self) -> List[str]:
        return self.__added_lines

    @property
    def added(self) -> int:
        return self.__added

    @property
    def deleted_lines(self) -> List[str]:
        return self.__deletedLines

    @property
    def deleted(self) -> int:
        return self.__deleted

    @property
    def code_churn(self) -> int:
        return self.__code_churn

    @code_churn.setter
    def code_churn(self, value):
        self.__code_churn = value

    @property
    def parsed_method(self):
        """
        If method is a test method return the a dict with test method informations
        else return dict with method informations.
        """
        if not self.test_method:
            return ParseMethod(self.source_code)
        else:
            return ParseTestMethod(self.source_code)

    @staticmethod
    def __CalculateLines(method, lines):
        counter = 0
        modified_lines = []
        if method is not None:
            code_lines = method.code_lines
            for code_line in code_lines:
                if code_line in lines:
                    counter += 1
                    modified_lines.append(code_line)

        return counter, modified_lines


class SummarizedMethod:
    def __init__(self, methods, isTestMethod):
        self.isTestMethod = isTestMethod
        if isTestMethod:
            self.test_methods = methods
            self.summarized_test_method = methods[-1]
        else:
            self.methods = methods
            self.summarized_production_method = methods[-1]

    @property
    def name(self) -> str:
        if self.isTestMethod:
            names = [x.long_name for x in self.test_methods]
        else:
            names = [x.long_name for x in self.methods]

        if len(set(names)) <= 1:
            name = list(set(names))[0]
            return name
        else:
            print("something went wrong")

    @property
    def summarized_method(self) -> Method:
        if self.isTestMethod:
            #code_churn = self.__CalculateCodeChurn(self.test_methods)
            test_method = self.test_methods[-1]
            #test_method.code_churn = code_churn
            return test_method
        else:
            #code_churn = self.__CalculateCodeChurn(self.methods)
            method = self.methods[-1]
            #method.code_churn = code_churn
            return method


