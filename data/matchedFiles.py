from typing import Dict, List, Tuple
from javalang.tree import BasicType
from data.methods import ModifiedMethod
from data.modificationTypes import Ratio


class MatchedFiles:
    """
    This class represents matched files and test files
    """

    def __init__(self, file_name, test_file_name, methods, test_methods):
        self.file_name = file_name
        self.test_file_name = test_file_name
        self.methods = methods
        self.test_methods = test_methods

    @property
    def matched_methods(self) -> Dict:
        """
        Returns dict of matched methods.
        """
        matched_methods = GetMethodsWithParsedData(self.methods, self.test_methods)
        matched_production_methods = set(method[0] for method in matched_methods)
        matched_test_methods = set(method[1] for method in matched_methods)

        result = {
            "matched_methods": matched_methods,
            "matched_production_methods": matched_production_methods,
            "matched_test_methods": matched_test_methods
        }
        return result


def GetMethodsWithParsedData(methods, test_methods) -> List[Tuple[ModifiedMethod, ModifiedMethod, Ratio]]:
    test_methods = [x for x in test_methods if "@Test" in x.source_code]
    matched_pairs = []

    for test_method in test_methods:
        # (test_method.source_code)
        test_method_parsed = test_method.parsed_method
        # print(test_method_parsed)
        for method in methods:
            method_parsed = method.parsed_method
            ratio = GetMatchedMethods(test_method_parsed, method_parsed)

            if ratio == Ratio.HIGH or ratio == Ratio.MEDIUM or ratio == Ratio.LOW:
                matched_pairs.append((method, test_method, ratio))
                # TODO: Best/ Good Practice => eine Testmethode testet eine Methode
                # wenn eine Testmethode mehrmals vorkommt, entscheiden, welche Übereinstimmung die richtige ist

    # print("len methods:", len(methods))
    matched_methods = set(x[0] for x in matched_pairs)
    # ("len matched methods:", len(matched_methods))
    # for x in matched_methods:
    # print(x.long_name)

    return matched_pairs


def GetMatchedMethods(test_method_parsed, method_parsed):
    test_methods = test_method_parsed["methods"]
    variables = test_method_parsed["variables"]
    if test_methods is None or method_parsed is None:
        return False, Ratio.NO_MATCH

    for x in test_methods:
        if x["name"] == method_parsed["name"]:
            if len(x["arguments"]) == len(method_parsed["arguments"]):
                # Case zero param:
                if len(method_parsed["arguments"]) == 0:
                    return Ratio.HIGH
                # Case: one parameter and multiple params true
                elif len(method_parsed["arguments"]) == 1 and method_parsed["arguments"][0].varargs:
                    return Ratio.NO_MATCH
                    #return Ratio.LOW
                # Case: one parameter and multiple param false
                elif len(method_parsed["arguments"]) == 1 and not method_parsed["arguments"][0].varargs:
                    # Case: One parameter and qualifier is an Object
                    if method_parsed["arguments"][0].type.name == "Object":
                        return Ratio.HIGH
                    # Case: entered parameter equals a string and method requires string
                    elif method_parsed["arguments"][0].type.name == "String":
                        if x["arguments"][0][0].startswith('"') and x["arguments"][0][0].endswith('"'):
                            return Ratio.HIGH
                    # Case: entered parameter equals a boolean and method requires boolean
                    elif method_parsed["arguments"][0].type.name == "boolean":
                        if x["arguments"][0][0] == "true" or x["arguments"][0][0] == "false":
                            return Ratio.HIGH
                    # Case: cover remaining cases
                    else:
                        ratio = CompareArgumentByType(method_parsed, variables, x)
                        return ratio
                # Multiple Params
                else:
                    ratio = CheckType(method_parsed["arguments"], x["arguments"])
                    if ratio == Ratio.HIGH:
                        return Ratio.HIGH
                    else:
                        # TODO: andere Cases betrachten
                        return Ratio.LOW
            elif len(x["arguments"]) != len(method_parsed["arguments"]):
                for arg in method_parsed["arguments"]:
                    if arg.varargs:
                        return Ratio.LOW


def CheckType(args, method_tested_args):
    match = []

    for method_arg, method_tested_arg in zip(args, method_tested_args):
        if method_arg.type.name == "Object":
            match.append(True)
        elif method_arg.type.name == "String":
            if method_tested_arg[0].startswith('"') and method_tested_arg[0].endswith('"'):
                match.append(True)
            else:
                match.append(False)
        elif method_arg.type.name == "boolean":
            if method_tested_arg[0] == "true" or method_tested_arg[0] == "false":
                match.append(True)
            else:
                match.append(False)
        else:
            match.append(False)

    if all(x == True for x in match):
        return Ratio.HIGH
    else:
        return Ratio.LOW


def CompareArgumentByType(method_parsed, variables, method_tested):
    args = []
    method_arg = method_parsed["arguments"][0]
    args.append(method_arg.type.name)
    # TODO:  if method_arg.type.arguments is not None: AttributeError: 'BasicType' object has no attribute 'arguments'
    if isinstance(method_arg.type, BasicType):
        print("method arg:", method_arg.type)
    elif method_arg.type.arguments is not None:
        for argument in method_arg.type.arguments:
            if argument.type is not None:
                args.append(argument.type.name)

    for variable in variables:
        if method_tested["arguments"][0][0] == variable["name"]:
            for arg in args:
                if len(variable["qualifier"]) > 0:
                    if arg in variable["qualifier"][0]:
                        return Ratio.HIGH
                    return Ratio.MEDIUM
                else:
                    return Ratio.LOW

    return Ratio.LOW


class NotMatchedFiles:
    """
    This class represent not matched files
    """

    def __init__(self, files, test_files, file_methods, test_file_methods):
        self.files = files
        self.test_files = test_files
        self.methods = file_methods
        self.test_methods = test_file_methods


class MatchedAnalyzedFiles:
    def __init__(self, production_file, test_file):
        self.production_file = production_file
        self.production_file_name = production_file.file_name
        self.production_methods = production_file.modified_methods
        self.test_file = test_file
        self.test_file_name = test_file.file_name
        self.test_methods = test_file.modified_methods

    @property
    def matched_methods(self) -> List[Tuple[ModifiedMethod, ModifiedMethod, Ratio]]:
        matched_methods = GetMethodsWithParsedData(self.production_methods, self.test_methods)
        return matched_methods

    @property
    def not_matched_methods(self) -> List[ModifiedMethod]:
        matched_methods = self.matched_methods
        methods = [x[0] for x in matched_methods]
        return [x for x in self.production_methods if x not in methods]


class NotMatchedAnalyzedFiles:
    def __init__(self, production_files, test_files):
        self.production_files = production_files
        self.test_files = test_files
