from django.urls import path
from WebsiteCHGR.views import userViews, adminViews

urlpatterns = [
    path('trangchu/', userViews.Home, name='Home'),
    path('thucdon/', userViews.Menu, name='Menu'),
    path('dangnhap/', userViews.Login, name='Login'),
    path('thoat/', userViews.Logout, name='Logout'),
    path('dangky/', userViews.Registration, name='Registration'),
    path('thongtin/', userViews.Profile, name='Profile'),
    path('thongtin/capnhatthongtin/<str:id>', userViews.EditProfile, name='EditProfile'),
    path('thongtin/lichsu/', userViews.HistoryView, name='History'),
    path('chitietsanpham/<str:type>/<str:id>', userViews.ProductDetail, name='ProductDetail'),
    path('giohang/', userViews.Shoppingcart, name='Shoppingcart'),
    path('thanhtoanOnline/', userViews.paymentOnline, name='PaymentOnline'),
    path('thanhtoanCash/', userViews.paymentCash, name='PaymentCash'),
    path('payment_return/', userViews.payment_return, name='payment_return'),
    path('themvaogiohang/<str:type>/<str:id>/', userViews.ThemGioHang, name='ThemGioHang'),
    path('capnhatgiohang/<str:id>', userViews.CapNhatGioHang, name='CapNhatGioHang'),
]