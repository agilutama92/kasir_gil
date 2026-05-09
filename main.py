import flet as ft

def main(page: ft.Page):
    page.title = "Kasir"
    page.scroll = "auto"
    page.theme_mode = "light"
    
    keranjang = []
    
    # === KOMPONEN ===
    nama_input = ft.TextField(label="Item Name", width=300, autofocus=True)
    harga_input = ft.TextField(label="Price") 
    jumlah_input = ft.TextField(label="Qty")
    diskon_input = ft.TextField(label="Discount %", value="0")
    
    list_keranjang = ft.Column(scroll="auto")
    total_text = ft.Text("TOTAL: Rp 0", size=24, weight="bold")
    error_text = ft.Text("", color="red")

    # === FUNGSI ===
    def update_ui():
        list_keranjang.controls.clear()
        total = 0
        for i, item in enumerate(keranjang):
            total += item["subtotal"]
            list_keranjang.controls.append(
                ft.Row([
                    ft.Text(f"{item['nama']} x{item['jumlah']} = Rp {item['subtotal']:,}", expand=True),
                    ft.IconButton(icon="delete", icon_color="red400", on_click=lambda _, idx=i: hapus_barang(idx))
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
            error_text.value = "Please enter valid item, price, and qty!"
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
        nama_input.focus()
        update_ui()

    def hapus_barang(idx):
        keranjang.pop(idx)
        update_ui()

    def reset_keranjang(e):
        keranjang.clear()
        diskon_input.value = "0"
        update_ui()

    # === TAMPILAN ===
    page.add(
        ft.Column([
            ft.Text("Kasir", size=30, weight="bold"),
            nama_input,
            ft.Row([harga_input, jumlah_input]),
            ft.ElevatedButton("Add Item", icon="add", on_click=tambah_barang),
            error_text,
            ft.Divider(),
            ft.Text("Cart:", size=18, weight="w500"),
            ft.Container(content=list_keranjang, height=200, border=ft.border.all(1, "grey300"), padding=10),
            ft.Divider(),
            ft.Row([diskon_input, ft.ElevatedButton("Calculate", icon="calculate", on_click=lambda e: update_ui())]),
            total_text,
            ft.ElevatedButton(
                "Clear All", 
                icon="delete_sweep", 
                bgcolor="red", 
                color="white",
                on_click=reset_keranjang
            ),
            ft.Container(height=20),
            ft.Text("Licensed to Agil © 2026", size=10, color="grey", opacity=0.6),
            ft.Text("All Rights Reserved", size=10, color="grey", opacity=0.6),
        ], spacing=12, width=400, horizontal_alignment="center")
    )

ft.app(target=main)
