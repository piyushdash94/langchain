import json
from typing import Any

import pytest

from langchain_community.utilities.clickup import ClickupAPIWrapper


@pytest.fixture
def wrapper(mocker: Any) -> ClickupAPIWrapper:
    mocker.patch("langchain_community.utilities.clickup.fetch_team_id", return_value="1")
    mocker.patch("langchain_community.utilities.clickup.fetch_space_id", return_value="2")
    mocker.patch("langchain_community.utilities.clickup.fetch_folder_id", return_value="3")
    mocker.patch("langchain_community.utilities.clickup.fetch_list_id", return_value="4")
    return ClickupAPIWrapper(access_token="token")


def test_create_folder_updates_folder_id(mocker: Any, wrapper: ClickupAPIWrapper) -> None:
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"id": 5, "name": "folder"}
    mocker.patch("langchain_community.utilities.clickup.requests.post", return_value=mock_response)

    assert wrapper.folder_id == "3"
    assert wrapper.list_id == "4"

    wrapper.create_folder(json.dumps({"name": "folder"}))

    assert wrapper.folder_id == 5
    assert wrapper.list_id == "4"
