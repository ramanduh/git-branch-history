# -*- coding: utf-8 -*-
import os

from branch_history import BranchHistory


class TestBranchHistory(object):

    def test_basic(self, tmpdir, capsys):
        # Create new history
        bh = BranchHistory(str(tmpdir))

        assert bh.history == []

        dest_file = str(tmpdir.join('.git-branch-checkout-history'))
        assert bh.history_file == dest_file

        # push one entry in the history
        assert os.path.exists(dest_file) is False
        bh.push('my_branch')
        assert bh.history == ['my_branch']
        assert os.path.exists(dest_file)

        # delete the current instanche instance and recreate it
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
