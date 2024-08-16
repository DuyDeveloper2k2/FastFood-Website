from django.urls import path
from WebsiteCHGR.views import adminViews

urlpatterns = [
    path('', adminViews.adminLogin, name='AdminLogin'),
    path('dangxuat/', adminViews.adminLogout, name='AdminLogout'),
    path('trangchu/', adminViews.adminIndex, name='Admin'),
    path('monan/', adminViews.adminMonan, name='AdminMonan'),
    path('monan/themloaimonan/', adminViews.adminLoaimonan, name='AdminLoaiMonan'),
    path('monan/edit/', adminViews.adminEditMonan, name='AdminEditMonan'),
    path('monan/delete/<str:id>/', adminViews.adminDeleteMonan, name='AdminDeleteMonan'),
    path('combo/', adminViews.adminCombo, name='AdminCombo'),
    path('combo/themloaicombo/', adminViews.adminLoaicombo, name='AdminLoaiCombo'),
    path('combo/edit/', adminViews.adminEditCombo, name='AdminEditCombo'),
    path('combo/delete/<str:id>/', adminViews.adminDeleteCombo, name='AdminDeleteCombo'),
    path('tinhtrang/', adminViews.adminTinhtrang, name='AdminTinhtrang'),
    path('nguyenlieu/', adminViews.adminNguyenlieu, name='AdminNguyenlieu'),
    path('khuyenmai/', adminViews.adminKhuyenmai, name='AdminKhuyenmai'),
    path('khuyenmai/edit/', adminViews.adminEditKhuyenmai, name='AdminEditKhuyenmai'),
    path('khuyenmai/delete/<str:id>/', adminViews.adminDeleteKhuyenmai, name='AdminDeleteKhuyenmai'),
]