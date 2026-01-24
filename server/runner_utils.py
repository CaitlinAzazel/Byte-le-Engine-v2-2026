import logging
from queue import Queue
from server.database import SessionLocal
from server.models.run import Run
from server.models.tournament import Tournament
from server.models.turn import Turn
from server.models.submission_run_info import SubmissionRunInfo
from server.models.team import Team
from server.models.team_type import TeamType
from server.models.university import University
from server.models.submission import Submission
from server.enums import RunnerOptions

import sys
import subprocess


class DB:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        self.db.begin()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


def worker_main(jobqueue: Queue):
    while not jobqueue.empty():
        job = jobqueue.get()
        func = job[0]
        args = job[1:]
        logging.debug(f'running {func.__name__}({args})')
        func(*args)
        jobqueue.task_done()


def run_runner(working_directory: str, runner_option: RunnerOptions, seed: int | None = None) -> bytes:
    """
    runs a script in the runner folder.
    end path is where the runner is located
    runner is the name of the script (no extension)
    """
    cmd: list[str] = [sys.executable, "launcher.pyz"]
    if runner_option == RunnerOptions.GENERATE:
        cmd += ['generate']
        if seed is not None:
            cmd += ['-s', f'{seed}']
    elif runner_option == RunnerOptions.RUN:
        cmd += ['run', '-q']
    elif runner_option == RunnerOptions.VISUALIZE:
        cmd += ['v', '-log', 'logs', '-end_time', '5', '-skip_start', '-fullscreen', '-playback_speed', '2.0']
    elif runner_option == RunnerOptions.VERSION:
        cmd += ['version']
    else:
        raise Exception("Not Implemented")

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=working_directory)
    stdout, stderr = p.communicate()
    p.wait()
    return stdout
