from flask import Flask, render_template, flash
from forms import InputRepoForm
from repoMiner import RepoMiner
from utils import visualization
import dashApp
import os
import uuid

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
            url = form.input.data
            firstCommit = form.commit1.data
            secondCommit = form.commit2.data
            date1 = form.date1.data
            date2 = form.date2.data

            if url and firstCommit and not secondCommit and not date1 and not date2:
                repo = RepoMiner(url, first=firstCommit)
            if url and firstCommit and secondCommit and not date1 and not date2:
                repo = RepoMiner(url, first=firstCommit, second=secondCommit)
            if url and not firstCommit and not secondCommit and date1 and date2:
                repo = RepoMiner(url, since=date1, to=date2)

            all_methods = repo.modified_methods
            only_methods = repo.production_methods
            test_methods = repo.test_methods
            projectName = repo.project_name
            commits = repo.commits
            files = repo.files
            all_methods_count = repo.modified_methods_count
            methods_count = repo.production_methods_count
            test_methods_count = repo.test_methods_count

            infos = [projectName, commits, files, all_methods_count, methods_count, test_methods_count]
            methods_data = [all_methods, only_methods, test_methods]
            tm = [visualization.Treemap(only_methods), getRandomId()]
            #bc = [visualization.MethodsPerCommit(repo), getRandomId()]

            dashApp.create_dashApp(__name__, app, tm[0], tm[1])
            #dashApp.create_dashApp(__name__, app, bc[0], bc[1])

            if os.path.isdir(url):
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
            print(e.with_traceback())
            return render_template('main.html', form=form)
    return render_template('main.html', form=form)


if __name__ == '__main__':
    app.run(debug=False)
