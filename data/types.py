from enum import Enum


class ModificationType(Enum):
    ADDED = 1
    DELETED = 2
    MODIFIED = 3
    RENAMED = 4
    NEWLY_ADDED = 5
    COMPLETELY_DELETED = 6
    UNKNOWN = 7


class RepoType(Enum):
    ALL_COMMITS = 1
    SINGLE_COMMIT = 2
    BETWEEN_COMMITS = 3
    DATETIME = 4
    ALL = 5
    FROM_COMMIT = 6


class Ratio(Enum):
    HIGH = 1  # Matched method name, matched number of param, matched param name with variable and matched param type
    MEDIUM = 2  # Matched method name, matched number of params, matched param name with variable but type doesnt match
    LOW = 3  # Matched method name, matched number of paras, param name not found as variable
    NO_MATCH = 4  # No match
