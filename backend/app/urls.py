from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet, ENNEAGRAMViewSet, VideoViewSet,
    MMPI2QuestionnaireViewSet, UploadVideoView, UserQuestionnaireCreateView,
    get_matched_professionals, BFTQuestionnaireCreateView, NPQViewSet,
    ADHDViewSet, BDIViewSet, GADViewSet, MDQViewSet, OCIRViewSet,
    IBTViewSet, QuestionnaireReportPDFView,
    GADQuestionnaireStatsView, OCIRQuestionnaireStatsView, ADHDQuestionnaireStatsView, EnneagramQuestionnaireStatsView, 
    BDIQuestionnaireStatsView, 
)
router = DefaultRouter()
# router.register(r'users', UserProfileViewSet)
# router.register(r'videos', VideoViewSet)  

urlpatterns = [
    path('', include(router.urls)),
    path('api/upload-video/', UploadVideoView.as_view(), name='upload-video'),
    path('api/questionnaire/', UserQuestionnaireCreateView.as_view(), name='questionnaire-create'),
    path('api/matched-professionals/', get_matched_professionals, name='matched_professionals'),

    
    path('api/mmpi2/', MMPI2QuestionnaireViewSet.as_view({'get': 'list', 'post': 'create'}), name='mmpi2-questionnaire'),
    path('api/mmpi2/<int:pk>/', MMPI2QuestionnaireViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='mmpi2-questionnaire-detail'),

    
    path('api/bft-questionnaire/', BFTQuestionnaireCreateView.as_view(), name='bft-questionnaire-create'),
     path('api/enneagram/', ENNEAGRAMViewSet.as_view({'get': 'list', 'post': 'create'}), name='enneagram-list'),
    path('api/enneagram/<int:pk>/', ENNEAGRAMViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='enneagram-detail'),
 
    path('api/npq/', NPQViewSet.as_view({'get': 'list', 'post': 'create'}), name='npq-list'),
    path('api/npq/<int:pk>/', NPQViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='npq-detail'),

    
    path('api/adhd/', ADHDViewSet.as_view({'get': 'list', 'post': 'create'}), name='adhd-list'),
    path('api/adhd/<int:pk>/', ADHDViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='adhd-detail'),

    
    path('api/bdi/', BDIViewSet.as_view({'get': 'list', 'post': 'create'}), name='bdi-list'),
    path('api/bdi/<int:pk>/', BDIViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='bdi-detail'),

    
    path('api/gad/', GADViewSet.as_view({'get': 'list', 'post': 'create'}), name='gad-list'),
    path('api/gad/<int:pk>/', GADViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='gad-detail'),

    
    path('api/mdq/', MDQViewSet.as_view({'get': 'list', 'post': 'create'}), name='mdq-list'),
    path('api/mdq/<int:pk>/', MDQViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='mdq-detail'),

    
    path('api/ocir/', OCIRViewSet.as_view({'get': 'list', 'post': 'create'}), name='ocir-list'),
    path('api/ocir/<int:pk>/', OCIRViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='ocir-detail'),

    
    path('api/ibt/', IBTViewSet.as_view({'get': 'list', 'post': 'create'}), name='ibt-list'),
    path('api/ibt/<int:pk>/', IBTViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='ibt-detail'),

    
    # path('api/mmpi2-questionnaire/stats/', MMPI2QuestionnaireStatsView.as_view(), name='mmpi2-questionnaire-stats'),

    path('api/gad-questionnaire/stats/', GADQuestionnaireStatsView.as_view(), name='gad_questionnaire_stats'),
    path('api/adhd-questionnaire/stats/', ADHDQuestionnaireStatsView.as_view(), name='adhd_questionnaire_stats'),
    path('api/bdi-questionnaire/stats/', BDIQuestionnaireStatsView.as_view(), name='bdi_questionnaire_stats'),
    path('api/ocir-questionnaire/stats/', OCIRQuestionnaireStatsView.as_view(), name='ocir_questionnaire_stats'),
    path('api/enneagram-questionnaire/stats/', EnneagramQuestionnaireStatsView.as_view(), name='enneagram_questionnaire_stats'),
    
    
    path('api/questionnaire/report/<str:user_id>/<str:questionnaire_type>/', QuestionnaireReportPDFView.as_view(), name='questionnaire-report'),

]
