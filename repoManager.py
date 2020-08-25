from typing import Any, Optional
from pydriller import RepositoryMining, GitRepository
from data.modificationTypes import RepoType, ModificationType
from data.methods import Method, ModifiedMethod, SummarizedMethod
from data.matchedFiles import MatchedFiles, NotMatchedFiles, MatchedAnalyzedFiles, NotMatchedAnalyzedFiles
from data.file import AnalyzedFile
from data.commit import AnalyzedCommit
from dateutil import parser
from typing import List
import Levenshtein
import re
import time

java_test_annotations = ["@BeforeClass", "@AfterClass", "@Before", "@After", "@Test", "@Parameters",
                         "@ParameterizedTest", "@MethodSource", "import org.junit"]

JAVA_FILE_SUFFIX = '.java'


class RepoManager:
    """
    This class represents a repoManager for analysing a repository.
    """

    def __init__(self, repoURL, first=None, second=None, fromCommit=None, since=None, to=None):
        start = time.perf_counter()
        self.__gitRepo = GitRepository(repoURL)

        if first is not None and second is not None and since is None and to is None:
            self.repo = RepositoryMining(repoURL, from_commit=first, to_commit=second)
            self.__repo_type = RepoType.BETWEEN_COMMITS
        elif first is not None and second is None and since is None and to is None:
            self.repo = RepositoryMining(repoURL, single=first)
            self.__repo_type = RepoType.SINGLE_COMMIT
        elif first is None and second is None and since is not None and to is not None:
            try:
                date1 = parser.parse(since)
                date2 = parser.parse(to)
                self.repo = RepositoryMining(repoURL, since=date1, to=date2)
                self.__repo_type = RepoType.DATETIME
            except Exception:
                raise Exception("Entered Datetime is not valid.")
        elif fromCommit is not None:
            self.repo = RepositoryMining(path_to_repo=repoURL, from_commit=fromCommit)
            print("from commit")
        else:
            print("all commits")
            self.repo = RepositoryMining(path_to_repo=repoURL)

        print("repoManager was created")

        self.__files = []  # number of analyzed files
        self.__files_with_methods = []
        self.__test_files = []  # number of test files
        self.__production_files = []  # number of production files
        self.__commits = []  # List[str] of analysed commits hash
        self.__commits_with_modified_methods = set()  # List[str] of analysed commits with modified methods hash
        self.__production_methods = []  # List[ModifiedMethods]
        self.__test_methods = []  # List[ModifiedMethods]
        self.__modified_methods = []  # List[ModifiedMethods]
        self.__moved_files_without_changes = []  # List of files without changes
        self.__analyzed_commits = []  # List[AnalyzedCommits]
        self.__matched_files = []  # List of matched files
        self.__not_matched_files = None  # instance of NotMatchedFiles
        self.__GetModifications()  # performs analysis
        end = time.perf_counter()
        self.__analyse_time = "{:.2f}".format((end - start) / 60)  # analysis performing time

    @property
    def analyze_time(self):
        """Returns time for analysis."""
        return self.__analyse_time

    @property
    def repo_type(self) -> RepoType:
        """
        Returns the repo type.
        """
        return self.__repo_type

    @property
    def project_name(self) -> str:
        """
        Returns the project name.
        """
        return self.__gitRepo.project_name

    @property
    def modified_methods_count(self) -> int:
        """
        Returns the number of all methods including the test methods.
        """
        # count = self.__CalculateMethodsCount(self.__all_methods_data)
        return len(self.__modified_methods)

    @property
    def production_methods_count(self) -> int:
        """
        Returns the number of methods excluding the test methods.
        """
        # count = self.__CalculateMethodsCount(self.__methods_data)
        return len(self.__production_methods)

    @property
    def test_methods_count(self) -> int:
        """
        Returns the number of test methods.
        """
        # count = self.__CalculateMethodsCount(self.__test_methods_data)
        return len(self.__test_methods)

    @property
    def files(self) -> int:
        """
        Returns number of analysed files that contain modified methods.
        """
        return len(self.__files)

    @property
    def unique_files(self):
        files = set(x for x in self.__files)
        return len(files)

    @property
    def test_files(self) -> int:
        """
        Returns the number of test files.
        """
        return len(self.__test_files)

    @property
    def unique_test_files(self):
        files = set(x for x in self.__test_files)
        return len(files)

    @property
    def production_files(self) -> int:
        """Returns number of production files."""
        return len(self.__production_files)

    @property
    def unique_production_files(self):
        files = set(x for x in self.__production_files)
        return len(files)

    @property
    def files_with_methods(self):
        """Returns number of analyzed files that contain methods."""
        return len(self.__files_with_methods)

    @property
    def unique_files_with_methods(self):
        """Returns number of unique analyzed files that contain methods."""
        files = set(x for x in self.__files_with_methods)
        return len(files)

    @property
    def commits(self) -> int:
        """Returns the number of commits."""
        count = len(self.__commits)
        return count

    @property
    def commits_with_modified_methods(self) -> int:
        """Returns the number of commits with modified methods."""
        count = len(self.__commits_with_modified_methods)
        return count

    @property
    def moved_files(self):
        """Returns a list of moves files without changes."""
        return self.__moved_files_without_changes

    @property
    def modified_methods(self) -> List[ModifiedMethod]:
        """Returns a list of all methods including the test methods."""
        return self.__modified_methods

    @property
    def production_methods(self) -> List[ModifiedMethod]:
        """Returns a list of only methods."""
        return self.__production_methods

    @property
    def highest_code_churn_methods(self) -> List[ModifiedMethod]:
        """Returns a list of recommended methods."""
        recommended_methods = self.GetRecommendedMethods(self.production_methods, 10, True)
        return recommended_methods

    @property
    def highest_change_frequency_methods(self) -> List[ModifiedMethod]:
        """Returns a list of recommended methods."""
        recommended_methods = self.GetRecommendedMethods(self.production_methods, 10, False)
        return recommended_methods

    @property
    def test_methods(self) -> List[ModifiedMethod]:
        """Returns a list of only test methods."""
        return self.__test_methods

    @property
    def matched_files(self) -> List[MatchedFiles]:
        """Returns a list of matched files between file and test file."""
        return self.__matched_files

    @property
    def matched_files_count(self) -> int:
        """Returns the number of matched files."""
        return len(self.__matched_files)

    @property
    def not_matched_files(self) -> NotMatchedFiles:
        """Returns a not matched file object of the analyze."""
        return self.__not_matched_files

    @property
    def summarized_production_methods(self) -> List[SummarizedMethod]:
        """Summarizes all instances of the same production method. Returns summarized production methods."""
        return self.SummarizeMethods(self.production_methods)

    @property
    def summarized_test_methods(self) -> List[SummarizedMethod]:
        """Summarizes all instances of the same test method. Returns summarized test methods."""
        return self.SummarizeMethods(self.test_methods, True)

    @property
    def analyzed_commits(self):
        """Returns a list of analyzed commits"""
        return self.__analyzed_commits

    def __GetModifications(self):
        """Return modified methods. (commit hash, file name, methods)"""

        print("analyze commits")
        for commit in self.repo.traverse_commits():
            commit_hash = commit.hash
            analyzed_files = []
            self.__commits.append(commit.hash)
            for file in commit.modifications:
                if JAVA_FILE_SUFFIX in file.filename:
                    print(commit.hash, file.filename)
                    self.__files.append(file.filename)
                    if file.source_code is None and file.source_code_before is None:
                        self.__moved_files_without_changes.append((commit.hash, file))
                    elif self.IsTestFile(file):
                        self.__test_files.append(file.filename)
                        test_methods = self.__AnalyseFile(file, True, commit_hash)
                        analyzed_files.append(AnalyzedFile(commit.hash, file, True, test_methods))
                        for method in test_methods:
                            self.__test_methods.append(method)
                            self.__modified_methods.append(method)
                    else:
                        self.__production_files.append(file.filename)
                        methods = self.__AnalyseFile(file, False, commit_hash)
                        analyzed_files.append(AnalyzedFile(commit.hash, file, False, methods))
                        for method in methods:
                            self.__production_methods.append(method)
                            self.__modified_methods.append(method)

            self.__analyzed_commits.append(AnalyzedCommit(commit, analyzed_files))

        self.__CalculateFrequencyOfChanges(self.__modified_methods)
        self.__GetMatchedFiles()
        # self.__GetMultipleTimesRenamedMethods()

    @staticmethod
    def IsTestFile(file) -> bool:
        files = re.findall(r'(test.java)|(tests.java)', file.filename.lower())
        imports = re.findall(r'org.junit.*',
                                      file.source_code.lower()) if file.source_code is not None else False
        path = re.findall(r'src\\test', file.new_path.lower()) if file.new_path is not None else False

        after = any(annotation in file.source_code for annotation in java_test_annotations) if \
            file.source_code is not None else False
        before = any(annotation in file.source_code_before for annotation in java_test_annotations) if \
            file.source_code_before is not None else False

        if file.source_code is not None and file.source_code_before is not None:
            if files or imports or path or before or after:
                return True
        elif file.source_code is not None and file.source_code_before is None:
            if files or imports or path or after:
                return True
        elif file.source_code is None and file.source_code_before is not None:
            if files or imports or path or before:
                return True

        return False

    def __AnalyseFile(self, file, isTestFile, commit_hash) -> List[ModifiedMethod]:
        """Analyzes a file and returns a list of modified methods."""

        deleted_lines, added_lines = self.GetLinesFromDiff(file)
        lines = [added_lines, deleted_lines]

        sourceCodeAfter = self.StoreSourceCodeAsLines(file.source_code)
        sourceCodeBefore = self.StoreSourceCodeAsLines(file.source_code_before)

        methodsAfter = self.GetMethods(file.methods, sourceCodeAfter, isTestFile, commit_hash)
        methodsBefore = self.GetMethods(file.methods_before, sourceCodeBefore, isTestFile, commit_hash)

        if file.change_type.name == "ADD":
            methods = self.GetAddedOrDeletedMethods(methodsAfter, ModificationType.NEWLY_ADDED, lines)

        elif file.change_type.name == "DELETE":
            methods = self.GetAddedOrDeletedMethods(methodsBefore, ModificationType.COMPLETELY_DELETED, lines)

        elif file.change_type.name == "RENAME":
            methods = self.GetModifiedMethods(methodsBefore, methodsAfter, lines,
                                              file.change_type.name)

        elif file.change_type.name == "MODIFY":
            methods = self.GetModifiedMethods(methodsBefore, methodsAfter, lines)

        else:
            methods = []

        if len(methods) > 0:
            self.__files_with_methods.append(file.filename)
            self.__commits_with_modified_methods.add(commit_hash)

        return methods

    @staticmethod
    def GetModifiedMethods(methodsBefore, methodsAfter, lines, fileType=None):
        """Return list of modified methods"""

        modifiedMethodsBefore = []
        modifiedMethodsAfter = []
        modifiedMethods = []

        # mapping deleted lines and methodsBefore and adding modification type
        for method in methodsBefore:
            modificationType = RepoManager.GetTypeOfMethods(method, lines[1], after=False)
            modifiedMethodsBefore.append((method, modificationType))

        # mapping added lines and methodsAfter and adding modification type
        for method in methodsAfter:
            modificationType = RepoManager.GetTypeOfMethods(method, lines[0], after=True)
            modifiedMethodsAfter.append((method, modificationType))

        # get renamed methods in modifiedMethodsBefore
        methodsBeforeRenamed = [x for x in modifiedMethodsBefore if x[1] == ModificationType.RENAMED]

        # get renamed methods in modifiedMethodsAfter
        methodsAfterRenamed = [x for x in modifiedMethodsAfter if x[1] == ModificationType.RENAMED]

        # get mapped renamed methods of methodsBeforeRenamed and methodsAfterRenamed
        renamedMethods = RepoManager.GetRenamedMethods(methodsBeforeRenamed,
                                                       methodsAfterRenamed,
                                                       lines)

        # get added methods (only additions)
        newlyAddedMethods = [method for method in modifiedMethodsAfter if method[1] == ModificationType.NEWLY_ADDED]

        # get deleted methods (only deletions)
        completelyDeletedMethods = [method for method in modifiedMethodsBefore if
                                    method[1] == ModificationType.COMPLETELY_DELETED]

        # remove method that are already considered
        modifiedMethodsBefore = RepoManager.RemoveMethods(modifiedMethodsBefore, completelyDeletedMethods)
        modifiedMethodsBefore = RepoManager.RemoveMethods(modifiedMethodsBefore, methodsBeforeRenamed)
        modifiedMethodsAfter = RepoManager.RemoveMethods(modifiedMethodsAfter, newlyAddedMethods)
        modifiedMethodsAfter = RepoManager.RemoveMethods(modifiedMethodsAfter, methodsAfterRenamed)

        # mapping methodsBefore and methodsAfter
        for methodBefore in modifiedMethodsBefore:
            try:
                if fileType:
                    fileNameBefore = methodBefore[0].long_name.split('::')[0]
                    methodNameBefore = methodBefore[0].long_name.lstrip(fileNameBefore).lstrip('::')
                    match = next(x for x in modifiedMethodsAfter if methodNameBefore in x[0].long_name)
                else:
                    match = next(x for x in modifiedMethodsAfter if methodBefore[0].long_name == x[0].long_name)

                if match[1] == ModificationType.ADDED and methodBefore[1] == ModificationType.DELETED:
                    modifiedMethods.append(ModifiedMethod(methodBefore=methodBefore[0],
                                                          methodAfter=match[0],
                                                          modificationType=ModificationType.MODIFIED.name,
                                                          lines=lines))

                elif match[1] == ModificationType.UNKNOWN and methodBefore[1] == ModificationType.DELETED:
                    modifiedMethods.append(ModifiedMethod(methodBefore=methodBefore[0],
                                                          methodAfter=match[0],
                                                          modificationType=ModificationType.DELETED.name,
                                                          lines=lines))

                elif match[1] == ModificationType.ADDED and methodBefore[1] == ModificationType.UNKNOWN:
                    modifiedMethods.append(ModifiedMethod(methodBefore=methodBefore[0],
                                                          methodAfter=match[0],
                                                          modificationType=ModificationType.ADDED.name,
                                                          lines=lines))

            except StopIteration:
                pass

        # append newly added methods
        for method in newlyAddedMethods:
            modifiedMethods.append(ModifiedMethod(methodAfter=method[0],
                                                  modificationType=method[1].name,
                                                  lines=lines))

        # append completely deleted methods
        for method in completelyDeletedMethods:
            modifiedMethods.append(ModifiedMethod(methodBefore=method[0],
                                                  modificationType=method[1].name,
                                                  lines=lines))

        # append renamed methods
        for method in renamedMethods:
            modifiedMethods.append(method)

        return modifiedMethods

    @staticmethod
    def RemoveMethods(methods, methodsToRemove):
        """Removes certain methods from a list and the remaining list of methods."""

        for method in methodsToRemove:
            methods.remove(method)

        return methods

    @staticmethod
    def GetLinesFromDiff(file):
        """Parses diff and return deleted and added lines."""

        parsed_diff: Any = file.diff_parsed
        return parsed_diff['deleted'], parsed_diff['added']

    @staticmethod
    def StoreSourceCodeAsLines(sourceCode) -> Optional[list]:
        """Stores source code as lines and returns list of source code lines."""
        if sourceCode is not None:
            sourceCodeLines = [line for line in sourceCode.split("\n")]
        else:
            sourceCodeLines = None
        return sourceCodeLines

    @staticmethod
    def GetTypeOfMethods(method, lines, after=True) -> ModificationType:
        """Returns type of methods depending on after value."""

        codeLines = method.code_lines
        if all(codeLine in lines for codeLine in codeLines):
            return ModificationType.NEWLY_ADDED if after else ModificationType.COMPLETELY_DELETED
        elif any(codeLine in lines for codeLine in codeLines):
            if not codeLines[0] in lines:
                return ModificationType.ADDED if after else ModificationType.DELETED
            elif codeLines[0] in lines:
                return ModificationType.RENAMED
        elif not any(codeLine in lines for codeLine in codeLines):
            return ModificationType.UNKNOWN

    @staticmethod
    def GetMethods(methods, sourceCode, isTestFile, commit_hash) -> List[Method]:
        """Returns list of methods."""

        listOfMethods = []
        sourceCodeLines = ''

        for method in methods:
            start = method.start_line - 1

            if isTestFile:
                if any(annotation in sourceCode[method.start_line - 2] for annotation in java_test_annotations):
                    start = method.start_line - 2

            for i in range(start, method.end_line):
                sourceCodeLines += sourceCode[i] + "\n"
            listOfMethods.append(Method(method, sourceCodeLines, commit_hash))
            sourceCodeLines = ''

        return listOfMethods

    @staticmethod
    def GetAddedOrDeletedMethods(methods, modificationType, lines) -> List[ModifiedMethod]:
        """Return newly added or completely deleted methods depending on the entered methods and type."""
        if modificationType.name == "COMPLETELY_DELETED":
            addedOrDeletedMethods = [ModifiedMethod(methodBefore=method,
                                                    modificationType=modificationType.name,
                                                    lines=lines)
                                     for method in methods]
        else:
            addedOrDeletedMethods = [ModifiedMethod(methodAfter=method,
                                                    modificationType=modificationType.name,
                                                    lines=lines)
                                     for method in methods]
        return addedOrDeletedMethods

    @staticmethod
    def GetRenamedMethods(methodsBefore, methodsAfter, lines, similarity=0.8) -> List[ModifiedMethod]:
        """Calculates the levenshtein distance between methods and returns a list of renamed methods."""

        MIN_SIMILARITY_SIGNATURE = similarity
        modifiedMethods = []
        methods = set()
        renamedMethodPairs = []
        notRenamedMethodPairs = []

        # consider special case:
        if len(methodsBefore) != len(methodsAfter):
            if len(methodsBefore) == 0 and len(methodsAfter) == 1:
                modifiedMethods.append(ModifiedMethod(methodAfter=methodsAfter[0][0],
                                                      modificationType=ModificationType.ADDED,
                                                      lines=lines))
                return modifiedMethods
            elif len(methodsBefore) == 1 and len(methodsAfter) == 0:
                modifiedMethods.append(ModifiedMethod(methodBefore=methodsBefore[0][0],
                                                      modificationType=ModificationType.DELETED,
                                                      lines=lines))
                return modifiedMethods

        for methodAfter in methodsAfter:
            for methodBefore in methodsBefore:
                ratio_signature = Levenshtein.ratio(methodBefore[0].signature, methodAfter[0].signature)
                ratio_method_body = Levenshtein.ratio(methodBefore[0].method_body, methodAfter[0].method_body)
                current_object = (methodBefore[0], methodAfter[0], ratio_signature, ratio_method_body)

                if ratio_signature >= 0.9:
                    MIN_SIMILARITY_METHOD_BODY = similarity
                else:
                    MIN_SIMILARITY_METHOD_BODY = ((1-similarity)/2)+similarity

                if len(methodsBefore) == 1 and len(methodsAfter) == 1:
                    renamedMethodPairs.append(current_object)
                elif ratio_signature >= MIN_SIMILARITY_SIGNATURE and ratio_method_body >= MIN_SIMILARITY_METHOD_BODY:
                    if methodBefore[0] in [x[0] for x in renamedMethodPairs]:
                        match = [x for x in renamedMethodPairs if methodBefore[0] == x[0]]
                        if current_object[2] > match[0][2]:
                            index = renamedMethodPairs.index(match[0])
                            renamedMethodPairs[index] = current_object
                    else:
                        renamedMethodPairs.append(current_object)
                else:
                    notRenamedMethodPairs.append(current_object)

        for method in renamedMethodPairs:
            if method[0] not in methods and method[1] not in methods:
                modifiedMethods.append(ModifiedMethod(methodBefore=method[0],
                                                      methodAfter=method[1],
                                                      modificationType=ModificationType.RENAMED.name,
                                                      ratio=(method[2], method[3]),
                                                      lines=lines))
                methods.add(method[0])
                methods.add(method[1])

        for method in notRenamedMethodPairs:
            if method[0] not in methods:
                modifiedMethods.append(
                    ModifiedMethod(methodBefore=method[0],
                                   modificationType=ModificationType.DELETED.name,
                                   lines=lines))
                methods.add(method[0])

            if method[1] not in methods:
                modifiedMethods.append(
                    ModifiedMethod(methodAfter=method[1],
                                   modificationType=ModificationType.ADDED.name,
                                   lines=lines))
                methods.add(method[1])

        return modifiedMethods

    @staticmethod
    def __CalculateFrequencyOfChanges(methods):
        """Calculate the change frequency for each method."""

        print("calculate change frequency")
        for x in methods:
            x.change_frequency = sum(x.long_name == y.long_name and x.file_name == y.file_name for y in methods)

    @staticmethod
    def SummarizeMethods(methods, isTestfile=None) -> List[SummarizedMethod]:
        """Summarizes the same method instances."""

        summarized_methods = []
        method_names = set(x.long_name for x in methods)

        for method_name in method_names:
            method = [x for x in methods if x.long_name == method_name]

            if isTestfile:
                summarized_methods.append(SummarizedMethod(method, isTestMethod=True))
            else:
                summarized_methods.append(SummarizedMethod(method, isTestMethod=False))

        return summarized_methods

    @staticmethod
    def __SortMethodsByChangedFrequency(methods) -> List[ModifiedMethod]:
        """Returns sorted list of methods by change frequency."""

        methods.sort(key=lambda x: x.change_frequency, reverse=True)

        return methods

    @staticmethod
    def GetRecommendedMethods(methods, number, code_churn):
        """Returns a list of recommended methods."""

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

    def __GetMatchedFiles(self):
        """Determines corresponding files and test files. Returns matched files."""

        print("calculate matched files")
        methods = self.production_methods
        test_methods = self.test_methods

        summarized_methods = self.SummarizeMethods(methods)
        summarized_test_method = self.SummarizeMethods(test_methods, True)

        methods_file_names = set(method.file_name for method in methods)
        test_methods_file_names = set(method.file_name for method in test_methods)

        matched, not_matched = self.GetMatchedFileNames(methods_file_names, test_methods_file_names)

        for match in matched:
            sublist_methods = []
            sublist_test_methods = []
            for method in summarized_methods:
                if match[0] == method.summarized_method.file_name:
                    sublist_methods.append(method.summarized_method)

            for method in summarized_test_method:
                if match[1] == method.summarized_test_method.file_name:
                    sublist_test_methods.append(method.summarized_test_method)

            self.__matched_files.append(
                MatchedFiles(match[0], match[1], sublist_methods, sublist_test_methods))

        not_matched_methods = [x for x in methods if x.file_name in not_matched[0]]
        not_matched_test_methods = [x for x in test_methods if x.file_name in not_matched[1]]

        self.__not_matched_files = NotMatchedFiles(not_matched[0], not_matched[1],
                                                   not_matched_methods, not_matched_test_methods)

    @staticmethod
    def GetMatchedFileNames(production_file_names, test_file_names):
        """Find pairs of corresponding file and test file names. Returns identified pairs."""

        matched = []

        for file_name in production_file_names:
            name = re.sub('<.*>', '', file_name)
            regEx1 = r"" + name.lower().split(".")[0] + r"test.java"
            regEx2 = r"" + name.lower().split(".")[0] + r"testcase.java"
            regEx3 = r"" + name.lower().split(".")[0] + r"tests.java"

            for test_file_name in test_file_names:
                match1 = re.fullmatch(regEx1, test_file_name.lower())
                match2 = re.fullmatch(regEx2, test_file_name.lower())
                match3 = re.fullmatch(regEx3, test_file_name.lower())
                if match1 or match2 or match3:
                    matched.append((file_name, test_file_name))

        matched_files = [y[0] for y in matched]
        matched_test_files = [y[1] for y in matched]

        not_match_files = [x for x in production_file_names if x not in matched_files]
        not_match_test_files = [x for x in test_file_names if x not in matched_test_files]

        not_matched = [not_match_files, not_match_test_files]

        print("len matched:", len(matched))

        return matched, not_matched

    # TODO: muss noch getestet werden
    def __GetMultipleTimesRenamedMethods(self, ):
        """Searches for each method multiple corresponding renamed methods."""

        all_methods = self.modified_methods
        all_renamed_methods = [x for x in all_methods if x.type == "RENAMED"]

        for x in all_renamed_methods:
            found_a_renamed_method = True
            renamed_method = x
            while found_a_renamed_method:
                found_a_renamed_method, renamed_method = self.__FindRenamedMethods(renamed_method, all_renamed_methods)
                if renamed_method is not None:
                    x.renamed_methods.append(renamed_method)
                    x.multiple_renamed = True

    @staticmethod
    def __FindRenamedMethods(method, methods):
        renamed_method = None
        for x in methods:
            if method.signature == x.old_signature and x.ratio_signature < 1.0:
                renamed_method = x
                break

        if renamed_method is not None:
            return True, renamed_method
        else:
            return False, None
