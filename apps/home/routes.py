from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
import pandas as pd
from Analyze.Predict import *
from apps import db
from apps.home.models import Analyzes
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
# Word Cloud
from matplotlib.figure import Figure
from wordcloud import WordCloud

from collections import Counter

UPLOAD_FOLDER = 'uploads'


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/analyze')
@login_required
def analyze():
    filename = request.args.get('filename')
    # file = request.args.get('file')

    if filename is not None:
        print("--------->", filename)
    text = get_text_from_file(filename)

    model_op = ModelOperations(text)
    result, polarities, aspects, pp_text, review_count = model_op.predict()

    if len(polarities) and len(aspects):
        new_aspects = aspects[:len(polarities)]
    f1score = 99.8

    # Record the fields to the database
    store_analyze_data(filename=filename, aspects=new_aspects, polarities=polarities, preprocessed_text=pp_text,
                       f1score=f1score, review_count=review_count)

    # Visualization
    fig_bar, fig_don, fig_word_cloud = visualize(aspects=new_aspects, polarities=polarities, pp_text=pp_text)
    fig_bar.show()
    fig_don.show()
    fig_word_cloud.show()

    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_don = json.dumps(fig_don, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_word_cloud = json.dumps(fig_word_cloud, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home/analyze.html', segment='analyze', graphJSON_bar=graphJSON_bar,
                           graphJSON_don=graphJSON_don, graphJSON_word_cloud=graphJSON_word_cloud)


def store_analyze_data(filename, aspects, polarities, preprocessed_text, f1score, review_count):
    columns = {'filename': filename, 'aspects': aspects, 'polarities': polarities,
               'preprocessed_text': preprocessed_text, 'f1score': f1score,
               'reviewCount': review_count, 'userId': current_user.id}
    analyze = Analyzes(columns)
    db.session.add(analyze)
    db.session.commit()


def get_text_from_file(filename):
    file = UPLOAD_FOLDER + '/' + filename
    df = pd.read_csv(file, delimiter=r"\n", header=None)
    text = df.iloc[:, 0]
    return text


def visualize(aspects, polarities, pp_text):
    # Bar chart
    fig_bar = px.bar(x=aspects, color=polarities, title="Aspect Categories and Polarities Bar Plot",
                     labels={"count": "All reviews", "x": "Aspect Categories", "color": "Polarities"},
                     color_discrete_map={"positive": "rgb(29, 233, 182)", "neutral": "rgb(4, 169, 245)",
                                         "negative": "rgb(163, "
                                                     "137, 212)"})

    values = []
    for counts in Counter(polarities).values():
        values.append(counts)
    labels = list(set(polarities))

    # Donut chart
    # Negative , neutral, positive
    colors = ['rgb(163, 137, 212)', 'rgb(4, 169, 245)', 'rgb(29, 233, 182)']
    # pull is given as a fraction of the pie radius
    fig_don = go.Figure(data=[go.Pie(hole=.4, labels=labels, values=values, marker_colors=colors
                                     , pull=[0, 0, 0, 0])])

    # Word Cloud
    all_words = ''.join(pp_text)

    wordcloud = WordCloud(background_color='white', max_words=len(all_words))

    wordcloud.generate(all_words)
    fig_word_cloud = px.imshow(wordcloud)
    fig_word_cloud.update_xaxes(showticklabels=False)
    fig_word_cloud.update_yaxes(showticklabels=False)

    return fig_bar, fig_don, fig_word_cloud


@blueprint.route('/prev-analyze')
@login_required
def prev_analyze():
    analyze_id = request.args.get('analyze_id')
    aspects = Analyzes.query.with_entities(Analyzes.aspects).filter(Analyzes.id == analyze_id).first()[0]
    aspects = aspects.split(',')  # Rejoining
    polarities = Analyzes.query.with_entities(Analyzes.polarities).filter(Analyzes.id == analyze_id).first()[0]
    polarities = polarities.split(',')  # Rejoining
    f1score = Analyzes.query.with_entities(Analyzes.f1score).filter(Analyzes.id == analyze_id).first()[0]
    pp_text = Analyzes.query.with_entities(Analyzes.preprocessed_text).filter(Analyzes.id == analyze_id).first()[0]
    pp_text = pp_text.split(',')  # Rejoining
    reviewCount = Analyzes.query.with_entities(Analyzes.reviewCount).filter(Analyzes.id == analyze_id).first()[0]

    positive_polarities_count = polarities.count('positive')
    negative_polarities_count = polarities.count('negative')
    neutral_polarities_count = polarities.count('neutral')

    # Visualization
    fig_bar, fig_don, fig_word_cloud = visualize(aspects=aspects, polarities=polarities, pp_text=pp_text)
    fig_bar.show()
    fig_don.show()
    fig_word_cloud.show()

    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_don = json.dumps(fig_don, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_word_cloud = json.dumps(fig_word_cloud, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home/prev-analyze.html', segment='prev-analyze', graphJSON_bar=graphJSON_bar,
                           graphJSON_don=graphJSON_don, graphJSON_word_cloud=graphJSON_word_cloud,
                           reviewCount=reviewCount,
                           positive_polarities_count=positive_polarities_count,
                           negative_polarities_count=negative_polarities_count,
                           neutral_polarities_count=neutral_polarities_count)


@blueprint.route('/prev-analyzes')
@login_required
def prev_analyzes():
    delete_id = request.args.get('delete_id')
    Analyzes.query.filter_by(id=delete_id).delete()
    current_analyzes = Analyzes.query.filter_by(userId=current_user.id).all()
    return render_template('home/prev-analyzes.html', segment='prev-analyzes.html', analyzes=current_analyzes,
                           current_user=current_user.username)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        analyzes = None
        if segment == "prev-analyzes.html":
            analyzes = Analyzes.query.filter_by(userId=current_user.id).all()

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, analyzes=analyzes,
                               current_user=current_user.username)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment

    except:
        return None
