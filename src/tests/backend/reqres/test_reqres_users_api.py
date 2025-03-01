import logging
from http import HTTPStatus

import allure
import pytest
from faker import Faker

from src.main.backend.helper.req_res_api_helper import UserApiHelper
from src.main.backend.helper.response_helper import ResponseHelper
from src.main.backend.model.reqres.reqres__model import (
    ReqResUsersResponse,
    ReqResUserResponse,
    ReqResUpdateResponse,
    UserRequestBody,
    UserResponseBody,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

faker = Faker()


@pytest.fixture(scope="session")
def user_api_helper() -> UserApiHelper:
    """Fixture for UserApiHelper instance."""
    return UserApiHelper()


@pytest.fixture
def response_helper() -> ResponseHelper:
    """Fixture for ResponseHelper instance."""
    return ResponseHelper()


def get_first_user_id(api_helper: UserApiHelper, per_page: int = 10) -> int:
    """Helper function to retrieve the first user ID from a paginated response."""
    response = api_helper.get_users(per_page=per_page)
    users_response = ReqResUsersResponse(**response.json())
    return users_response.data[0].id if users_response.data else None


@pytest.mark.positive
@allure.title("Positive test retrieving a paginated list of users.")
def test_get_users(user_api_helper, response_helper):
    """Test retrieving a paginated list of users."""
    response = user_api_helper.get_users()
    response_helper.assert_response_status_code(response, HTTPStatus.OK)
    users_response = ReqResUsersResponse(**response.json())
    expected_total_resources = 12
    expected_total_pages = 12
    assert users_response.total == expected_total_resources, (
        f"Expected total users {expected_total_resources}, got {users_response.total}"
    )
    assert users_response.total_pages == expected_total_pages, (
        f"Expected total pages {expected_total_pages}, got {users_response.total_pages}"
    )


@pytest.mark.positive
@allure.title("Positive test retrieving a single user by ID.")
def test_get_user(user_api_helper, response_helper):
    """Test retrieving a single user by ID."""
    user_id = 1
    response = user_api_helper.get_user(user_id)
    response_helper.assert_response_status_code(response, HTTPStatus.OK)
    user_response = ReqResUserResponse(**response.json())
    expected_first_name = "George"
    expected_last_name = "Bluth"
    assert user_response.data.id == user_id, (
        f"Expected user ID {user_id}, got {user_response.data.id}"
    )
    assert user_response.data.first_name == expected_first_name, (
        f"Expected first name {expected_first_name}, got {user_response.data.first_name}"
    )
    assert user_response.data.last_name == expected_last_name, (
        f"Expected last name {expected_last_name}, got {user_response.data.last_name}"
    )


@pytest.mark.negative
@pytest.mark.parametrize("non_existent_user_id", [10000000, "*=", "0"])
@allure.title(
    "Negative test retrieving a non-existent user returns NOT_FOUND with an empty body."
)
def test_get_nonexistent_user(user_api_helper, response_helper, non_existent_user_id):
    """Test retrieving a non-existent user returns NOT_FOUND with an empty body."""
    response = user_api_helper.get_user(non_existent_user_id)
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)
    response_helper.assert_body_is_empty(response)


@pytest.mark.positive
@allure.title("Positive test creating a new user.")
def test_post_user(user_api_helper, response_helper):
    """Test creating a new user."""
    post_request = UserRequestBody(name=faker.name(), job=faker.job())
    response = user_api_helper.create_user(post_request)
    response_helper.assert_response_status_code(response, HTTPStatus.CREATED)
    created_user = UserResponseBody(**response.json())
    response_helper.recursive_compare(
        created_user, post_request, ignore_fields=["createdAt", "id"]
    )


@pytest.mark.negative
@pytest.mark.xfail(
    reason="Known bug: Creating user with an empty body should return BAD_REQUEST"
)
@allure.title("Negative test creating a new user with an empty body.")
def test_post_user_with_empty_body(user_api_helper, response_helper):
    """Test creating a user with an empty body should fail (currently a known bug)."""
    post_request = UserRequestBody(name="", job="")
    response = user_api_helper.create_user(post_request)
    response_helper.assert_response_status_code(
        response, HTTPStatus.CREATED
    )  # Expected BAD_REQUEST


@pytest.mark.positive
@allure.title("Positive test updating a user with PUT.")
def test_update_user(user_api_helper, response_helper):
    """Test updating a user with PUT."""
    user_id = get_first_user_id(user_api_helper)
    put_response = user_api_helper.update_user(user_id, {}, method="PUT")
    response_helper.assert_response_status_code(put_response, HTTPStatus.OK)
    update_response = ReqResUpdateResponse(**put_response.json())
    response_helper.assert_update_time(update_response.updatedAt)


@pytest.mark.positive
@allure.title("Positive test updating a user with PATCH.")
def test_patch_user(user_api_helper, response_helper):
    """Test updating a user with PATCH."""
    response = user_api_helper.get_users(per_page=10)
    users_response = ReqResUsersResponse(**response.json())
    if len(users_response.data) < 2:
        pytest.skip("Not enough users to test PATCH update.")
    second_user_id = users_response.data[1].id
    patch_response = user_api_helper.update_user(second_user_id, {}, method="PATCH")
    response_helper.assert_response_status_code(patch_response, HTTPStatus.OK)
    update_response = ReqResUpdateResponse(**patch_response.json())
    response_helper.assert_update_time(update_response.updatedAt)


@pytest.mark.negative
@pytest.mark.xfail(
    reason="Known bug: Updating a non-existent user with PATCH returns OK"
)
@allure.title("Negative test updating a non-existing user with PATCH.")
def test_patch_nonexistent_user(user_api_helper, response_helper):
    """Test PATCH on a non-existent user; expected failure."""
    patch_response = user_api_helper.update_user(0, {}, method="PATCH")
    response_helper.assert_response_status_code(patch_response, HTTPStatus.OK)


@pytest.mark.negative
@pytest.mark.xfail(reason="Known bug: Updating a non-existent user with PUT returns OK")
@allure.title("Negative test updating a non-existing user with PUT.")
def test_put_nonexistent_user(user_api_helper, response_helper):
    """Test PUT on a non-existent user; expected failure."""
    put_response = user_api_helper.update_user(0, {}, method="PUT")
    response_helper.assert_response_status_code(put_response, HTTPStatus.OK)


@pytest.mark.positive
@allure.title("Positive test deleting an existing user.")
def test_delete_user(user_api_helper, response_helper):
    """Test deleting an existing user."""
    response = user_api_helper.get_users(per_page=10)
    users_response = ReqResUsersResponse(**response.json())
    if len(users_response.data) < 3:
        pytest.skip("Not enough users to test delete operation.")
    user_id_to_delete = users_response.data[2].id
    delete_response = user_api_helper.delete_user(user_id_to_delete)
    response_helper.assert_response_status_code(delete_response, HTTPStatus.NO_CONTENT)
    response_helper.assert_body_is_empty(delete_response)


@pytest.mark.negative
@pytest.mark.xfail(
    reason="Known bug: Deleting a non-existent user should return an error"
)
@allure.title("Negative test deleting a non-existing user.")
def test_delete_nonexistent_user(user_api_helper, response_helper):
    """Test deleting a non-existent user; expected failure."""
    delete_response = user_api_helper.delete_user(0)
    response_helper.assert_response_status_code(delete_response, HTTPStatus.NO_CONTENT)
