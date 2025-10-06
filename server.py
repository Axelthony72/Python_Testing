import json
from flask import Flask, render_template, request, redirect, url_for, flash

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions
    
def loadBookings():
    with open('bookings.json') as b:
        listOfBookings = json.load(b)['bookings']
        return listOfBookings    

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
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    placesRequired = int(request.form['places'])

    # Vérifications des erreurs
    if int(club['points']) < placesRequired:
        flash("You do not have enough points to make this purchase.", "danger")
    elif placesRequired > int(competition['numberOfPlaces']):
        flash("Not enough places available.", "danger")
    elif placesRequired > 12:
        flash("You cannot purchase more than 12 places.", "danger")
    else:
        # --- NOUVELLE LOGIQUE D'ENREGISTREMENT ---
        # 1. Mettre à jour les points et les places
        club['points'] = str(int(club['points']) - placesRequired)
        competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)

        # 2. Charger les réservations existantes
        bookings = loadBookings()

        # 3. Créer la nouvelle réservation
        new_booking = {
            "club": club['name'],
            "competition": competition['name'],
            "places": placesRequired
        }
        bookings.append(new_booking)

        # 4. Réécrire le fichier avec la nouvelle réservation
        with open('bookings.json', 'w') as b:
            json.dump({'bookings': bookings}, b, indent=4)
        # --- FIN DE LA NOUVELLE LOGIQUE ---

        flash('Great-booking complete!', 'success')

    # On passe `club=club` pour que la page se réaffiche correctement
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', clubs=clubs)

@app.route('/bookings/<club_name>')
def bookings(club_name):
    bookings = loadBookings()
    # On filtre pour ne garder que les réservations du club demandé
    club_bookings = [b for b in bookings if b['club'] == club_name]
    return render_template('bookings.html', club_name=club_name, bookings=club_bookings)
