# -*- coding: utf-8 -*-

import argparse
from collections import deque
import os
import subprocess
from subprocess import check_output
import sys
import yaml


HISTORY_FILENAME = 'branch-checkout-history.yaml'


class BranchHistory(object):
    MAX_HISTORY_LEN = 10

    def __init__(self, history_dir):
        """Initialize a new branch history.

        The branch checkout history is stored in a yaml file

        :param history_dir: a path where the history db will be stored
        :type history_dir: str
        """
        self._history_file = os.path.join(history_dir, HISTORY_FILENAME)
        try:
            with open(self._history_file, 'r') as fd:
                self._history = yaml.safe_load(fd)
        except (OSError, IOError, yaml.YAMLError):
            self._history = []
        else:
            self._history = self._history or []

        if not isinstance(self._history, list):  # pragma: no cover
            raise RuntimeError(
                'Invalid content of the history file {0}'.format(
                    self._history_file
                )
            )

        self._history = deque(
            self._history[:self.MAX_HISTORY_LEN],
            self.MAX_HISTORY_LEN
        )

    @property
    def history(self):
        return list(self._history)

    @property
    def history_file(self):
        return self._history_file

    def push(self, branch):
        """Add a new branch in the history.

        If the branch is already present in the history,
        put it at the top of the list

        :param branch: name of the branch
        :type branch: str
        """
        try:
            self._history.remove(branch)
        except ValueError:
            pass
        finally:
            self._history.appendleft(branch)

        with open(self._history_file, 'w') as fd:
            yaml.safe_dump(
                list(self._history),
                fd,
            )

    def get(self, index):
        """Get a branch name belonging to an index.

        :param index: the index we want to get
        :type index: int

        :return: branch name

        :raise: IndexError
        """
        return self._history[index]

    def list(self):
        """Print the history (branch name and their indexes)."""
        for index, branch in enumerate(self._history):
            print("{index: <9}{branch}".format(index=index, branch=branch))


def _run_cmd(cmd):
    try:
        return check_output(cmd)
    except subprocess.CalledProcessError as e:
        sys.exit(str(e))


def _currentGitDir():
    cmd = ['git', 'rev-parse', '--show-toplevel']
    return _run_cmd(cmd).strip()


def parse_args():
    description = 'Manage checkout branch history'
    parser = argparse.ArgumentParser(description)
    parser.add_argument(
        '--history-dir',
        '-f',
        help='A directory where to keep the history file',
        dest='history_dir',
        default=os.path.join(_currentGitDir(), '.git')
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--push',
        '-p',
        dest='branch',
        help='Add a branch in the history file',
    )
    group.add_argument(
        'branch_index',
        metavar='N',
        type=int,
        nargs='?',
        help=('Checkout the branch with the index N,'
              ' or show the history if N is not provided')
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        bh = BranchHistory(args.history_dir)
    except RuntimeError as e:
        sys.exit(str(e))

    # Add a new entry in the history
    if args.branch is not None:
        bh.push(args.branch)

    # checkout the branch at a given index
    elif args.branch_index is not None:
        try:
            branch = bh.get(args.branch_index)
        except IndexError:
            sys.exit('Index not found in the history')
        else:
            cmd = ['git', 'checkout', branch]
            _run_cmd(cmd)

    # list all branches in the history db with their indexes
    else:
        bh.list()


if __name__ == '__main__':
    main()
