from flask import Flask, render_template, flash
from RepoManager.forms import InputRepoForm
from RepoManager.repoManager import RepoManager
from RepoManager.utils import visualization
import RepoManager.dashApp
import os
import uuid


app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'

@app.route("/")
@app.route("/main", methods=['GET', 'POST'])
def main():
    form = InputRepoForm()
    message = None

    if form.validate_on_submit():
        try:
            repo = None
            url = form.input.data
            firstCommit = form.commit1.data
            secondCommit = form.commit2.data
            date1 = form.date1.data
            date2 = form.date2.data

            if url and firstCommit and not secondCommit and not date1 and not date2:
                message = 'single commit'
                repo = RepoManager(url, firstCommit=firstCommit)
            if url and firstCommit and secondCommit and not date1 and not date2:
                message = 'between commits'
                repo = RepoManager(url, firstCommit=firstCommit, secondCommit=secondCommit)
            if url and not firstCommit and not secondCommit and date1 and date2:
                message = 'between datetimes'
                repo = RepoManager(url, since=date1, to=date2)

            all_methods = repo.all_methods_data
            only_methods = repo.methods_data
            test_methods = repo.test_methods_data
            projectName = repo.project_name
            commits = repo.commits
            files = repo.files
            all_methods_count = repo.all_methods_count
            methods_count = repo.methods_count
            test_methods_count = repo.test_methods_count

            dashAppId = str(uuid.uuid1())
            infos = [projectName, commits, files, all_methods_count, dashAppId, methods_count, test_methods_count]
            methods_data = [all_methods, only_methods, test_methods]
            tm = visualization.Treemap(all_methods)

            dashApp.create_dashApp(__name__, app, tm, dashAppId)

            if os.path.isdir(url):
                flash(f'The entered repository is a local directory and analysed for  {message}!', 'success')
            else:
                flash(f'The entered repository is not a local directory and analysed for  {message}!', 'warning')

            return render_template('main.html',
                                   form=form,
                                   methods_data=methods_data,
                                   infos=infos,
                                   treemap=tm)

        except Exception as e:
            flash(f'Something went wrong', 'danger')
            print(e.with_traceback())
            return render_template('main.html', form=form)
    return render_template('main.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
