"""libraryApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import oauth2_provider.views as oauth2_views
from django.conf import settings
from libraryApp import views
# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]
urlpatterns = [
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider_app', ), namespace='oauth2_provider'), ),
    path('admin/', admin.site.urls),

    path('sign_up/', views.SignUp.as_view(), name="sign_up"),

    path('books/', views.getBooks.as_view(),name="books"),
    path('loaned_books/', views.getLoanedBooks.as_view(),name="loaned_books"),
    path('add_book/', views.AddBook.as_view(),name="add_book"),
    path('delete_book/', views.DeleteBook.as_view(),name="delete_book"),

    path('loan_book/', views.loanBooks.as_view(),name="loan_book"),
    path('return_book/', views.returnBooks.as_view(),name="return_book"),
    path('fines/', views.getFines.as_view(),name="fines")
    
]
