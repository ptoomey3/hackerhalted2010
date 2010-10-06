from hackerhalted.appscantests.models import User, Session1, Session2, XSSData, SensitiveData, SQLInjectionData
from django.contrib import admin


admin.site.register(User)
admin.site.register(Session1)
admin.site.register(Session2)
admin.site.register(XSSData)
admin.site.register(SensitiveData)
admin.site.register(SQLInjectionData)