# Asset Manager 

## About the project

This project acts as an asset manager where users can create, read, and update information about the assets. This helps the user to keep track of all current assets and the amount of assets they have. Users are able to add new assets to the system which are assigned to themselves, they can also add assets to themselves which may already exist and any description about the asset will be added to the existing assets description leading to highly detailed assets once a number of users have added the sepcific asset. The user may also update information about the asset to ensure assets are most up to date with description and are accurate. Users will have access to nicely view all of their current assets assigned to them which can help keep track and manage all current assets.

Users do not recieve as many privilages as an admin would, the admin is able to do all the user can but is also able to delete data from tables and from the asset manager. The admin can choose to delete all data about an asset including removing it from all users and from the database, the admin can also remove specific assets from specific users.

The asset manager should help manage and keep track of all assets for users within the organisation.

## Technologies used

This project was created using a range of technologies to support development, details of all can be seen below.

The main technologies used within development are:
- Python Flask
- SQL lite
- SQL alchemy
- Jinja2


The methodology used to create this program followed agile kanban and has been developed following kanban practices.

## Prerequisites

Note: This is assuming use of a **linux** machine - if opting for **linux ubuntu** use the latest stable Long Term Support (**LTS**) version (currently **20.04**).

1. A recent version of Python is necessary and the requirement to use __pip__.

2. Install flask using: 
    ``` 
    pip install flask
    ```

3. Install sql alchemy for flask
    ```
    pip instal flask-sqlalchemy
    ```

4. Install flask-login using:
    ```
    pip install flask-login
    ```

## How to run

To start the program, run the main.py file or from the command line interface (**CLI**) navigate into the asset manager directory and run: 
```
python3 main.py
```

The database will then be created if not already created and the program will be exposed.

## Usage

For local deployments the program is exposed on 127.0.0.1 on port 5000. To access the program navigate to http://127.0.0.1:5000/ in a browser.

Users should create an account if they do not already have one. If users already have an account they are able to login and continue using an existing account with stored data.

### Requirements for creating a user:
- Username must be unique - all usernames will become lowercase.
- Username must be longer than 4 characters
- Password must be longer than 7 characters
- Password must include at least one of the following symbols: !, @, #, $, £
- Password must include at least one digit
- Password must include at least one uppercase letter

### Using the application

Once logged in the user will have the ability to use the applications features. 

The application is split into three main features for standard users:
- View assets
- Add assets
- Update assets

**View assets**

The view assets page will shows all the assets the user owns, displaying them to the user with detailed information. If the user does not have any assets then list of assets will appear - the user can use the *add assets* function to populate this screen. Detailed information about each asset include: 
- Asset name
- Description
- Quantity owned
- Date of first asset store

**Add assets**

The add assets page allows the user to add their personal assets to the database, with thoughtful functions to ensure assets are effectively stored.

The user must add details about the assets including: 
- Asset name
- Description
- Quantity owned
- Date of first asset store

In the case the asset does not already exist elsewhere and the user does not already own the same asset then a new asset is created and the users personal data for the asset is stored.

In the case the user already owns the asset then the data about the asset is not altered but the asset quantity is added onto the existing amount the user owned.

In the case the asset already exists and the user does not currently own the asset then the description the user wrote about the asset is added onto the existing description to ensure a detailed explanation of the product and a complete new asset is not made. The user will have their personal data about the asset stored.

**Update assets**

A user is able to update information about any asset that exists in the case they have not added the asset yet but wish to update the assets details.

The name and description of an asset can be edited and this will take effect for all users.

The name cannot be changed to an asset that already exists and must be a valid by being at least two characters long.

There must be a description entered.

**Alerts**

Throughout the application when the user is using any functionality they are displayed with relevant and helpful alerts which appear as colour banners with detailed messages at the top of the screen. These alerts act to update users about any action they have performed and the success or problems of their action.

There are two banner types:

Green banners indicate a success and confirm the success of a given action, e.g. success of adding a new asset.

Amber banners indicate warning and information about a users interation to guide the user how to properly use the application, e.g. trying to sign up without following the valid password rules.

**Admin users** 

There is one admin user which holds the username of admin, the admin is able to use all the functionality that the user has, but is also able to delete assets and users assets. The functionality to delete will delete data from the database and relevant impacts to any users will be carried out, e.g. a users asset is removed. 

For the logging which an admin may want to see, logging is detailed and categorised into two options, *information* and *warning*, these can be seen in the logs of the application session (if ran locally, in the command line the application is run from.

## Creator

This application has been created by Simraaj.
