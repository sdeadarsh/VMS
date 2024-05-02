from rest_framework.response import Response

class ResponseProcess:

    def __init__(self,data,message,count=None,headers=None):
        self.data=data
        self.message=message
        self.count = count
        self.headers=headers

    def successfull_response(self):
        if self.count==None:
            return Response({"message":self.message,"data":self.data,"error":False})
        return Response({"message":self.message,"data":self.data,"error":False,'total_count':self.count})

    def errord_response(self):
        if self.count==None:
            return Response({"message": self.message, "data": self.data, "error": True})
        return Response({"message": self.message, "data": self.data, "error": True,'total_count':self.count})



    def successfull_response_with_headers(self):
        if self.count==None:
            return Response({"message":self.message,"data":self.data,"error":False,"headers":self.headers})
        return Response({"message":self.message,"data":self.data,"error":False,'total_count':self.count,"headers":self.headers})


    def errord_response_with_headers(self):
        if self.count==None:
            return Response({"message": self.message, "data": self.data, "error": True,"headers":self.headers})
        return Response({"message": self.message, "data": self.data, "error": True,'total_count':self.count,"headers":self.headers})



