'''
Created on 13 juin 2017

@author: Bruno
'''
from kivy.network.urlrequest import UrlRequest



try:
    import cPickle as pickle
except ImportError:
    import pickle



class RatingScale():
    def __init__(self, type, scale):
        self.type = type
        self.scale = scale
        
   # def
class Student():
    pass
    #todo


class Extparams():
    
    def __init__(self):
        self.accounts = {}
        self.activities = {}
        self.commentaries=[]
        try:
             results = pickle.load(open("mydata.data", "rb"))
             self.datas(req=None, result=results)
        except:
             pass



    def build_from_url2(self,url):
        url = url.replace("https", "http")
        self.req=UrlRequest(url,self.datas)
        print (url)

       # box = BoxLayout(orientation='vertical')
       # box.add_widget(Label(text=url, font_size='20sp'))





        #mysm.get_screen("qrscr").add_widget(box)
    def build_from_url(self):
        # (temporary implementation to test)
       # self.activities = {"act 1" : {"id" : "http://stuff/act1ID",
        #                              "scale": RatingScale("note",20)}
        #                   ,"act 2" : {"id" : "http://stuff/act2ID",
        #                              "scale": RatingScale("letters", 4)}
        #                   }

        self.students = Student() #todo
    def datas(self,req,result):
        pickle.dump(result, open("mydata.data", "wb"))
        student_dict = result["STUDENTS"]
        for stu in student_dict:
            key = stu["login"]
            val = {"name" : stu["name"], "mdp":stu["mdp"]}
            self.accounts[key]=val
        print(self.accounts)
        activity_dict=result["ACTIVITIES"]
        for act in activity_dict:
            key2=act["name"]
            ech=RatingScale(act["ratingscale"]["type"], act["ratingscale"]["scale"])
            self.activities[key2]=ech
        print (self.activities)
        commentary_list=result["COMMENTARIES"]
        for com in commentary_list:
            self.commentaries.append(com)
        print (self.commentaries)
        #App._running_app.check()

        #for values in result:
        #    print (values)
        #print (result)