import random
import pytest

from entities import Resource, alice_user, bob_user, charlie_user, doug_user


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
