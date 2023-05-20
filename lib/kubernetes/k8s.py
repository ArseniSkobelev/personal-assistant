from contextlib import contextmanager
from pprint import pprint

from classes.kubernetes import (
    Node,
)
from lib.configlib import KubernetesConfig
from lib.logger import Logger
from lib.exceptions import *
from lib.http import Http


class Kubernetes:
    def __init__(self, creds: KubernetesConfig):
        Logger.attention("Trying to establish a connection to the Kubernetes API server")

        if not isinstance(creds, KubernetesConfig):
            raise ConfigException("Incorrect config type provided to the class constructor")

        self.api_url = creds.k8s_api_url
        self.service_account_token = creds.k8s_serviceaccount_token
        self.healthz_api_url = creds.k8s_healthz_url
        self.namespaced_api_url = creds.k8s_api_url_namespaced

        try:
            Logger.attention("Checking API server health.. Please wait")

            # api server health check. raises exception if server is 💀💀💀 or the healthz url is incorrect
            self.verify_server_health()

            if not self.does_namespace_exist(creds.namespace):
                self.create_init_namespace(namespace=creds.namespace)
        except KubernetesException:
            Logger.error("API server unavailable. Please check your Kubernetes environment.")
            raise

    def create_object(self, object_definition, uri):
        Logger.attention('Attempting to save a new Kubernetes object')

        _http = Http({"Authorization": f"Bearer {self.service_account_token}"})

        api_response = _http.post(url=f"{self.namespaced_api_url}{uri}", json_content=object_definition)
        api_response_json = api_response.json()

        if api_response.status_code != 201:
            raise KubernetesException(f"Object creation failed\nMessage: {api_response_json['message']}")

        Logger.success('Successfully saved a new Kubernetes object to the API')

    def delete_object(self, object_name, uri):
        Logger.attention('Attempting to delete a Kubernetes object')

        _http = Http({"Authorization": f"Bearer {self.service_account_token}"})

        api_response = _http.delete(url=f"{self.namespaced_api_url}{uri}/{object_name}")
        api_response_json = api_response.json()

        if api_response.status_code != 200:
            raise KubernetesException(f"Object deletion failed\nMessage: {api_response_json['message']}")

        Logger.success('Successfully deleted a Kubernetes object')

    def get_object(self, object_name, uri):
        Logger.attention('Attempting to retrieve an object from the Kubernetes API')

        _http = Http({"Authorization": f"Bearer {self.service_account_token}"})

        api_response = _http.get(url=f"{self.namespaced_api_url}{uri}/{object_name}")
        api_response_json = api_response.json()

        if api_response.status_code != 200:
            raise KubernetesException(f"Could not get object '{object_name}'\n"
                                      f"Message: {api_response_json['message']}")

        Logger.success('Successfully retrieved a Kubernetes object from the API')

        return api_response.json()

    def verify_server_health(self):
        _http = Http(headers={"Authorization": f"Bearer {self.service_account_token}"})

        api_response = _http.get(url=self.healthz_api_url)

        if api_response.status_code != 200:
            raise KubernetesException("Unable to check Kubernetes cluster health")
        return True

    def does_namespace_exist(self, namespace: str) -> bool:
        _http = Http(headers={"Authorization": f"Bearer {self.service_account_token}"})
        _uri = "/namespaces"

        api_response = _http.get(url=f"{self.api_url}{_uri}/{namespace}/status")

        if api_response.status_code != 200:
            return False

        return True

    def create_init_namespace(self, namespace: str):
        _http = Http(headers={"Authorization": f"Bearer {self.service_account_token}"})
        _uri = "/namespaces"

        json_object_definition = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": namespace,
            }
        }

        api_response = _http.post(f"{self.api_url}{_uri}", json_content=json_object_definition)

        if api_response.status_code != 201:
            pprint(api_response.json())
            raise KubernetesException('Unable to create the initial namespace')

    def __enter__(self):
        Logger.success("Connection to Kubernetes API server established successfully")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Logger.attention("Kubernetes API Gateway closed successfully")
        pass
