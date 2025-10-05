import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [c for c in clubs if c['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        flash("Sorry, that email is not found.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    placesRequired = int(request.form['places'])

    # Ajout de la vérification de la règle des 12 places
    if placesRequired > 12:
        flash("You cannot purchase more than 12 places.")
    else:
        # Cette partie ne s'exécute que si la condition est fausse
        club['points'] = int(club['points']) - placesRequired
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        flash('Great-booking complete!')

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))