from enum import Enum


class Role(Enum):
    ADMIN = "Admin"
    EDITOR = "Editor"
    VIEWER = "Viewer"


class Sex(Enum):
    MALE = "Male"
    FEMALE = "Female"
