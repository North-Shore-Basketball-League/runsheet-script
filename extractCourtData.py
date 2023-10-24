import datetime
from pathlib import Path
from dateutil.parser import parse
from thefuzz import fuzz, process
from extractWebData import ExtractWebData
import re
from printing import Printing


def check_similarity_string(str1, str2) -> bool:
    if fuzz.ratio(str1, str2) > 70:
        return True
    return False

def max_compare_tuple(e):
  return e[1]

def check_similarity_collection(str1, arr) -> str:
    similarityScore = process.extract(str1, arr, scorer=fuzz.ratio)
    closest = max(similarityScore, key=max_compare_tuple)
    return closest[0]

def get_court_data(teamPlayerData, years):
    iframeJSFP = Path(__file__).parent / "data" / "getIframeURL.js"
    webData = {}

    date = ""

    currentDate = datetime.datetime.now()

    for year in years:
        Printing().print_inline(f"Extracting years {year[0]} web data")
        yearData = {}
        extract = ExtractWebData()

        tableLinks = extract.get_table_urls(year[1], str(iframeJSFP))
        tableDataDf = extract.get_table_data(tableLinks, "times")

        tableData = tableDataDf.to_dict()

        rowIndex = -1

        if year[0] == "adults":
            dateIndex = "Dates:"
        else:
            dateIndex = "Dates & Times:"

        for gameDateIndex in tableData[dateIndex]:
            gameDate = tableData[dateIndex][gameDateIndex]

            gameDate = parse(gameDate)
            gameDate = datetime.datetime.fromtimestamp(
                gameDate.timestamp() + 86400)

            if gameDate > currentDate and rowIndex == -1:
                date = tableData[dateIndex][gameDateIndex]
                rowIndex = gameDateIndex

        if rowIndex == -1:
            raise Exception("Date could not be found")

        for col in tableData:
            colData = re.match(
                r"(?P<location>(BELROSE)|(ST IVES))?\W?(?P<time>(?P<timeNum>\d{0,3})\w\w) (?:(?:\(C(?:[tT]\s*)?)|Court)\s?(?P<court>\d)(?:\))?", col)

            if colData:
                if colData.groups()[0]:
                    venue = colData.group("location").title()
                else:
                    venue = "St Ives"
                court = colData.group("court")
                timeNum = colData.group("timeNum")
                time = colData.group("time")

                gameTeams = tableData[col][rowIndex]

                if re.search(r"long weekend", gameTeams.lower()):
                    raise Exception("No game this week")

                # This may throw some errors, is a very complex regex string
                teams = re.match(
                    r"(?P<team1>.*?)\W?(?:(\(W\) (?:v )?)|( v ))(?P<team2>.*?)\W?(?:\(B\).*)?$", tableData[col][rowIndex])


                if year[0] == "adults":
                    currentYear = "adults"

                    teamColours = [
                        "white",
                        "pink",
                        "yellow",
                        "orange",
                        "green",
                        "blue",
                        "red",
                        "black"
                    ]

                    teamOneFuzzy = check_similarity_collection(teams.group("team1"))
                    teamTwoFuzzy = check_similarity_collection(teams.group("team2")) 

                    if teamColours.index(teamOneFuzzy) < teamColours.index(teamTwoFuzzy):
                        white = teamOneFuzzy
                        black = teamTwoFuzzy
                    else:
                        white = teamTwoFuzzy
                        black = teamOneFuzzy

                else:
                    white = teams.group("team1")
                    black = teams.group("team2")

                    matchYearNum = re.search(
                        r"(?P<y1>[1-9][0-9]|[1-9]).(?P<y2>[1-9][0-9]|[1-9])", year[0])
                    currentYear = matchYearNum.group(
                        "y1") + "/" + matchYearNum.group("y2")

                playerDataWhite = white + "-" + currentYear

                playerDataBlack = black + "-" + currentYear

                for i in teamPlayerData:
                    match = re.match(
                        r"(?P<name>.*)-(?P<year>([0-9]+/[0-9]+)|adults)", i)
                    team = match.group("name")
                    dataYear = match.group("year")

                    if dataYear != currentYear:
                        continue

                    if check_similarity_string(white, team):
                        playerDataWhite = i

                    if check_similarity_string(black, team):
                        playerDataBlack = i

                if venue.lower() == "st ives":
                    dataIndex = timeNum + "_c" + court + "_s"
                elif venue.lower() == "belrose":
                    dataIndex = timeNum + "_c" + court + "_b"
                else:
                    raise Exception("venue not st ives or belrose")

                yearData[dataIndex] = {"venue": venue, "time": time, "court": court, "date": date,
                                       "white": white, "black": black, white: teamPlayerData[playerDataWhite], black: teamPlayerData[playerDataBlack]}

        webData[year[0]] = yearData

        del extract

    return webData, date
