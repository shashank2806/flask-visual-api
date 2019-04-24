from flask import Flask, request
import seaborn as sns
import json
import pandas as pd
import requests
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

PALLETE = 'Set2'

@app.route('/graph', methods=["POST"])
def bar_graph():
    meta = request.json['metadata']
    data = pd.DataFrame.from_records(request.json['data'])
    sns.set_style("darkgrid", {"axes.facecolor": "0.9"})
    plt.xticks(rotation=45)
    plot = sns.barplot(x=data.X, y=data.Y, palette=PALLETE)
    plt.xlabel(meta['X'])
    plt.ylabel(meta['Y'])
    plt.tight_layout()
    plot.figure.savefig('plot.png')
    plt.clf()
    return base64.b64encode(open('plot.png', 'rb').read())


@app.route('/lineplot', methods=["POST"])
def line_plot():
    meta = request.json['metadata']
    df = pd.DataFrame.from_records(request.json['data'])
    sns.set_style("darkgrid", {"axes.facecolor": "0.9"})
    plot = sns.lineplot(data=df, dashes=False, hue="event",
                        style="event", markers=True, palette=PALLETE)
    plt.xticks(rotation=45)
    plt.xlabel(meta['X'])
    plt.ylabel(meta['Y'])
    plt.tight_layout()
    plot.figure.savefig('lineplot.png')
    plt.clf()
    return base64.b64encode(open('lineplot.png', 'rb').read())

@app.route('/multibar', methods=["POST"])
def multi_bar():
    meta = request.json['metadata']
    df = pd.DataFrame.from_records(request.json['data'])
    df.reset_index(inplace=True, level=0)
    df = df.melt(id_vars=['index'], var_name="line")
    plt.figure(figsize=(12, 4))
    sns.set_style("darkgrid", {"axes.facecolor": "0.9"})
    plot = sns.barplot(data=df, hue='line', x='index',
                       y='value', palette=PALLETE)
    plt.xticks(rotation=45)
    plt.xlabel(meta['X'])
    plt.ylabel(meta['Y'])
    plt.tight_layout()
    plot.figure.savefig('multibar.png')
    plt.clf()
    return base64.b64encode(open('multibar.png', 'rb').read())

@app.route('/')
def home():
    return "Working"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
