
class MySpecialDict(dict):

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    def retrieve(self, path_list, neg_depth=0):

        current = self
        c = 0
        m = len(path_list)

        while c < m:
            key = path_list[c]
            current = current[key]
            c += 1
        return current

    def myset(self, path_list, key_or_data):
        path_list = path_list.copy()
        c = 0
        d = self

        while path_list != []:
            if len(path_list) > 1:
                d[path_list[0]] = MySpecialDict()
                d = d[path_list[0]]

            if len(path_list) == 1:
                d[path_list[0]] = key_or_data

            path_list.pop(0)

        return self

    def mypop(self, path_list, key_or_data, c=0, d=None):

        if d == None:
            d = self

        key = path_list[0]
        if key in d:
            if len(d[key]) != 0:
                if type(d[key]) == type(self):

                    r = self.mypop(path_list[1:], key_or_data, c+1, d[key])
                    if r:
                        d.pop(key)

                        if len(d) == 0:
                            return True

                if key in d:
                    if d[key] == key_or_data:
                        return True


def test():
    d = MySpecialDict()

    # setup
    d["hello"]["there"]["my"]["friend"] = "a"
    d_save = d.copy()

    path_l = ["hello", "there", "my", "friend"]
    data = "a"

    d["hello"]["there"]["dude"] = 2

    # teardowns
    d.mypop(path_l, data)
    assert d == d_save

    d2 = MySpecialDict()
    d2.myset(path_l, data)

    d2.mypop(path_l, data)
    assert MySpecialDict() == d2


if __name__ == "__main__":
    test()
