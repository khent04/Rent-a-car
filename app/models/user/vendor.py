from ferris import BasicModel, ndb
from app.models.user.user import User


class Vendor(User):

    company = ndb.StringProperty(required=True, indexed=True)
    unit_number = ndb.IntegerProperty(required=True, indexed=False)
    street_address = ndb.StringProperty(required=True, indexed=False)
    country = ndb.StringProperty(required=True, indexed=False)
    fleet_size = ndb.IntegerProperty(required=False, indexed=False)
    #logo = blob TBA
    credential = ndb.KeyProperty(kind='Certificate', required=False, repeated=True, indexed=False)
    # the vendor may upload file for aproval
    votes = ndb.KeyProperty(kind='User', required=False, repeated=True, indexed=False)
    # came from the renter who already have experience, new users has no capability of doing so to avoid hoax credibility
    credibility = IntegerProperty(required=False, indexed=False)
    # 1 certificate = 2 points
    # 1 vote from experienced renter = 1 point
    # a total of 25 points = 100% credibility
    company_rules = ndb.TextProperty(required=False, indexed=False)
    abouts = ndb.TextProperty(required=False, indexed=False)






