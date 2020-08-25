from typing import List
from RepoManager.data.file import AnalyzedFile
from RepoManager.data.methods import ModifiedMethod
from RepoManager.data.matchedFiles import MatchedAnalyzedFiles
import re


class AnalyzedCommit:
    def __init__(self, commit, files):
        self.__commit = commit
        self.__files = files
        self.__CalculateChangeFrequency(self.__files)
        self.__matched_files = self.__CalculateMatchedFiles(self.analyzed_production_files,
                                                            self.analyzed_test_files,)

    @property
    def hash(self) -> str:
        """Return commits hash."""
        return self.__commit.hash

    @property
    def analyzed_files(self) -> List[AnalyzedFile]:
        """Returns list of analysed file."""
        return self.__files

    @property
    def analyzed_production_files(self) -> List[AnalyzedFile]:
        """Returns a list of analyzed production files."""
        production_files = [x for x in self.__files if not x.is_test_file]
        return production_files

    @property
    def analyzed_test_files(self) -> List[AnalyzedFile]:
        """Returns a list of analysed test files."""
        test_files = [x for x in self.__files if x.is_test_file]
        return test_files

    @property
    def production_methods(self) -> List[ModifiedMethod]:
        """Returns a list of modified production methods."""
        production_methods = self.__GetAllModifiedMethods(self.analyzed_production_files)
        return production_methods

    @property
    def production_methods_count(self) -> int:
        """Returns number of production methods."""
        return len(self.production_methods)

    @property
    def test_methods(self) -> List[ModifiedMethod]:
        """Returns a list of modified test methods."""
        test_methods = self.__GetAllModifiedMethods(self.analyzed_test_files)
        return test_methods

    @property
    def test_methods_count(self) -> int:
        """Returns number of test methods"""
        return len(self.test_methods)

    @property
    def modified_methods(self) -> List[ModifiedMethod]:
        """Returns a list of all modified methods including production and test methods"""
        methods = self.__GetAllModifiedMethods(self.__files)
        return methods

    @property
    def modified_methods_count(self) -> int:
        """Returns number of all modified methods."""
        return len(self.modified_methods)

    @property
    def production_methods_ratio(self) -> float:
        """Returns ratio of production methods number divided by number of all methods."""
        if self.production_methods_count == 0:
            return 0
        else:
            return round(self.production_methods_count / self.modified_methods_count, 2)

    @property
    def test_methods_ratio(self) -> float:
        """Returns ratio of test methods number divided by number of all methods."""
        if self.test_methods_count == 0:
            return 0
        else:
            return round(self.test_methods_count / self.modified_methods_count, 2)

    @staticmethod
    def __GetAllModifiedMethods(files):
        modified_methods = []
        for file in files:
            for method in file.modified_methods:
                modified_methods.append(method)

        return modified_methods

    @staticmethod
    def __CalculateChangeFrequency(files):
        methods = []

        for file in files:
            for method in file.modified_methods:
                methods.append(method)

        for x in methods:
            x.change_frequency = sum(x.long_name == y.long_name for y in methods)

    @property
    def matched_files(self):
        """Returns list of matched files"""
        return self.__matched_files

    @property
    def related_files_changed(self):
        return True if len(self.matched_files) > 0 else False

    @staticmethod
    def __CalculateMatchedFiles(production_files, test_files):
        matched = []

        for production_file in production_files:
            regEx1 = r"" + production_file.file_name.lower().split(".")[0] + r"test.java"
            regEx2 = r"" + production_file.file_name.lower().split(".")[0] + r"testcase.java"
            regEx3 = r"" + production_file.file_name.lower().split(".")[0] + r"tests.java"

            for test_file in test_files:
                match1 = re.fullmatch(regEx1, test_file.file_name.lower())
                match2 = re.fullmatch(regEx2, test_file.file_name.lower())
                match3 = re.fullmatch(regEx3, test_file.file_name.lower())
                if match1 or match2 or match3:
                    matched.append(MatchedAnalyzedFiles(production_file, test_file))

        return matched

    @property
    def highest_code_churn(self):
        """Returns list of modified methods with highest code churn"""
        methods = self.__GetRecommendedMethods(self.production_methods, 5, True)
        return methods

    @property
    def highest_change_frequency(self):
        """Returns list of modified methods with highest change frequency"""
        methods = self.__GetRecommendedMethods(self.production_methods, 5, False)
        return methods

    @staticmethod
    def __GetRecommendedMethods(methods, number, code_churn=True):
        """
        Returns a list of recommended methods.
        """
        recommended_methods = []
        filteredMethod = None

        if number > len(methods):
            print("number is bigger then identified methods")
            number = len(methods)

        for i in range(0, number):
            max_value = 0
            for method in methods:
                value = method.code_churn if code_churn else method.change_frequency
                if value > max_value:
                    max_value = value
                    filteredMethod = method

            methods = [x for x in methods if x.long_name != filteredMethod.long_name]
            recommended_methods.append(filteredMethod)

        return recommended_methods

    @property
    def ratio_modified_lines_by_methods(self) -> List[float]:
        changes = []
        for file in self.__files:
            if not file.is_test_file:
                changes.append(file.ratio_modified_lines)
        return changes

    @property
    def ratio_added_lines_by_methods(self) -> List[float]:
        changes = []
        for file in self.__files:
            if not file.is_test_file:
                changes.append(file.ratio_added_lines)
        return changes

    @property
    def ratio_deleted_lines_by_methods(self) -> List[float]:
        changes = []
        for file in self.__files:
            if not file.is_test_file:
                changes.append(file.ratio_deleted_lines)
        return changes

    @property
    def ratio_other_changes(self) -> List[float]:
        changes = []
        for file in self.__files:
            if not file.is_test_file:
                changes.append(file.ratio_other_changes)
        return changes

    @property
    def ratio_co_evolved_files(self) -> float:
        if len(self.analyzed_production_files) == 0:
            return 0
        else:
            if len(self.matched_files) == 0:
                return 0
            else:
                return len(self.matched_files) / len(self.analyzed_production_files)

    @property
    def ratio_not_co_evolved_files(self) -> float:
        if len(self.analyzed_production_files) == 0:
            return 0
        else:
            not_co_evolved = len(self.analyzed_production_files) - len(self.matched_files)
            return not_co_evolved / len(self.analyzed_production_files)
















