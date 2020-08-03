import abc
import typing
import random
from dataclasses import dataclass

import pytest
import casbin


# Entities


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
approve_action = Action(name="approve")
manage_action = Action(name="manage")  # manage action is an arbitrary domain action


# Initialize
enforcer = casbin.Enforcer("model.conf", "policy.csv")


# Fixtures


@pytest.fixture
def object_id():
    return "".join((random.choice("abcdef2345678") for i in range(3)))


@pytest.fixture
def user():
    return random.choice([alice_user, bob_user, charlie_user])


@pytest.fixture
def approver():
    return random.choice([charlie_user, doug_user])


@pytest.fixture
def order(object_id, user, approver):
    return Resource(
        name="order",
        owner_urn=user.urn,
        approver_urn=approver.urn,
        identity=f"ord_{object_id}",
    )


# Tests


@pytest.mark.parametrize(
    "user,expected",
    [(alice_user, True), (bob_user, True), (charlie_user, True), (doug_user, False)],
)
def test_user_can_write_order(user, expected):
    assert bool(enforcer.enforce(user, order_resource, write_action)) == expected


@pytest.mark.parametrize("order", range(10), indirect=True)
def test_user_can_only_read_owned_resources(order, user):
    result = enforcer.enforce(user, order, read_action)

    if user.urn == order.owner_urn:
        assert result
    else:
        assert not result


@pytest.mark.parametrize("order", range(10), indirect=True)
def test_user_can_only_change_owned_resources(order, user):
    result = enforcer.enforce(user, order, change_action)

    if user.urn == order.owner_urn:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "user,expected",
    [(alice_user, False), (bob_user, False), (charlie_user, True), (doug_user, True)],
)
def test_user_cannot_approve_order(user, expected):
    assert bool(enforcer.enforce(user, order_resource, approve_action)) == expected


@pytest.mark.parametrize("order", range(10), indirect=True)
def test_approver_can_only_approve_order_resources_pending_their_approval(
    order, approver
):
    result = enforcer.enforce(approver, order, approve_action)

    if approver.urn == order.approver_urn:
        assert result
    else:
        assert not result


@pytest.mark.parametrize(
    "user,expected",
    [
        (alice_user, False),
        (bob_user, False),
        (charlie_user, False),
        (eli_user, True),
        (frank_user, False),
        (gary_user, False),
    ],
)
def test_user_cannot_manage_settings(user, expected):
    assert bool(enforcer.enforce(user, settings_resource, manage_action)) == expected


def test_manager_can_manage_settings():
    assert enforcer.enforce(eli_user, settings_resource, manage_action)
    assert enforcer.enforce(eli_user, user_settings_resource, manage_action)
    assert enforcer.enforce(eli_user, finance_settings_resource, manage_action)


def test_user_manager_can_manage_user_settings():
    assert enforcer.enforce(frank_user, user_settings_resource, manage_action)
    assert not enforcer.enforce(frank_user, settings_resource, manage_action)
    assert not enforcer.enforce(frank_user, finance_settings_resource, manage_action)


def test_finance_manager_can_manage_user_settings():
    assert enforcer.enforce(gary_user, finance_settings_resource, manage_action)
    assert not enforcer.enforce(gary_user, settings_resource, manage_action)
    assert not enforcer.enforce(gary_user, user_settings_resource, manage_action)
