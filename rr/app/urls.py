from django.conf.urls import url, include,patterns
from app.views import *

urlpatterns = [
url(r'^login/$', user_login, name='user_login'),
url(r'^addproduct/$', addproduct, name='product_upload'),
url(r'^productdetail/$', product_detail, name='product_detail'),
url(r'^user/getallproduct/$', get_all_user_product, name='get_all_user_product'),
url(r'^getallproduct/$',get_all_product, name='get_all_product'),
]
