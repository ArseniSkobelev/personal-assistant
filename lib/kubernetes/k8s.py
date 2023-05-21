import os
from enum import Enum
from pprint import pprint

from lib.logger import Logger
from lib.exceptions import *
from lib.http import Http


class HttpMethods(Enum):
    GET = 1
    POST = 2
    DELETE = 3
    PATCH = 4


class Kubernetes:
    def __init__(self):
        Logger.attention("Trying to establish a connection to the Kubernetes API server")

        self.base_api_url = os.getenv("KUBERNETES_BASE_URL")
        self.service_account_token = os.getenv("KUBERNETES_SERVICE_ACCOUNT_TOKEN")

        # create an instance of http client
        self._http = Http(headers={'Authorization': f"Bearer {self.service_account_token}"})

        try:
            Logger.attention("Checking API server health.. Please wait")

            # api server health check. raises exception if server is 💀💀💀 or the healthz url is incorrect
            self.verify_server_health()

            if not self.does_namespace_exist(os.getenv('KUBERNETES_NAMESPACE')):
                self.create_init_namespace(namespace=os.getenv('KUBERNETES_NAMESPACE'))
        except KubernetesException:
            Logger.error("API server unavailable. Please check your Kubernetes environment.")
            raise

    def send_request(self, resource_path, method: HttpMethods, json_content=None, object_name=None):
        match method:
            case HttpMethods.POST:
                return self._http.post(url=f"{self.base_api_url}{resource_path}", json_content=json_content)
            case HttpMethods.GET:
                return self._http.get(url=f"{self.base_api_url}{resource_path}")
            case HttpMethods.DELETE:
                return self._http.delete(url=f"{self.base_api_url}{resource_path}")

    # def create_object(self, object_definition, uri):
    #     Logger.attention('Attempting to save a new Kubernetes object')
    #
    #     _http = Http({"Authorization": f"Bearer {self.service_account_token}"})
    #
    #     api_response = _http.post(url=f"{self.namespaced_api_url}{uri}", json_content=object_definition)
    #     api_response_json = api_response.json()
    #
    #     if api_response.status_code != 201:
    #         raise KubernetesException(f"Object creation failed\nMessage: {api_response_json['message']}")
    #
    #     Logger.success('Successfully saved a new Kubernetes object to the API')
    #
    # def delete_object(self, object_name, uri):
    #     Logger.attention('Attempting to delete a Kubernetes object')
    #
    #     _http = Http({"Authorization": f"Bearer {self.service_account_token}"})
    #
    #     api_response = _http.delete(url=f"{self.namespaced_api_url}{uri}/{object_name}")
    #     api_response_json = api_response.json()
    #
    #     if api_response.status_code != 200:
    #         raise KubernetesException(f"Object deletion failed\nMessage: {api_response_json['message']}")
    #
    #     Logger.success('Successfully deleted a Kubernetes object')
    #
    # def get_object(self, object_name, uri):
    #     Logger.attention('Attempting to retrieve an object from the Kubernetes API')
    #
    #     _http = Http({"Authorization": f"Bearer {self.service_account_token}"})
    #
    #     api_response = _http.get(url=f"{self.namespaced_api_url}{uri}/{object_name}")
    #     api_response_json = api_response.json()
    #
    #     if api_response.status_code != 200:
    #         raise KubernetesException(f"Could not get object '{object_name}'\n"
    #                                   f"Message: {api_response_json['message']}")
    #
    #     Logger.success('Successfully retrieved a Kubernetes object from the API')
    #
    #     return api_response.json()

    def verify_server_health(self):
        api_response = self._http.get(url=f"{self.base_api_url}/healthz")

        if api_response.status_code != 200:
            raise KubernetesException("Unable to check Kubernetes cluster health")
        return True

    def does_namespace_exist(self, namespace: str) -> bool:
        _uri = "/api/v1/namespaces"

        api_response = self._http.get(url=f"{self.base_api_url}{_uri}/{namespace}/status")

        if api_response.status_code != 200:
            return False

        return True

    def create_init_namespace(self, namespace: str):
        _uri = "/api/v1/namespaces"

        json_object_definition = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": namespace,
            }
        }

        api_response = self._http.post(f"{self.base_api_url}{_uri}", json_content=json_object_definition)

        if api_response.status_code != 201:
            raise KubernetesException('Unable to create the initial namespace')

    def __enter__(self):
        Logger.success("Connection to Kubernetes API server established successfully")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Logger.attention("Kubernetes API Gateway closed successfully")
        pass
