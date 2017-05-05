from common import exec_command


def test_help():
    returncode, stdout, stderr = exec_command(
        ['dcos-oneview', 'oneview', '--help'])

    assert returncode == 0
    assert stdout == b"""DCOS OneView Example Subcommand

Usage:
    dcos oneview --info

Options:
    --help           Show this screen
    --status        Show status
    --capacity      Show capacity
    --addnode       Add node
    --removenode    Remove node
"""
    assert stderr == b''
