import json
import urllib.parse
import requests

from src.main.backend.model.reqres.reqres__model import (
    UserRequestBody,
    RegisterRequestBody,
)


class BaseApiHelper:
    """Common functionality for API helpers."""

    BASE_URL = "https://reqres.in/api"

    def __init__(self):
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def build_url(self, endpoint: str, **query_params) -> str:
        """
        Construct the full URL for a given endpoint with optional query parameters.

        :param endpoint: API endpoint (e.g., 'users', 'resource/1')
        :param query_params: Dictionary of query parameters
        :return: A complete URL string
        """
        url = f"{self.BASE_URL}/{endpoint}"
        if query_params:
            url += "?" + urllib.parse.urlencode(query_params)
        return url

    def request(self, method: str, endpoint: str, query_params=None, **kwargs):
        """
        Perform an HTTP request with the given method and endpoint.

        :param method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        :param endpoint: API endpoint string
        :param query_params: Dictionary of query parameters
        :param kwargs: Additional arguments to pass to requests
        :return: Response object from requests
        """
        url = self.build_url(endpoint, **(query_params or {}))
        return self.session.request(method, url, headers=self.headers, **kwargs)


class UserApiHelper(BaseApiHelper):
    """Helper class for user-related endpoints."""

    def get_users(self, page=1, per_page=1):
        """
        Retrieve a paginated list of users.

        :param page: Page number
        :param per_page: Number of users per page
        :return: Response object from GET /users
        """
        return self.request(
            "GET", "users", query_params={"page": page, "per_page": per_page}
        )

    def get_user(self, user_id):
        """
        Retrieve a single user by ID.

        :param user_id: Unique identifier of the user
        :return: Response object from GET /users/{user_id}
        """
        return self.request("GET", f"users/{user_id}")

    def create_user(self, body: UserRequestBody):
        """
        Create a new user.

        :param body: Dictionary containing user data
        :return: Response object from POST /users
        """
        return self.request("POST", "users", data=body.model_dump_json())

    def update_user(self, user_id, body: dict, method="PUT"):
        """
        Update an existing user using PUT or PATCH.

        :param user_id: Unique identifier of the user
        :param body: Dictionary containing user data to update
        :param method: HTTP method ("PUT" or "PATCH")
        :return: Response object from PUT/PATCH /users/{user_id}
        """
        if method.upper() not in ["PUT", "PATCH"]:
            raise ValueError("Method must be either PUT or PATCH")
        return self.request(method, f"users/{user_id}", data=json.dumps(body))

    def delete_user(self, user_id):
        """
        Delete a user by ID.

        :param user_id: Unique identifier of the user
        :return: Response object from DELETE /users/{user_id}
        """
        return self.request("DELETE", f"users/{user_id}")

    def register(self, body: RegisterRequestBody):
        """
        Register a new user.

        :param body: Dictionary containing registration data
        :return: Response object from POST /register
        """
        return self.request("POST", "register", data=body.model_dump_json())

    def login(self, body: RegisterRequestBody):
        """
        Log in a user.

        :param body: Dictionary containing login credentials
        :return: Response object from POST /login
        """
        return self.request("POST", "login", data=body.model_dump_json())


class ResourceApiHelper(BaseApiHelper):
    """Helper class for resource-related endpoints."""

    def get_resources(self, page=1, per_page=1):
        """
        Retrieve a paginated list of resources.

        :param page: Page number
        :param per_page: Number of resources per page
        :return: Response object from GET /resource
        """
        return self.request(
            "GET", "resource", query_params={"page": page, "per_page": per_page}
        )

    def get_resource(self, resource_id):
        """
        Retrieve a single resource by ID.

        :param resource_id: Unique identifier of the resource
        :return: Response object from GET /resource/{resource_id}
        """
        return self.request("GET", f"resource/{resource_id}")

    def update_resource(self, resource_id, method="PUT"):
        """
        Update a resource using PUT or PATCH.

        :param resource_id: Unique identifier of the resource
        :param method: HTTP method ("PUT" or "PATCH")
        :return: Response object from PUT/PATCH /resource/{resource_id}
        """
        if method.upper() not in ["PUT", "PATCH"]:
            raise ValueError("Method must be either PUT or PATCH")
        return self.request(method, f"resource/{resource_id}")

    def delete_resource(self, resource_id):
        """
        Delete a resource by ID.

        :param resource_id: Unique identifier of the resource
        :return: Response object from DELETE /resource/{resource_id}
        """
        return self.request("DELETE", f"resource/{resource_id}")
