from django.db import models

from django.core.validators import MaxValueValidator , MinValueValidator

def get_default_profile_image():
    return "/default/Steve Jobs.jpg"
class Customer(models.Model):

    username = models.CharField(max_length = 50 , blank = False ,null=True ,unique = True)
    password = models.CharField(max_length = 100 , blank = False , null = True )
    prof_pic = models.ImageField(null = True,blank = True, default = get_default_profile_image )
    security_key = models.CharField(max_length = 100 , blank = False , null = True )
    desc = models.CharField(null=True , max_length=200, blank = True)
    email = models.CharField(null=True , max_length=200, blank = True)

    invited_by = models.ForeignKey('self',null = True ,related_name="invitor", on_delete= models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True, null = True)
    last_login =        models.DateTimeField(verbose_name="created_date" , auto_now = True )


    is_blocked = models.BooleanField(default = True , null = True)
    is_login = models.BooleanField(default = False , null = True)
    is_customer = True
    is_editor = models.BooleanField(default = False , null = True)
    is_owner = models.BooleanField(default = False , null = True)
    is_invited = models.BooleanField(default = False , null = True)


    GENDER = (('MALE','MALE'),('FEMALE','FEMALE'))
    gender = models.CharField(max_length = 20 , choices = GENDER, blank = True)
    INTERESTED = (('MALE','MALE'),('FEMALE','FEMALE'),('BOTH','BOTH'))
    interested = models.CharField(max_length = 20 , choices = INTERESTED, blank = True)


    def makeeditor(self):
        self.is_certified = True
    def unmakeeditor(self):
        self.is_certified = False

    def makeinvited(self):
        self.is_invited = True
    def unmakeinvited(self):
        self.is_invited = False


    def loginit(self):
        self.is_login = True

    def logoutit(self):
        self.is_login = False


    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False


    def __str__(self):
        return f" username={self.username}, gender= {self.gender} , created_date={self.created_date}"



class Invitecode(models.Model):
    text = models.CharField(max_length = 10 , blank = False , unique = True)
    from_user =   models.ForeignKey(Customer, null = True , related_name="from_invitor", on_delete= models.CASCADE)
    to_user =  models.ForeignKey(Customer, null = True ,blank=True, related_name="to_invitee", on_delete= models.CASCADE)
    is_restricted = models.BooleanField(default = True , null = True)
    created_date = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f" text={self.text}, from= {self.from_user} , to={self.to_user}"


class Tag(models.Model):
    tagtext = models.CharField(max_length = 50 , blank = False , unique = True,null = True)
    TOPIC = (('Genre','Genre'),('Category','Category'),('Positions','Positions'),('Company','Company'),('Actors','Actors'),('Location','Location'))
    topic = models.CharField(max_length = 20 , choices = TOPIC, blank = True)
    views = models.PositiveIntegerField(default=0, null = True)
    def __str__(self):
        return f" tagtext={self.tagtext}, category={self.topic}"

class File(models.Model):
    creator = models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    desc = models.CharField(max_length = 500)
    content = models.FileField(null = True,blank = True, default = get_default_profile_image )
    imagefile =  models.ImageField(null = True,blank = True, default = get_default_profile_image )
    is_block = models.BooleanField(default = False , null = True)
    is_special = models.BooleanField(default = False , null = True)
    is_promoted = models.BooleanField(default = False , null = True)
    is_highdemand = models.BooleanField(default = False , null = True)
    tags = models.ManyToManyField(Tag, related_name="tagsadded")
    likers = models.ManyToManyField(Customer, related_name="content_liked")
    num_of_comments = models.PositiveIntegerField(default=0, null = True)
    is_private = models.BooleanField(null = True , default = False)
    date_created = models.DateTimeField(auto_now_add=True , null = True)
    views =  models.PositiveIntegerField(default=0, null = True)
    is_vid = models.BooleanField(null = True, blank = True, default = False)
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


    def specialit(self):
        self.is_special = True
    def unspecialit(self):
        self.is_special = False



    def promoteit(self):
        self.is_promoted = True
    def unpromoteit(self):
        self.is_promoted = False


    def highdemandit(self):
        self.is_highdemand = True
    def unhighdemandit(self):
        self.is_highdemand = False


    def add_comment(self):
        self.num_of_comments += 1

    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False





    def __str__(self):
        return f" desc={self.desc}, creator = {self.creator}"



class Request(models.Model):
    is_accepted = models.BooleanField(blank = True, null = True, default = None)
    account = models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True , null = True)
    def __str__(self):
        return f" status={self.is_accepted}, account = {self.account} at date: {self.date_created}"



class Watchhistory(models.Model):
    person = models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    watch = models.ForeignKey(File , null=True, on_delete= models.SET_NULL)
    last_viewed = models.DateTimeField(auto_now_add=True , null = True)

    def __str__(self):
        return f" person={self.person}, watch={self.watch}, created on : {self.last_viewed}"




class Comment(models.Model):
    creator =  models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    post =  models.ForeignKey(File,null = True , on_delete= models.SET_NULL)
    text = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True , null = True)




    def __str__(self):
        return f" creator={self.creator}, text = {self.text} , post = {self.post} "




class Ad(models.Model):
    maker = models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    desc = models.CharField(max_length = 500)
    content = models.ImageField(null = True,blank = True, default = get_default_profile_image )
    is_block = models.BooleanField(default = False , null = True)
    is_special = models.BooleanField(default = False , null = True)
    is_promoted = models.BooleanField(default = False , null = True)
    is_highdemand = models.BooleanField(default = False , null = True)
    date_created = models.DateTimeField(auto_now_add=True , null = True)
    duration = models.PositiveIntegerField(null = True , blank = True , default = 7)
    def __str__(self):
        return f" creator={self.maker}, text = {self.desc} , date_created = {self.date_created} "
class ForgotPasswordRequest(models.Model):
    typedusername = models.CharField(max_length = 50 , blank = False)
    hisemail = models.CharField(null=True , max_length=200, blank = True)
    def __str__(self):
        return f" request generated for username={self.typedusername} "

class Safe(models.Model):
    master = models.ForeignKey(Customer,null = True , on_delete= models.CASCADE)
    safefile =  models.ForeignKey(File,null = True , on_delete= models.CASCADE)
