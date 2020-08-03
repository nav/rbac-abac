import pytest
import casbin

from entities import *


enforcer = casbin.Enforcer("model.conf", "policy.csv")


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
