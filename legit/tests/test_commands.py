from click.testing import CliRunner
import pytest

from legit.cli import cli
from legit.core import __version__


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.cli
def test_cli(runner):
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


@pytest.mark.cli
def test_help(runner):
    """Test help output expected from no-command invocation"""
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "Options" in result.output
    assert "Usage Examples" in result.output
    assert "Commands" in result.output


@pytest.mark.cli
def test_switch(runner):
    """Test switch command"""
    result = runner.invoke(cli, ["switch", "kenneth", "--fake"])
    assert result.exit_code == 0
    assert "Switching to kenneth" in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_sw(runner):
    """Test switch alias sw"""
    result = runner.invoke(cli, ["sw", "kenneth", "--fake"])
    assert result.exit_code == 0
    assert "Switching to kenneth" in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_switch_no_branch(runner):
    """Test switch command with no branch"""
    result = runner.invoke(cli, ["switch", "--fake"])
    assert result.exit_code == 2
    assert "Please specify a branch to switch" in result.output
    assert "Faked!" not in result.output


@pytest.mark.cli
def test_sync_known_branch(runner):
    """Test sync command"""
    result = runner.invoke(cli, ["sync", "master", "--fake"])
    assert "Pulling commits from the server." in result.output
    assert result.exit_code == 0
    assert "Pushing commits to the server." in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_sy_known_branch(runner):
    """Test sync alias sy"""
    result = runner.invoke(cli, ["sy", "master", "--fake"])
    assert result.exit_code == 0
    assert "Pulling commits from the server." in result.output
    assert "Pushing commits to the server." in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_sync_unknown_branch(runner):
    """Test sync command with bad branch"""
    result = runner.invoke(cli, ["sync", "kenneth", "--fake"])
    assert result.exit_code == 2
    assert "Branch kenneth is not published." in result.output
    assert "Faked!" not in result.output


@pytest.mark.cli
def test_publish(runner):
    """Test publish command"""
    result = runner.invoke(cli, ["publish", "kenneth", "--fake"])
    assert result.exit_code == 0
    assert "Publishing kenneth" in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_pub(runner):
    """Test publish alias pub"""
    result = runner.invoke(cli, ["pub", "kenneth", "--fake"])
    assert result.exit_code == 0
    assert "Publishing kenneth" in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_publish_published_branch(runner):
    """Test publish command with published branch"""
    result = runner.invoke(cli, ["publish", "develop", "--fake"])
    assert result.exit_code == 2
    assert "Branch develop is already published." in result.output
    assert "Faked!" not in result.output


@pytest.mark.cli
def test_unpublish(runner):
    """Test unpublish command"""
    result = runner.invoke(cli, ["unpublish", "develop", "--fake"])
    assert result.exit_code == 0
    assert "Faked!" in result.output


@pytest.mark.cli
def test_unp(runner):
    """Test unpublish alias unp"""
    result = runner.invoke(cli, ["unp", "develop", "--fake"])
    assert result.exit_code == 0
    assert "Faked!" in result.output


@pytest.mark.cli
def test_unpublish_unknown_branch(runner):
    """Test unpublish with unknown branch"""
    result = runner.invoke(cli, ["unp", "kenneth", "--fake"])
    assert result.exit_code == 2
    assert "Branch kenneth is not published." in result.output
    assert "Faked!" not in result.output


@pytest.mark.cli
def test_unpublish_no_branch(runner):
    """Test unpublish command with no branch"""
    result = runner.invoke(cli, ["unpublish", "--fake"])
    assert result.exit_code == 2
    assert "Please specify a branch to unpublish" in result.output
    assert "Faked!" not in result.output


@pytest.mark.cli
def test_undo(runner):
    """Test undo command"""
    result = runner.invoke(cli, ["undo", "--fake"])
    assert result.exit_code == 0
    assert "Last commit removed from history." in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_un(runner):
    """Test undo alias un"""
    result = runner.invoke(cli, ["un", "--fake"])
    assert result.exit_code == 0
    assert "Last commit removed from history." in result.output
    assert "Faked!" in result.output


@pytest.mark.cli
def test_install(runner):
    """Test --install option"""
    result = runner.invoke(cli, ["--install", "--fake"])
    assert result.exit_code == 0
    assert "Faked!" in result.output


@pytest.mark.cli
def test_uninstall(runner):
    """Test --uninstall option"""
    result = runner.invoke(cli, ["--uninstall", "--fake"])
    assert result.exit_code == 0
    assert "Faked!" in result.output


@pytest.mark.cli
def test_config(runner):
    """Test --config option"""
    result = runner.invoke(cli, ["--config", "--fake"])
    assert result.exit_code == 0
    assert "Faked!" in result.output


@pytest.mark.cli
def test_branches(runner):
    """Test undo alias un"""
    result = runner.invoke(cli, ["branches"])
    assert result.exit_code == 0
