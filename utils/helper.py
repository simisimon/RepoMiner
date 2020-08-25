from utils.visualization import BoxPlot, ScatterPlot, BoxPlotCoEvolvedFiles, LinePlot, PieChart, \
    BarChart_Production_And_Test_Methods_Per_Commit
import numpy as np


def CompositionOfChanges(repo):
    counter_p_methods = []
    counter_t_methods = []
    total = []
    added = []
    deleted = []
    other = []
    commits = []
    counter_files = 0
    counter_files_with_changes = 0

    for i in range(0, repo.commits):
        commits.append(i + 1)

    for commit in repo.analyzed_commits:
        counter_t_methods.append(commit.test_methods_count)
        counter_p_methods.append(commit.production_methods_count)
        total += commit.ratio_modified_lines_by_methods
        added += commit.ratio_added_lines_by_methods
        deleted += commit.ratio_deleted_lines_by_methods
        other += commit.ratio_other_changes
        for x in commit.analyzed_files:
            counter_files += 1
            if len(x.modified_methods) > 0:
                counter_files_with_changes += 1

    sum_total = sum(total)
    sum_added = sum(added)
    sum_deleted = sum(deleted)
    sum_other = sum(other)

    print("length total:", len(total))
    print("average total:", sum_total / len(total), np.median(total))
    print("average added:", sum_added / len(added), np.median(added))
    print("average deleted:", sum_deleted / len(deleted), np.median(deleted))
    print("average other:", sum_other / len(other), np.median(other))
    BoxPlot(total, added, deleted, other)
    print("files:", counter_files)
    print("files with changes :", counter_files_with_changes)


def ChangeHistory(repo):
    counter_commit = 1
    data = []
    for commit in repo.analyzed_commits:
        prod_file_counter = 1
        prod_commits = []
        prod = []
        for file in commit.analyzed_files:
            if not file.is_test_file:
                prod.append(prod_file_counter)
                prod_file_counter += 1

        for i in range(0, len(prod)):
            prod_commits.append(counter_commit)

        test_file_counter = 1
        test_commits = []
        test = []
        for file in commit.analyzed_files:
            if file.is_test_file:
                test.append(test_file_counter)
                test_file_counter += 1

        for i in range(0, len(test)):
            test_commits.append(counter_commit)

        counter_commit += 1

        tmp = {
            "prod_files": prod,
            "prod_commit": prod_commits,
            "test_files": test,
            "test_commit": test_commits
        }

        data.append(tmp)

    ScatterPlot(data)


def AverageOfFilteredCommitsWithCoEvolvedFiles(repo):
    co_evolved_commits = []
    not_co_evolved_commits = []
    for commit in repo.analyzed_commits:
        if len(commit.modified_methods) > 0:
            if commit.related_files_changed:
                co_evolved_commits.append(1)
                not_co_evolved_commits.append(0)
            else:
                co_evolved_commits.append(0)
                not_co_evolved_commits.append(1)

    print("length:", len(co_evolved_commits))

    sum_co_evolved = sum(co_evolved_commits)
    sum_not_co_evolved = sum(not_co_evolved_commits)

    print("commits with at least one changed file")
    print("co-evolved:", co_evolved_commits)
    print("length co-evolved:", len(co_evolved_commits))
    print("average of commits with co-evolved files :", sum_co_evolved / len(co_evolved_commits), np.median(co_evolved_commits))
    print("not co-evolved:", not_co_evolved_commits)
    print("length not co-evolved:", len(not_co_evolved_commits))
    print("average of commits without not co-evolved files:", sum_not_co_evolved / len(not_co_evolved_commits), np.median(not_co_evolved_commits))
    PieChart(sum_co_evolved, sum_not_co_evolved)


def DistributionOfCoEvolvedFiles(repo):
    co_evolved_files = []
    not_co_evolved_files = []
    for commit in repo.analyzed_commits:
        if len(commit.analyzed_production_files) > 0 and commit.production_methods_count > 0:
            print(commit.hash)
            co_evolved_files.append(commit.ratio_co_evolved_files)
            not_co_evolved_files.append(commit.ratio_not_co_evolved_files)

    sum_co_evolved = sum(co_evolved_files)
    sum_not_co_evolved = sum(not_co_evolved_files)

    print("co-evolved:", co_evolved_files)
    print("average co-evolved:", sum_co_evolved / len(co_evolved_files), np.median(co_evolved_files))
    print("not co-evolved:", not_co_evolved_files)
    print("average not co-evolved:", sum_not_co_evolved / len(not_co_evolved_files), np.median(not_co_evolved_files))
    BoxPlotCoEvolvedFiles(co_evolved_files, not_co_evolved_files)


def CourseOfCoEvolvedCommits(repo):
    commits = []
    commit_counter = 1
    co_evolved = []
    test1 = 0
    test2 = 0
    for commit in repo.analyzed_commits:
        commits.append(commit_counter)
        commit_counter += 1
        if commit.related_files_changed:
            co_evolved.append(1)
            test1 += 1
        else:
            co_evolved.append(0)
            test2 += 1

    print("test1:", test1)
    print("test2:", test2)
    LinePlot(commits, co_evolved)


def RelationOfCoEvolvedCommits(repo):
    co_evolved = 0
    not_co_evolved = 0
    for commit in repo.analyzed_commits:
        if commit.related_files_changed:
            co_evolved += 1
        else:
            not_co_evolved +=1

    print("co-evolved commits:", co_evolved)
    print("not co-evolved commits:", not_co_evolved)

    PieChart(co_evolved, not_co_evolved)


def AverageOfAllCommitsWithCoEvolvedFiles(repo):
    co_evolved_commits = []
    not_co_evolved_commits = []
    commits = []
    for commit in repo.analyzed_commits:
        if commit.related_files_changed:
            commits.append(commit.hash)
            co_evolved_commits.append(1)
            not_co_evolved_commits.append(0)
        else:
            co_evolved_commits.append(0)
            not_co_evolved_commits.append(1)

    sum_co_evolved = sum(co_evolved_commits)
    sum_not_co_evolved = sum(not_co_evolved_commits)

    print("all commits")
    print("co-evolved:", co_evolved_commits)
    print("length co-evolved:", len(co_evolved_commits))
    print("average of commits with co-evolved files :", sum_co_evolved / len(co_evolved_commits), np.median(co_evolved_commits))
    print("not co-evolved:", not_co_evolved_commits)
    print("length not co-evolved:", len(not_co_evolved_commits))
    print("average of commits without not co-evolved files:", sum_not_co_evolved / len(not_co_evolved_commits), np.median(not_co_evolved_commits))
    PieChart(sum_co_evolved, sum_not_co_evolved)


def MethodsPerCommit(repo):
    commits = []
    for i in range(0, repo.commits):
        commits.append(i + 1)

    counter_p_methods = []
    counter_t_methods = []
    for commit in repo.analyzed_commits:
        counter_t_methods.append(commit.test_methods_count)
        counter_p_methods.append(commit.production_methods_count)

    BarChart_Production_And_Test_Methods_Per_Commit(commits, counter_p_methods, counter_t_methods)

