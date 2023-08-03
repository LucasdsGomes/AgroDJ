from django.urls import path
from .views import home, register, edit, update, delete, logout, logging, section, cont, plant, colhen, insum, dist, folga

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('editar/<int:id>', edit, name='editar'),
    path('update/<int:id>', update, name='update'),
    path('delete/<int:id>', delete, name='delete'),
    path('logout/', logout, name='logout'),
    path('logging/', logging, name='logging'),
    path('section/', section, name='section'),
    path('cont/', cont, name='cont'),
    path('plant', plant, name='plant'),
    path('colhen/', colhen, name='colhen'),
    path('insum/', insum, name='insum'),
    path('dist', dist, name='dist'),
    path('folga', folga, name='folga'),
]
