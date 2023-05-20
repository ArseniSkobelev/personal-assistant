from enum import Enum


class DialogueType(Enum):
    CreateKubernetesObject = 1
    DeleteKubernetesObject = 2
    GetKubernetesObject = 3
    UpdateKubernetesObject = 4


class DialogueSubject(Enum):
    General = 1
    Kubernetes = 2


class Dialogue:
    def __init__(self, dialogue_subject: DialogueSubject, dialogue_type: DialogueType):
        self.dialogue_subject = dialogue_subject
        self.dialogue_type = dialogue_type
