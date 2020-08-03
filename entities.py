import abc
import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Subject(abc.ABC):
    identity: str


@dataclass(frozen=True)
class Role(Subject):
    @property
    def urn(self):
        return f"role:{self.identity}"


@dataclass(frozen=True)
class User(Subject):
    @property
    def urn(self):
        return f"user:{self.identity}"


@dataclass(frozen=True)
class Resource:
    name: str
    owner_urn: typing.Optional[str] = None
    approver_urn: typing.Optional[str] = None
    identity: typing.Optional[str] = None

    @property
    def urn(self):
        if self.identity:
            return f"resource:{self.name}:{self.identity}"
        return f"resource:{self.name}"


@dataclass(frozen=True)
class Action:
    name: str

    @property
    def urn(self):
        return f"action:{self.name}"


# Instances

user_role = Role(identity="user")
approver_role = Role(identity="approver")
manager_role = Role(identity="manager")
admin_role = Role(identity="admin")

alice_user = User(identity="alice")
bob_user = User(identity="bob")
charlie_user = User(identity="charlie")
doug_user = User(identity="doug")
eli_user = User(identity="eli")
frank_user = User(identity="frank")
gary_user = User(identity="gary")

order_resource = Resource(name="order")
settings_resource = Resource(name="settings")
user_settings_resource = Resource(name="settings", identity="user")
finance_settings_resource = Resource(name="settings", identity="finance")

read_action = Action(name="read")
write_action = Action(name="write")
change_action = Action(name="change")
approve_action = Action(name="approve")  # approve action is an arbitrary domain action
manage_action = Action(name="manage")  # manage action is an arbitrary domain action
