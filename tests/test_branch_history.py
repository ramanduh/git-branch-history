# -*- coding: utf-8 -*-
import os

import branch_history
from branch_history import BranchHistory


class TestBranchHistory(object):

    def test_basic(self, tmpdir, capsys):
        # Create new history
        bh = BranchHistory(str(tmpdir))

        assert bh.history == []

        history_file_path = str(tmpdir.join(branch_history.HISTORY_FILENAME))
        assert bh.history_file == history_file_path

        # push one entry in the history
        assert os.path.exists(history_file_path) is False
        bh.push('my_branch')
        assert bh.history == ['my_branch']
        assert os.path.exists(history_file_path)

        # delete the current instance and recreate it
        del bh
        bh = BranchHistory(str(tmpdir))
        assert bh.history == ['my_branch']
        assert bh.get(0) == 'my_branch'

        # push one more history
        bh.push('my_new_branch')
        assert bh.history == ['my_new_branch', 'my_branch']
        assert bh.get(0) == 'my_new_branch'
        assert bh.get(1) == 'my_branch'

        # push max - 1 entry in the history, the last entry should be
        # my_new_branch, ie my_branch is removed
        for i in range(bh.MAX_HISTORY_LEN - 1):
            bh.push(i)
        assert len(bh.history) == bh.MAX_HISTORY_LEN
        assert bh.history[-1] == 'my_new_branch'

        # list history
        bh.list()
        out, err = capsys.readouterr()
        assert not err
        assert 'my_new_branch' in out
