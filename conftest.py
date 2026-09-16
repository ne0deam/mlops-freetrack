from unittest.mock import MagicMock, patch

_patcher = patch("recommender.load_model", return_value=MagicMock())
_patcher.start()
