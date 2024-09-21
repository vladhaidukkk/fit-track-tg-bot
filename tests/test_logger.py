import logging
from typing import get_args

from bot.logger import LogLevelName


class TestBotLogger:
    def test_log_level_name_literal_has_only_five_names(self) -> None:
        literal_log_level_names = get_args(LogLevelName)
        assert len(literal_log_level_names) == 5

    def test_log_level_name_literal_has_valid_names(self) -> None:
        literal_log_level_names = set(get_args(LogLevelName))
        all_log_level_names = set(logging.getLevelNamesMapping())
        assert literal_log_level_names & all_log_level_names == literal_log_level_names
