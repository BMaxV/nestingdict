
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

    def mysetter(self, path_list, key_or_data):
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

    def mypop(self, path_list, key_or_data, c=0, d=None, rm_rf=True):
        """takes a list of keys specifying the 'path' and the value to be removed"""
        if d == None:
            d = self
        #try:
        #    assert path_list != []
        #except AssertionError:
            
        #print(path_list)
        key = path_list[0]
        if key in d:
            if len(d[key]) != 0:
                if type(d[key]) == type(self):
                    new_path=path_list[1:]
                    if new_path!=[]:
                        r = self.mypop(new_path, key_or_data, c+1, d[key])
                    else:
                        #this bit toggles whether it's allowed to pop
                        #possibly not empty dicts from the path
                        #deleting everything to the "right"
                        #not sure if I want this yet
                        #but the potential to shoot
                        #yourself in the foot is definitely given.
                        if rm_rf:
                            r=True
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
    d2.mysetter(path_l, data)

    d2.mypop(path_l, data)
    assert MySpecialDict() == d2
    
    d3=MySpecialDict()
    d3["1"]["2"]["3"]["4"]="5"
    d3["a"]["b"]["c"]="d"
    print(d3)
    d3.mypop(["1","2"],"4")
    print(d3)


if __name__ == "__main__":
    test()
