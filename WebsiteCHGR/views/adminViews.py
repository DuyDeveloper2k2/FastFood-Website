import base64
from datetime import datetime
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages

from WebsiteCHGR.decorators import login_required
from WebsiteCHGR.models import Bophan, Chitietcombo, Chitietkhuyenmai, Chitietphanan, Chitietphieunhap, Chitiettinhtrang, Chucvu, Combo, Khuyenmai, Kichco, Loaicombo, Loaimonan, Monan, Nguyenlieu, Nhacungcap, Nhanvien, Phieunhap, Taikhoan, Tinhtrang

#------------------------------------------------------------------------------------------------------------------------
def generate_maloai():
    last_loaimonan = Loaimonan.objects.order_by('maloai').last()
    if not last_loaimonan:
        return 'LM001'
    maloai = last_loaimonan.maloai
    maloai_int = int(maloai.split('LM')[-1])
    new_maloai_int = maloai_int + 1
    new_maloai = 'LM' + str(new_maloai_int).zfill(3)
    return new_maloai

def generate_mamonan():
    last_monan = Monan.objects.order_by('mamonan').last()
    if not last_monan:
        return 'MA001'
    mamonan = last_monan.mamonan
    mamonan_int = int(mamonan.split('MA')[-1])
    new_mamonan_int = mamonan_int + 1
    new_mamonan = 'MA' + str(new_mamonan_int).zfill(3)
    return new_mamonan

def generate_machitietphanan():
    last_chitietphanan = Chitietphanan.objects.order_by('machitietphanan').last()
    if not last_chitietphanan:
        return 'CTPA001'
    machitietphanan = last_chitietphanan.machitietphanan
    machitietphanan_int = int(machitietphanan.split('CTPA')[-1])
    new_machitietphanan_int = machitietphanan_int + 1
    new_machitietphanan = 'CTPA' + str(new_machitietphanan_int).zfill(3)
    return new_machitietphanan

def generate_maloaicombo():
    last_loaicombo = Loaicombo.objects.order_by('maloaicombo').last()
    if not last_loaicombo:
        return 'LCB001'
    maloaicombo = last_loaicombo.maloaicombo
    maloaicombo_int = int(maloaicombo.split('LCB')[-1])
    new_maloaicombo_int = maloaicombo_int + 1
    new_maloaicombo = 'LCB' + str(new_maloaicombo_int).zfill(3)
    return new_maloaicombo

def generate_macombo():
    last_combo = Combo.objects.order_by('macombo').last()
    if not last_combo:
        return 'CB001'
    macombo = last_combo.macombo
    macombo_int = int(macombo.split('CB')[-1])
    new_macombo_int = macombo_int + 1
    new_macombo = 'CB' + str(new_macombo_int).zfill(3)
    return new_macombo

def generate_machitietcombo():
    last_chitietcombo = Chitietcombo.objects.order_by('machitietcombo').last()
    if not last_chitietcombo:
        return 'CTCB001'
    machitietcombo = last_chitietcombo.machitietcombo
    machitietcombo_int = int(machitietcombo.split('CTCB')[-1])
    new_machitietcombo_int = machitietcombo_int + 1
    new_machitietcombo = 'CTCB' + str(new_machitietcombo_int).zfill(3)
    return new_machitietcombo

def generate_maphieunhap():
    last_phieunhap = Phieunhap.objects.order_by('maphieunhap').last()
    if not last_phieunhap:
        return 'PN0001'
    maphieunhap = last_phieunhap.maphieunhap
    maphieunhap_int = int(maphieunhap.split('PN')[-1])
    new_maphieunhap_int = maphieunhap_int + 1
    new_maphieunhap = 'PN' + str(new_maphieunhap_int).zfill(4)
    return new_maphieunhap

def generate_machitietphieunhap():
    last_chitietphieunhap = Chitietphieunhap.objects.order_by('machitietphieunhap').last()
    if not last_chitietphieunhap:
        return 'CTPN0001'
    machitietphieunhap = last_chitietphieunhap.machitietphieunhap
    machitietphieunhap_int = int(machitietphieunhap.split('CTPN')[-1])
    new_machitietphieunhap_int = machitietphieunhap_int + 1
    new_machitietphieunhap = 'CTPN' + str(new_machitietphieunhap_int).zfill(4)
    return new_machitietphieunhap

def generate_makhuyenmai():
    last_makhuyenmai = Khuyenmai.objects.order_by('makhuyenmai').last()
    if not last_makhuyenmai:
        return 'KM001'
    makhuyenmai = last_makhuyenmai.makhuyenmai
    makhuyenmai_int = int(makhuyenmai.split('KM')[-1])
    new_makhuyenmai_int = makhuyenmai_int + 1
    new_makhuyenmai = 'KM' + str(new_makhuyenmai_int).zfill(3)
    return new_makhuyenmai

def generate_machitietkhuyenmai():
    last_machitietkhuyenmai = Chitietkhuyenmai.objects.order_by('machitietkhuyenmai').last()
    if not last_machitietkhuyenmai:
        return 'CTKM001'
    machitietkhuyenmai = last_machitietkhuyenmai.machitietkhuyenmai
    machitietkhuyenmai_int = int(machitietkhuyenmai.split('CTKM')[-1])
    new_machitietkhuyenmai_int = machitietkhuyenmai_int + 1
    new_machitietkhuyenmai = 'CTKM' + str(new_machitietkhuyenmai_int).zfill(3)
    return new_machitietkhuyenmai

#------------------------------------------------------------------------------------------------------------------------
def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Taikhoan.objects.get(tendangnhap=username, matkhau=password)
            nhanvien = Nhanvien.objects.get(manhanvien = user.manhanvien)
            # Save user id in session
            request.session['user_id'] = user.manhanvien_id
            request.session['user_name'] = nhanvien.hoten
            return redirect('Admin')
        except Taikhoan.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
    
    
    return render(request, 'Quanly/admin-login.html')

def adminLogout(request):
    # Clear session data
    request.session.clear()
    
    # Redirect to admin login page
    return redirect('AdminLogin')

@login_required
def adminIndex(request):
    Nhanviens = Nhanvien.objects.all()
    MonanTotal = Monan.objects.count()
    ComboTotal = Combo.objects.count()
    KhuyenmaiTotal = Khuyenmai.objects.count()
    NhanvienInfo = []

    for nhanvien in Nhanviens:
        try:
            chucvu = get_object_or_404(Chucvu, machucvu = nhanvien.machucvu)
            bophan = get_object_or_404(Bophan, mabophan = nhanvien.mabophan)

            NhanvienInfo.append({
                'tennhanvien': nhanvien.hoten,
                'ngaysinh': nhanvien.ngaysinh,
                'gioitinh': nhanvien.gioitinh,
                'sdt': nhanvien.sodienthoai,
                'email': nhanvien.email,
                'diachi': nhanvien.diachi,
                'chucvu': chucvu.tenchucvu,
                'bophan': bophan.tenbophan
            })
        except Http404:
            NhanvienInfo.append({
                'tennhanvien': nhanvien.hoten,
                'ngaysinh': nhanvien.ngaysinh,
                'gioitinh': nhanvien.gioitinh,
                'sdt': nhanvien.sodienthoai,
                'email': nhanvien.email,
                'diachi': nhanvien.diachi,
                'chucvu': None,
                'bophan': None
            })


    return render(request, 'QuanLy/admin.html', {'Nhanviens': NhanvienInfo, 'MonanTotal': MonanTotal, 'ComboTotal': ComboTotal, 'KhuyenmaiTotal': KhuyenmaiTotal})

@login_required
def adminLoaimonan(request):
    if request.method == 'POST':
        maloai = generate_maloai()
        tenloai = request.POST.get('tenloaimonan')

        if tenloai:
            # Create a new Loaimonan instance
            new_loaimonan = Loaimonan.objects.create(
                maloai=maloai,
                tenloai=tenloai
            )

            return JsonResponse({'success': True, 'maloai': maloai, 'tenloai': tenloai})
        else:
            return JsonResponse({'success': False, 'error': 'Tên loại món ăn không được bỏ trống.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def adminMonan(request):
    DetailInfo = []
    Loaimons = Loaimonan.objects.all()
    Kichcos = Kichco.objects.all()

    loaimon_selected = request.GET.get('loaimon', '')
    if loaimon_selected:
        Monans = Monan.objects.filter(maloai__maloai=loaimon_selected)
        for monan in Monans:
            try:
                loaimonan = get_object_or_404(Loaimonan, maloai = monan.maloai)
                DetailInfo.append({
                    'id': monan.mamonan,
                    'anhmonan': base64.b64encode(monan.anhmonan).decode('utf-8'),
                    'loaimon': loaimonan.tenloai,
                    'tenmonan': monan.tenmonan,
                    'mota': monan.mota,
                    'gia': monan.giamon,
                })
            except Http404:
                DetailInfo.append({
                    'id': monan.mamonan,
                    'anhmonan': base64.b64encode(monan.anhmonan).decode('utf-8'),
                    'loaimon': None,
                    'tenmonan': monan.tenmonan,
                    'mota': monan.mota,
                    'gia': monan.giamon,
                })
    else:
        Monans = Monan.objects.all()
        for monan in Monans:
            try:
                loaimonan = get_object_or_404(Loaimonan, maloai = monan.maloai)
                DetailInfo.append({
                    'id': monan.mamonan,
                    'anhmonan': base64.b64encode(monan.anhmonan).decode('utf-8'),
                    'loaimon': loaimonan.tenloai,
                    'tenmonan': monan.tenmonan,
                    'mota': monan.mota,
                    'gia': monan.giamon,
                })
            except Http404:
                DetailInfo.append({
                    'id': monan.mamonan,
                    'anhmonan': base64.b64encode(monan.anhmonan).decode('utf-8'),
                    'loaimon': None,
                    'tenmonan': monan.tenmonan,
                    'mota': monan.mota,
                    'gia': monan.giamon,
                })

    if request.method == 'POST':
        mamonan = generate_mamonan()
        tenmonan = request.POST.get('tenmonan')
        mota = request.POST.get('mota')
        maloai = request.POST.get('maloai')
        MonanImage = request.FILES.get('MonanImage')

        # Create a new Monan instance
        new_monan = Monan.objects.create(
            mamonan=mamonan,
            tenmonan=tenmonan,
            mota=mota,
            maloai_id=maloai,
            giamon=None,
            anhmonan=MonanImage.read() if MonanImage else None
        )

        # Process the selected sizes and their prices
        kichco_list = []
        for key in request.POST:
            if key.startswith('kichco_price_'):
                makichco = key.split('_')[-1]
                giaban = request.POST[key]
                if giaban:
                    kichco_list.append((makichco, int(giaban)))

        # Create Chitietphanan instances
        chitietphanan_instances = []
        for makichco, giaban in kichco_list:
            kichco_instance = Kichco.objects.get(pk=makichco)
            chitietphanan = Chitietphanan.objects.create(
                machitietphanan=generate_machitietphanan(),
                mamonan=new_monan,
                makichco=kichco_instance,
                giaban=giaban
            )
            chitietphanan_instances.append(chitietphanan)

        # Update Monan.giamon with the first chitietphanan giaban
        if chitietphanan_instances:
            new_monan.giamon = chitietphanan_instances[0].giaban
            new_monan.save()

        messages.success(request, 'Thêm thành công')
        return redirect('AdminMonan')

    return render(request, 'QuanLy/admin-monan.html', {'Monans': DetailInfo, 'Loaimons': Loaimons, 'Kichcos': Kichcos, 'loaimon_selected': loaimon_selected})

def adminDeleteMonan(request, id):
    monan = get_object_or_404(Monan, pk=id)
    chitietphanan = Chitietphanan.objects.filter(mamonan = monan)
    chitietphanan.delete()
    monan.delete()
    messages.success(request, 'Xóa thành công')
    return redirect('AdminMonan')

@login_required
def adminLoaicombo(request):
    if request.method == 'POST':
        tenloaicombo = request.POST.get('tenloaicombo')
        if tenloaicombo:
            # Generate maloaicombo using helper function
            maloaicombo = generate_maloaicombo()

            # Create a new Loaicombo instance
            loaicombo = Loaicombo(maloaicombo=maloaicombo, tenloaicombo=tenloaicombo)
            loaicombo.save()  # Save the instance to the database

            # Retrieve updated list of Loaicombos
            loaicombos = Loaicombo.objects.all()

            # Prepare data to send back as JSON response
            loaicombos_data = [{'maloaicombo': lc.maloaicombo, 'tenloaicombo': lc.tenloaicombo} for lc in loaicombos]

            # Return JSON response with success message and updated list of loaicombos
            return JsonResponse({'success': 'Loai combo created successfully', 'loaicombos': loaicombos_data})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def adminCombo(request):
    DetailInfo = []
    Loaicombos = Loaicombo.objects.all()
    ListCTPA = Chitietphanan.objects.all()
    Chitietphanans = []
    for chitietphanan in ListCTPA:
        MonanInfo = get_object_or_404(Monan, mamonan = chitietphanan.mamonan)
        KichcoInfo = get_object_or_404(Kichco, makichco = chitietphanan.makichco)
        Chitietphanans.append({
            "mactpa": chitietphanan.machitietphanan,
            "tenmonan": MonanInfo.tenmonan,
            "kichco": KichcoInfo.tenkichco,
            "giaban": chitietphanan.giaban,
        })  

    loaicombo_selected = request.GET.get('loaicombo', '')
    if loaicombo_selected:
        Combos = Combo.objects.filter(maloaicombo__maloaicombo=loaicombo_selected)
        for combo in Combos:
            try:
                loaicombo = get_object_or_404(Loaicombo, maloaicombo = combo.maloaicombo)
                DetailInfo.append({
                    'id': combo.macombo,
                    'anhcombo': base64.b64encode(combo.anhcombo).decode('utf-8'),
                    'loaicombo': loaicombo.tenloaicombo,
                    'tencombo': combo.tencombo,
                    'mota': combo.mota,
                    'gia': combo.giacombo,
                })
            except Http404:
                DetailInfo.append({
                    'id': combo.macombo,                    
                    'anhcombo': base64.b64encode(combo.anhcombo).decode('utf-8'),
                    'loaicombo': None,
                    'tencombo': combo.tencombo,
                    'mota': combo.mota,
                    'gia': combo.giacombo,
                })
    else:
        Combos = Combo.objects.all()
        for combo in Combos:
            try:
                loaicombo = get_object_or_404(Loaicombo, maloaicombo = combo.maloaicombo)
                DetailInfo.append({
                    'id': combo.macombo,
                    'anhcombo': base64.b64encode(combo.anhcombo).decode('utf-8'),
                    'loaicombo': loaicombo.tenloaicombo,
                    'tencombo': combo.tencombo,
                    'mota': combo.mota,
                    'gia': combo.giacombo,
                })
            except Http404:
                DetailInfo.append({
                    'id': combo.macombo,
                    'anhcombo': base64.b64encode(combo.anhcombo).decode('utf-8'),
                    'loaicombo': None,
                    'tencombo': combo.tencombo,
                    'mota': combo.mota,
                    'gia': combo.giacombo,
                })

    if request.method == 'POST':
        chitietphanan_ids = request.POST.getlist('chitietphanan[]')
        if len(chitietphanan_ids) >= 2:
            combo_id = generate_macombo()
            tencombo = request.POST.get('tencombo')
            giacombo = request.POST.get('giacombo')
            mota = request.POST.get('mota')
            maloaicombo = request.POST.get('maloaicombo')
            anhcombo = request.FILES.get('ComboImage')

            # Create the Combo object
            combo = Combo.objects.create(
                macombo=combo_id,
                tencombo=tencombo,
                giacombo=giacombo,
                mota=mota,
                maloaicombo_id=maloaicombo,
                anhcombo = anhcombo.read() if anhcombo else None,
            )

            print(chitietphanan_ids)
            # Save the selected food items for the combo
            for chitietphanan_id in chitietphanan_ids:
                quantity = request.POST.get(f'{chitietphanan_id}_SL')
                chitietphanan = Chitietphanan.objects.get(machitietphanan=chitietphanan_id)
                machitietcombo = generate_machitietcombo()

                # Create Chitietcombo object linking Combo with Chitietphanan
                Chitietcombo.objects.create(
                    machitietcombo = machitietcombo,
                    macombo=combo,
                    machitietphanan=chitietphanan,
                    soluong=quantity
                )

            messages.success(request, 'Thêm combo thành công')
            return redirect('AdminCombo')
        else:
            messages.error(request, 'Không thể tạo combo dưới 2 món ăn')
            return redirect('AdminCombo')
    

    return render(request, 'QuanLy/admin-combo.html', {'Combos': DetailInfo, 'Loaicombos': Loaicombos, 'loaicombo_selected': loaicombo_selected, 'Chitietphanans': Chitietphanans})

def adminDeleteCombo(request, id):
    combo = get_object_or_404(Combo, pk=id)
    chitietcombo = Chitietcombo.objects.filter(macombo = combo)
    chitietcombo.delete()
    combo.delete()
    messages.success(request, 'Xóa thành công')
    return redirect('AdminCombo')

@login_required
def adminTinhtrang(request):
    Chitiettinhtrangs = []
    tinhtrangs = Tinhtrang.objects.all()

    tinhtrang_selected = request.GET.get('tinhtrang', '')
    if tinhtrang_selected:
        listCTTT = Chitiettinhtrang.objects.filter(matinhtrang__matinhtrang=tinhtrang_selected)
    else:
        listCTTT = Chitiettinhtrang.objects.all()

    for CTTT in listCTTT:
        tinhtrang = Tinhtrang.objects.get(matinhtrang = CTTT.matinhtrang)
        if CTTT.manhanvien:
            nhanvien = Nhanvien.objects.get(manhanvien = CTTT.manhanvien)
            Chitiettinhtrangs.append({
                'mahoadon': CTTT.mahoadon,
                'tinhtrang': tinhtrang.tentinhtrang,
                'nhanvien': nhanvien.hoten,
                'thoigianxacnhan': CTTT.thoigianxacnhan,
                'thoigianthanhtoan': CTTT.thoigianthanhtoan,
                'thoigiannhanhang': CTTT.thoigiannhanhang
            })
        else:
            Chitiettinhtrangs.append({
                'mahoadon': CTTT.mahoadon,
                'tinhtrang': tinhtrang.tentinhtrang,
                'nhanvien': None,
                'thoigianxacnhan': CTTT.thoigianxacnhan,
                'thoigianthanhtoan': CTTT.thoigianthanhtoan,
                'thoigiannhanhang': CTTT.thoigiannhanhang
            })

    if request.method == 'POST':
        manhanvien = request.session['user_id']
        nhanvien = Nhanvien.objects.get(manhanvien = manhanvien)
        mahoadon = request.POST.get('mahoadon')
        matinhtrang = request.POST.get('tinhtrang')
        tinhtrang = Tinhtrang.objects.get(matinhtrang = matinhtrang)
        tgxacnhan = request.POST.get('tgxacnhan')
        tgthanhtoan = request.POST.get('tgthanhtoan')
        tgnhanhang = request.POST.get('tgnhanhang')


        # Retrieve the Chitiettinhtrang object to update
        chitiet = Chitiettinhtrang.objects.get(mahoadon=mahoadon)

        # Update the fields
        chitiet.manhanvien = nhanvien
        chitiet.matinhtrang = tinhtrang
        chitiet.thoigianxacnhan = tgxacnhan if tgxacnhan else None
        chitiet.thoigianthanhtoan = tgthanhtoan if tgthanhtoan else None
        chitiet.thoigiannhanhang = tgnhanhang if tgnhanhang else None

        # Save the updated object
        chitiet.save()        
        messages.success(request, 'Cập nhật tình trạng thành công')
        return redirect('AdminTinhtrang')
    return render(request, 'QuanLy/admin-tinhtrang.html', {'Tinhtrangs': tinhtrangs, 'tinhtrang_selected': tinhtrang_selected, 'Chitiettinhtrangs': Chitiettinhtrangs})

@login_required
def adminNguyenlieu(request):
    DetailInfo = []
    maphieunhap = generate_maphieunhap()
    nguyenlieus = Nguyenlieu.objects.all()
    nhanvien = Nhanvien.objects.get(manhanvien = request.session['user_id'])

    for nguyenlieu in nguyenlieus:
        nhacungcap = Nhacungcap.objects.get(manhacungcap = nguyenlieu.manhacungcap)
        DetailInfo.append({
            'manguyenlieu': nguyenlieu.manguyenlieu,
            'tennguyenlieu': nguyenlieu.tennguyenlieu,
            'soluongtonkho': nguyenlieu.soluongtonkho,
            'donvi': nguyenlieu.donvi,
            'nhacungcap': nhacungcap.tennhacungcap
        })

    history = []
    phieunhaps = Phieunhap.objects.all()
    for phieunhap in phieunhaps:
        info = []
        nhanvien = Nhanvien.objects.get(manhanvien = phieunhap.manhanvien)
        chitietphieunhaps = Chitietphieunhap.objects.filter(maphieunhap = phieunhap.maphieunhap)
        for chitietphieunhap in chitietphieunhaps:
            nguyenlieu = Nguyenlieu.objects.get(manguyenlieu = chitietphieunhap.manguyenlieu)
            info.append({
                'tennguyenlieu': nguyenlieu.tennguyenlieu,
                'donvi': nguyenlieu.donvi,
                'soluong': chitietphieunhap.soluong,
                'gianhap': chitietphieunhap.gianhap
            })
        history.append({
            'maphieunhap': phieunhap.maphieunhap,
            'thongtin': info,
            'ngaynhap': phieunhap.ngaynhap,
            'nhanvien': nhanvien.hoten
        })

    if request.method == 'POST':
        nguyenlieu_ids = request.POST.getlist('nguyenlieu[]')
        if len(nguyenlieu_ids) >= 1:
            # Create phieu nhap
            phieunhap = Phieunhap.objects.create(
                maphieunhap=maphieunhap,
                manhanvien=nhanvien,
                ngaynhap=datetime.today().date(),
            )

            for nguyenlieu_id in nguyenlieu_ids:
                quantity = float(request.POST.get(f'{nguyenlieu_id}_SL'))
                giaban = float(request.POST.get(f'{nguyenlieu_id}_Giaban'))
                nguyenlieu = Nguyenlieu.objects.get(manguyenlieu=nguyenlieu_id)

                Chitietphieunhap.objects.create(
                    machitietphieunhap = generate_machitietphieunhap(),
                    maphieunhap=phieunhap,
                    manguyenlieu=nguyenlieu,
                    soluong=quantity,
                    gianhap=giaban,
                )

                nguyenlieu.soluongtonkho = nguyenlieu.soluongtonkho + quantity
                nguyenlieu.save()
        else:
            messages.error(request, 'Không thể tạo phiếu nhập dưới 1 nguyên liệu')
            return redirect('AdminNguyenlieu')
        
        messages.success(request, 'Tạo phiếu nhập thành công')
        return redirect('AdminNguyenlieu')


    return render(request, 'Quanly/admin-nguyenlieu.html', {'Nguyenlieus': DetailInfo, 'Lichsus': history, 'Maphieunhap': maphieunhap, 'Nhanvien': nhanvien.hoten})

@login_required
def adminKhuyenmai(request):
    DetailInfo = []
    khuyenmais = Khuyenmai.objects.all()
    loai_khuyenmai = request.GET.get('loaikhuyenmai', '')

    for khuyenmai in khuyenmais:
        chitietkhuyenmai_list = Chitietkhuyenmai.objects.filter(makhuyenmai=khuyenmai.makhuyenmai)

        for chitietkhuyenmai in chitietkhuyenmai_list:
            if loai_khuyenmai == 'monan' and chitietkhuyenmai.machitietphanan:
                chitietphanan = Chitietphanan.objects.get(machitietphanan=chitietkhuyenmai.machitietphanan)
                monan = Monan.objects.get(mamonan=chitietphanan.mamonan)
                DetailInfo.append({
                    'id': khuyenmai.makhuyenmai,
                    'tenkhuyenmai': khuyenmai.tenkhuyenmai,
                    'mota': chitietkhuyenmai.mota,
                    'sanpham': monan.tenmonan,
                    'phantram': chitietkhuyenmai.phantramkhuyenmai,
                    'ngaytao': khuyenmai.ngaytao,
                    'ngaybd': khuyenmai.ngaybatdau,
                    'ngaykt': khuyenmai.ngayketthuc,
                })
            elif loai_khuyenmai == 'combo' and chitietkhuyenmai.macombo:
                combo = Combo.objects.get(macombo=chitietkhuyenmai.macombo)
                DetailInfo.append({
                    'id': khuyenmai.makhuyenmai,
                    'tenkhuyenmai': khuyenmai.tenkhuyenmai,
                    'mota': chitietkhuyenmai.mota,
                    'sanpham': combo.tencombo,
                    'phantram': chitietkhuyenmai.phantramkhuyenmai,
                    'ngaytao': khuyenmai.ngaytao,
                    'ngaybd': khuyenmai.ngaybatdau,
                    'ngaykt': khuyenmai.ngayketthuc,
                })
            elif loai_khuyenmai == '':
                if chitietkhuyenmai.machitietphanan:
                    chitietphanan = Chitietphanan.objects.get(machitietphanan=chitietkhuyenmai.machitietphanan)
                    monan = Monan.objects.get(mamonan=chitietphanan.mamonan)
                    DetailInfo.append({
                        'id': khuyenmai.makhuyenmai,
                        'tenkhuyenmai': khuyenmai.tenkhuyenmai,
                        'mota': chitietkhuyenmai.mota,
                        'sanpham': monan.tenmonan,
                        'phantram': chitietkhuyenmai.phantramkhuyenmai,
                        'ngaytao': khuyenmai.ngaytao,
                        'ngaybd': khuyenmai.ngaybatdau,
                        'ngaykt': khuyenmai.ngayketthuc,
                    })
                elif chitietkhuyenmai.macombo:
                    combo = Combo.objects.get(macombo=chitietkhuyenmai.macombo)
                    DetailInfo.append({
                        'id': khuyenmai.makhuyenmai,
                        'tenkhuyenmai': khuyenmai.tenkhuyenmai,
                        'mota': chitietkhuyenmai.mota,
                        'sanpham': combo.tencombo,
                        'phantram': chitietkhuyenmai.phantramkhuyenmai,
                        'ngaytao': khuyenmai.ngaytao,
                        'ngaybd': khuyenmai.ngaybatdau,
                        'ngaykt': khuyenmai.ngayketthuc,
                    })

    
    Chitietphanans = []
    Combos = []
    ListCTPA = Chitietphanan.objects.all()
    combos = Combo.objects.all()
    for combo in combos:
        check_exists = Chitietkhuyenmai.objects.filter(macombo = combo.macombo)
        if not check_exists:
            Combos.append(combo)
            
    for chitietphanan in ListCTPA:
        check_exists = Chitietkhuyenmai.objects.filter(machitietphanan = chitietphanan.machitietphanan)
        if not check_exists:
            MonanInfo = get_object_or_404(Monan, mamonan = chitietphanan.mamonan)
            KichcoInfo = get_object_or_404(Kichco, makichco = chitietphanan.makichco)
            Chitietphanans.append({
                "mactpa": chitietphanan.machitietphanan,
                "tenmonan": MonanInfo.tenmonan,
                "kichco": KichcoInfo.tenkichco,
            })

    makhuyenmai = generate_makhuyenmai()
    if request.method == 'POST':
        selected_items = request.POST.getlist('chitietphanan[]')
        if len(selected_items) >= 1:
            ten = request.POST.get('tenkhuyenmai')
            ngaybd = request.POST.get('ngaybd')
            ngaykt = request.POST.get('ngaykt')
            mota = request.POST.get('mota')
            phantramkhuyenmai = request.POST.get('phantram')

            new_khuyenmai = Khuyenmai.objects.create(
                makhuyenmai = makhuyenmai,
                tenkhuyenmai = ten,
                ngaytao = datetime.today().date(),
                ngaybatdau = ngaybd,
                ngayketthuc = ngaykt
            )

            monan_ids = [item.split('_')[1] for item in selected_items if item.startswith('monan_')]
            combo_ids = [item.split('_')[1] for item in selected_items if item.startswith('combo_')]

            # Process selected Món ăn and Combo items as needed
            for monan_id in monan_ids:
                new_chitietkhuyenmai = Chitietkhuyenmai.objects.create(
                    machitietkhuyenmai = generate_machitietkhuyenmai(),
                    makhuyenmai = new_khuyenmai,
                    machitietphanan = Chitietphanan.objects.get(machitietphanan = monan_id),
                    macombo = None,
                    phantramkhuyenmai = phantramkhuyenmai,
                    mota = mota,
                )

            for combo_id in combo_ids:
                new_chitietkhuyenmai = Chitietkhuyenmai.objects.create(
                    machitietkhuyenmai = generate_machitietkhuyenmai(),
                    makhuyenmai = new_khuyenmai,
                    machitietphanan = None,
                    macombo = Combo.objects.get(macombo = combo_id),
                    phantramkhuyenmai = phantramkhuyenmai,
                    mota = mota,
                )

        messages.success(request, 'Thêm đợt khuyến mãi thành công')
        return redirect('AdminKhuyenmai')

    return render(request, 'Quanly/admin-khuyenmai.html', {'Khuyenmais': DetailInfo, 'Chitietphanans': Chitietphanans, 'Combos': Combos, 'loai_khuyenmai': loai_khuyenmai, 'makm': makhuyenmai})

def adminDeleteKhuyenmai(request, id):
    khuyenmai = get_object_or_404(Khuyenmai, pk=id)
    chitietkhuyenmai = Chitietkhuyenmai.objects.filter(makhuyenmai = khuyenmai)
    chitietkhuyenmai.delete()
    khuyenmai.delete()
    messages.success(request, 'Xóa thành công')
    return redirect('AdminKhuyenmai')


def adminEditMonan(request):
    messages.warning(request, 'Chức năng hiện đang được cập nhật')
    return redirect('AdminMonan')

def adminEditCombo(request):
    messages.warning(request, 'Chức năng hiện đang được cập nhật')
    return redirect('AdminCombo')

def adminEditKhuyenmai(request):
    messages.warning(request, 'Chức năng hiện đang được cập nhật')
    return redirect('AdminKhuyenmai')