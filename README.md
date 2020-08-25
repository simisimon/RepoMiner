# RepoManager
RepoManager is a Python framework to analyze the historical changes of software systems stored in version control systems. The analysis aims at finding ciritical code areas in form of modified methods and at finding test gaps. We call this approach the change-based analysis of software repositories.

This approach was developed in the context of our master thesis. We validated different aspects of our change-based analysis by a comprehensive sample-based inspection. We provide detailed results of validating the sample sets (e.g. code artifacts, metric values, ratings, reasons), on our complementary [google docs document](https://docs.google.com/spreadsheets/d/1LMwUOiO33gK4oeYTnHs4tAKA53Rp1NBLijPJ28WjEmI/edit?usp=sharing).

We integrated the change-based analysis into a web application to visualize its results. Currently, we show only a table with modified methods and a zoomable tree map. The web application is still in development and has not been tested.

## How to start the web application?
1. Clone the repository
2. Install all missing packages
3. Start the web application using the terminal
   - Go to the directory where main.py is located
   - Use the following commands:
   ```bash
   $ export FLASK_APP=main.py
   $ flask run
   ```
   - on windows, the environment variable syntax depends on command line interpreter:
   ```bash
   $ C:\path\to\app>set FLASK_APP=main.py
   ```
   - otherwise check out the [Flask](https://flask.palletsprojects.com/en/1.1.x/) introduction
   
## How to use the web application?
1. Enter the path to a software repository. (It is recommended to clone the software repository in advance and to use the corresponding local directory.)
2. Select variant of the analysis.
3. If necessary, enter commits to configure the scope of the analysis variant.
4. Start the analysis by pressing the start button.

