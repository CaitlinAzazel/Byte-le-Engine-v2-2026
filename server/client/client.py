import os
from typing import Optional
from requests.models import HTTPError, Response
from server.client.client_utils import ClientUtils, Result
import json

CLIENT_DIRECTORY = "./"
CLIENT_KEYWORD = "client"


class Client:
    def __init__(self, args):
        # If vID exists, read it
        if os.path.isfile('vID'):
            with open('vID') as f:
                self.vid = f.read()

        self.utils = ClientUtils(args.csv)
        self.handle_client(args)

    # Determines what action the client wants to do

    def handle_client(self, args):
        try:
            # If the subparse is None, don't attempt to do the rest of the code
            if args.subparse is None:
                print("The server command needs more information. Try 'python launcher.pyz s -h' for help")
                return

            # If the subparse doesn't contain an expected value, don't do anything
            if args.subparse.lower() == 'stats' or args.subparse.lower() == 'st':
                if args.runs_for_submission != -1:
                    temp: Result = self.utils.get_runs_for_submission(args.runs_for_submission, self.vid)
                    if temp.is_err():
                        print(temp.Err)
                    return
                if args.get_submissions:
                    self.utils.get_submissions(self.vid)
                    return
                if args.get_code_for_submission != -1:
                    temp: Result = self.utils.get_code_from_submission(args.get_code_for_submission, self.vid)
                    if temp.is_err():
                        print(temp.Err)
                    return
                # This is connected to the '-get_details_for_submission' command. The difference in naming is to
                # separate the frontend user experience from the backend work
                if args.get_submission_run_info != -1:
                    temp: Result = self.utils.get_submission_run_info(args.get_submission_run_info, self.vid)
                    if temp.is_err():
                        print(temp.Err)
                    return
                return

            if args.subparse.lower() == 'leaderboard' or args.subparse.lower() == "l":
                temp: Result = self.utils.get_leaderboard(args.all, args.include_alumni, args.id)
                if temp.is_err():
                    print(temp.Err)
                return

        except HTTPError as e:
            print(f"Error: {json.loads(e.response._content)}")

    def register(self, name: Optional[str] = None, uni_id: Optional[int] = None, team_type_id: Optional[int] = None):
        # Check if vID already exists and cancel out
        if os.path.isfile('vID'):
            print('You have already registered.')
            return

        # Ask for team name
        team_name = name or input("Enter your team name: ")

        if team_name == '':
            print("Team name can't be empty.")
            return

        temp: Result[list[dict]] = self.utils.get_unis()

        if temp.is_err():
            print(temp.Err)
            return

        unis: list[dict] = temp.Ok

        print("Select a university (id)")
        self.utils.print_table(unis)

        try:
            uni_id = uni_id or int(input())
        except ValueError:
            print('Invalid integer!')

        if uni_id not in map(lambda x: x['uni_id'], unis):
            print("Not a valid uni id")
            return

        temp = self.utils.get_team_types()
        if temp.is_err():
            print(temp.Err)
            return

        team_types = temp.Ok

        print("Select a team type (id)")
        self.utils.print_table(team_types)

        team_type_id = team_type_id or int(input())

        if team_type_id not in map(lambda x: x['team_type_id'], team_types):
            print("Not a valid team type")
            return

        temp: Result[Response] = self.utils.register(uni_id, team_type_id, team_name)

        if temp.is_err():
            print(str(temp.Err))
            return

        response = temp.Ok

        if not response.ok:
            print('Team name contains illegal characters or is already taken.')
            return

        # Receive uuid
        # vID = await self.reader.read(BUFFER_SIZE)
        # vID = vID.decode()

        v_id = response.content
        if v_id == '':
            print('Something broke.')
            return

        jsn: dict = json.loads(response.content)
        # Put uuid into file for verification (vID)
        with open('vID', 'w+') as f:
            f.write(jsn['team_uuid'])

        print("Registration successful.")
        print("You have been given an ID file in your Byte-le folder. Don't move or lose it!")
        print("You can give a copy to your teammates so they can submit and view stats.")

    def submit(self):
        if not self.verify():
            print('You need to register first.')
            return

        # Check and verify client file
        file = None
        for filename in os.listdir(CLIENT_DIRECTORY):
            if CLIENT_KEYWORD.upper() not in filename.upper():
                # Filters out files that do not contain CLIENT_KEYWORD in their filename
                continue

            if not filename.endswith('.py'):
                continue

            if os.path.isdir(os.path.join(CLIENT_DIRECTORY, filename)):
                # Skips folders
                continue

            user_check = input(f'Submitting {filename}, is this ok? (y/n): ')
            if 'y' in user_check.lower():
                file = filename
                break
        else:
            file = input(
                'Could not find file: please manually type file name: ')

        if not os.path.isfile(CLIENT_DIRECTORY + file):
            print('File not found.')
            return

        # Send client file
        print('Submitting file.\n')
        with open(CLIENT_DIRECTORY + file) as fl:
            fil = bytes("".join(fl.readlines()), 'utf-8')
            temp: Result = self.utils.submit_file(fil, self.vid)
            if temp.is_err():
                print(temp.Err)
                return
        print('File sent successfully.')

    def verify(self):
        # Check vID for uuid
        if not os.path.isfile('vID'):
            print("Cannot find vID, please register first.")
            return False

        return True
