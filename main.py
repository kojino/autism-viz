# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
from nvd3 import pieChart, lineChart


from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello():
    type = 'pieChart'
    moodchart = pieChart(name=type, color_category='category20c', height=450, width=450)
    xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
    ydata = [3, 4, 0, 1, 5, 7, 3]
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
    moodchart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    moodchart.buildcontent()

    stresschart = lineChart(name="lineChart", x_is_date=False, x_axis_format="AM_PM")
    xdata = range(24)
    ydata = [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 4, 3, 3, 5, 7, 5, 3, 16, 6, 9, 15, 4, 12]
    ydata2 = [9, 8, 11, 8, 3, 7, 10, 8, 6, 6, 9, 6, 5, 4, 3, 10, 0, 6, 3, 1, 0, 0, 0, 1]

    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}
    stresschart.add_serie(y=ydata, x=xdata, name='sine', extra=extra_serie)
    extra_serie = {"tooltip": {"y_start": "", "y_end": " min"}}
    stresschart.add_serie(y=ydata2, x=xdata, name='cose', extra=extra_serie)
    stresschart.buildhtml()

    harmchart = lineChart(name="lineChart", x_is_date=False, x_axis_format="AM_PM")
    xdata = range(24)
    ydata = [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 4, 3, 3, 5, 7, 5, 3, 16, 6, 9, 15, 4, 12]
    ydata2 = [9, 8, 11, 8, 3, 7, 10, 8, 6, 6, 9, 6, 5, 4, 3, 10, 0, 6, 3, 1, 0, 0, 0, 1]

    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}
    harmchart.add_serie(y=ydata, x=xdata, name='sine', extra=extra_serie)
    extra_serie = {"tooltip": {"y_start": "", "y_end": " min"}}
    harmchart.add_serie(y=ydata2, x=xdata, name='cose', extra=extra_serie)
    harmchart.buildhtml()

    return render_template('index.html', moodchart=moodchart, stresschart=stresschart, harmchart=harmchart)


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
