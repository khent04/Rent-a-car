from ferris import ndb, BasicModel

class Request(BasicModel):

    vendor = ndb.KeyProperty(kind="User", indexed=False)
