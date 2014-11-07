class MyDb(dict):
    def __getitem__(self, i):
        print("getting from db " + i)
        return "from db"
#        return dict.__getitem__(self, i)

    def __setitem__(self, key, value):
        print("setting {} to {}".format(key, value))


#db = dict()
db = MyDb()

db["sam"] = "hej"
print(db["sam"])
