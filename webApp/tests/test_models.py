# Imports
from webApp.models import User, Asset
from werkzeug.security import check_password_hash, generate_password_hash


# User table tests
def test_new_user():
    # Simple test of new user, password is not hashed when passed in
    new_user = User(
        username="testuser1",
        password="Icecream34!",
    )
    assert new_user.username == "testuser1"
    assert new_user.password == "Icecream34!"


def test_new_user_hashed():
    # Simple test of new user, password is hashed when passed in and checked as done in app
    new_user = User(
        username="testuser2",
        password=generate_password_hash("Icecream34!", method="sha256"),
    )
    assert new_user.username == "testuser2"
    assert check_password_hash(new_user.password, "Icecream34!") == True


# Asset table tests
def test_new_asset():
    # Simple test of new asset
    new_asset = Asset(
        name="cable",
        description="5m HDMI",
    )
    assert new_asset.name == "cable"
    assert new_asset.description == "5m HDMI"