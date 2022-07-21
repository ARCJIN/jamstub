from django.contrib import admin
from app1.models import  Customer , Invitecode, File, Request,Watchhistory, Comment,Tag,Ad,ForgotPasswordRequest,Safe
# Register your models here.

admin.site.register(Customer)
admin.site.register(Invitecode)
admin.site.register(File)
admin.site.register(Request)
admin.site.register(Watchhistory)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Ad)
admin.site.register(Safe)
admin.site.register(ForgotPasswordRequest)
