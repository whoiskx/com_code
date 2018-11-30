class FacebookData(object):
    def __init__(self, account_name='', home_page='', location='', come_form='', job='', followers='', degree='',
                 sex='', is_get=''):
        self.account_name = account_name
        self.location = location
        self.come_form = come_form
        self.job = job
        self.followers = followers
        self.degree = degree
        self.sex = sex
        self.is_get = is_get
        self.home_page = home_page

    def obj_to_dict(self):
        return self.__dict__
