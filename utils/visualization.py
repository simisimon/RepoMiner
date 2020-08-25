import plotly.express as px
import plotly.graph_objects as go
import re


def Treemap(commit_data):
    methods = []
    for file in commit_data:
        for method in file[2]:
            data = {
                "commit": file[0],
                "file_name": file[1],
                "long_name": method.long_name,
                "code_churn": method.code_churn,
                "change_frequency": method.change_frequency,
                "type": method.type,
            }
            methods.append(data)

    # bei Dateien bestimmt der Average der Summe der veränderten Methoden die Färbung
    fig = px.treemap(methods,
                     path=['commit', 'file_name', 'long_name'],
                     values='change_frequency',
                     color='code_churn',
                     color_continuous_scale='Reds',
                     hover_data=["long_name", "type"],
                     )

    return fig


def ShowTreemap(modified_methods):
    methods = []
    for method in modified_methods:
        data = {
            "commit": method.commit,
            "file_name": method.file_name,
            "long_name": method.long_name,
            "code_churn": method.code_churn,
            "change_frequency": method.change_frequency,
        }
        methods.append(data)

    # bei Dateien bestimmt der Average der Summe der veränderten Methoden die Färbung
    fig = px.treemap(methods,
                     path=['commit', 'file_name', 'long_name'],
                     values='change_frequency',
                     color='code_churn',
                     color_continuous_scale='Reds',
                     hover_data=["long_name"],
                     )

    fig.show()


def TreeMapOnlyMethods(modified_methods):
    methods = []
    for method in modified_methods:
        name = re.sub('<T>', '', method.file_name)
        data = {
            "commit": method.commit,
            "file_name": name,
            "name": method.name,
            "code_churn": method.code_churn,
            "change_frequency": method.change_frequency,
        }
        methods.append(data)

    # bei Dateien bestimmt der Average der Summe der veränderten Methoden die Färbung
    fig = px.treemap(methods,
                     path=['commit', 'file_name', "name"],
                     values='change_frequency',
                     color='code_churn',
                     color_continuous_scale='Reds',
                     )

    fig.update_layout(autosize=False,
                      width=800,
                      height=550)

    fig.show()


def BarChart_Production_Test_Methods(production_methods, test_methods):
    methods = ["Test Methods", "Production Methods"]
    data = [test_methods, production_methods]
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
                          title='Number of Methods',
                          titlefont_size=16,
                          tickfont_size=14,
                      ),
                      xaxis=dict(
                          title='Methods',
                          titlefont_size=16,
                          tickfont_size=14,
                      ))

    # return fig
    fig.show()


def BarChart_Methods_Per_Commit(number_commits, methods_per_commit):
    fig = go.Figure(data=[go.Bar(x=methods_per_commit,
                                 y=number_commits,
                                 marker_color='cornflowerblue'
                                 )])

    fig.update_layout(autosize=False,
                      width=1200,
                      height=750,
                      yaxis=dict(
                          title='Number of Modified Methods in the Commit',
                          # titlefont_size=16,
                          # tickfont_size=14,
                      ),
                      xaxis=dict(
                          title='Analyzed Commit',
                          # titlefont_size=16,
                          # tickfont_size=14,
                          # tickmode='linear'
                      ))
    # xaxis_tickangle=-45)
    # return fig
    fig.show()


def BarChart_Production_And_Test_Methods_Per_Commit(commits, production_methods, test_methods):
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
                      ),
                      #template="simple_white"
                      )

    fig.update_xaxes(showline=True, linewidth=1.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=1.5, linecolor='black')

    # return fig
    fig.show()


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


def Table_Matched_Files(matched_files):
    production_files = [x.file_name for x in matched_files]
    test_files = [x.test_file_name for x in matched_files]

    fig = go.Figure(data=[go.Table(header=dict(values=['Production Files', 'Test Files']),
                                   cells=dict(values=[production_files, test_files]))
                          ])

    fig.update_layout(width=1200)

    fig.show()


def Table_Not_Matched_Files(prod_files, test_files):
    fig = go.Figure(data=[go.Table(header=dict(values=['Production Files', 'Test Files']),
                                   cells=dict(values=[prod_files, test_files]))
                          ])

    fig.update_layout(width=1200)

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
                          'text': "test",
                          'y': 0.9,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'}
                      )

    # return fig
    fig.show()


def BoxPlot(total, added, deleted, other):
    fig = go.Figure()

    fig.add_trace(go.Box(y=total, name="All Changes in Methods", marker_color="cornflowerblue"))
    fig.add_trace(go.Box(y=added, name="Added Lines in Methods", marker_color="green"))
    fig.add_trace(go.Box(y=deleted, name="Deleted Lines in Methods", marker_color="indianred"))
    fig.add_trace(go.Box(y=other, name="Other Changes", marker_color="grey"))

    fig.update_layout(width=900,
                      height=550,
                      yaxis_title='Distribution of Changes in Changed Files',
                      # legend=dict(
                      #    yanchor="top",
                      #     y=0.99,
                      #    xanchor="right",
                      #   x=0.99
                      # )
                      showlegend=False
                      )

    fig.show()


def LineChart(total, added, deleted):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=deleted, y=total,
                             mode='lines',
                             name='lines'))
    fig.add_trace(go.Scatter(x=added, y=total,
                             mode='lines+markers',
                             name='lines+markers'))

    fig.update_layout(width=800,
                      height=550,
                      yaxis_title='Composition of Changes in Files')

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
                      width=1100,
                      height=550,
                      xaxis_title="Commit",
                      yaxis_title="Number of changed files",
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


def LinePlot(commits, co_evolved):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=commits, y=co_evolved, line_shape='hv'))

    fig.update_layout(width=900,
                      height=550,
                      yaxis_title='Co-Evolved Commits',
                      xaxis_title='Commits',
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
