import plotly.express as px
import plotly.graph_objects as go
import re

def Treemap(methods):
    # If methods is empty, return a placeholder figure
    if not methods:
        fig = go.Figure()
        fig.update_layout(title="No data available for Treemap")
        return fig

    # If methods is a list of objects, convert to list of dicts
    if hasattr(methods[0], '__dict__'):
        data = [m.__dict__ for m in methods]
    else:
        data = methods

    # Check for required columns
    required_columns = {"commit", "file_name", "long_name", "change_frequency", "type"}
    if not all(col in data[0] for col in required_columns):
        fig = go.Figure()
        fig.update_layout(title="Data format error for Treemap")
        return fig

    fig = px.treemap(
        data,
        path=['commit', 'file_name', 'long_name'],
        values='change_frequency',
        color='type',
        hover_data=["long_name", "type"],
    )
    return fig


def MethodsPerCommit(repo):

    commits = []
    for i in range(0, repo.commits):
        commits.append(i + 1)

    production_methods = []
    test_methods = []
    for commit in repo.analyzed_commits:
        test_methods.append(commit.test_methods_count)
        production_methods.append(commit.production_methods_count)

    fig = go.Figure(data=[go.Bar(name="Production Methods",
                                 x=commits,
                                 y=production_methods,
                                 marker_color='cornflowerblue'
                                 ),
                          go.Bar(name="Test Methods",
                                 x=commits,
                                 y=test_methods,
                                 marker_color='crimson')])

    fig.update_layout(autosize=False,
                      width=800,
                      height=575,
                      yaxis=dict(
                          title='Number of Modified Methods in a Commit',
                          # titlefont_size=16,
                          # tickfont_size=14,
                      ),
                      xaxis=dict(
                          title='Commits',
                          # titlefont_size=16,
                          # tickfont_size=14,
                          # tickmode='linear'
                      ),
                      # xaxis_tickangle=-45,
                      barmode='stack',
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="right",
                          x=0.99
                      ))

    #fig.show()
    return fig



def PieChart_Production_And_Test_Methods(production_methods, test_methods):
    fig = go.Figure(data=[go.Pie(labels=["Production Methods", "Test Methods"],
                                 values=[production_methods, test_methods],
                                 textinfo='label+percent'
                                 )])

    fig.update_traces(textfont_size=20)

    fig.update_layout(autosize=False,
                      width=750,
                      height=600)

    # return fig
    fig.show()


def BarChart_CoEvolvedFiles_In_Commits(co_evolved_commit, not_co_evolved_commits):
    methods = ["Commits with co-evolved files", "Commits with no co-evolved files"]
    data = [co_evolved_commit, not_co_evolved_commits]
    fig = go.Figure(data=[go.Bar(x=methods,
                                 y=data,
                                 text=data,
                                 textposition='auto',
                                 width=[0.1, 0.1],
                                 marker_color=['crimson', 'cornflowerblue'])])

    fig.update_layout(autosize=False,
                      width=750,
                      height=750,
                      bargap=0.5,
                      yaxis=dict(
                          title='Number of Commits',
                          titlefont_size=16,
                          tickfont_size=14,
                      ),
                      xaxis=dict(
                          title='Commits',
                          titlefont_size=16,
                          tickfont_size=14,
                      ))

    # return fig
    fig.show()


def PieChart(co_evolved, not_co_evolved):
    fig = go.Figure(data=[go.Pie(labels=["Commits with co-evolved files", "Commits without co-evolved files"],
                                 values=[co_evolved, not_co_evolved],
                                 textinfo='value+percent',
                                 marker_colors=["crimson", "cornflowerblue"]
                                 )])

    fig.update_traces(textfont_size=20)

    fig.update_layout(autosize=False,
                      width=650,
                      height=500,
                      legend=dict(
                          yanchor="top",
                          y=-0.3,
                          xanchor="center",
                          x=0.5
                      ),
                      title={
                          'text': "Test",
                          'y': 0.9,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'}
                      )

    # return fig
    fig.show()


def ScatterPlot(data):
    fig = go.Figure()

    for i in range(0, len(data)):
        fig.add_trace(go.Scatter(
            x=data[i]['prod_commit'],
            y=data[i]["prod_files"],
            mode='markers',
            showlegend=False,
            marker=dict(
                color="cornflowerblue",
                opacity=0.5,
                line=dict(
                    color='black',
                    width=0.5,
                )
            )))

        fig.add_trace(go.Scatter(
            x=data[i]['test_commit'],
            y=data[i]["test_files"],
            mode='markers',
            showlegend=False,
            marker=dict(
                color="crimson",
                opacity=0.5,
                line=dict(
                    color='black',
                    width=0.5
                )),
        ))

    fig.update_layout(autosize=False,
                      width=800,
                      height=550,
                      xaxis_title="Commit",
                      yaxis_title="File ID's",
                      legend=dict(yanchor="top",
                                  y=0.99,
                                  xanchor="left",
                                  x=0.01)
                      )

    fig.show()


def BoxPlotCoEvolvedFiles(co_evolved, not_co_evolved):
    fig = go.Figure()

    fig.add_trace(go.Box(y=co_evolved, name="Co-Evolved Files", marker_color="cornflowerblue"))
    fig.add_trace(go.Box(y=not_co_evolved, name="Not Co-Evolved Files", marker_color="crimson"))

    fig.update_layout(width=900,
                      height=550,
                      yaxis_title='Distribution of Co-Evolved Files in Commits',
                      # legend=dict(
                      #    yanchor="top",
                      #     y=0.99,
                      #    xanchor="right",
                      #   x=0.99
                      # )
                      showlegend=False
                      )

    fig.show()


def ScatterPlot2(data):
    commits = [139, 278, 417, 556, 695, 834]
    fig = go.Figure()

    for i in range(0, len(data)):
        average = [sum(data[i]) / 139]
        x = [commits[i]]
        fig.add_trace(go.Scatter(
            x=x,
            y=average,
            mode='markers',
            showlegend=False,
            marker=dict(
                color="cornflowerblue",
                opacity=0.5,
                line=dict(
                    color='black',
                    width=0.5,
                )
            )))

    fig.show()
