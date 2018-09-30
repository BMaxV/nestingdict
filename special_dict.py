
class MySpecialDict(dict):

    #def __missing__(self, key):
    #    value = self[key] = type(self)()
    #    return value
    
    #def __contains__(self,other):
    #    print("contains",self,other)
    #    r=super().__contains__(other)
    #    
    #    return r
        
    def retrieve(self, path_list, neg_depth=0):

        current = self
        c = 0
        m = len(path_list)

        while c < m:
            key = path_list[c]
            current = current[key]
            c += 1
        return current

def mysetter(d, path_list, key_or_data):
    path_list = path_list.copy()
    c = 0

    while path_list != []:
        if len(path_list) > 1:
            d[path_list[0]] = {}
            d = d[path_list[0]]

        if len(path_list) == 1:
            d[path_list[0]] = key_or_data

        path_list.pop(0)

    return d

def mypop(d,path_list, key_or_data, c=0, rm_rf=True):
    """takes a list of keys specifying the 'path' and the value to be removed"""
    #print(d)
    #print(path_list)
    key = path_list[0]
    if key in d:
        #print(d)
        #print(d[key])
        if len(d[key]) != 0:
            if type(d[key]) == type(d):
                #print(d)
                new_path=path_list[1:]
                if new_path!=[]:
                    r = mypop(d[key],new_path, key_or_data, c+1)
                   
                else:
                    #this bit toggles whether it's allowed to pop
                    #possibly not empty dicts from the path
                    #deleting everything to the "right"
                    #not sure if I want this yet
                    #but the potential to shoot
                    #yourself in the foot is definitely given.
                    if rm_rf:
                        r=True
                #print(r)
                if r:
                    d.pop(key)
                    if len(d) == 0:
                        return True

            if key in d:
                if d[key] == key_or_data:
                    return True


def test():
    d={}

    mysetter(d,["hello","there","my","friend"],"a")
    assert d =={"hello":{"there":{"my":{"friend":"a"}}}}
    d_save = d.copy()

    path_l = ["hello", "there", "my", "friend"]
    data = "a"

    mysetter(d,["hello","there","dude"], 2)
    #d.mysetter(["hello","there","my","friend"
    # teardowns
    
    mypop(d,path_l, data)
    #print(d)
    assert d=={"hello":{"there":{"dude":2}}}
    
    #return
    #d2 = {}
    #mysetter(d2,path_l, data)

    #mypop(d2,path_l, data)
    #assert {} == d2
    
    d3={}
    mysetter(d3,["1","2","3","4"],"5")
    mysetter(d3,["a","b","c"],"d")
    #d3["1"]["2"]["3"]["4"]="5"
    #d3["a"]["b"]["c"]="d"
    #print(d3)
    mypop(d3,["1","2"],"4")
    print("d3",d3)
    assert d3 == {"a":{"b":{"c":"d"}}}
    
    #d4={}
    #mysetter(d4,["1","2","3"],"4")
    


if __name__ == "__main__":
    test()
