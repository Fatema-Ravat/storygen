from rest_framework.routers import DefaultRouter
from .views import WorksheetGeneratorView

router = DefaultRouter()
router.register('worksheet',WorksheetGeneratorView,basename='worksheet')

urlpatterns= router.urls