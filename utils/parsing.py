import javalang
import re
from javalang.parser import JavaSyntaxError
from javalang.tree import Literal, MemberReference, MethodInvocation, \
    BinaryOperation, TypeArgument, BasicType, VariableDeclarator, \
    ClassCreator, MethodDeclaration, ConstructorDeclaration, FieldDeclaration

modifiers = ["public", "protected", "private", "static", "final", "native", "synchronized", "abstract"]


def ParseMethod(method):
    arguments = []
    try:
        signature = javalang.parse.parse_member_signature(method)
    except JavaSyntaxError:
        return None

    if isinstance(signature, FieldDeclaration):
        name = ""
    elif len(signature.parameters) > 0:
        name = signature.name
        for parameter in signature.parameters:
            arguments.append(parameter)
    else:
        name = signature.name

    if isinstance(signature, MethodDeclaration):
        if signature.return_type is None:
            return_type = "void"
        else:
            return_type = signature.return_type.name
    elif isinstance(signature, ConstructorDeclaration):
        return_type = "class"
    else:
        return_type = None

    return {"name": name,
            "modifiers": signature.modifiers,
            "return_type": return_type,
            "arguments": arguments}


def ParseTestMethod(source_code):
    local_variables = []
    methods = []
    classes = []

    if "@Test" in source_code:
        try:
            tree = javalang.parse.parse_member_signature(source_code)
        except JavaSyntaxError:
            return None

        for path, node in tree.filter(javalang.tree.MethodInvocation):
            methods.append(__ParseMethodInvocation(node))

        for path, node in tree.filter(javalang.tree.ClassCreator):
            classes.append(__ParseClassCreator(node))

        for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
            local_variables.append(__ParseLocalVariable(node))

        return {"variables": local_variables,
                "methods": methods,
                "classes": classes}


def __ParseMethodInvocation(node):
    arguments = []
    if len(node.arguments) > 0:
        for argument in node.arguments:
            if isinstance(argument, Literal):
                arguments.append((argument.value, "Literal"))
            elif isinstance(argument, MemberReference):
                arguments.append((argument.member, "MemberReference"))
            elif isinstance(argument, MethodInvocation):
                arguments.append((argument.member, "MethodInvocation"))
            elif isinstance(argument, BinaryOperation):
                operation, types = __ParseBinaryOperation(argument.operandl,
                                                          argument.operandr)
                arguments.append((operation, types))
            elif isinstance(argument, ClassCreator):
                arguments.append((argument.type.name, "ClassCreator"))

    return {"name": node.member,
            "qualifier": node.qualifier,
            "arguments": arguments}


def __ParseBinaryOperation(left, right):
    operand_left = ""
    operand_right = ""
    types = []

    if isinstance(left, Literal) and isinstance(right, MemberReference):
        operand_left = left.value
        operand_right = right.member
        types.append(("Literal", "MemberReference"))
    elif isinstance(left, MemberReference) and isinstance(right, Literal):
        operand_left = left.member
        operand_right = right.value
        types.append(("MemberReference", "Literal"))

    return operand_left + " + " + operand_right, types


def __ParseClassCreator(node):
    arguments = []
    type_arguments = []

    if len(node.arguments) == 0:
        if node.type.arguments is not None and len(node.type.arguments) > 0:
            for argument in node.type.arguments:
                if isinstance(argument, TypeArgument):
                    type_arguments.append((argument.type.name,
                                           "TypeArgument"))

    else:
        for argument in node.arguments:
            if isinstance(argument, MemberReference):
                arguments.append((argument.member, "MemberReference"))

        if node.type.arguments is not None and len(node.type.arguments) > 0:
            for type_argument in node.type.arguments:
                if isinstance(type_argument, TypeArgument):
                    type_arguments.append((type_argument.type.name,
                                           "TypeArgument"))

    return {"name": node.type.name,
            "arguments": arguments,
            "type_arguments": type_arguments}


def __ParseLocalVariable(node):
    declarator = []
    qualifier = []

    if isinstance(node.declarators[0], VariableDeclarator):
        if isinstance(node.declarators[0].initializer, MethodInvocation):
            declarator.append((node.declarators[0].initializer.member,
                               "MethodInvocation"))
        elif isinstance(node.declarators[0].initializer, ClassCreator):
            declarator.append((node.declarators[0].initializer.type.name,
                               "ClassCreator"))

    if isinstance(node.type, BasicType):
        qualifier.append((node.type, "BasicType"))
    # else:
    # if node.type.arguments is not None and len(node.type.arguments) > 0:
    # for argument in node.type.arguments:
    # if isinstance(argument, TypeArgument):
    # print("node.type.name:", node.type.name)
    # print("argumemt.type.name:", argument.type.name)
    # qualifier.append((node.type.name, argument.type.name,
    #                 "TypeArgument"))
    # else:
    # qualifier.append(node.type.name)

    return {"name": node.declarators[0].name,
            "qualifier": qualifier,
            "declaratores": declarator}


def GetReturnTypeMethod(signature):
    """Parses the methods signature to extract the return type"""
    try:
        method_signature = javalang.parse.parse_member_signature(signature)
    except JavaSyntaxError:
        return None

    if method_signature.return_type is None:
        return_type = "void"
    else:
        return_type = method_signature.return_type.name

    return return_type


def GetAccessModifier(signature):
    """Parses the method signature to extract the access modifiers."""
    access_modifiers = []
    try:
        method_signature = javalang.parse.parse_member_signature(signature)
    except JavaSyntaxError:
        return None

    if isinstance(method_signature, MethodDeclaration):
        for x in method_signature.modifiers:
            access_modifiers.append(x)
    else:
        for x in modifiers:
            match = re.search(x, signature)
            if match:
                access_modifiers.append(x)

    return access_modifiers


def GetMethodName(signature):
    """Parses the method signature to extract the method name."""
    try:
        method_signature = javalang.parse.parse_member_signature(signature)
    except JavaSyntaxError:
        return None

    if isinstance(method_signature, MethodDeclaration):
        name = method_signature.name
    else:
        name = None

    return name
