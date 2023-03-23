# import pytest

# from webApp import create_app, appDB


# @pytest.fixture()
# def app():
#     app = create_app("sqlite://")

#     with app.app_context():
#         appDB.create_all

#     yield app


# @pytest.fixture()
# def client(app):
#     return app.test_client()
