import flet as ft

def main(page: ft.Page):
    page.title = "Kasir Gil V14"
    page.scroll = "auto"
    
    keranjang = []
    
    nama_input = ft.TextField(label="Nama Barang", width=300)
    harga_input = ft.TextField(label="Harga") 
    jumlah_input = ft.TextField(label="Jumlah")
    diskon_input = ft.TextField(label="Diskon %", value="0")
    
    list_keranjang = ft.Column()
    total_text = ft.Text("TOTAL: Rp 0", size=22, weight="bold")
    error_text = ft.Text("", color="red")

    def update_ui():
        list_keranjang.controls.clear()
        total = 0
        for i, item in enumerate(keranjang):
            total += item["subtotal"]
            list_keranjang.controls.append(
                ft.Row([
                    ft.Text(f"{item['nama']} x{item['jumlah']} = Rp {item['subtotal']:,}", expand=True),
                    ft.IconButton(icon="delete", on_click=lambda _, idx=i: hapus_barang(idx))
                ])
            )
        
        try:
            diskon = float(diskon_input.value or 0)
        except:
            diskon = 0
            
        if total > 100000 and 0 < diskon < 100:
            potongan = total * diskon / 100
            total_text.value = f"TOTAL: Rp {total - potongan:,.0f}"
        else:
            total_text.value = f"TOTAL: Rp {total:,.0f}"
        page.update()

    def tambah_barang(e):
        error_text.value = ""
        try:
            nama = nama_input.value.strip().title()
            harga = int(harga_input.value)
            jumlah = int(jumlah_input.value)
            if not nama or harga <= 0 or jumlah <= 0:
                raise ValueError
        except:
            error_text.value = "Isi nama, harga, jumlah yg bener!"
            page.update()
            return
            
        keranjang.append({
            "nama": nama,
            "harga": harga, 
            "jumlah": jumlah,
            "subtotal": harga * jumlah
        })
        nama_input.value = ""
        harga_input.value = ""
        jumlah_input.value = ""
        update_ui()

    def hapus_barang(idx):
        keranjang.pop(idx)
        update_ui()

    page.add(
        ft.Column([
            ft.Text("KASIR GIL V14 🔥", size=28, weight="bold"),
            nama_input,
            ft.Row([harga_input, jumlah_input]),
            ft.ElevatedButton("Tambah Barang", on_click=tambah_barang),
            error_text,
            ft.Divider(),
            ft.Text("Keranjang:", size=18),
            list_keranjang,
            ft.Divider(),
            ft.Row([diskon_input, ft.ElevatedButton("Hitung", on_click=lambda e: update_ui())]),
            total_text,
        ], spacing=10)
    )

ft.app(target=main)
