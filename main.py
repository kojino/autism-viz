# -*- coding: utf-8 -*-
# [START app]
import logging
from nvd3 import pieChart, lineChart, lineWithFocusChart
from urllib2 import urlopen
import json
from flask import Flask, render_template
from collections import OrderedDict
import requests

app = Flask(__name__)

def get_request(path):
    """
    Given a path, e.g. '/search/' and params, return the response in json form.
    You may request additional parameters by overriding the params method
    """
    response = urlopen(path)

    str_response = response.read().decode('utf-8')
    result = json.loads(str_response)


    return result

def get_emotion_dict(events):
    event_dict = OrderedDict([('joy', 0), ('sorrow', 0), ('anger', 0), ('surprise', 0), ('neutral', 0)])
    for event in events:
        mood = event['mood']
        if mood in event_dict:
            event_dict[mood] += 1
    return event_dict

def get_stress_level(events):
    xdata = []
    ydata_stress = []
    ydata_harm = []
    ydata_physical = []
    for event in events:
        xdata.append(event['time'])
        ydata_stress.append(event['stress_level'])
        ydata_physical.append(event['physical_activity_level'])
        ydata_harm.append(event['self_harm_level'])
    return xdata, ydata_stress, ydata_harm, ydata_physical

def get_table_items(events):
    data = []
    for event in events:
        row = [event['trigger'], event['resolution'], event['additional_notes']]
        data.append(row)
    return data

@app.route('/')
def hello():
    events = requests.get("https://autism-tracker-server.appspot.com/events").json()
    emotion_dict = get_emotion_dict(events)
    type = 'pieChart'
    moodchart = pieChart(name=type, color_category='category20c', height=450, width=450)
    xdata = [key for key in ['😁 joy', '😢 sorrow', '😠 anger', '😲 surprise', '😐 neutral']]
    ydata = [emotion_dict[key] for key in emotion_dict]

    extra_serie = {"tooltip": {"y_start": "", "y_end": " %"}}
    moodchart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    moodchart.buildcontent()
    stresschart = lineWithFocusChart(name='lineWithFocusChart', x_is_date=True, x_axis_format="%d %b %Y")
    xdata, ydata_stress, ydata_harm, ydata_physical = get_stress_level(events)
    extra_serie = {"tooltip": {"y_start": "", "y_end": " ext"},
                   "date_format": "%d %b %Y %H"}
    stresschart.add_serie(name="Stress Level", y=ydata_stress, x=xdata, extra=extra_serie)
    stresschart.add_serie(name="Self Harm Level", y=ydata_harm, x=xdata, extra=extra_serie)
    stresschart.add_serie(name="Physical Activity Level", y=ydata_physical, x=xdata, extra=extra_serie)

    stresschart.buildhtml()

    html = """<table>
                <tr>
                  <th>Trigger</th>
                  <th>Resolution</th>
                  <th>Additional Notes</th>
                </tr>
                {0}
              </table>"""
    items = get_table_items(events)
    tr = "<tr>{0}</tr>"
    td = "<td>{0}</td>"
    subitems = [tr.format(''.join([td.format(a) for a in item])) for item in items]
    table = html.format("".join(subitems))


    return render_template('index.html', table=table, moodchart=moodchart, stresschart=stresschart)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
