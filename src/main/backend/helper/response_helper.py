from datetime import datetime, timezone
from http import HTTPStatus
from typing import List, Union, Any, Dict, Optional

import allure
import requests
from pydantic import BaseModel


class ResponseHelper:
    """
    A helper class providing various static methods for asserting conditions on HTTP responses.
    """

    EXPECTED_SUCCESS_STATUS = "success"

    @staticmethod
    @allure.step("Assert content type")
    def assert_response_content_type(
        response: requests.Response, expected_type: str = "application/json"
    ) -> None:
        """
        Asserts that the response's Content-Type header matches the expected type.

        :param response: The HTTP response object.
        :param expected_type: The expected Content-Type value.
        """
        content_type = response.headers.get("Content-Type", "")
        assert content_type == expected_type, (
            f"Expected content type '{expected_type}', got '{content_type}'"
        )

    @staticmethod
    @allure.step("Expected status code '{expected_status_code}', but got '{response}'")
    def assert_response_status_code(
        response: requests.Response,
        expected_status_code: Union[int, HTTPStatus] = HTTPStatus.OK,
    ) -> None:
        """
        Asserts that the response's status code matches the expected status code.

        :param response: The HTTP response object.
        :param expected_status_code: The expected HTTP status code.
        """
        assert response.status_code == expected_status_code, (
            f"Expected status code '{expected_status_code}', got '{response.status_code}'"
        )

    @staticmethod
    def assert_response_body_status(
        response_status: str, expected_status: str = EXPECTED_SUCCESS_STATUS
    ) -> None:
        """
        Asserts that the response status string matches the expected status.

        :param response_status: The status extracted from the response body.
        :param expected_status: The expected status string.
        """
        assert response_status == expected_status, (
            f"Expected status '{expected_status}', got '{response_status}'"
        )

    @staticmethod
    @allure.step("Check that the body '{response}' is empty")
    def assert_body_is_empty(response: requests.Response) -> None:
        """
        Asserts that the response body is empty.

        :param response: The HTTP response object.
        """
        if response.content:
            try:
                json_body = response.json()
            except ValueError:
                json_body = None
            assert json_body == {} or response.text.strip() == "", (
                f"Expected empty body, got: {json_body or response.text}"
            )

    @staticmethod
    @allure.step("Check that the url '{urls}' contains message '{expected_message}'")
    def assert_url_contains(
        urls: List[Union[str, requests.Response]], expected_message: str
    ) -> None:
        """
        Asserts that at least one URL (or response converted to string) in the provided list contains the expected message.

        :param urls: List of URL strings or response objects.
        :param expected_message: The substring expected to be found in one of the URLs.
        """
        assert any(expected_message in str(url) for url in urls), (
            f"No URL in '{urls}' contains '{expected_message}'"
        )

    @staticmethod
    @allure.step(
        "Check that the response object '{response_obj}' has expected data '{expected_data}'"
    )
    def recursive_compare(
        response_obj: Any,
        expected_data: Union[Dict[str, Any], BaseModel],
        field_name: Optional[str] = "",
        ignore_fields: Optional[List[str]] = None,
    ) -> None:
        """
        Recursively compares the response object with the expected data.

        Both response_obj and expected_data can be dictionaries or Pydantic models.
        It asserts that there are no unexpected fields and that all expected values match.

        :param response_obj: The actual response data.
        :param expected_data: The expected data, either as a dict or a Pydantic model.
        :param field_name: A prefix for field names to provide context in assertion messages.
        :param ignore_fields: List of field names to ignore during comparison.
        """
        if ignore_fields is None:
            ignore_fields = []
        if field_name is None:
            field_name = ""

        if isinstance(expected_data, BaseModel):
            expected_data = expected_data.model_dump()
        if isinstance(response_obj, BaseModel):
            response_obj = response_obj.model_dump()
        elif not isinstance(response_obj, dict) and hasattr(response_obj, "__dict__"):
            response_obj = vars(response_obj)

        if isinstance(response_obj, dict):
            extra_keys = (
                set(response_obj.keys())
                - set(expected_data.keys())
                - set(ignore_fields)
            )
            assert not extra_keys, (
                f"Unexpected fields in response at '{field_name}': {extra_keys}"
            )

        for key, expected_value in expected_data.items():
            if key in ignore_fields:
                continue

            response_value = (
                response_obj.get(key)
                if isinstance(response_obj, dict)
                else getattr(response_obj, key, None)
            )

            try:
                response_value_int = int(response_value)
                expected_value_int = int(expected_value)
                response_value = response_value_int
                expected_value = expected_value_int
            except (ValueError, TypeError):
                pass

            if response_value is None and expected_value == "":
                continue
            elif expected_value is None and response_value == "":
                continue

            if isinstance(expected_value, dict) and (
                isinstance(response_value, dict)
                or isinstance(response_value, BaseModel)
            ):
                if isinstance(response_value, BaseModel):
                    response_value = response_value.model_dump()
                ResponseHelper.recursive_compare(
                    response_value,
                    expected_value,
                    field_name=field_name + key + ".",
                    ignore_fields=ignore_fields,
                )
            else:
                assert response_value == expected_value, (
                    f"Mismatch in field '{field_name + key}': expected {expected_value}, got {response_value}"
                )

    @staticmethod
    @allure.step("Check that updated time '{updated_at}'")
    def assert_update_time(updated_at: str) -> None:
        """
        Asserts that the provided update timestamp is within an allowed tolerance of the current UTC time.

        The expected timestamp format is "%Y-%m-%dT%H:%M:%S.%fZ".

        :param updated_at: The timestamp string from the response.
        """
        current_time = datetime.now(timezone.utc)
        try:
            parsed_time = datetime.strptime(
                updated_at, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=timezone.utc)
        except ValueError as e:
            raise AssertionError(f"Timestamp format error: {e}")
        time_difference = abs((current_time - parsed_time).total_seconds())
        allowed_tolerance = 10
        assert time_difference <= allowed_tolerance, (
            f"Time difference {time_difference} exceeds allowed tolerance of {allowed_tolerance} seconds"
        )
