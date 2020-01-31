import os
import sys
from datetime import *
import requests
from pprint import pprint
from typing import List
import json

# The purpose of this script is to find the largest deficit that a
# Rocket Richard Winner (or equivalent) has come back from.
# The first year with data is the 1917 season

lookupURL = "https://statsapi.web.nhl.com/api/v1/game/YYYY02ZZZZ/boxscore"


def is_message_valid(json_object) -> bool:
    try:
        if json_object['message'] == "Game data couldn't be found":
            return False
    except:
        return True


def is_skater(json_object, player_id) -> bool:
    try:
        if json_object[player_id]['stats']['skaterStats']:
            return True
    except:
        return False


# Pass in the player stats from team level
def parse_player_stats_from_message(json_object) -> List:
    # return list of tuples, ("player_name", num_of_goals)
    player_stats = []

    # parse home team first
    for player_id in json_object['home']['players']:
        # Let's just exclude goalies. Sorry Marty
        if is_skater(json_object['home']['players'], player_id):
            player_stats.append((json_object['home']['players'][player_id]['person']['fullName'],
                                 json_object['home']['players'][player_id]['stats']['skaterStats']['goals']))
    # parse away team next
    for player_id in json_object['away']['players']:
        # Let's just exclude goalies. Sorry Marty
        if is_skater(json_object['away']['players'], player_id):
            player_stats.append((json_object['away']['players'][player_id]['person']['fullName'],
                                 json_object['away']['players'][player_id]['stats']['skaterStats']['goals']))
    return player_stats


def find_rocket_winners(year) -> List:
    player_goal_count = dict()
    game_list = []
    # Game format is 'year''02''Game ID' where year is 4 digits, 02 means regular season, and game Id increases from 0

    # There are currently 1271 games played per year. Will need to update when Seattle is a team
    for game_number in range(1, 1271):
        if game_number % 10 == 0:
            print("Looking up game number " + str(game_number) + " in year " + str(year))
        game_request_string = lookupURL.replace("YYYY", str(year)).replace("ZZZZ", str(game_number).zfill(4))
        while True:
            try:
                response = requests.get(game_request_string)
                break;
            except requests.ConnectionError:
                pass
        json_object = response.json()
        if is_message_valid(json_object):
            player_list = parse_player_stats_from_message(json_object['teams'])
        else:
            print("Breaking because the message is invalid for " + game_request_string)
            break

        game_list.append(player_list)

        for player in player_list:
            if player[0] in player_goal_count:
                player_goal_count[player[0]] = player_goal_count[player[0]] + player[1]
            else:
                player_goal_count[player[0]] = player[1]

    winners = []
    for key, value in reversed(sorted(player_goal_count.items(), key=lambda x: x[1])):
        if not winners:
            winners.append((key, value))
        elif winners[0][1] == value:
            winners.append((key, value))
    return winners, game_list


def find_largest_deficit(year, rocker_winners, game_list) -> tuple:
    player_goal_count = dict()
    max_deficit = dict()

    for winner in rocker_winners:
        max_deficit[winner[0]] = ("None", 0)
    # Game format is 'year''02''Game ID' where year is 4 digits, 02 means regular season, and game Id increases from 0

    # There are currently 1271 games played per year. Will need to update when Seattle is a team
    game_number = 0
    for player_list in game_list:
        game_number += 1
        if game_number % 10 == 0:
            print("Looking up game number " + str(game_number) + " in year " + str(year))

        for player in player_list:
            if player[0] in player_goal_count:
                player_goal_count[player[0]] = player_goal_count[player[0]] + player[1]
            else:
                player_goal_count[player[0]] = player[1]

            for winner in rocker_winners:
                if winner[0] in player_goal_count and \
                        (player_goal_count[player[0]] - player_goal_count[winner[0]]) > max_deficit[winner[0]][1]:
                    max_deficit[winner[0]] = (player[0], player_goal_count[player[0]] - player_goal_count[winner[0]])
                elif winner[0] not in player_goal_count and player_goal_count[player[0]] > max_deficit[winner[0]][1]:
                    max_deficit[winner[0]] = (player[0], player_goal_count[player[0]])

    for key, value in reversed(sorted(max_deficit.items(), key=lambda x: x[1])):
        return key, value[0], value[1], year


def main():
    # unfortunately, there is no way to look at league statistics entirely.
    # We have to run through all seasons to find the winner, then run the season again to see
    # where the deficit was the largest

    # The first year with data is 1917
    start_season = 1917
    end_season = date.today().year - 1

    # if the current season hasn't ended yet, go back to the previous year
    if date(date.today().year, date.today().month, date.today().day) < date(date.today().year, 4, 15):
        end_season -= 1

    max_largest_deficit = ("", "", 0, 1900)

    for year in range(start_season, end_season):
        rocket_winners = find_rocket_winners(year)
        winners = rocket_winners[0]
        game_list = rocket_winners[1]

        if len(rocket_winners) is None:
            continue

        # find largest deficit
        largest_deficit_this_year = find_largest_deficit(year, winners, game_list)

        if largest_deficit_this_year is None:
            continue

        if largest_deficit_this_year[2] > max_largest_deficit[2]:
            max_largest_deficit = largest_deficit_this_year

    print(
        "The largest deficit was in " + str(max_largest_deficit[3]) + "  was " + max_largest_deficit[0] + " trailing " +
        max_largest_deficit[1] + " by " +
        str(max_largest_deficit[2]) + " goals")


if __name__ == '__main__':
    main()
