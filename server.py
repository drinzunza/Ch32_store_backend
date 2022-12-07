from flask import Flask, request, abort
import json
import random
from config import me
from mock_data import catalog
from config import db
from bson import ObjectId

app = Flask("server")


@app.get("/")
def home():
    return "Hello from Flask!"

@app.get("/test")
def test():
    return "This is another endpoint"

@app.get("/about")
def about():
    return "Sergio Inzunza"




####################################################
##############     CATALOG API  ####################
####################################################

@app.get("/api/version")
def version():
    version = {
        "v": "v1.0.4",
        "name": "zombie rabbit"
    }

    # parse a dict into json string
    return json.dumps(version)



@app.get("/api/about")
def api_about():
    return json.dumps(me)



# GET /api/catalog
# returns the catalog as json
# try it in the browser
@app.get("/api/catalog")
def get_catalog():
    # read form db
    cursor = db.Products.find({})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

# POST /api/catalog
@app.post("/api/catalog")
def save_product():
    product = request.get_json()

    # validations
    if "title" not in product:
        return abort(400, "Title is required")

    if len(product["title"]) < 5:
        return abort(400, "Title should contain 5 chars or more")

    if "category" not in product:
        return abort(400, "Category is required")

    if "price" not in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], (float, int) ):
        return abort(400, "Price must be a valid number")

    if product["price"] < 0:
        return abort(400, "Price must be greater than 0")


    # save product to db
    db.Products.insert_one(product) # save the object, will assign an _id: ObjectId(12368713287613)
    # fix the _id value
    product["_id"] = str(product["_id"])

    return json.dumps(product)


# GET /api/test/count
# return the number of products in the list
@app.get("/api/test/count")
def num_of_products():   
    count = db.Products.count_documents({}) 
    return json.dumps({"total": count})


@app.get("/api/catalog/<category>")
def by_category(category):
    results = []
    cursor = db.Products.find({ "category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)



# GET /api/catalog/search/<text>
# return products whose title contains the text
@app.get("/api/catalog/search/<text>")
def search_by_text(text):
    text = text.lower()
    results = []
    cursor = db.Products.find({"title": { "$regex": text, "$options": "i"}})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)





# GET /api/categories
# return a list with all the categories inside
@app.get("/api/categories")
def get_categories():
    results = []
    cursor = db.Products.distinct("category")
    for cat in cursor:
        results.append(cat)

    return json.dumps(results)



# get /api/test/value
# sum all prices and return the result
@app.get("/api/test/value")
def total_value():
    total = 0
    cursor = db.Products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)




# create an endpoint that returns the cheapest product
@app.get("/api/product/cheapest")
def search_cheapest():
    cursor = db.Products.find({})
    cheapest = cursor[0]
    for product in cursor:
        if product["price"] < cheapest["price"]:
            cheapest = product

    return json.dumps(cheapest)


# create an endpoint that returns a product based on a give _id
@app.get("/api/product/<id>")
def search_by_id(id):
    objId = ObjectId(id)
    prod = db.Products.find_one({"_id": objId})
    if not prod:
        return abort(404, "Product not found")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)
    





# app.run(debug=True)



######################################################################
#################### COUPON CODES ####################################
######################################################################

# save:       POST /api/coupons 
# db.Cupons 
# validatios:   
#   must have a code
#   must have a discount that should be a number (float or int)


@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()

    # validations
    if "code" not in coupon:
        abort(400, "code is required")

    if "discount" not in coupon:
        abort(400, "discount is required")

    db.Coupons.insert_one(coupon)

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)



# get all:    GET /api/coupons
@app.get("/api/coupons")
def all_coupons():
    cursor = db.Coupons.find({})
    results = []
    for coupon in cursor:
        coupon["_id"] = str(coupon["_id"])
        results.append(coupon)

    return json.dumps(results)
    

# get by id:  GET /api/coupons/<id>
@app.get("/api/coupons/<id>")
def coupon_id(id):
    objId = ObjectId(id)
    coupon = db.Coupons.find_one({"_id": objId })
    if not coupon:
        return abort(404, "Coupon not found")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)


# get by code GET/api/coupons/validate/<code>
@app.get("/api/coupons/validate/<code>")
def coupon_code(code):
    coupon = db.Coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Invalid code")

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)