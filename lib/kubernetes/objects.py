import os
from enum import Enum
from lib.exceptions import KubernetesException
from lib.kubernetes.k8s import Kubernetes, HttpMethods


# --- to be implemented ---
# StatefulSet = 5
# DaemonSet = 6
# -------------------------

# Service = 7 # Service
# PersistentVolume = 9
# PersistentVolumeClaim = 10
# ConfigMap = 8 # Config
# Secret = 11 # Config

class KubernetesObject:
    uri = ''
    name = None

    def __init__(self, uri, name):
        self.uri = uri
        self.name = name

    def create_object_definition(self):
        raise KubernetesException('Unable to create object definition')

    def create_object(self):
        with Kubernetes() as _k8s:
            _k8s.send_request(
                resource_path=self.uri,
                method=HttpMethods.POST,
                json_content=self.create_object_definition()
            )

    def delete_object(self):
        with Kubernetes() as _k8s:
            _k8s.delete_object(object_name=self.name, uri=self.uri)

    def get_object(self):
        with Kubernetes() as _k8s:
            _k8s.get_object(object_name=self.name, uri=self.uri)


class Namespace(KubernetesObject):
    def __init__(self, name: str):
        super().__init__(uri='/api/v1/namespaces', name=name)

    def __str__(self):
        return self.name

    def create_object_definition(self):
        return {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
                "name": self.name,
            }
        }


class Pod(KubernetesObject):
    def __init__(self, pod_name, image, labels=None):
        self.namespace = os.getenv('KUBERNETES_NAMESPACE')
        super().__init__(uri=f'/api/v1/namespaces/{self.namespace}/pods', name=pod_name)
        self.labels = labels or {}
        self.image = image

    def create_object_definition(self):
        return {
            "kind": "Pod",
            "apiVersion": "v1",
            "metadata": {
                "name": self.name,
                "labels": self.labels
            },
            "spec": {
                "containers": [
                    {
                        "name": self.name,
                        "image": self.image,
                    }
                ],
            }
        }


class Deployment(KubernetesObject):
    def __init__(self, name, image, labels=None):
        super().__init__(uri='/deployment', name=name)
        self.labels = labels or {}
        self.image = image

#
#
# class AccessMode(str, Enum):
#     ReadWriteOnce = "ReadWriteOnce"
#     ReadOnlyMany = "ReadOnlyMany"
#     ReadWriteMany = "ReadWriteMany"
#
#
# class Service:
#     def __init__(self):
#         raise NotImplemented
#
#
# class Deployment:
#     def __init__(self):
#         raise NotImplemented
#
#
# class PersistentVolumeClaim:
#     def __init__(self, name: str, capacity: str = '10Gi', access_mode: AccessMode = AccessMode.ReadWriteOnce,
#                  storage_class_name: str = 'manual'):
#         self.name = name
#         self.capacity = capacity
#         self.access_mode = access_mode
#         self.storage_class_name = storage_class_name
#
#     def get_object(self) -> dict:
#         return {
#             "apiVersion": "v1",
#             "kind": "PersistentVolumeClaim",
#             "metadata": {
#                 "name": f"{self.name}"
#             },
#             "spec": {
#                 "resources": {
#                     "requests": {
#                         "storage": f"{self.capacity}"
#                     }
#                 },
#                 "accessModes": [
#                     f"{self.access_mode}"
#                 ],
#                 "storageClassName": f"{self.name}",
#             }
#         }
#
#
# class PersistentVolume:
#     uri = 'persistentvolumes'
#
#     def __init__(self, name: str, labels: dict = None, capacity: str = '10Gi', access_mode: AccessMode =
#     AccessMode.ReadWriteOnce,
#                  storage_class_name: str = 'manual', host_path: str = '/personalhub/pv', reclaim_policy: str =
#                  'Recycle'):
#         self.name = name
#         self.capacity = capacity
#         self.labels = labels or {}
#         self.access_mode = access_mode
#         self.storage_class_name = storage_class_name
#         self.host_path = host_path
#         self.reclaim_policy = reclaim_policy
#
#     def __str__(self) -> str:
#         return f"Persistent volume:\n" \
#                f"Name: {self.name}\n" \
#                f"Storage capacity: {self.capacity}\n" \
#                f"Labels: {self.labels}\n" \
#                f"Access mode: {self.access_mode}\n" \
#                f"Storage class name: {self.storage_class_name}\n" \
#                f"Reclaim policy: {self.reclaim_policy}\n" \
#                f"Host path: {self.host_path}\n"
#
#     def create_object_definition(self) -> dict:
#         return {
#             "apiVersion": "v1",
#             "kind": "PersistentVolume",
#             "metadata": {
#                 "name": f"{self.name}"
#             },
#             "spec": {
#                 "capacity": {
#                     "storage": f"{self.capacity}"
#                 },
#                 "accessModes": [
#                     f"{self.access_mode}"
#                 ],
#                 "persistentVolumeReclaimPolicy": f"{self.reclaim_policy}",
#                 "volumeMode": "Filesystem",
#                 "storageClassName": f"{self.name}",
#                 "hostPath": {
#                     "path": f"{self.host_path}"
#                 }
#             }
#         }
#
#     def save_object(self, creds: KubernetesConfig):
#         with Kubernetes(creds) as _k8s:
#             _k8s.create_object(object_definition=self.create_object_definition(), uri=self.uri)
#
#     def delete_object(self, creds: KubernetesConfig):
#         with Kubernetes(creds) as _k8s:
#             _k8s.delete_object(object_name=self.name, uri=self.uri)
#
#     def get_object(self, creds: KubernetesConfig):
#         with Kubernetes(creds) as _k8s:
#             _k8s.get_object(object_name=self.name, uri=self.uri)
#
#
# class Secret:
#     def __init__(self):
#         raise NotImplemented
