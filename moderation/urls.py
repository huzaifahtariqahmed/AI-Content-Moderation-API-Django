from ntpath import basename
from rest_framework.routers import DefaultRouter
from .views import ModerationViewSet

router = DefaultRouter()
router.register(
    r"moderations",
    ModerationViewSet, 
    basename="moderation"
)

urlpatterns = router.urls