basic_types = ['boolean', 'byte', 'char', 'double', 'float', 'int', 'long', 'short', 'String']


class MethodParameter:
    def __init__(self, variable_type, variable_name, varargs):
        self.__type = variable_type
        self.__variable = variable_name
        self.__varargs = varargs

    @property
    def type(self) -> str:
        """Returns the type."""
        return self.__type

    @property
    def variable_name(self) -> str:
        """Returns the variable name."""
        return self.__variable

    @property
    def varargs(self) -> bool:
        """Returns true if varargs"""
        return self.__varargs
