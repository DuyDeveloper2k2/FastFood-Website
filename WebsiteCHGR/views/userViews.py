import base64
import hashlib
import hmac
import urllib.parse

from datetime import datetime, timezone
from decimal import Decimal
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from CuaHangGaRan import settings
from ..models import Chitietcombo, Chitiethoadon, Chitietkhuyenmai, Chitietphanan, Chitiettinhtrang, Hoadon, Khachhang, Kichco, Loaicombo, Monan, Loaimonan, Combo, Nhanvien, Tinhtrang
from ..forms import EditForm, LoginForm, PaymentForm, RegistrationForm
from ..vnpay import vnpay

#-----------------------------------------------------------------------------------------------------------------------

def generate_mahoadon():
    last_hoadon = Hoadon.objects.order_by('mahoadon').last()
    if not last_hoadon:
        return 'HD001'
    mahoadon = last_hoadon.mahoadon
    mahoadon_int = int(mahoadon.split('HD')[-1])
    new_mahoadon_int = mahoadon_int + 1
    new_mahoadon = 'HD' + str(new_mahoadon_int).zfill(3)
    return new_mahoadon

def generate_machitiethoadon():
    last_cthd = Chitiethoadon.objects.order_by('machitiethoadon').last()
    if not last_cthd:
        return 'CTHD001'
    macthd = last_cthd.machitiethoadon
    macthd_int = int(macthd.split('CTHD')[-1])
    new_macthd_int = macthd_int + 1
    new_macthd = 'CTHD' + str(new_macthd_int).zfill(3)
    return new_macthd

#-----------------------------------------------------------------------------------------------------------------------
# Create your views here.
def Home (request):
    Monans = Monan.objects.all()
    Loaimonans = Loaimonan.objects.all()
    Loaicombos = Loaicombo.objects.all()
    Combos = Combo.objects.all()

    for monan in Monans:
        if monan.anhmonan:
            monan.anhmonan_base64 = base64.b64encode(monan.anhmonan).decode('utf-8')

        List = Chitietphanan.objects.filter(mamonan=monan.mamonan)
        for chitietphanan in List:
            khuyenmai = Chitietkhuyenmai.objects.filter(machitietphanan = chitietphanan.machitietphanan)
            if khuyenmai:
                monan.khuyenmai = True
            else:
                monan.khuyenmai = False

    for combo in Combos:
        if combo.anhcombo:
            combo.anhcombo_base64 = base64.b64encode(combo.anhcombo).decode('utf-8')

        khuyenmai = Chitietkhuyenmai.objects.filter(macombo = combo.macombo)
        if khuyenmai:
            combo.khuyenmai = True
        else:
            combo.khuyenmai = False
                
    return render(request, 'Khachhang/index.html', {'Monans': Monans, 'Loaimonans': Loaimonans, 'Combos': Combos, 'Loaicombos': Loaicombos})

def Menu (request):
    Monans = Monan.objects.all()
    Loaimonans = Loaimonan.objects.all()
    Combos = Combo.objects.all()
    Loaicombos = Loaicombo.objects.all()

    for monan in Monans:
        if monan.anhmonan:
            monan.anhmonan_base64 = base64.b64encode(monan.anhmonan).decode('utf-8')

        List = Chitietphanan.objects.filter(mamonan=monan.mamonan)
        chitietphanan = List.first()
        khuyenmai = Chitietkhuyenmai.objects.filter(machitietphanan = chitietphanan.machitietphanan)
        if khuyenmai:
            monan.khuyenmai = True
        else:
            monan.khuyenmai = False

    for combo in Combos:
        if combo.anhcombo:
            combo.anhcombo_base64 = base64.b64encode(combo.anhcombo).decode('utf-8')

        khuyenmai = Chitietkhuyenmai.objects.filter(macombo = combo.macombo)
        if khuyenmai:
            combo.khuyenmai = True
        else:
            combo.khuyenmai = False
                
    return render(request, 'Khachhang/menu.html', {'Monans': Monans, 'Loaimonans': Loaimonans, 'Combos': Combos, 'Loaicombos': Loaicombos})

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            sdt = form.cleaned_data['sdt']
            mk = form.cleaned_data['mk']
            
            try:
                khachhang = Khachhang.objects.get(sodienthoai=sdt, matkhau=mk)
                request.session['khachhang_id'] = khachhang.makhachhang
                request.session['khachhang_name'] = khachhang.tenkhachhang
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('Home')
            except Khachhang.DoesNotExist:
                messages.error(request, 'Số điện thoại hoặc mật khẩu không chính xác!')
                return redirect('Login')
        else:
            messages.error(request, 'Dữ liệu không hợp lệ')
    
    form = LoginForm()
    return render(request, 'Khachhang/login.html', {'form': form})

def Logout(request):
    if 'khachhang_id' in request.session:
        del request.session['khachhang_id']
    return redirect('Login')

def Profile(request):
    khachhang_id = request.session.get('khachhang_id')
    if not khachhang_id:
        messages.error(request, 'Bạn cần đăng nhập để xem trang này!')
        return redirect('Login')
    
    khachhang = Khachhang.objects.get(makhachhang=khachhang_id)

    return render(request, 'Khachhang/profile.html', {'khachhang': khachhang})

def EditProfile(request, id):
    khachhang = Khachhang.objects.get(makhachhang = id)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=khachhang)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công')
            return redirect('Profile')
    else:
        form = EditForm(instance=khachhang)

    return render(request, 'Khachhang/edit-profile.html', {'form': form, 'khachhang': khachhang})

def Registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['matkhau']
            password_confirm = form.cleaned_data['xacnhanmatkhau']
            if password != password_confirm:
                return HttpResponse('Mật khẩu và xác nhận mật khẩu không khớp.')
            
            last_id = Khachhang.objects.order_by('-makhachhang').first()
            if last_id is not None:
                last_number = int(last_id.makhachhang[2:])  # Extract the number part
                new_number = last_number + 1
                new_id = 'KH{:03d}'.format(new_number)  # Format the new ID
            else:
                new_id = 'KH001'  # If no existing entries
            
            form.instance.makhachhang = new_id

            form.save()
            messages.success(request, 'Đăng ký thành công!')
            return redirect('Login')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin đăng ký')
            return redirect('Registration')
    else:
        form = RegistrationForm()
    return render(request, 'Khachhang/registration.html', {'form': form})

def ProductDetail(request, type, id):
    if type == 'comboType':
        Detail = get_object_or_404(Combo, macombo=id)

        try:
            khuyenmai = get_object_or_404(Chitietkhuyenmai, macombo=id)

            giakhuyenmai = Detail.giacombo - (Detail.giacombo*khuyenmai.phantramkhuyenmai)/100
            if khuyenmai:
                ProductInfo = {'macombo': Detail.macombo,
                            'tencombo': Detail.tencombo,
                            'mota': Detail.mota,
                            'giacombo': Detail.giacombo,
                            'anhcombo': base64.b64encode(Detail.anhcombo).decode('utf-8'),
                            'khuyenmai': khuyenmai.phantramkhuyenmai,
                            'giakhuyenmai': giakhuyenmai}
        except Http404:
                ProductInfo = {'macombo': Detail.macombo,
                            'tencombo': Detail.tencombo,
                            'mota': Detail.mota,
                            'giacombo': Detail.giacombo,
                            'anhcombo': base64.b64encode(Detail.anhcombo).decode('utf-8')}

        
        return render(request, 'Khachhang/product-detail.html', {'Type': type, 'ComboInfo': ProductInfo})
        
    elif type == 'monanType':
        Detail = get_object_or_404(Monan, mamonan=id)
        chitietphananList = Chitietphanan.objects.filter(mamonan=id)
        productDetail = chitietphananList.first()
        if productDetail.makichco:
            KichCoDetail = Kichco.objects.get(makichco = productDetail.makichco)
            try: 
                khuyenmai = get_object_or_404(Chitietkhuyenmai, machitietphanan = productDetail.machitietphanan)
                giakhuyenmai = productDetail.giaban - (productDetail.giaban*khuyenmai.phantramkhuyenmai)/100

                ProductInfo = {'mactpa': productDetail.machitietphanan,
                            'tenmonan': Detail.tenmonan,
                            'mota': Detail.mota,
                            'giaban': productDetail.giaban,
                            'tenkichco': KichCoDetail.tenkichco,
                            'kichco': productDetail.makichco,
                            'anhmonan': base64.b64encode(Detail.anhmonan).decode('utf-8'),
                            'khuyenmai': khuyenmai.phantramkhuyenmai,
                            'giakhuyenmai': giakhuyenmai
                }
            except Http404:
                ProductInfo = {'mactpa': productDetail.machitietphanan,
                            'tenmonan': Detail.tenmonan,
                            'mota': Detail.mota,
                            'giaban': productDetail.giaban,
                            'tenkichco': KichCoDetail.tenkichco,
                            'kichco': productDetail.makichco,
                            'anhmonan': base64.b64encode(Detail.anhmonan).decode('utf-8'),
                }
        else:
            ProductInfo = {'mactpa': productDetail.machitietphanan,
                            'tenmonan': Detail.tenmonan,
                            'mota': Detail.mota,
                            'giaban': productDetail.giaban,
                            'kichco': productDetail.makichco,
                            'anhmonan': base64.b64encode(Detail.anhmonan).decode('utf-8'),
                }

        
        
        kichcoList = list([chitietphanan.makichco for chitietphanan in chitietphananList])
        kichcoInfo = Kichco.objects.filter(makichco__in=kichcoList).values_list('makichco', 'tenkichco')

        if request.method == 'POST':
            selected_kichco = request.POST.get('kichco')
            if selected_kichco:
                selected_entry = chitietphananList.filter(makichco=selected_kichco).first()
                if selected_entry:
                    KichCoDetail = Kichco.objects.get(makichco = selected_entry.makichco)
                    try:
                        khuyenmai = get_object_or_404(Chitietkhuyenmai, machitietphanan = selected_entry.machitietphanan)
                        giakhuyenmai = selected_entry.giaban - (selected_entry.giaban*khuyenmai.phantramkhuyenmai)/100

                        ProductInfo = {'mactpa': selected_entry.machitietphanan,
                                       'tenmonan': Detail.tenmonan,
                                       'mota': Detail.mota,
                                       'giaban': selected_entry.giaban,
                                       'tenkichco': KichCoDetail.tenkichco,
                                       'kichco': selected_entry.makichco,
                                       'anhmonan': base64.b64encode(Detail.anhmonan).decode('utf-8'),
                                       'khuyenmai': khuyenmai.phantramkhuyenmai,
                                       'giakhuyenmai': giakhuyenmai
                        }
                    except Http404:
                        ProductInfo = {'mactpa': selected_entry.machitietphanan,
                                       'tenmonan': Detail.tenmonan,
                                       'mota': Detail.mota,
                                       'giaban': selected_entry.giaban,
                                       'tenkichco': KichCoDetail.tenkichco,
                                       'kichco': selected_entry.makichco,
                                       'anhmonan': base64.b64encode(Detail.anhmonan).decode('utf-8'),
                        }


        return render(request, 'Khachhang/product-detail.html', {'Type': type, 'MonanInfo': ProductInfo, 'KichcoInfo': kichcoInfo})

def HistoryView(request):
    khachhang_id = request.session.get('khachhang_id')
    if not khachhang_id:
        messages.error(request, 'Bạn cần đăng nhập để xem trang này!')
        return redirect('Login')
    
    khachhang = get_object_or_404(Khachhang, makhachhang=khachhang_id)
    Hoadons = Hoadon.objects.filter(makhachhang = khachhang.makhachhang)

    HoadonDetails = []

    for hoadon in Hoadons:
        tong = 0
        all = []
        thongtin = []
        tenMonan = None
        tenCombo = None

        print(hoadon.mahoadon)
        cttt = Chitiettinhtrang.objects.get(mahoadon = hoadon.mahoadon)
        print(cttt.matinhtrang)
        tinhtrang = Tinhtrang.objects.get(matinhtrang = cttt.matinhtrang)

        chitiethoadons = Chitiethoadon.objects.filter(mahoadon = hoadon.mahoadon)
        for chitiethoadon in chitiethoadons:
            tong += int(chitiethoadon.giaban)

            if chitiethoadon.machitietphanan:
                chitietphanan = Chitietphanan.objects.get(machitietphanan = chitiethoadon.machitietphanan)
                monan = Monan.objects.get(mamonan = chitietphanan.mamonan)
                kichco = Kichco.objects.get(makichco = chitietphanan.makichco)
                tenMonan = f'{monan.tenmonan} ({kichco.tenkichco})'

                all.append({
                    'type': 'Monan',
                    'ten': tenMonan,
                })

            else:
                combo = Combo.objects.get(macombo = chitiethoadon.macombo)
                chitietcombos = Chitietcombo.objects.filter(macombo = combo.macombo)
                tenCombo = combo.tencombo

                for chitietcombo in chitietcombos:
                    chitietphanan = Chitietphanan.objects.get(machitietphanan = chitietcombo.machitietphanan)
                    monan = Monan.objects.get(mamonan = chitietphanan.mamonan)
                    kichco = Kichco.objects.get(makichco = chitietphanan.makichco)

                    thongtin.append({
                    'tenmon': monan.tenmonan,
                    'kichco': kichco.tenkichco,
                    'soluong': chitietcombo.soluong,
                })
                    
                all.append({
                    'type': 'Combo',
                    'ten': tenCombo,
                    'thongtin': thongtin
                })

        HoadonDetails.append({
            'mahd': hoadon.mahoadon,
            'ngaylap': hoadon.ngaylaphoadon,
            'all': all,
            'tongtien': tong,
            'trangthai': tinhtrang.tentinhtrang
        })
    return render(request, 'Khachhang/history.html', {'HoadonDetails': HoadonDetails})

def Shoppingcart (request):
    khachhang_id = request.session.get('khachhang_id')
    if khachhang_id:
        khachhang = Khachhang.objects.get(makhachhang = khachhang_id)
    else:
        khachhang = None
    cart = request.session.get('cart', {})

    for item_id, item in cart.items():
        if item['type'] == 'comboType':
            Detail = get_object_or_404(Combo, macombo=item_id)
            chitietcomboList = Chitietcombo.objects.filter(macombo=Detail.macombo)
            DetailInfo = []
            for chitiet in chitietcomboList:
                try:
                    chitietphanan = get_object_or_404(Chitietphanan, machitietphanan = chitiet.machitietphanan)
                    monan = get_object_or_404(Monan, mamonan = chitietphanan.mamonan)
                    kichco = get_object_or_404(Kichco, makichco = chitietphanan.makichco)
                    DetailInfo.append({
                        'tenmonan': monan.tenmonan,
                        'kichco': kichco.tenkichco,
                        'giaban': chitietphanan.giaban,
                        'soluong': chitiet.soluong,
                    })
                except Http404:
                    DetailInfo.append({
                        'tenmonan': monan.tenmonan,
                        'kichco': None,
                        'giaban': chitietphanan.giaban,
                        'soluong': chitiet.soluong,
                    })

            item['image'] = base64.b64encode(Detail.anhcombo).decode('utf-8')
            item['name'] = Detail.tencombo
            item['detail'] = DetailInfo
            if item['price'] != Detail.giacombo:
                try:
                    khuyenmai = get_object_or_404(Chitietkhuyenmai, macombo = Detail.macombo)
                    if item['sale']:
                        item['price'] = Detail.giacombo
                        item['sale'] = khuyenmai.phantramkhuyenmai
                        item['saleprice'] = Detail.giacombo - (Detail.giacombo*khuyenmai.phantramkhuyenmai)/100
                except Http404:
                    item['price'] = Detail.giacombo    
                
        elif item['type'] == 'monanType':
            chitietphanan = get_object_or_404(Chitietphanan, machitietphanan=item_id)
            Detail = get_object_or_404(Monan, mamonan=chitietphanan.mamonan)

            try:
                kichco = get_object_or_404(Kichco, makichco = chitietphanan.makichco)
                item['size'] = kichco.tenkichco
            except Http404:
                item['size'] = None

            if item['price'] != str(chitietphanan.giaban):
                try:
                    khuyenmai = get_object_or_404(Chitietkhuyenmai, machitietphanan = chitietphanan.machitietphanan)
                    if item['sale']:
                        item['price'] = chitietphanan.giaban
                        item['sale'] = khuyenmai.phantramkhuyenmai
                        item['saleprice'] = chitietphanan.giaban - (chitietphanan.giaban*khuyenmai.phantramkhuyenmai)/100
                except Http404:
                    item['price'] = chitietphanan.giaban

    total = 0
    for item_id, item in cart.items():
        if item['type'] == 'comboType':
            if 'saleprice' in item and item['saleprice'] is not None:
                total += Decimal(item['saleprice']) * item['quantity']
            else:
                total += Decimal(item['price']) * item['quantity']
        elif item['type'] == 'monanType':
            if 'saleprice' in item and item['saleprice'] is not None:
                total += Decimal(item['saleprice']) * item['quantity']
            else:
                total += Decimal(item['price']) * item['quantity']
    
    total_quantity = sum(1 for item in cart.values())
    request.session['total_quantity'] = total_quantity

    return render(request, 'Khachhang/shopping-cart.html', {'cart': cart, 'total': total, 'khachhang': khachhang})

def paymentOnline(request):
    cart = request.session.get('cart', {})

    total = 0
    for item_id, item in cart.items():
        if item['type'] == 'comboType':
            if 'saleprice' in item and item['saleprice'] is not None:
                total += Decimal(item['saleprice']) * item['quantity']
            else:
                total += Decimal(item['price']) * item['quantity']
        elif item['type'] == 'monanType':
            if 'saleprice' in item and item['saleprice'] is not None:
                total += Decimal(item['saleprice']) * item['quantity']
            else:
                total += Decimal(item['price']) * item['quantity']

    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            cartTotal = form.cleaned_data['cartTotal']
            bank_code = form.cleaned_data['bank_code']
            ipaddr = get_client_ip(request)
            mahoadon = generate_mahoadon()

            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_CONFIG['vnp_TmnCode']
            vnp.requestData['vnp_Amount'] = cartTotal * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = mahoadon
            vnp.requestData['vnp_OrderInfo'] = 'Thanh toán hóa đơn'
            vnp.requestData['vnp_OrderType'] = 'billpayment'
            vnp.requestData['vnp_Locale'] = 'vn'
            vnp.requestData['vnp_BankCode'] = bank_code
            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_CONFIG['vnp_ReturnUrl']

            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_CONFIG['vnp_Url'], settings.VNPAY_CONFIG['vnp_HashSecret'])

            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
            print(form.errors)
    return render(request, "Khachhang/shopping-cart.html")

def paymentCash(request):
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        khachhang_id = request.session.get('khachhang_id')
        khachhang = Khachhang.objects.get(makhachhang = khachhang_id)
        cart = request.session.get('cart', {})

        new_hoadon = Hoadon.objects.create(
            mahoadon=generate_mahoadon(),  # Assuming the transaction reference is used as mahoadon
            makhachhang=khachhang,  # Assuming the user is logged in and related to Khachhang
            ngaylaphoadon= datetime.now().date()
        )

        new_chitiettinhtrang = Chitiettinhtrang.objects.create(
            mahoadon = new_hoadon,
            manhanvien = None,
            matinhtrang = Tinhtrang.objects.get(matinhtrang = 'TT001'),
            thoigianxacnhan = datetime.now().date(),
            thoigianthanhtoan = datetime.now().date(),
            thoigiannhanhang = datetime.now().date()
        )
        
        for item_id, item in cart.items():
            Chitiethoadon.objects.create(
                machitiethoadon=generate_machitiethoadon(),  # Implement this function to generate unique machitiethoadon
                mahoadon=new_hoadon,
                machitietphanan=Chitietphanan.objects.get(machitietphanan=item_id) if item['type'] == 'monanType' else None,
                macombo= Combo.objects.get(macombo=item_id) if item['type'] == 'comboType' else None,
                soluong=item['quantity'],
                giaban=item['saleprice'] if 'saleprice' in item and item['saleprice'] is not None else item['price']
            )

        del request.session['cart']
    return render(request, 'Khachhang/payment-return.html')

def payment_return(request):
    vnp_HashSecret = settings.VNPAY_CONFIG['vnp_HashSecret']
    
    vnp_Params = request.GET.dict()
    vnp_SecureHash = vnp_Params.pop('vnp_SecureHash', None)
    
    # Verify the hash
    query_string = urllib.parse.urlencode(sorted(vnp_Params.items()))
    hash_data = hmac.new(
        bytes(vnp_HashSecret, 'utf-8'),
        bytes(query_string, 'utf-8'),
        hashlib.sha512
    ).hexdigest()
    
    if hash_data == vnp_SecureHash:
        if 'cart' in request.session:
            khachhang_id = request.session.get('khachhang_id')
            khachhang = Khachhang.objects.get(makhachhang = khachhang_id)
            cart = request.session.get('cart', {})

            new_hoadon = Hoadon.objects.create(
                mahoadon=vnp_Params['vnp_TxnRef'],  # Assuming the transaction reference is used as mahoadon
                makhachhang=khachhang,  # Assuming the user is logged in and related to Khachhang
                ngaylaphoadon= datetime.now().date()
            )

            new_chitiettinhtrang = Chitiettinhtrang.objects.create(
                mahoadon = new_hoadon,
                manhanvien = None,
                matinhtrang = Tinhtrang.objects.get(matinhtrang = 'TT001'),
                thoigianxacnhan = datetime.now().date(),
                thoigianthanhtoan = datetime.now().date(),
                thoigiannhanhang = datetime.now().date()
            )
            
            for item_id, item in cart.items():
                Chitiethoadon.objects.create(
                    machitiethoadon=generate_machitiethoadon(),  # Implement this function to generate unique machitiethoadon
                    mahoadon=new_hoadon,
                    machitietphanan=Chitietphanan.objects.get(machitietphanan=item_id) if item['type'] == 'monanType' else None,
                    macombo= Combo.objects.get(macombo=item_id) if item['type'] == 'comboType' else None,
                    soluong=item['quantity'],
                    giaban=item['saleprice'] if 'saleprice' in item and item['saleprice'] is not None else item['price']
                )

            del request.session['cart']
            del request.session['total_quantity']
        return render(request, 'Khachhang/payment-return.html')
    else:
        # Payment failed
        return render(request, 'Khachhang/payment-return.html')

def ThemGioHang(request, type, id):
    # Initialize the cart if it does not exist
    quantity = int(request.GET.get('quantity', 1))
    cart = request.session.get('cart', {})

    if type == 'comboType':
        Detail = get_object_or_404(Combo, macombo=id)   
        chitietcomboList = Chitietcombo.objects.filter(macombo=id)
        DetailInfo = []
        for chitiet in chitietcomboList:
            try:
                chitietphanan = get_object_or_404(Chitietphanan, machitietphanan = chitiet.machitietphanan)
                monan = get_object_or_404(Monan, mamonan = chitietphanan.mamonan)
                kichco = get_object_or_404(Kichco, makichco = chitietphanan.makichco)

                DetailInfo.append({
                    'tenmonan': monan.tenmonan,
                    'kichco': kichco.tenkichco,
                    'giaban': chitietphanan.giaban,
                })
            except Http404:
                DetailInfo.append({
                    'tenmonan': monan.tenmonan,
                    'kichco': None,
                    'giaban': chitietphanan.giaban,
                })

        if Detail.macombo in cart:
            cart[Detail.macombo]['quantity'] += 1
        else:
            try:
                khuyenmai = get_object_or_404(Chitietkhuyenmai, macombo = Detail.macombo)
                giakhuyenmai = Detail.giacombo - (Detail.giacombo*khuyenmai.phantramkhuyenmai)/100
                
                cart[Detail.macombo] = {
                    'type': 'comboType',
                    'image': base64.b64encode(Detail.anhcombo).decode('utf-8'),
                    'name': Detail.tencombo,
                    'detail': DetailInfo,
                    'sale': khuyenmai.phantramkhuyenmai,
                    'price': str(Detail.giacombo),
                    'saleprice': giakhuyenmai,
                    'quantity': quantity
                }

            except Http404:
                cart[Detail.macombo] = {
                    'type': 'comboType',
                    'image': base64.b64encode(Detail.anhcombo).decode('utf-8'),
                    'name': Detail.tencombo,
                    'detail': DetailInfo,
                    'price': str(Detail.giacombo),
                    'quantity': quantity
                }

    elif type == 'monanType':
        chitietphanan = get_object_or_404(Chitietphanan, machitietphanan=id)
        monan = get_object_or_404(Monan, mamonan = chitietphanan.mamonan)
        
        try:
            kichco = get_object_or_404(Kichco, makichco = chitietphanan.makichco)
            itemSize = kichco.tenkichco
        except Http404:
            itemSize = None

        item_id = chitietphanan.machitietphanan

        if item_id in cart:
            cart[item_id]['quantity'] += 1
        else:
            try:
                khuyenmai = get_object_or_404(Chitietkhuyenmai, machitietphanan = chitietphanan.machitietphanan)
                giakhuyenmai = chitietphanan.giaban - (chitietphanan.giaban*khuyenmai.phantramkhuyenmai)/100
                
                cart[item_id] = {
                    'type': 'monanType',
                    'image': base64.b64encode(monan.anhmonan).decode('utf-8'),
                    'name': monan.tenmonan,
                    'size': itemSize,
                    'sale': khuyenmai.phantramkhuyenmai,
                    'price': chitietphanan.giaban,
                    'saleprice': giakhuyenmai,
                    'quantity': quantity
                }
            except Http404:
                cart[item_id] = {
                    'type': 'monanType',
                    'image': base64.b64encode(monan.anhmonan).decode('utf-8'),
                    'name': monan.tenmonan,
                    'size': itemSize,
                    'price': chitietphanan.giaban,
                    'quantity': quantity
                }

    request.session['cart'] = cart
    return redirect('Shoppingcart')

def CapNhatGioHang(request, id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if action == 'increase':
            cart[id]['quantity'] += 1
        elif action == 'decrease':
            if cart[id]['quantity'] > 1:
                cart[id]['quantity'] -= 1
            else:
                del cart[id]
                request.session.save()
        elif action == 'delete':
            del cart[id]
            request.session.save()

        request.session['cart'] = cart
        return redirect('Shoppingcart')
    else:
        return HttpResponseBadRequest('Invalid request method.')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip