from flask import Flask
import flask
import numpy as np

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route("/")
def main():
    return "This is the Alune Server Homepage."

names = np.load('data/setup/names.npy')
poproles = np.load('data/setup/poproles.npy')
roledict = np.load('data/setup/roledict.npy', allow_pickle=True).item()
namedict = np.load('data/setup/namedict.npy', allow_pickle=True).item()
rolechamps = np.load('data/setup/rolechamps.npy', allow_pickle=True).item()
for i in range(5):
    rolechamps[i] = np.array(rolechamps[i]).tolist()

@application.route("/data/setup/names")
def getnames():
    response = flask.jsonify(names.tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route("/data/setup/poproles")
def getpoproles():
    response = flask.jsonify(poproles.tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route("/data/setup/roledict")
def getroledict():
    response = flask.jsonify(roledict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route("/data/setup/namedict")
def getnamedict():
    response = flask.jsonify(namedict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route("/data/setup/rolechamps")
def getrolechamps():
    response = flask.jsonify(rolechamps)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route('/data/<patch>/total')
def total(patch):
    response = flask.jsonify(np.load('data/'+patch+'/total.npy').tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route('/data/<patch>/games')
def games(patch):
    response = flask.jsonify(np.load('data/'+patch+'/games.npy').tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route('/data/<patch>/synergies')
def synergies(patch):
    response = flask.jsonify(np.load('data/'+patch+'/synergies.npy').tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route('/data/<patch>/counters')
def counters(patch):
    response = flask.jsonify(np.load('data/'+patch+'/counters.npy').tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route('/data/<patch>/roledeltas')
def roledeltas(patch):
    response = flask.jsonify(np.load('data/'+patch+'/roledeltas.npy').tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@application.route('/data/<patch>/basedeltas')
def basedeltas(patch):
    response = flask.jsonify(np.load('data/'+patch+'/basedeltas.npy').tolist())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# run the app.
if __name__ == "__main__":
    application.run()