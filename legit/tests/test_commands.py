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
    def test_help(self):
        """Test help output expected from no-command invocation"""
        runner = CliRunner()
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert 'Options' in result.output
        assert 'Usage Examples' in result.output
        assert 'Commands' in result.output

    @pytest.mark.cli
    def test_switch(self):
        """Test switch command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['switch', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Switching to kenneth' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_sw(self):
        """Test switch alias sw"""
        runner = CliRunner()
        result = runner.invoke(cli, ['sw', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Switching to kenneth' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_switch_no_branch(self):
        """Test switch command with no branch"""
        runner = CliRunner()
        result = runner.invoke(cli, ['switch', '--fake'])
        assert result.exit_code == 2
        assert 'Please specify a branch to switch' in result.output
        assert 'Faked!' not in result.output

    @pytest.mark.cli
    def test_sync_known_branch(self):
        """Test sync command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['sync', 'develop', '--fake'])
        assert result.exit_code == 0
        assert 'Pulling commits from the server.' in result.output
        assert 'Pushing commits to the server.' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_sy_known_branch(self):
        """Test sync alias sy"""
        runner = CliRunner()
        result = runner.invoke(cli, ['sy', 'develop', '--fake'])
        assert result.exit_code == 0
        assert 'Pulling commits from the server.' in result.output
        assert 'Pushing commits to the server.' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_sync_unknown_branch(self):
        """Test sync command with bad branch"""
        runner = CliRunner()
        result = runner.invoke(cli, ['sync', 'kenneth', '--fake'])
        assert result.exit_code == 2
        assert "Branch kenneth is not published." in result.output
        assert 'Faked!' not in result.output

    @pytest.mark.cli
    def test_publish(self):
        """Test publish command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['publish', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Publishing kenneth' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_pub(self):
        """Test publish alias pub"""
        runner = CliRunner()
        result = runner.invoke(cli, ['pub', 'kenneth', '--fake'])
        assert result.exit_code == 0
        assert 'Publishing kenneth' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_publish_published_branch(self):
        """Test publish command with published branch"""
        runner = CliRunner()
        result = runner.invoke(cli, ['publish', 'develop', '--fake'])
        assert result.exit_code == 2
        assert "Branch develop is already published." in result.output
        assert 'Faked!' not in result.output

    @pytest.mark.cli
    def test_unpublish(self):
        """Test unpublish command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['unpublish', 'develop', '--fake'])
        assert result.exit_code == 0
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_unp(self):
        """Test unpublish alias unp"""
        runner = CliRunner()
        result = runner.invoke(cli, ['unp', 'develop', '--fake'])
        assert result.exit_code == 0
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_unpublish_unknown_branch(self):
        """Test unpublish with unknown branch"""
        runner = CliRunner()
        result = runner.invoke(cli, ['unp', 'kenneth', '--fake'])
        assert result.exit_code == 2
        assert "Branch kenneth is not published." in result.output
        assert 'Faked!' not in result.output

    @pytest.mark.cli
    def test_unpublish_no_branch(self):
        """Test unpublish command with no branch"""
        runner = CliRunner()
        result = runner.invoke(cli, ['unpublish', '--fake'])
        assert result.exit_code == 2
        assert 'Please specify a branch to unpublish' in result.output
        assert 'Faked!' not in result.output

    @pytest.mark.cli
    def test_undo(self):
        """Test undo command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['undo', '--fake'])
        assert result.exit_code == 0
        assert 'Last commit removed from history.' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_un(self):
        """Test undo alias un"""
        runner = CliRunner()
        result = runner.invoke(cli, ['un', '--fake'])
        assert result.exit_code == 0
        assert 'Last commit removed from history.' in result.output
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_install(self):
        """Test --install option"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--install', '--fake'])
        assert result.exit_code == 0
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_uninstall(self):
        """Test --uninstall option"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--uninstall', '--fake'])
        assert result.exit_code == 0
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_config(self):
        """Test --config option"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', '--fake'])
        assert result.exit_code == 0
        assert 'Faked!' in result.output

    @pytest.mark.cli
    def test_branches(self):
        """Test undo alias un"""
        runner = CliRunner()
        result = runner.invoke(cli, ['branches'])
        assert result.exit_code == 0
