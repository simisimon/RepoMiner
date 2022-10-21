class AnalyzedFile:
    def __init__(self, commit, file, is_test_file, methods):
        self.commit = commit  # str: commit hash
        self.file_name = file.filename  # str: file_name
        self.modified_methods = methods  # List[ModifiedMethod]
        self.added = file.added_lines  # int: total number of added lines
        self.deleted = file.deleted_lines  # int: total number of deleted lines
        self.modified_lines = file.added_lines + file.deleted_lines  # int: total number of modified lines
        self.is_test_file = is_test_file  # bool: returns true if file is test file, otherwise false
        self.type = file.change_type.name  # change type of file
        self.source_code = file.source_code  # str: source code

    @property
    def added_lines_of_methods(self) -> int:
        added = 0
        for x in self.modified_methods:
            added += x.added
        return added

    @property
    def deleted_lines_of_methods(self) -> int:
        deleted = 0
        for x in self.modified_methods:
            deleted += x.deleted
        return deleted

    @property
    def all_changes_of_methods(self) -> int:
        all_changes = 0
        for x in self.modified_methods:
            all_changes += x.deleted + x.added
        return all_changes

    @property
    def ratio_other_changes(self):
        other = self.modified_lines - self.all_changes_of_methods

        return other / self.modified_lines if not self.modified_lines == 0 else 0

    @property
    def ratio_modified_lines(self) -> float:
        return self.all_changes_of_methods / self.modified_lines if not self.modified_lines == 0 else 0

    @property
    def ratio_added_lines(self) -> float:
        return self.added_lines_of_methods / self.modified_lines if not self.modified_lines == 0 else 0

    @property
    def ratio_deleted_lines(self) -> float:
        return self.deleted_lines_of_methods / self.modified_lines if not self.modified_lines == 0 else 0
