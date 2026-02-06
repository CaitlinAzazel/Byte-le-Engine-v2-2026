import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone, tzinfo
from typing import Any, TypeVar, Callable, Generic

import requests
import urllib3
from requests import Response, HTTPError

# Generic type for Ok which gets specified in a called method
T = TypeVar('T')


@dataclass
class Result(Generic[T]):
    Ok: T | None = None
    Err: str | None = None

    def is_ok(self) -> bool:
        return self.Err is None

    def is_err(self) -> bool:
        return self.Err is not None


def as_result(func: Callable):
    # wraps into Result if it does not already return a Result
    def wrapper(*args, **kwargs):
        try:
            temp: Any = func(*args, **kwargs)

            if isinstance(temp, Result):
                return Result(Ok=temp.Ok, Err=temp.Err)

            return Result(Ok=temp)

        except Exception as e:
            return Result(Err=str(e))
    return wrapper


class ClientUtils:
    def __init__(self, csv_bool: bool) -> None:
        urllib3.disable_warnings()
        self.IP = 'http://134.129.106.84:8000/'
        self.path_to_public = False
        self.use_csv: bool = csv_bool
        self.tournaments: list = []

    # convert utc to local time
    def convert_utc_to_local(self, utc_str: str = '2000-10-31T06:30:00Z') -> datetime:
        a: datetime = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        tz: tzinfo = datetime.now().astimezone().tzinfo
        a = a.replace(tzinfo=timezone.utc)

        return a.astimezone(tz)

    # get team types
    @as_result
    def get_team_types(self) -> Result[list[dict]]:
        resp = requests.get(self.IP + 'team_types/',
                            verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return json.loads(resp.content)

    # get unis
    @as_result
    def get_unis(self) -> Result[list[dict]]:
        resp = requests.get(self.IP + 'universities/', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return json.loads(resp.content)

    # post get score over time - fix later
    @as_result
    def get_score_over_time(self, vid, group_run_id, team_uuid):
        resp = requests.post(
            self.IP + 'get_score_over_time', json={'vid': vid}, verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        jsn = json.loads(resp.content)
        print('The following is your team\'s performance in each tournament')
        self.print_table(jsn)

    # post submission
    @as_result
    def submit_file(self, fil: bytes, vid: str) -> Result[dict]:
        data = {'submission_id': 0, 'submission_time': datetime.utcnow().isoformat(), 'file_txt': fil.decode("utf-8"),
                'team_uuid': vid}
        resp = requests.post(
            self.IP + 'submission/', json=data, verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return json.loads(resp.content)

    # gets the runs from an INDIVIDUAL get_submission
    @as_result
    def get_submission(self, subid: int, vid: str, prints_table: bool = True) -> dict:
        resp = requests.get(
            self.IP + f'submission?submission_id={subid}&team_uuid={vid}', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        jsn = json.loads(resp.content)
        jsn['submission_time'] = self.convert_utc_to_local(utc_str=jsn['submission_time']).strftime(
            '%m/%d/%Y, %H:%M:%S')

        to_table: dict = {'ID': jsn['submission_id'],
                          'Submission Time': jsn['submission_time']}
        if prints_table:
            self.print_table(to_table)
        return jsn

    @as_result
    def get_submission_run_info(self, subid: int, vid: str) -> Result[None]:
        resp = requests.get(
            self.IP + f'submission?submission_id={subid}&team_uuid={vid}', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        jsn = json.loads(resp.content)
        jsn = jsn['submission_run_infos']
        if len(jsn) == 0:
            raise ValueError('This submission has no details.')
        for sri in jsn:
            del sri['run']

        self.print_table(jsn)

    # MULTIPLE get_submissions
    @as_result
    def get_submissions(self, vid: str) -> None:
        resp = requests.get(
            self.IP + f'submissions?team_uuid={vid}', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        jsn = json.loads(resp.content)
        to_table: list = sorted([{'ID': x['submission_id'],
                                  'Submission Time': self.convert_utc_to_local(utc_str=x['submission_time']).strftime(
                                      '%m/%d/%Y, %H:%M:%S'),
                                  } for x in jsn], key=lambda x: x['Submission Time'], reverse=True)

        self.print_table(to_table)

    # post
    @as_result
    def register(self, uni_id: int, team_type_id: int, team_name: str) -> Result[Response]:
        data = {'uni_id': uni_id, 'team_type_id': team_type_id, 'team_name': team_name}
        resp = requests.post(
            self.IP + 'team', json=data, verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return resp

    # get all runs
    @as_result
    def get_runs(self) -> dict:
        resp = requests.get(self.IP + f'run/', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return json.loads(resp.content)

    # get runs that match a tournament id and a team uuid
    @as_result
    def get_runs_filter(self, tournament_id: int, vid: str) -> None:
        resp = requests.get(self.IP + f'get_run?tournament_id={tournament_id}&team_uuid={vid}',
                            verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        jsn = json.loads(resp.content)
        jsn['run_time'] = self.convert_utc_to_local(utc_str=jsn['run_time']).strftime('%m/%d/%Y, %H:%M:%S')
        self.print_table(jsn)

    @as_result
    def get_runs_for_submission(self, submission_id: int, team_uuid: str) -> Result[None]:
        resp = requests.get(self.IP + f'submission?submission_id={submission_id}&team_uuid={team_uuid}',
                            verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        jsn = json.loads(resp.content)
        jsn = [submission_run_info['run'] for submission_run_info in jsn['submission_run_infos']]
        if len(jsn) == 0:
            raise ValueError('This submission has no runs.')
        for run in jsn:
            run['run_time'] = self.convert_utc_to_local(utc_str=run['run_time']).strftime('%m/%d/%Y, %H:%M:%S')
            del run['results']
        self.print_table(jsn)

    # gets the code file from the specified submission using the submission id
    @as_result
    def get_code_from_submission(self, submission_id, vid) -> Result:
        temp: Result[dict] = self.get_submission(submission_id, vid, False)
        if temp.is_err():
            return temp
        submission_json: dict = temp.Ok
        if submission_json['file_txt'] == "":
            print("Bad Vid and subid combination (probably)")
        else:
            content = submission_json['file_txt']
            with open(f"./code_for_submission_{submission_id}.py", "w") as fl:
                fl.write(content)
            print(
                f"Code for submission {submission_id} has been written {os.path.realpath(fl.name)}")
        return Result()

    # Building a comma-separated-values list table or ascii table based on passed in data below
    # The tables are used to build the leaderboard

    # helper method to format the csv or ascii table
    def get_longest_cell_in_cols(self, json, json_atribs):
        col_longest_length = {}
        for key in json_atribs:
            col_longest_length[key] = (len(key))
        for col in json_atribs:
            for row in json:
                if len(str(row[col])) > col_longest_length[col]:
                    col_longest_length[col] = len(str(row[col]))
        return col_longest_length

    # creates a line that separates rows of information in the table
    def get_seperator_line(self, col_longest_length, padding):
        rtn = ''
        for key in col_longest_length:
            rtn += '+' + ('-' * (col_longest_length[key] + padding))
        return rtn + '+'

    # prints table based on passed bool on instantiation
    def print_table(self, json):
        print()  # used for formatting
        if self.use_csv:
            self.print_csv_table(json)
        else:
            self.print_ascii_table(json)

    # prints the csv table
    def print_csv_table(self, json):
        try:
            padding = 4
            json_atribs = json[0].keys()
            output = ''
            for index, key in enumerate(json_atribs):
                output += key
                if index != len(json_atribs) - 1:
                    output += ','
            output += '\n'
            for row in json:
                for index, col in enumerate(row):
                    if isinstance(row[col], int) or isinstance(row[col], float):
                        output += str(row[col])
                    else:
                        output += '"' + str(row[col]) + '"'
                    if index != len(row) - 1:
                        output += ','
                output += '\n'
            print(output)
        except BaseException as e:
            print(e)
            print(
                "Something went wrong. Maybe there isn't data for what you're looking for")

    # prints the ascii table
    def print_ascii_table(self, json):
        try:
            padding = 4
            json_atribs = json[0].keys()
            col_longest_length = self.get_longest_cell_in_cols(
                json, json_atribs)
            line_seperator = self.get_seperator_line(
                col_longest_length, padding)
            row_format = ''
            for key in json_atribs:
                row_format += "|{:^" + \
                              str(col_longest_length[key] + padding) + '}'
            row_format += '|'
            print(line_seperator)
            print(row_format.format(*json_atribs))
            for row in json:
                print(line_seperator)
                print(row_format.format(*[str(x) for x in row.values()]))
            print(line_seperator)
        except BaseException as e:
            print(e)
            print(
                "Something went wrong. Maybe there isn't data for what you're looking for")

    # get tournaments for leaderboard
    @as_result
    def get_tournaments(self):
        resp = requests.get(self.IP + 'tournaments/', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return json.loads(resp.content)

        # get tournaments for leaderboard

    @as_result
    def get_tournament(self, tournament_id: int):
        resp = requests.get(self.IP + f'tournament?tournament_id={tournament_id}', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return [json.loads(resp.content), ]

    @as_result
    def get_latest_tournament(self):
        resp = requests.get(self.IP + 'latest_tournament/', verify=self.path_to_public)
        if resp.status_code >= 400:
            raise HTTPError(resp.content.decode('utf-8'))
        return [json.loads(resp.content), ]

    # finds uni_id and uni_name for building the leaderboard by calling get_unis() method
    @as_result
    def get_leaderboard(self, wants_all: bool, include_ineligible: bool, leaderboard_id: int | None) -> Result:
        # collect info needed to build leaderboard
        temp: Result = self.get_leaderboard_uni_info()
        if temp.is_err():
            return temp
        uni_info: dict = temp.Ok

        temp: Result = self.get_leaderboard_team_type_info()
        if temp.is_err():
            return temp
        team_info: dict = temp.Ok

        # put info together to build leaderboard
        temp: Result = self.print_leaderboard_info(wants_all, uni_info, team_info, include_ineligible,
                                                   leaderboard_id)

        if temp.is_err():
            return temp

        return Result()

    @as_result
    def get_leaderboard_uni_info(self) -> Result | dict:
        temp: Result = self.get_unis()
        if temp.is_err():
            return temp
        unis_info: list[dict] = temp.Ok
        return {uni['uni_id']: uni['uni_name'] for uni in unis_info}

    # finds the type_type_id, team_name, and eligible
    @as_result
    def get_leaderboard_team_type_info(self) -> Result | dict:
        temp: Result = self.get_team_types()
        if temp.is_err():
            return temp
        team_types: list[dict] = temp.Ok
        return {team_type['team_type_id']: {'name': team_type['team_type_name'], 'eligible': team_type['eligible']}
                for team_type in team_types}

    # collects all data needed for building the leaderboard
    @as_result
    def print_leaderboard_info(self, wants_all: bool,  uni_info: dict, team_info: dict, include_ineligible: bool,
                               leaderboard_id: int | None) -> Result:
        temp: Result

        if wants_all:
            temp = self.get_tournaments()
        elif leaderboard_id is not None and leaderboard_id > -1:
            temp = self.get_tournament(leaderboard_id)
        elif not wants_all and leaderboard_id is None:
            temp = self.get_latest_tournament()
        else:
            temp = self.get_tournaments()

        if temp.is_err():
            return temp

        tournaments: list[dict] = temp.Ok

        tournament_id = 0 if not wants_all else self.__print_leaderboard_info_helper(tournaments)

        results: dict = {}

        temp = self.get_tournament(tournaments[tournament_id]['tournament_id'])

        if temp.is_err():
            return temp

        for run in temp.Ok[0]['runs']:
            if any([1 for submission_run_info in run['submission_run_infos']
                    if not include_ineligible and not team_info[submission_run_info['submission']['team'][
                    'team_type_id']]['eligible']]):
                continue
            for submission_run_info in run['submission_run_infos']:
                team_name: str = submission_run_info['submission']['team']['team_name']

                # makes a dict of {'Example Team Name': {all info needed to build leaderboard}}
                if results.get(team_name) is None:
                    results[team_name] = {'Team Name': team_name,
                                          'University': uni_info[submission_run_info['submission']['team']['uni_id']],
                                          'Points Awarded': submission_run_info['points_awarded'],
                                          'Team Type':
                                              team_info[submission_run_info['submission']['team']['team_type_id']][
                                                  'name'],
                                          'Eligible':
                                              team_info[submission_run_info['submission']['team']['team_type_id']][
                                                  'eligible']}
                else:
                    results[team_name]['Points Awarded'] += submission_run_info['points_awarded']
        result = list(results.values())
        result.sort(key=lambda row: row['Points Awarded'], reverse=True)

        if len(result) == 0:
            raise Exception('No runs for latest tournament.')

        self.print_table(result)

        return Result()

    # Helper method to print the print_leaderboard_method
    def __print_leaderboard_info_helper(self, tournaments: list[dict]) -> int:
        list_result: list = []

        for index, tournament in enumerate(tournaments):
            if not tournament['is_finished']:
                continue
            # A list of dictionaries that stores the tournament, its index in the list, and when it started
            list_result.append({
                'Index': index,
                'Tournament ID': tournament['tournament_id'],
                'Start Time': self.convert_utc_to_local(tournament['start_run'])
            })

        self.print_table(list_result)

        print()  # just used for formatting
        tournament_id: int = self.__validate_to_int('Specify the index of the tournament you would like to view > ')
        print()  # just used for formatting

        return tournament_id

    def __validate_to_int(self, prompt: str, cancel: str = '-1') -> int | None:
        while True:
            given: str = input(prompt)

            if given == cancel:
                return None
            try:
                return int(given)
            except:
                ...
