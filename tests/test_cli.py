from source_to_skill.cli import main


def test_cli_prints_version(capsys):
    result = main(["--version"])

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.strip() == "source-to-skill 0.2.0"
