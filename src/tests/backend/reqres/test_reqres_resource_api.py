import logging
from http import HTTPStatus

import allure
import pytest

from src.main.backend.helper.req_res_api_helper import ResourceApiHelper, UserApiHelper
from src.main.backend.helper.response_helper import ResponseHelper
from src.main.backend.model.reqres.reqres__model import (
    ReqResResourcesResponse,
    ReqResResourceResponse,
    ReqResUpdateResponse,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session")
def resource_api_helper() -> ResourceApiHelper:
    """Provides an instance of ResourceApiHelper for resource-related endpoints."""
    return ResourceApiHelper()


@pytest.fixture(scope="session")
def user_api_helper() -> UserApiHelper:
    """Provides an instance of UserApiHelper for user-related endpoints (used for update/patch/delete)."""
    return UserApiHelper()


@pytest.fixture
def response_helper() -> ResponseHelper:
    """Provides an instance of ResponseHelper for response validations."""
    return ResponseHelper()


def get_resource_id(
    api_helper: ResourceApiHelper, index: int = 0, per_page: int = 10
) -> int:
    """
    Helper function to retrieve a resource ID from a paginated response.

    :param api_helper: The ResourceApiHelper instance.
    :param index: Index in the list of resources to return.
    :param per_page: Number of resources per page.
    :return: The ID of the resource at the specified index.
    """
    response = api_helper.get_resources(per_page=per_page)
    resources = ReqResResourcesResponse(**response.json())
    if len(resources.data) <= index:
        raise ValueError("Not enough resources returned to fetch the desired index")
    return resources.data[index].id


@pytest.mark.positive
@allure.title(
    "Positive test for retrieving a paginated list of resources returns expected totals."
)
def test_get_resources(resource_api_helper, response_helper):
    """Test that retrieving a paginated list of resources returns expected totals."""
    response = resource_api_helper.get_resources()
    response_helper.assert_response_status_code(response, HTTPStatus.OK)
    resources_response = ReqResResourcesResponse(**response.json())
    expected_total_resources = 12
    expected_total_pages = 12
    assert resources_response.total == expected_total_resources, (
        f"Expected total resources {expected_total_resources}, got {resources_response.total}"
    )
    assert resources_response.total_pages == expected_total_pages, (
        f"Expected total pages {expected_total_pages}, got {resources_response.total_pages}"
    )


@pytest.mark.positive
@allure.title("Positive test that a single resource is retrieved correctly by its ID.")
def test_get_resource(resource_api_helper, response_helper):
    """Test that a single resource is retrieved correctly by its ID."""
    resource_id = 1
    response = resource_api_helper.get_resource(resource_id)
    response_helper.assert_response_status_code(response, HTTPStatus.OK)
    resource_response = ReqResResourceResponse(**response.json())
    expected_name = "cerulean"
    expected_year = 2000
    expected_color = "#98B2D1"
    assert resource_response.data.id == resource_id, (
        f"Expected resource ID {resource_id}, got {resource_response.data.id}"
    )
    assert resource_response.data.name == expected_name, (
        f"Expected resource name '{expected_name}', got '{resource_response.data.name}'"
    )
    assert resource_response.data.year == expected_year, (
        f"Expected resource year {expected_year}, got {resource_response.data.year}"
    )
    assert resource_response.data.color == expected_color, (
        f"Expected resource color '{expected_color}', got '{resource_response.data.color}'"
    )


@pytest.mark.negative
@pytest.mark.parametrize("non_existent_resource_id", [55555, "!", 0])
@allure.title(
    "Negative test that  requesting a non-existent resource returns a NOT_FOUND status and an empty response body."
)
def test_get_nonexistent_resource(
    resource_api_helper, response_helper, non_existent_resource_id
):
    """
    Test that requesting a non-existent resource returns a NOT_FOUND status
    and an empty response body.
    """
    response = resource_api_helper.get_resource(non_existent_resource_id)
    response_helper.assert_response_status_code(response, HTTPStatus.NOT_FOUND)
    response_helper.assert_body_is_empty(response)


@pytest.mark.positive
@allure.title("Positive test updating a resource using PUT.")
def test_update_resource(resource_api_helper, response_helper, user_api_helper):
    """
    Test updating a resource using PUT.

    Note: Although the GET resource is via ResourceApiHelper, the update operation
    is performed using user_api_helper (if the API design is similar across endpoints).
    """
    resource_id = get_resource_id(resource_api_helper, index=0)
    put_response = user_api_helper.update_user(resource_id, {}, method="PUT")
    response_helper.assert_response_status_code(put_response, HTTPStatus.OK)

    update_response = ReqResUpdateResponse(**put_response.json())
    response_helper.assert_update_time(update_response.updatedAt)


@pytest.mark.positive
@allure.title("Positive test updating a resource using PATCH.")
def test_patch_resource(resource_api_helper, response_helper, user_api_helper):
    """
    Test updating a resource using PATCH.

    Note: This test uses the user_api_helper's update_user method to patch a resource.
    """
    resource_id = get_resource_id(resource_api_helper, index=1, per_page=10)
    patch_response = user_api_helper.update_user(resource_id, {}, method="PATCH")
    response_helper.assert_response_status_code(patch_response, HTTPStatus.OK)

    update_response = ReqResUpdateResponse(**patch_response.json())
    response_helper.assert_update_time(update_response.updatedAt)


@pytest.mark.positive
@allure.title("Positive test deleting a resource")
def test_delete_resource(resource_api_helper, response_helper, user_api_helper):
    """
    Test deleting a resource.

    This test retrieves a resource ID from a paginated list and attempts to delete it.
    """
    resource_id = get_resource_id(resource_api_helper, index=2, per_page=10)
    delete_response = user_api_helper.delete_user(resource_id)
    response_helper.assert_response_status_code(delete_response, HTTPStatus.NO_CONTENT)
    response_helper.assert_body_is_empty(delete_response)
