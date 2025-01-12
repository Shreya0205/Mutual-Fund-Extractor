from rest_framework.routers import DefaultRouter
from .views import MutualFundFamilyViewSet

router = DefaultRouter()
router.register('mutual-fund-families', MutualFundFamilyViewSet, basename='mutual-fund-families')

urlpatterns = router.urls
