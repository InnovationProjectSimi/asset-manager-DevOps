from webApp.models import User
from werkzeug.security import generate_password_hash


# Test password hashing is in place
def test_password_hashing():
    # Test to ensure the password input is not the same as the database by checking password is hashed with function
    new_user = User(
        username="testuser2",
        password=generate_password_hash("Pizza567!", method="sha256"),
    )

    assert new_user.password != "Pizza567!"
    assert generate_password_hash("Pizza567!", method="sha256") != "Pizza567!"
