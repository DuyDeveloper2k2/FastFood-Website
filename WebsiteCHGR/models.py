from django.db import models

# Create your models here.
class Bophan(models.Model):
    mabophan = models.CharField(db_column='MaBoPhan', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenbophan = models.CharField(db_column='TenBoPhan', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mota = models.TextField(db_column='MoTa', db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'BoPhan'

    def __str__(self):
        return self.mabophan

class Chucvu(models.Model):
    machucvu = models.CharField(db_column='MaChucVu', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenchucvu = models.CharField(db_column='TenChucVu', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mota = models.TextField(db_column='MoTa', db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChucVu'

    def __str__(self):
        return self.machucvu
    
class Nhanvien(models.Model):
    manhanvien = models.CharField(db_column='MaNhanVien', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    hoten = models.CharField(db_column='HoTen', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gioitinh = models.CharField(db_column='GioiTinh', max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NgaySinh', blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sodienthoai = models.CharField(db_column='SoDienThoai', max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    machucvu = models.ForeignKey(Chucvu, models.DO_NOTHING, db_column='MaChucVu', blank=True, null=True)  # Field name made lowercase.
    mabophan = models.ForeignKey(Bophan, models.DO_NOTHING, db_column='MaBoPhan', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'NhanVien'

    def __str__(self):
        return self.manhanvien
    
class Taikhoan(models.Model):
    tendangnhap = models.CharField(db_column='TenDangNhap', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    matkhau = models.CharField(db_column='MatKhau', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    manhanvien = models.OneToOneField(Nhanvien, models.DO_NOTHING, db_column='MaNhanVien', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TaiKhoan'

class Kichco(models.Model):
    makichco = models.CharField(db_column='MaKichCo', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenkichco = models.CharField(db_column='TenKichCo', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'KichCo'
        
    def __str__(self):
        return self.makichco

class Loaimonan(models.Model):
    maloai = models.CharField(db_column='MaLoai', primary_key=True, max_length=6, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenloai = models.CharField(db_column='TenLoai', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LoaiMonAn'

    def __str__(self):
        return self.maloai
    
class Monan(models.Model):
    mamonan = models.CharField(db_column='MaMonAn', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenmonan = models.CharField(db_column='TenMonAn', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mota = models.TextField(db_column='MoTa', db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    maloai = models.ForeignKey(Loaimonan, models.DO_NOTHING, db_column='MaLoai')  # Field name made lowercase.
    giamon = models.IntegerField(db_column='GiaMon', blank=True, null=True)  # Field name made lowercase.
    anhmonan = models.BinaryField(db_column='AnhMonAn', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'MonAn'

    def __str__(self):
        return self.mamonan
    
class Chitietphanan(models.Model):
    machitietphanan = models.CharField(db_column='MaChiTietPhanAn', primary_key=True, max_length=7, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    mamonan = models.ForeignKey('Monan', models.DO_NOTHING, db_column='MaMonAn')  # Field name made lowercase.
    makichco = models.ForeignKey('Kichco', models.DO_NOTHING, db_column='MaKichCo')  # Field name made lowercase.
    giaban = models.IntegerField(db_column='GiaBan', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChiTietPhanAn'

    def __str__(self):
        return self.machitietphanan
    
class Loaicombo(models.Model):
    maloaicombo = models.CharField(db_column='MaLoaiComBo', primary_key=True, max_length=6, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenloaicombo = models.CharField(db_column='TenLoaiComBo', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'LoaiComBo'

    def __str__(self):
        return self.maloaicombo
    
class Combo(models.Model):
    macombo = models.CharField(db_column='MaComBo', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tencombo = models.CharField(db_column='TenComBo', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    giacombo = models.IntegerField(db_column='GiaComBo', blank=True, null=True)  # Field name made lowercase.
    mota = models.TextField(db_column='MoTa', db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    maloaicombo = models.ForeignKey('Loaicombo', models.DO_NOTHING, db_column='MaLoaiComBo', blank=True, null=True)  # Field name made lowercase.
    anhcombo = models.BinaryField(db_column='AnhCombo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ComBo'

    def __str__(self):
        return self.macombo    

class Chitietcombo(models.Model):
    machitietcombo = models.CharField(db_column='MaChiTietComBo', primary_key=True, max_length=7, db_collation='Latin1_General_CI_AS')  # Field name made lowercase. The composite primary key (MaChiTietComBo, MaComBo, MaChiTietPhanAn) found, that is not supported. The first column is selected.
    macombo = models.ForeignKey('Combo', models.DO_NOTHING, db_column='MaComBo')  # Field name made lowercase.
    machitietphanan = models.ForeignKey('Chitietphanan', models.DO_NOTHING, db_column='MaChiTietPhanAn')  # Field name made lowercase.
    soluong = models.IntegerField(db_column='SoLuong', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChiTietComBo'
        unique_together = (('machitietcombo', 'macombo', 'machitietphanan'),)

    def __str__(self):
        return self.machitietcombo

class Khachhang(models.Model):
    makhachhang = models.CharField(db_column='MaKhachHang', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenkhachhang = models.CharField(db_column='TenKhachHang', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gioitinh = models.CharField(db_column='GioiTinh', max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NgaySinh', blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sodienthoai = models.CharField(db_column='SoDienThoai', max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cccd = models.CharField(db_column='CCCD', max_length=12, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    matkhau = models.CharField(db_column='MatKhau', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'KhachHang'

    def __str__(self):
        return self.makhachhang

class Hoadon(models.Model):
    mahoadon = models.CharField(db_column='MaHoaDon', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    makhachhang = models.ForeignKey('Khachhang', models.DO_NOTHING, db_column='MaKhachHang')  # Field name made lowercase.
    ngaylaphoadon = models.DateField(db_column='NgayLapHoaDon', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'HoaDon'

    def __str__(self):
        return self.mahoadon

class Chitiethoadon(models.Model):
    machitiethoadon = models.CharField(db_column='MaChiTietHoaDon', primary_key=True, max_length=7, db_collation='Latin1_General_CI_AS')  # Field name made lowercase. The composite primary key (MaChiTietHoaDon, MaHoaDon) found, that is not supported. The first column is selected.
    mahoadon = models.ForeignKey('Hoadon', models.DO_NOTHING, db_column='MaHoaDon')  # Field name made lowercase.
    machitietphanan = models.ForeignKey('Chitietphanan', models.DO_NOTHING, db_column='MaChiTietPhanAn', blank=True, null=True)  # Field name made lowercase.
    macombo = models.ForeignKey('Combo', models.DO_NOTHING, db_column='MaComBo', blank=True, null=True)  # Field name made lowercase.
    soluong = models.IntegerField(db_column='SoLuong', blank=True, null=True)  # Field name made lowercase.
    giaban = models.IntegerField(db_column='GiaBan', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChiTietHoaDon'
        unique_together = (('machitiethoadon', 'mahoadon'),)

    def __str__(self):
        return self.machitiethoadon
    
class Tinhtrang(models.Model):
    matinhtrang = models.CharField(db_column='MaTinhTrang', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tentinhtrang = models.CharField(db_column='TenTinhTrang', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TinhTrang'

    def __str__(self):
        return self.matinhtrang
    
class Chitiettinhtrang(models.Model):
    mahoadon = models.OneToOneField('Hoadon', models.DO_NOTHING, db_column='MaHoaDon', primary_key=True)  # Field name made lowercase.
    manhanvien = models.ForeignKey('Nhanvien', models.DO_NOTHING, db_column='MaNhanVien', blank=True, null=True)  # Field name made lowercase.
    matinhtrang = models.OneToOneField('Tinhtrang', models.DO_NOTHING, db_column='MaTinhTrang')  # Field name made lowercase. The composite primary key (MaTinhTrang, MaHoaDon) found, that is not supported. The first column is selected.
    thoigianxacnhan = models.DateField(db_column='ThoiGianXacNhan', blank=True, null=True)  # Field name made lowercase.
    thoigianthanhtoan = models.DateField(db_column='ThoiGianThanhToan', blank=True, null=True)  # Field name made lowercase.
    thoigiannhanhang = models.DateField(db_column='ThoiGianNhanHang', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChiTietTinhTrang'
        unique_together = (('matinhtrang', 'mahoadon'),)

class Khuyenmai(models.Model):
    makhuyenmai = models.CharField(db_column='MaKhuyenMai', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tenkhuyenmai = models.CharField(db_column='TenKhuyenMai', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaytao = models.DateField(db_column='NgayTao', blank=True, null=True)  # Field name made lowercase.
    ngaybatdau = models.DateField(db_column='NgayBatDau', blank=True, null=True)  # Field name made lowercase.
    ngayketthuc = models.DateField(db_column='NgayKetThuc', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'KhuyenMai'

    def __str__(self):
        return self.makhuyenmai

class Chitietkhuyenmai(models.Model):
    machitietkhuyenmai = models.CharField(db_column='MaChiTietKhuyenMai', primary_key=True, max_length=7, db_collation='Latin1_General_CI_AS')  # Field name made lowercase. The composite primary key (MaChiTietKhuyenMai, MaKhuyenMai) found, that is not supported. The first column is selected.
    makhuyenmai = models.ForeignKey('Khuyenmai', models.DO_NOTHING, db_column='MaKhuyenMai')  # Field name made lowercase.
    machitietphanan = models.ForeignKey('Chitietphanan', models.DO_NOTHING, db_column='MaChiTietPhanAn', blank=True, null=True)  # Field name made lowercase.
    macombo = models.ForeignKey('Combo', models.DO_NOTHING, db_column='MaComBo', blank=True, null=True)  # Field name made lowercase.
    phantramkhuyenmai = models.IntegerField(db_column='PhanTramKhuyenMai', blank=True, null=True)  # Field name made lowercase.
    mota = models.TextField(db_column='MoTa', db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChiTietKhuyenMai'
        unique_together = (('machitietkhuyenmai', 'makhuyenmai'),)

    def __str__(self):
        return self.machitietkhuyenmai
    
class Nhacungcap(models.Model):
    manhacungcap = models.CharField(db_column='MaNhaCungCap', primary_key=True, max_length=6, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tennhacungcap = models.CharField(db_column='TenNhaCungCap', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sodienthoai = models.CharField(db_column='SoDienThoai', max_length=10, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaycongtac = models.DateField(db_column='NgayCongTac', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'NhaCungCap'

    def __str__(self):
        return self.manhacungcap
    
class Nguyenlieu(models.Model):
    manguyenlieu = models.CharField(db_column='MaNguyenLieu', primary_key=True, max_length=5, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    tennguyenlieu = models.CharField(db_column='TenNguyenLieu', max_length=100, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    soluongtonkho = models.FloatField(db_column='SoLuongTonKho', blank=True, null=True)  # Field name made lowercase.
    donvi = models.CharField(db_column='DonVi', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    manhacungcap = models.ForeignKey('Nhacungcap', models.DO_NOTHING, db_column='MaNhaCungCap')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'NguyenLieu'

    def __str__(self):
        return self.manguyenlieu

class Chitietnguyenlieu(models.Model):
    machitietnguyenlieu = models.CharField(db_column='MaChiTietNguyenLieu', primary_key=True, max_length=7, db_collation='Latin1_General_CI_AS')  # Field name made lowercase. The composite primary key (MaChiTietNguyenLieu, MaNguyenLieu, MaChiTietPhanAn) found, that is not supported. The first column is selected.
    soluong = models.FloatField(db_column='SoLuong', blank=True, null=True)  # Field name made lowercase.
    donvi = models.CharField(db_column='DonVi', max_length=50, db_collation='Latin1_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    manguyenlieu = models.ForeignKey('Nguyenlieu', models.DO_NOTHING, db_column='MaNguyenLieu')  # Field name made lowercase.
    machitietphanan = models.ForeignKey('Chitietphanan', models.DO_NOTHING, db_column='MaChiTietPhanAn')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChiTietNguyenLieu'
        unique_together = (('machitietnguyenlieu', 'manguyenlieu', 'machitietphanan'),)

    def __str__(self):
        return self.machitietnguyenlieu

class Phieunhap(models.Model):
    maphieunhap = models.CharField(db_column='MaPhieuNhap', primary_key=True, max_length=6, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    manhanvien = models.ForeignKey(Nhanvien, models.DO_NOTHING, db_column='MaNhanVien', blank=True, null=True)  # Field name made lowercase.
    ngaynhap = models.DateField(db_column='NgayNhap', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PhieuNhap'

    def __str__(self):
        return self.maphieunhap

class Chitietphieunhap(models.Model):
    machitietphieunhap = models.CharField(db_column='MaChiTietPhieuNhap', primary_key=True, max_length=8, db_collation='Latin1_General_CI_AS')  # Field name made lowercase. The composite primary key (MaChiTietPhieuNhap, MaPhieuNhap, MaNguyenLieu) found, that is not supported. The first column is selected.
    maphieunhap = models.ForeignKey('Phieunhap', models.DO_NOTHING, db_column='MaPhieuNhap')  # Field name made lowercase.
    manguyenlieu = models.ForeignKey('Nguyenlieu', models.DO_NOTHING, db_column='MaNguyenLieu')  # Field name made lowercase.
    soluong = models.IntegerField(db_column='SoLuong', blank=True, null=True)  # Field name made lowercase.
    gianhap = models.IntegerField(db_column='GiaNhap', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ChiTietPhieuNhap'
        unique_together = (('machitietphieunhap', 'maphieunhap', 'manguyenlieu'),)

    def __str__(self):
        return self.machitietphieunhap