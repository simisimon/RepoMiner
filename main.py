from doctest import OutputChecker
from flask import Flask, render_template, flash
from forms import InputRepoForm
from repoMiner import RepoMiner
from utils import visualization
from dash import Input, Output
import dashApp
import os
import uuid
import traceback

app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'


def getRandomId():
    return str(uuid.uuid1())


@app.route("/")
@app.route("/main", methods=['GET', 'POST'])
def main():
    form = InputRepoForm()

    if form.validate_on_submit():
        try:
            repo = None
            repo_path = form.input.data
            firstCommit = form.commit1.data
            secondCommit = form.commit2.data
            date1 = form.date1.data
            date2 = form.date2.data

            # Only allow local paths
            is_url = repo_path.startswith("http://") or repo_path.startswith("https://")
            if is_url:
                flash('Only local repository paths are allowed. Please clone the repository and provide the local path.', 'danger')
                return render_template('main.html', form=form)

            repo_path = os.path.abspath(repo_path)
            print("repo_path", repo_path)

            if repo_path and firstCommit and not secondCommit and not date1 and not date2:
                repo = RepoMiner(repo_path, first=firstCommit)
            if repo_path and firstCommit and secondCommit and not date1 and not date2:
                repo = RepoMiner(repo_path, first=firstCommit, second=secondCommit)
            if repo_path and not firstCommit and not secondCommit and date1 and date2:
                repo = RepoMiner(repo_path, since=date1, to=date2)

            all_methods = repo.modified_methods
            only_methods = repo.production_methods
            test_methods = repo.test_methods
            projectName = repo.project_name
            commits = repo.commits
            files = repo.files
            all_methods_count = repo.modified_methods_count
            methods_count = repo.production_methods_count
            test_methods_count = repo.test_methods_count

            randomId = getRandomId()

            infos = [projectName, commits, files, all_methods_count, methods_count, test_methods_count, randomId]
            methods_data = [all_methods, only_methods, test_methods]
            tm = visualization.Treemap(only_methods)
            bc = visualization.MethodsPerCommit(repo)

            charts = [tm, bc]

            try:
                dashApp.create_dashApp(__name__, app, charts, randomId)
            except Exception:
               flash(f'Visualizations cannot be created!', 'error') 

            if os.path.isdir(repo_path):
                flash(f'The entered repository is a local directory!', 'success')
            else:
                flash(f'The entered repository is not a local directory!', 'warning')

            return render_template('main.html',
                                   form=form,
                                   methods_data=methods_data,
                                   infos=infos,
                                   treemap=tm,
                                   )

        except Exception as e:
            flash(f'Something went wrong', 'danger')
            traceback.print_exc()  # <-- This will print the full traceback to the terminal
            return render_template('main.html', form=form)
    return render_template('main.html', form=form)


if __name__ == '__main__':
    app.run(debug=False)
