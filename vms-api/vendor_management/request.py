class RequestProcess:

    def __init__(self,data):
        self.data =data
        self.errors =[]


    def has(self,list_of_fields):

        for field in list_of_fields:
            if field not in self.data:
                self.errors.append(f'{field} is required')
                continue
            if self.data[field]=='':
                self.errors.append(f'{field} should not be blank')
                continue
            if self.data[field]==None:
                self.errors.append(f'{field} should not be null')


    def has_errors(self):
        if self.errors:
            return self.errors[0]
        return None