#-----DATA ANALYSIS-----#


# we import the csv library to read the given dataset and import datetime to read each row['race_created'] and row['race_driven']

from flask import Flask, render_template, request
import csv 
from datetime import datetime
from collections import Counter
from bokehPlots import gamesPieChart, barChartChosenAndAverage, xSortedDictBarChart # these charts are lists of scripts and divs that will be used in html files






#------FUNCTIONS------#

# getListOfAllPlayers loops through a csv-file (our race data) and returns a list of all players without duplicates

def getListOfAllPlayers(dataset):
    players = []
    for row in dataset:
        if int(row['challenger']) != 0:
            players.append(int(row['challenger']))

        if int(row['opponent']) != 0:
            players.append(int(row['opponent']))

    return list(set(players)) # set: removes duplicates



# the function getListOfActivePlayers() creates a list of all challengers and opponents
# (who participated in at least one race) from our data and removes its duplicates

def getListOfActivePlayers(dataset):
    players = []
    for row in dataset:
        if row['status'] == 'finished':
            players.append(int(row['challenger']))
            players.append(int(row['opponent']))
    return list(set(players))



# getNumOfTracks returns the number of tracks from our data

def getNumOfTracks(dataset):
    tracks = []
    for row in dataset:
        tracks.append(row['track_id'])
    
    return len(set(tracks))



# getListOfTracks returns a list of all tracks from our data

def getListOfTracks(dataset):
    tracks = []
    for row in dataset:
        if row['status'] == 'finished':
            tracks.append(int(row['track_id']))

    return list(set(tracks))



# the function getDates uses our data to determine in which timespan all 
# races from our data were created and actually held; it returns the first and last date as a list

def getDates(dataset):
    dates = []
    for row in dataset:
        date_str1 = row['race_created']
        CreationDate = datetime.strptime(date_str1, '%d.%m.%Y')
        dates.append(CreationDate)

        d = row['race_driven']
        date_str2 = d.split(' ')

        if date_str2[0] != '0000-00-00':
            RaceDate = datetime.strptime(date_str2[0], '%d.%m.%Y')
            dates.append(RaceDate)
             
    firstDate = min(dates)
    lastDate = max(dates)
        
    return [firstDate.date(),lastDate.date()]



# the function getNumberOfGames creates and returns a dictionary 
# that holds all players as keys and their corresponding number of games as values

def getNumberOfGames(players, dataset):
    numOfGames = dict()
    for player in players:
        numOfGames[player] = 0

    for row in dataset:
        if row['status'] == 'finished': # we only consider the races that have been finished yet
            numOfGames[int(row['challenger'])] += 1
            numOfGames[int(row['opponent'])] += 1
    
    return numOfGames



# the function getRacesOnTrack creates a list of all tracks of the dataset and then determines 
# how many races have taken place on each of them. It returns a dictionary
#  with tracks as keys and the number of races on them as their values

def getRacesOnTracks(dataset):
    tracks = []
    for row in dataset:
        tracks.append(int(row['track_id']))
    
    racesByTrack = dict()

    for track in tracks:
        racesByTrack[track] = 0
    
    for row in dataset:
        if row['status'] == 'finished':
            racesByTrack[int(row['track_id'])] += 1
    
    return racesByTrack



# the function winLossRatio creates and returns a dictionary that holds all players 
# as keys and their win/loss ratios as values  

def winLossRatio(players, dataset):
    numOfWins = dict()
    numOfDefeats = dict()

    for player in players:
        numOfWins[player] = 0
        numOfDefeats[player] = 0

    for row in dataset:
        opp = int(row['opponent'])
        cha = int(row['challenger'])

        if cha == int(row['winner']):
            try:
                numOfWins[cha] += 1 
                numOfDefeats[opp] += 1
            except KeyError: 
                pass

        if opp == int(row['winner']):
            try:
                numOfWins[opp] += 1
                numOfDefeats[cha] += 1
            except KeyError:
                pass

    winLossRatios = dict()            
    for player in players:
        if numOfDefeats[player] == 0: 
            winLossRatios[player] = numOfWins[player] # prevents us from dividing by zero
        else:
            winLossRatios[player] = numOfWins[player]/numOfDefeats[player]

    return winLossRatios



# bigNumber rewrites large numbers with dots as thousands seperators

def bigNumber(number):
    if isinstance(number, int) or isinstance(number, float):
        if len(str(number)) > 3:
            num = f'{number:,}'.replace(',', ' ').replace('.', ',').replace(' ', '.') # replacing commas (American way of writing numbers) by dots
            return num
        else:
            return number
    else:
        return number



# the function getNumberOffFinishedRaces returns the number of all finished races from our data

def getNumberOfFinishedRaces(dataset):
    counter = 0
    for row in dataset:
        if row['status'] == 'finished':
            counter += 1
    return counter



# the function getIds loops through our dataset to creates a list of all ids

def getIds(dataset):
    ids = []
    for row in dataset:
        ids.append(int(row['id']))
    return ids



#  the function getBetMoney loops through our dataset and adds together the bet money of all finished races

def getBetMoney(dataset):
    totalMoney = 0
    for row in dataset:
        if row['status'] == 'finished':
            totalMoney += int(row['money'])
    return totalMoney



# COMMENT STILL NEEDED

def getNumOfWins(players, dataset):
    wins = dict()
    
    for player in players:
        wins[player] = 0
    
    for row in dataset:
        try:
            wins[int(row['winner'])] += 1
        except KeyError: # if player zero is stated as the winner (if the race is not finished yet), we get a KeyError
            pass
    
    return wins
    

 
# getHighest lets us receive any number of items that have the highest values in a dictionary.
# We can decide whether we want getHighest to return the keys or values of a dictionary by assigning parameter 'k' or 'v'

def getHighest(numberOfItems, dictionary, keyOrValue):
    
    c = Counter(dictionary)
    highest = c.most_common(numberOfItems) # highest is a list of tuples. Index 0 contains keys and index 1 contains the corresponding values
    
    keys = []
    values = []

    if keyOrValue == 'k':
        for h in highest:
            keys.append(h[0])
        return keys

    elif keyOrValue == 'v':
        for h in highest:
            values.append(h[1])
        return values



# moneyLostWon creates and returns a dictionary that holds players as keys and their 
# corresponding profit/loss in the game as values

def moneyLostWon(players, dataset):
    moneyWonLost = dict()

    for p in players:
        moneyWonLost[p] = 0

    for row in dataset:
        cha = int(row['challenger'])
        opp = int(row['opponent'])
        
        if int(row['winner']) == cha and cha != 0:
            moneyWonLost[cha] += int(row['money'])
            moneyWonLost[opp] -= int(row['money'])
        
        elif int(row['winner']) == opp and opp != 0:
            moneyWonLost[opp] += int(row['money'])
            moneyWonLost[cha] -= int(row['money'])

    return moneyWonLost



# getRank returns the index of a chosen player's value in a dictionary whose values are ordered by magnitude.
# By assigning 'False' to the parameter BigNumbersWin, we order the dictionary's values from big to small

def getRank(dictionary, players, chosenPlayer, bigNumbersWin = True):
    values = []
    for player in players:
        values.append(dictionary[player])

    sortedValues = sorted(values, reverse=bigNumbersWin)
    rank = sortedValues.index(dictionary[chosenPlayer]) + 1

    return rank



# getOpponentsGames returns a dict that holds a chosen player's opponents as keys 
# and their games against him/her as values

def getOpponentsGames(player, dataset, players):
    opponentsGames = dict()

    for p in players:
        opponentsGames[p] = 0

    for row in dataset:
        if int(row['challenger']) == player and row['status'] == 'finished':
            opponentsGames[int(row['opponent'])] += 1

        if int(row['opponent']) == player and row['status'] == 'finished':
            opponentsGames[int(row['challenger'])] += 1

    return opponentsGames



# getMostlychallenged returns a dictionary that holds players our chosen player has challenged as keys;
# values are the number of times our player had challenged each opponent (key)

def getMostlyChallenged(player, dataset, players):
    challenges = dict()

    for p in players:
        challenges[p] = 0
    
    for row in dataset:
        if player == int(row['challenger']):
            if int(row['opponent']) != 0:
                challenges[int(row['opponent'])] += 1

    return challenges



# getMostlychallenged returns a dictionary that holds players that challenged our chosen player as keys;
# values are the number of times our player had been challenged by each opponent (key)

def getMostlyChallengedBy(player, dataset, players):
    challengedBy = dict()

    for p in players:
        challengedBy[p] = 0

    for row in dataset:
        if player == int(row['opponent']):
            challengedBy[int(row['challenger'])] += 1

    return challengedBy



# ChallengeDeclineRatio returns the percentage of challenges that our chosen player has declined

def ChallengeDeclineRatio(player, dataset):
    challenges = 0
    declines = 0
    for row in dataset:
        if player == int(row['opponent']):
            challenges += 1
            if row['status'] == 'declined':
                declines += 1
    ratio = declines/challenges
    percentage = round(ratio, 3)

    return percentage*100



# getAverageBetByPlayer returns a dictionary that holds players as its keys and their average bet per game as values

def getAverageBetByPlayer(players, dataset, numOfGames):
    betDict = dict()
    avBets = dict()

    for player in players:
        betDict[player] = 0
    
    for row in dataset:
        if row['status'] == 'finished':
            betDict[int(row['challenger'])] += int(row['money'])
            betDict[int(row['opponent'])] += int(row['money'])

    for player in players:
        if betDict[player] == 0:
            avBets[player] = 0
        else:
            avBets[player] = betDict[player]/numOfGames[player]

    return avBets



# trackPreference returns a dictionary that holds tracks our chosen player drove as keys;
# values are the number of times he/she drove each of them

def trackPreference(player, dataset, tracks):
    racesOnTracks = dict()
    for track in tracks:
        racesOnTracks[int(track)] = 0
        
    for row in dataset:
        if player == int(row['challenger']) or player == int(row['opponent']):
            if row['status'] == 'finished':
                racesOnTracks[int(row['track_id'])] += 1

    return racesOnTracks

    
    
# handleForecast edits the forecast data in our csv file in a way that lets us access it as a list of dictionaries 
# of which each holds the four types of weather as keys and their corresponding probabilities as values   

def handleForecast(dataset):
    forecasts = []
    
    for row in dataset:
        probabilities = dict()

        f = row['forecast'].split('{')
        forecast = f[1].split(';')

        probabilities['sunny'] = forecast[1].split(':')[1]
        probabilities['rainy'] = forecast[3].split(':')[1]
        probabilities['thundery'] = forecast[5].split(':')[1]
        probabilities['snowy'] = forecast[7].split(':')[1]
        forecasts.append(probabilities)

    return forecasts
        

    
# getForecastPreference returns a dictionary that holds the four types of weather as keys and the amount
# of games that a chosen player had driven when the corresponding weather was predicted as values

def getForecastPreference(dataset, player, forecasts):
    favorites = []
    racesByForecast = dict()

    for row in dataset:
        if int(row['challenger']) == player or int(row['opponent']) == player:
            if row['status'] == 'finished':
                probs = []
                currentForecast = forecasts[int(row['id'])-1]
                probs.append(int(currentForecast['sunny']))
                probs.append(int(currentForecast['rainy']))
                probs.append(int(currentForecast['thundery']))
                probs.append(int(currentForecast['snowy']))
                sort = sorted(probs)

                for i in range(0,3):
                    if probs[i] == sort[3]:
                        if i == 0:
                            favorites.append('sunny')
                        elif i == 1:
                            favorites.append('rainy')
                        elif i == 2:
                            favorites.append('thundery')
                        elif i == 3:
                            favorites.append('snowy')

    sunnyRaces = 0
    for f in favorites:
        if f == 'sunny':
            sunnyRaces += 1

    rainyRaces = 0
    for f in favorites:
        if f == 'rainy':
            rainyRaces += 1

    thunderyRaces = 0
    for f in favorites:
        if f == 'thundery':
            thunderyRaces += 1

    snowyRaces = 0
    for f in favorites:
        if f == 'snowy':
            snowyRaces += 1

    racesByForecast['Sonnig'] = sunnyRaces
    racesByForecast['Regnerisch'] = rainyRaces
    racesByForecast['Gewittrig'] = thunderyRaces
    racesByForecast['Verschneit'] = snowyRaces

    return racesByForecast



# weatherSwitch changes the English weather nominations to the German ones so that we can implement them in our html files

def weatherSwitch(weather):

    if weather == 'sunny':
        return 'Sonnig'

    if weather == 'rainy':
        return 'Regnerisch'
    
    if weather == 'thundery':
        return 'Gewittrig'
    
    if weather == 'snowy':
        return 'Verschneit'

    

# getPerformanceByWeather returns a dictionary that holds the four types of weather as keys and our
# chosen player's win/loss ratio when racing during the specific weather circumstances as values

def getPerformanceByWeather(player, dataset):
    winsByWeather = dict()
    defeatsByWeather = dict()
    winLossByWeather = dict()
    keys = ['Sonnig', 'Regnerisch', 'Gewittrig', 'Verschneit']

    for key in keys:
        winsByWeather[key] = 0
        defeatsByWeather[key] = 0

    for row in dataset:
        if row['status'] == 'finished':
            if player == int(row['challenger']) or player == int(row['opponent']):
                weather = row['weather']

                if player == int(row['winner']):
                    winsByWeather[weatherSwitch(weather)] += 1
                
                if player != int(row['winner']):
                    defeatsByWeather[weatherSwitch(weather)] += 1


    for key in keys:
        try:
            if defeatsByWeather[key] == 0:
                winLossByWeather[key] = winsByWeather[key]
            else:
                winLossByWeather[key] = winsByWeather[key]/defeatsByWeather[key]
        except KeyError:
            winLossByWeather[key] = 0

    return winLossByWeather





#-----FLASK APP-----#


with open('resources/races.csv', mode='r') as csv_file: # opening the csv file and assigning the variable name 'rd' to our race data
        race_data = csv.DictReader(csv_file, delimiter=';')
        rd = list(race_data)

app = Flask(__name__, static_url_path='/static')



@app.route('/') # homepage
def main():

    allPlayers = getListOfAllPlayers(rd)
    firstLastDate = getDates(rd)
    fd = firstLastDate[0].strftime("%d.%m.%Y") # transforming dates to German notation
    ld = firstLastDate[1].strftime("%d.%m.%Y")
    nfr = getNumberOfFinishedRaces(rd)
    np = len(getListOfActivePlayers(rd))
    nr = len(getIds(rd))
    p = round(nfr/nr, 3)*100
    mny = getBetMoney(rd)
    avBet = round(mny/nfr, 1)
    nt = getNumOfTracks(rd)


    return render_template('index.html', allPlayers = bigNumber(len(allPlayers)), firstDate = fd, lastDate = ld, finishedRaces = bigNumber(nfr),  numOfPlayers = bigNumber(np),
                            numOfRaces = bigNumber(nr), percentage = p, totalMoney = bigNumber(mny), averageBet = bigNumber(avBet), numOfTracks = nt)



@app.route('/Sieger-und-Verlierer')
def rankings():
    players = getListOfActivePlayers(rd)
    numOfGames = getNumberOfGames(players, rd)
    numOfWins = getNumOfWins(players, rd)
    winLoss = winLossRatio(players, rd)
    money = moneyLostWon(players,rd)
    racesByTrack = getRacesOnTracks(rd)
    finishedRaces = getNumberOfFinishedRaces(rd)
    tracks = getListOfTracks(rd)
    racesOnTracks = getRacesOnTracks(rd)
    tracks = getListOfTracks(rd)


    moneyLost = dict()
    fewRaces = dict()


    for track in tracks:
        fewRaces[track] = -1*racesByTrack[track]
    

    for p in players:
        moneyLost[p] = -1*money[p]
    
    leastRacesByTrack = getHighest(3, fewRaces, 'k')
    fewRacesByTrack = getHighest(3, fewRaces, 'v')
    mostRacesByTrack = getHighest(3, racesByTrack, 'k')
    racesByTrack = getHighest(3, racesByTrack, 'v')
    mostGamesByPlayer = getHighest(3, numOfGames, 'k')
    gamesByPlayer = getHighest(3, numOfGames, 'v')
    winLossPlayers = getHighest(3, winLoss, 'k')
    winLossRatios = getHighest(3, winLoss, 'v')
    mostMoneyLostPlayers = getHighest(3, moneyLost, 'k')
    mostMoneyLost = getHighest(3, moneyLost, 'v')
    mostMoneyWonPlayers = getHighest(3, money, 'k')
    mostMoneyWon = getHighest(3, money, 'v')
    bestPlayers = getHighest(3, numOfWins, 'k')
    playersWins = getHighest(3, numOfWins, 'v')

    playersGames = []
    playersRatios = []


    for bp in bestPlayers:
        playersGames.append(numOfGames[bp])
        ratio = numOfWins[bp]/numOfGames[bp]
        playersRatios.append(round(ratio*100, 1))

    for race in fewRacesByTrack:
        s = str(race)
        newS = s.replace("-", "")
        index = fewRacesByTrack.index(race)
        fewRacesByTrack[index] = newS

    for wlr in winLossRatios:
        rounded = round(wlr,1)
        index = winLossRatios.index(wlr)
        winLossRatios[index] = rounded

    for mmw in mostMoneyWon:
        adjusted = bigNumber(mmw)
        index = mostMoneyWon.index(mmw)
        mostMoneyWon[index] = adjusted
    
    for mml in mostMoneyLost:
        adjusted = bigNumber(mml)
        index = mostMoneyLost.index(mml)
        mostMoneyLost[index] = adjusted



        gamesPie = gamesPieChart(players, numOfGames, finishedRaces)
        tracksBars = xSortedDictBarChart(tracks, racesOnTracks, 'Rennen pro Strecke')

    return render_template('rankings.html', bestPlayers = bestPlayers, playersWins = playersWins, playersGames = playersGames, ratios = playersRatios,
                            mostGamesByPlayer = mostGamesByPlayer, gamesByPlayer = gamesByPlayer, winLossPlayers = winLossPlayers, winLossRatios = winLossRatios,
                            mostMoneyWonPlayers = mostMoneyWonPlayers, mostMoneyWon = mostMoneyWon, mostMoneyLostPlayers = mostMoneyLostPlayers, mostMoneyLost = mostMoneyLost,
                            mostRacesByTrack = mostRacesByTrack, racesByTrack = racesByTrack, leastRacesByTrack = leastRacesByTrack, fewRacesByTrack = fewRacesByTrack,
                            gamesPieChartScript = gamesPie[0], gamesPieChartDiv = gamesPie[1], tracksBarChartScript = tracksBars[0], tracksBarChartDiv = tracksBars[1])




@app.route('/Spieler', methods = ["POST","GET"])
def pickPlayer():
    players = getListOfAllPlayers(rd)
    return render_template("pickplayer.html", players = players)




@app.route('/Spieler/SpielerDaten', methods=["POST", "GET"])
def test():
    p = request.form.get('comp_select')
    player = int(p)
    players = getListOfAllPlayers(rd)
    
    opponentsGames = getOpponentsGames(player, rd, players)
    numberOfGames = getNumberOfGames(players, rd)
    numberOfWins = getNumOfWins(players, rd)
    winLossRatios = winLossRatio(players, rd)
    moneyDict = moneyLostWon(players, rd)
    mostlyChallenged = getMostlyChallenged(player, rd, players)
    mostlyChallengedBy = getMostlyChallengedBy(player, rd, players)
    avBets = getAverageBetByPlayer(players, rd, numberOfGames)
    trackPref = trackPreference(player, rd, getListOfTracks(rd))
    weather = handleForecast(rd)
    forecastPref = getForecastPreference(rd, player, weather)
    performanceByWeather = getPerformanceByWeather(player, rd)

    money = bigNumber(moneyDict[player])
    ratio = round(winLossRatios[player], 2)
    numOfGames = numberOfGames[player]
    numOfWins = numberOfWins[player]
    
    favTrack = getHighest(1, trackPref, 'k')
    racesOnTrack = getHighest(1, trackPref, 'v')
    mainChallenger = getHighest(1, mostlyChallengedBy, 'k')
    howOftenChallengedBy = getHighest(1, mostlyChallengedBy, 'v')
    mainlyChallenged = getHighest(1, mostlyChallenged, 'k')
    howOftenChallenged = getHighest(1, mostlyChallenged, 'v')
    commonOpponent = getHighest(1, opponentsGames, 'k')
    gamesWithOpponent = getHighest(1, opponentsGames, 'v')
    favWeatherForecast = getHighest(1, forecastPref, 'k')
    bestWeatherPerformance = getHighest(1, performanceByWeather, 'k')

    revTrackDict = dict()
    for i in trackPref.items():
        revTrackDict[i[0]] = -1 * i[1]

    leastFavTrack = getHighest(1, revTrackDict, 'k')
    racesOnLeastFav = getHighest(1, revTrackDict, 'v')


    


    rankMoney = getRank(moneyDict, players, player)
    rankGames = getRank(numberOfGames, players, player)
    rankWins = getRank(numberOfWins, players, player)
    rankRatio = getRank(winLossRatios, players, player)
    rankAvBet = getRank(avBets, players, player)


    barChartRacesOnTrack = xSortedDictBarChart(getListOfTracks(rd), trackPref, 'Rennen pro Strecke')
    barChartGames = barChartChosenAndAverage(players, numberOfGames, player, "Anzahl an Spielen des gewählten Spielers und des Durchschnitts")
    barChartWins = barChartChosenAndAverage(players, numberOfWins, player, "Anzahl an Siegen des gewählten Spielers und des Durchschnitts")
    barChartAvBet = barChartChosenAndAverage(players, avBets, player, "Durchschnittlicher Einsatz pro Spiel")
    forecastChart = xSortedDictBarChart(['Sonnig', 'Regnerisch', 'Gewittrig', 'Verschneit'], forecastPref, 'Rennen je nach Wettervorhersage')
    weatherPerformanceChart = xSortedDictBarChart(['Sonnig', 'Regnerisch', 'Gewittrig', 'Verschneit'], performanceByWeather, "Sieg/Niederlage-Verhältnis je nach Wetter")

    return render_template('playerData.html', player = player, rankGames = rankGames, numOfGames = numOfGames, numOfWins = numOfWins, rankWins = rankWins, 
                                              ratio = ratio, rankRatio = rankRatio, money = money, rankMoney = rankMoney,
                                              scriptBarChartGames = barChartGames[0], divBarChartGames = barChartGames[1], scriptBarChartWins = barChartWins[0],
                                              divBarChartWins = barChartWins[1], commonOpponent = commonOpponent, gamesWithOpponent = gamesWithOpponent, mainChallenger = mainChallenger,
                                              howOftenChallengedBy = howOftenChallengedBy, mainlyChallenged = mainlyChallenged, howOftenChallenged = howOftenChallenged,
                                              declineRatio = ChallengeDeclineRatio(player, rd), rankAvBet = rankAvBet, avBet = round(avBets[player],1), scriptBetChart = barChartAvBet[0],
                                              divBetChart = barChartAvBet[1], favTrack = favTrack, racesOnTrack = racesOnTrack, leastFavTrack = leastFavTrack, racesOnLeastFav = -1*racesOnLeastFav[0],
                                              scriptRacesOnTrack = barChartRacesOnTrack[0], divRacesOnTrack = barChartRacesOnTrack[1], favWeatherForecast = favWeatherForecast,
                                              scriptForecastChart = forecastChart[0], divForecastChart = forecastChart[1], bestWeatherPerformance = bestWeatherPerformance, 
                                              scriptWeatherChart = weatherPerformanceChart[0], divWeatherChart = weatherPerformanceChart[1])

    


if __name__ == '__main__':
    app.run(debug = True)





