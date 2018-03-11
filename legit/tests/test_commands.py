from click.testing import CliRunner
import pytest

from legit.cli import cli
from legit.core import __version__


class TestLegit(object):

    @pytest.mark.cli
    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert __version__ in result.output

    @pytest.mark.cli
    def test_switch(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['switch', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Switching to kenneth' in result.output

    @pytest.mark.cli
    def test_sw(self):
        """Test switch alias sw"""
        runner = CliRunner()
        result = runner.invoke(cli, ['sw', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Switching to kenneth' in result.output

    @pytest.mark.cli
    def test_sync(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['sync', '--fake'])
        assert result.exit_code == 0
        assert 'Pulling commits from the server.' in result.output
        assert 'Pushing commits to the server.' in result.output

    @pytest.mark.cli
    def test_sy(self):
        """Test sync alias sy"""
        runner = CliRunner()
        result = runner.invoke(cli, ['sy', '--fake'])
        assert result.exit_code == 0
        assert 'Pulling commits from the server.' in result.output
        assert 'Pushing commits to the server.' in result.output

    @pytest.mark.cli
    def test_publish(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['publish', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Publishing kenneth' in result.output

    @pytest.mark.cli
    def test_pub(self):
        """Test publish alias pub"""
        runner = CliRunner()
        result = runner.invoke(cli, ['pub', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Publishing kenneth' in result.output

    @pytest.mark.cli
    def test_unpublish(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['unpublish', 'kenneth', '--fake'])
        assert result.exit_code == 1
        assert "Branch kenneth isn't published." in result.output

    @pytest.mark.cli
    def test_unp(self):
        """Test unpublish alias unp"""
        runner = CliRunner()
        result = runner.invoke(cli, ['unp', 'kenneth', '--fake'])
        assert result.exit_code == 1
        assert "Branch kenneth isn't published." in result.output

    @pytest.mark.cli
    def test_undo(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['undo', '--fake'])
        assert result.exit_code == 0
        assert 'Last commit removed from history.' in result.output

    @pytest.mark.cli
    def test_un(self):
        """Test undo alias un"""
        runner = CliRunner()
        result = runner.invoke(cli, ['un', '--fake'])
        assert result.exit_code == 0
        assert 'Last commit removed from history.' in result.output

    @pytest.mark.cli
    def test_install(self):
        """Test undo alias un"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--install', '--fake'])
        assert result.exit_code == 0

    @pytest.mark.cli
    def test_uninstall(self):
        """Test undo alias un"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--uninstall', '--fake'])
        assert result.exit_code == 0

    @pytest.mark.cli
    def test_branches(self):
        """Test undo alias un"""
        runner = CliRunner()
        result = runner.invoke(cli, ['branches'])
        assert result.exit_code == 0
