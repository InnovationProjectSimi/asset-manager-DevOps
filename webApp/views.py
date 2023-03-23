# Imports
import datetime
from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template,
    request,
    flash,
    current_app,
)
from flask_login import login_required, current_user
from .models import UserAsset, Asset, appDB
from .functions import sanitise_input

# Create a blueprint for a collection of routes for the website viewing components
views = Blueprint("views", __name__)


# Home page is set to the website route /
@views.route("/")
def homePage():
    # Render the home page html template
    return render_template("home.html")


# View assets page is set to the website route /viewAssets
@views.route("/viewAssets")
# Require the user to be logged in to access
@login_required
def viewAssets():
    # Get and store the user assets which belong to the current logged in user
    userAssets = UserAsset.query.filter_by(userID=current_user.id).all()
    assetList = []
    # Store each individual asset the user owns
    for userAsset in userAssets:
        singleAsset = Asset.query.filter_by(id=userAsset.assetID).first()
        assetList.append(singleAsset)
    # endfor

    # Render the viewAssets template and send three parameters
    return render_template(
        "viewAssets.html",
        assets=assetList,
        userAssets=userAssets,
        listSize=len(assetList),
    )


# Add assets page is set to the website route /addAssets
@views.route("/addAsset", methods=["GET", "POST"])
# Require the user to be logged in to access
@login_required
def addAsset():
    # Check if the request is a post - A submitted form
    if request.method == "POST":
        # Save the form data
        formData = request.form
        # Get any existing asset which match the same of the asset the user entered
        existingAsset = Asset.query.filter_by(
            name=sanitise_input(formData.get("assetName").lower())
        ).first()

        # Validation of the form data
        # Check asset name is atleast 2 characters in length
        if len(sanitise_input(formData.get("assetName"))) < 2:
            current_app.logger.warning("Add asset failed - asset name too short")
            # Notify the user of the problem
            flash("Asset name is not long enough", category="Information")
        # Check description is not empty
        elif sanitise_input(formData.get("description")) == "":
            current_app.logger.warning("Add asset failed - no asset description")
            # Notify the user of the problem
            flash("Must add a desciption", category="Information")
        # Check quantity is atleast 1
        elif int(formData.get("quantity")) < 1:
            # Already checked client side
            current_app.logger.warning("Add asset failed - invalid quantity")
            # Notify the user of the problem
            flash("Quantity must be 1 or higher", category="Information")
        # Check date is not empty
        elif formData.get("date") == "":
            current_app.logger.warning("Add asset failed - date does not exist")
            # Notify the user of the problem
            flash("Must input a date", category="Information")
        # Check if the asset already exists
        elif existingAsset:
            userExistingAsset = UserAsset.query.filter_by(
                assetID=existingAsset.id, userID=current_user.id
            ).first()
            # Check if the user specifically already owns the asset
            if userExistingAsset:
                # If the user already owns the asset the quantity should be updated as the existing asset
                userExistingAsset.quantity = userExistingAsset.quantity + int(
                    formData.get("quantity")
                )
                # Commit to the database
                appDB.session.commit()
                current_app.logger.info(
                    "Add asset success - asset already owned, updated quantity"
                )
                # Notify the user
                flash(
                    "You already own this asset, you quantity of this asset had been added and updated.",
                    category="Information",
                )
            # The asset already exists but is not owned by the user
            else:
                # In this case the users new description is appended to the existing description and add the asset to the user
                existingAsset.description = "{}. {}".format(
                    existingAsset.description,
                    sanitise_input(formData.get("description")),
                )
                dateFormat = datetime.datetime(
                    *[
                        int(v)
                        for v in formData.get("date")
                        .replace("T", "-")
                        .replace(":", "-")
                        .split("-")
                    ]
                )
                new_userAsset = UserAsset(
                    userID=current_user.id,
                    assetID=existingAsset.id,
                    dateStored=dateFormat,
                    quantity=formData.get("quantity"),
                )
                # Add and commit to the database
                appDB.session.add(new_userAsset)
                appDB.session.commit()
                current_app.logger.info(
                    "Add asset success - asset exists, updated description"
                )
                # Notify the user
                flash(
                    "This asset already exists, you description has been added onto the existing asset and added to your user.",
                    category="Information",
                )

        # If the entered data passes all checks
        else:
            # Add the asset to the database
            new_asset = Asset(
                name=sanitise_input(formData.get("assetName")).lower(),
                description=sanitise_input(formData.get("description")),
            )
            appDB.session.add(new_asset)
            appDB.session.commit()
            # Add the user asset to the database
            dateFormat = datetime.datetime(
                *[
                    int(v)
                    for v in formData.get("date")
                    .replace("T", "-")
                    .replace(":", "-")
                    .split("-")
                ]
            )
            new_userAsset = UserAsset(
                userID=current_user.id,
                assetID=new_asset.id,
                dateStored=dateFormat,
                quantity=formData.get("quantity"),
            )
            appDB.session.add(new_userAsset)
            appDB.session.commit()
            current_app.logger.info("Add asset success")
            # Notify the user
            flash("Asset added", category="Success")

    # Render the addAssets template and send one parameter
    return render_template("addAsset.html", user=current_user)


# Update asset page is set to the website route /updateAsset
@views.route("/updateAsset", methods=["GET", "POST"])
# Require the user to be logged in to access
@login_required
def updateAsset():
    # Check if the request is a post - A submitted form
    if request.method == "POST":
        # Redirect the user to a page to update the asset selected and send one parameter from the form
        return redirect(
            url_for("views.updateSelectedAsset", name=request.form.get("assetList"))
        )

    # Get all assets from the database to be used to display on the page
    assets = Asset.query.all()
    # Render the updateAsset template and send five parameters
    return render_template(
        "updateAsset.html",
        user=current_user,
        UserAsset=UserAsset,
        Assets=assets,
        name="",
        description="",
    )


# Update asset page is set to the website route /updateSelectedAsset/<name of asset>
@views.route("/updateSelectedAsset/<name>", methods=["GET", "POST"])
# Require the user to be logged in to access
@login_required
def updateSelectedAsset(name):
    # One parameter passed
    #   Parameter is name which is name of the asset to update

    # Get asset details about the asset from the database
    asset = Asset.query.filter_by(name=name).first()

    # Check if the request is a post - A submitted form
    if request.method == "POST":
        existingAsset = Asset.query.filter_by(
            name=sanitise_input((request.form.get("newName")).lower())
        ).first()
        # Validation of the form data
        # Check new name is atleast 2 characters in length
        if len(sanitise_input(request.form.get("newName"))) < 2:
            current_app.logger.warning("Update asset failed - asset name too short")
            # Notify the user of the problem
            flash("Asset name is not long enough", category="Information")
        # Check new description is not empty
        elif sanitise_input(request.form.get("newDescription")) == "":
            current_app.logger.warning("Update asset failed - no asset description")
            # Notify the user of the problem
            flash("Must add a description", category="Information")
        # Check the asset is not set to an already existing asset
        elif existingAsset and existingAsset.id != asset.id:
            current_app.logger.warning("Update asset failed - asset already exists")
            # Notify the user of the problem
            flash(
                "Asset name cannot be renamed to an existing asset",
                category="Information",
            )
        # If the entered data passes all checks
        else:
            # Update the name and description of the asset
            asset.name = sanitise_input((request.form.get("newName")).lower())
            asset.description = sanitise_input(request.form.get("newDescription"))
            appDB.session.commit()
            current_app.logger.info("Update asset success")
            # Notify the user of the success
            flash("Asset has been updated", category="Success")

    # Render the updateSelectedAsset template and send one parameter
    return render_template("updateSelectedAsset.html", Asset=asset)


# Update delete page is set to the website route /deleteAsset
@views.route("/deleteAsset", methods=["GET", "POST"])
# Require the user to be logged in to access
@login_required
def deleteAsset():
    # Check if the request is a post and ensure the user is an admin
    if request.method == "POST" and current_user.username == "admin":
        # Check which form has been accessed
        if "userAssetList" in request.form:
            # Remove the user asset which has been selected
            deleteUserAsset = UserAsset.query.get(request.form.get("userAssetList"))
            appDB.session.delete(deleteUserAsset)
            appDB.session.commit()
            current_app.logger.info("User asset removed success")
            # Notify about the user asset being removed
            flash(
                "UserAsset {} has been removed".format(
                    request.form.get("userAssetList")
                ),
                category="Success",
            )
        else:
            # Remove the all user assets that includes the selected asset
            # and also remove the user asset from the database
            deleteAsset = Asset.query.get(request.form.get("assetList"))
            deleteUserAssetList = UserAsset.query.filter_by(
                assetID=deleteAsset.id
            ).all()

            appDB.session.delete(deleteAsset)
            for deleteUserAsset in deleteUserAssetList:
                appDB.session.delete(deleteUserAsset)
            appDB.session.commit()
            current_app.logger.info("Asset removed success")
            # Nofity the user that the asset has been removed
            flash("Asset has been removed", category="Success")

    # Check the method is post but only users that are not admin will be checked
    elif request.method == "POST":
        current_app.logger.warning("Delete failed - User not admin")
        # Notify the user that they cannot access the page as they are not admin
        flash("You must be admin to perform this function", category="Information")

    # Query the database for data which will be needed for the template
    assets = Asset.query.all()
    userAssets = UserAsset.query.all()
    # Render the deleteAsset template and send two parameters
    return render_template("deleteAsset.html", Assets=assets, UserAssets=userAssets)
