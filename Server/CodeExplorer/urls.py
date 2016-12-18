
from django.conf.urls import url

import views_html
import views_rest

urlpatterns = [
    # HTML
    url(r'^$', views_html.index),

    # REST
    url(r'^node/(?P<node_id>\S+)/$', views_rest.NodeRest.as_view()),
    url(r'^graph/(?P<type>\S+)$', views_rest.GraphRest.as_view()),
]

