from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'new_shop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin_trans_prod/$', 'new_shop.views.admin_trans_prod'),
    url(r'^admin_trans_user/$', 'new_shop.views.admin_trans_user'),
    url(r'^admin_trans_userinfo/(?P<u_id>\d+)/$', 'new_shop.views.admin_trans_userinfo'),
    url(r'^admin_trans/$', 'new_shop.views.admin_trans'),    
    url(r'^admin_trans_user/$', 'new_shop.views.admin_trans_user'),
    url(r'^disptrans/$', 'new_shop.views.disptrans'),
    url(r'^category/(?P<prod_cat>[A-Za-z\-]+)/$', 'new_shop.views.category'),
    url(r'^submit_com/(?P<prod_id>\d+)/$', 'new_shop.views.submit_com'),
    url(r'^srch/$', 'new_shop.views.srch'),
    url(r'^logout/$', 'new_shop.views.logout'),
    url(r'^showtrans/$', 'new_shop.views.showtrans'),
    url(r'^showcart/$', 'new_shop.views.showcart'),
    url(r'^addtocart/(?P<product_id>\d+)/$', 'new_shop.views.addtocart'),
    url(r'^signup/$', 'new_shop.views.signup'),    
    url(r'^login/$', 'new_shop.views.login'),    
    url(r'^product/(?P<product_id>\d+)/$', 'new_shop.views.prd'),
    url(r'^home/$', 'new_shop.views.home'),
    url(r'^admin/', include(admin.site.urls)),
                       
)

