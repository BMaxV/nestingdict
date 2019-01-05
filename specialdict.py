
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

def mysetter(d, path_list, key_or_data,in_list=False):
    path_list = path_list.copy()
    c = 0

    while path_list != []:
        if len(path_list) > 1:
            if path_list[0] not in d:
                d[path_list[0]] = {}
            d = d[path_list[0]]

        if len(path_list) == 1:
            if path_list[0] in d:
                if type(d[path_list[0]])==list and in_list:
                    d[path_list[0]].append(key_or_data)
                else:
                    #overwrite
                    d[path_list[0]]=key_or_data
            else:
                if in_list:
                    print(d)
                    d[path_list[0]] = [key_or_data]
                else:
                    d[path_list[0]] = key_or_data

        path_list.pop(0)

    return d

def mypop(d,path_list, key_or_data=None, c=0, rm_rf=True):
    """takes a list of keys specifying the 'path' and the value to be removed"""
    
    key = path_list[0]
    if key in d:
        if type(d[key]) == type(d):
            if len(d[key]) != 0:
            
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
                if r:
                    d.pop(key)
                    if len(d) == 0:
                        return True

        if key in d:
            if d[key] == key_or_data or key_or_data==None:
                d.pop(key)
                if len(d)==0:
                    return True
                return False


def mycheck(d,path_list,key_or_data=None,c=0):
    r=None
    
    key = path_list[0]
    if key in d:
        if type(d[key]) == type(d):
            if len(d[key]) != 0:            
                new_path=path_list[1:]
                if new_path!=[]:
                    
                    r=mycheck(d[key],new_path, key_or_data, c+1)
                    if r:
                        return True
                    else:
                        return False
            
        if key in d:
            if d[key] == key_or_data or key_or_data==None:
                return True
            if type(d[key])==list:
                if key_or_data in d[key] or key_or_data==None:
                    return True
                        
            return False
    return False
                    

def test():
    d={}


    
    mysetter(d,["hello","there","my","friend"],"a")
    assert d =={"hello":{"there":{"my":{"friend":"a"}}}}
    d_save = d.copy()

    path_l = ["hello", "there", "my", "friend"]
    data = "a"

    mysetter(d,["hello","there","dude"], 2)
    # teardowns
    
    mypop(d,path_l, data)
    
    assert d=={"hello":{"there":{"dude":2}}}
    
    d3={}
    mysetter(d3,["1","2","3","4"],"5")
    
    
    mysetter(d3,["a","b","c"],"hurr",in_list=True)
    mysetter(d3,["a","b","c"],"d",in_list=True)
    mypop(d3,["1","2"],"4")
    #mysetter(d3,["a","b","c"],"hurr")
    assert d3 == {"a":{"b":{"c":["hurr","d"]}}}
    
    r=mycheck(d3,["a","b","c"],"d")
    assert r == True
    
    r2=mycheck(d3,["hey","dude"],1)
    assert r2 == False
    
if __name__ == "__main__":
    test()
