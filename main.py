import flet as ft

def main(page: ft.Page):
    page.title = "Kasir"
    page.scroll = "auto"
    page.theme_mode = "light"
    page.padding = 20 # Kasih jarak dari pinggir layar
    page.window.width = 400 # Biar gak kepotong
    
    keranjang = []
    
    # === KOMPONEN ===
    nama_input = ft.TextField(label="Item Name", autofocus=True)
    harga_input = ft.TextField(label="Price", keyboard_type="number") 
    jumlah_input = ft.TextField(label="Qty", keyboard_type="number")
    diskon_input = ft.TextField(label="Discount %", value="0", keyboard_type="number")
    
    list_keranjang = ft.ListView(height=150, spacing=5, auto_scroll=True) # Dikecilin + bisa scroll
    total_text = ft.Text("TOTAL: Rp 0", size=24, weight="bold")
    error_text = ft.Text("", color="red")

    # === FUNGSI ===
    def update_ui():
        list_keranjang.controls.clear()
        total = 0
        for i, item in enumerate(keranjang):
            total += item["subtotal"]
            list_keranjang.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{item['nama']} x{item['jumlah']}", expand=2),
                        ft.Text(f"Rp {item['subtotal']:,}", expand=1, text_align="right"),
                        ft.IconButton(icon="delete_outline", icon_color="red400", on_click=lambda _, idx=i: hapus_barang(idx))
                    ]),
                    bgcolor="grey100",
                    padding=8,
                    border_radius=5
                )
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

    # === TAMPILAN BARU - SEMUA SEJAJAR KEBAWAH ===
    page.add(
        ft.Column([
            ft.Text("Kasir", size=30, weight="bold"),
            
            # 1. Input sejajar kebawah, full width
            nama_input,
            harga_input, 
            jumlah_input,
            
            ft.ElevatedButton("Add Item", icon="add", width=400, on_click=tambah_barang),
            error_text,
            ft.Divider(),
            
            ft.Text("Cart:", size=18, weight="w500"),
            
            # 2. Kotak cart dikecilin + border
            ft.Container(
                content=list_keranjang, 
                border=ft.border.all(1, "grey400"), 
                border_radius=8,
                padding=10
            ),
            
            ft.Divider(),
            
            # 3. Diskon + Calculate gak kepotong lagi
            diskon_input,
            ft.ElevatedButton("Calculate", icon="calculate", width=400, on_click=lambda e: update_ui()),
            
            total_text,
            
            ft.ElevatedButton(
                "Clear All", 
                icon="delete_sweep", 
                bgcolor="red", 
                color="white",
                width=400,
                on_click=reset_keranjang
            ),
            
            ft.Container(height=20),
            ft.Text("Licensed to Agil © 2026", size=10, color="grey"),
            ft.Text("All Rights Reserved", size=10, color="grey"),
        ], spacing=10, width=400, scroll="auto") # Scroll biar muat di HP kecil
    )

ft.app(target=main)
