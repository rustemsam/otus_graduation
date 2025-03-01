import logging
from http import HTTPStatus

import allure
import pytest
from faker import Faker

from src.main.backend.helper.req_res_api_helper import UserApiHelper
from src.main.backend.helper.response_helper import ResponseHelper
from src.main.backend.model.reqres.reqres__model import (
    ReqResUsersResponse,
    RegisterRequestBody,
    RegisterResponseBody,
    RegisterErrorResponse,
    LoginResponseBody,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

faker = Faker()


@pytest.fixture(scope="session")
def user_api_helper() -> UserApiHelper:
    """Provides an instance of UserApiHelper for API interactions."""
    return UserApiHelper()


@pytest.fixture
def response_helper() -> ResponseHelper:
    """Provides an instance of ResponseHelper for response validations."""
    return ResponseHelper()


def get_valid_email(api_helper: UserApiHelper) -> str:
    """
    Helper function to retrieve a valid email from the users list.

    :param api_helper: Instance of UserApiHelper.
    :return: A valid email address from the first user in the list.
    """
    response = api_helper.get_users()
    users_response = ReqResUsersResponse(**response.json())
    if not users_response.data:
        raise ValueError("No users found to extract email.")
    return users_response.data[0].email


@pytest.mark.positive
@allure.title("Positive test for user registration")
def test_post_register(user_api_helper, response_helper):
    """
    Positive test for user registration.

    Retrieves a valid email, creates a registration request with a generated password,
    and asserts that the registration response returns a valid id and a non-empty token.
    """
    email = get_valid_email(user_api_helper)
    post_request = RegisterRequestBody(email=email, password=faker.password())
    register_response = user_api_helper.register(post_request)
    response_helper.assert_response_status_code(register_response, HTTPStatus.OK)

    register_resp_body = RegisterResponseBody(**register_response.json())
    # Assert that an id was returned. Depending on your API design,
    # you might not be able to compare it directly with the id from get_users.
    assert register_resp_body.id is not None, (
        f"Expected a registration id, but got {register_resp_body.id}"
    )
    assert register_resp_body.token, (
        "Expected a non-empty 'token' field in the registration response."
    )


@pytest.mark.negative
@allure.title("Negative test for user registration.")
def test_post_register_negative(user_api_helper, response_helper):
    """
    Negative test for user registration.

    Sends a registration request without a password and expects a BAD_REQUEST response
    with an error message indicating the missing password.
    """
    email = get_valid_email(user_api_helper)
    post_request = RegisterRequestBody(email=email)
    register_response = user_api_helper.register(post_request)
    response_helper.assert_response_status_code(
        register_response, HTTPStatus.BAD_REQUEST
    )

    error_response = RegisterErrorResponse(**register_response.json())
    expected_error = "Missing password"
    assert error_response.error == expected_error, (
        f"Expected error message '{expected_error}', got '{error_response.error}'"
    )


@pytest.mark.positive
@allure.title("Positive test for user login.")
def test_post_login(user_api_helper, response_helper):
    """
    Positive test for user login.

    Retrieves a valid email, creates a login request with a generated password,
    and asserts that the login response contains a non-empty token.
    """
    email = get_valid_email(user_api_helper)
    post_request = RegisterRequestBody(email=email, password=faker.password())
    login_response = user_api_helper.login(post_request)
    response_helper.assert_response_status_code(login_response, HTTPStatus.OK)

    login_resp_body = LoginResponseBody(**login_response.json())
    assert login_resp_body.token, (
        "Expected a non-empty 'token' field in the login response."
    )


@pytest.mark.negative
@allure.title("Negative test for user login.")
def test_post_login_negative(user_api_helper, response_helper):
    """
    Negative test for user login.

    Sends a login request without a password and expects a BAD_REQUEST response with
    an error message indicating the missing password.
    """
    email = get_valid_email(user_api_helper)
    post_request = RegisterRequestBody(email=email)
    login_response = user_api_helper.login(post_request)
    response_helper.assert_response_status_code(login_response, HTTPStatus.BAD_REQUEST)

    error_response = RegisterErrorResponse(**login_response.json())
    expected_error = "Missing password"
    assert error_response.error == expected_error, (
        f"Expected error message '{expected_error}', got '{error_response.error}'"
    )
