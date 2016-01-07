from ferris import ndb
from app.models.user.user import User


class Vendor(User):

    company = ndb.StringProperty(indexed=True)
    unit_number = ndb.StringProperty(indexed=False)
    street_address = ndb.StringProperty(indexed=False)
    country = ndb.StringProperty(indexed=False)
    fleet_size = ndb.StringProperty(indexed=False)
    # logo = blob TBA
    credentials = ndb.KeyProperty(kind='Certificate', repeated=True, indexed=False)
    # the vendor may upload file for aproval
    votes = ndb.KeyProperty(kind='User', repeated=True, indexed=False)
    # came from the renter who already have experience, new users has no
    # capability of doing so to avoid hoax credibility
    credibility = ndb.IntegerProperty(indexed=False)
    # 1 certificate = 2 points
    # 1 vote from experienced renter = 1 point
    # a total of 25 points = 100% credibility
    company_rules = ndb.TextProperty(indexed=False)
    abouts = ndb.TextProperty(indexed=False)
    activated = ndb.BooleanProperty(default=False, indexed=True)
    submitted = ndb.BooleanProperty(default=False, indexed=True)


    @classmethod
    def vendor_request(cls):
        return cls.query(cls.submitted == True, cls.activated == False).fetch()
