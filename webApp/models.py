# Imports
from . import appDB
from flask_login import UserMixin

# Create the User table
class User(appDB.Model, UserMixin):
    id          = appDB.Column(appDB.Integer, primary_key=True) # id is primary key
    username    = appDB.Column(appDB.String(50), unique=True) # username must be unique and max length of 50 characters
    password    = appDB.Column(appDB.String(100)) # password max length of 100 characters
    assets      = appDB.relationship("UserAsset") # Create a relationship with the UserAsset table

# Create the Asset table
class Asset(appDB.Model):
    id          = appDB.Column(appDB.Integer, primary_key=True) # id is primary key
    name        = appDB.Column(appDB.String(200)) # name max length of 200 characters
    description = appDB.Column(appDB.String(1000)) # description max length of 1000 characters
    assets      = appDB.relationship("UserAsset") # Create a relationship with the UserAsset table

# Create the UserAsset table
class UserAsset(appDB.Model):
    UserAssetID = appDB.Column(appDB.Integer, primary_key=True) # UserAssetID is primary key
    userID      = appDB.Column(appDB.Integer, appDB.ForeignKey("user.id")) # userID is foreign key from User table
    assetID     = appDB.Column(appDB.Integer, appDB.ForeignKey("asset.id"))# assetID is foreign key from Asset table
    dateStored  = appDB.Column(appDB.DateTime(timezone=True)) # dateStored is in correct timezone
    quantity    = appDB.Column(appDB.Integer) # quantity stored as integer