import flet as ft

def main(page: ft.Page):
    page.title = "Kasir"
    page.window_width = 400
    page.window_height = 850
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = ft.padding.symmetric(horizontal=15, vertical=10)
    page.scroll = ft.ScrollMode.AUTO

    # STATE
    keranjang = []
    barang_terakhir_dihapus = [None]
    BATAS_DISKON = 100000

    # KOMPONEN INPUT
    nama_barang = ft.TextField(label="Item Name", border_radius=8, border_color=ft.colors.BLACK)
    harga = ft.TextField(label="Price", border_radius=8, border_color=ft.colors.BLACK, keyboard_type=ft.KeyboardType.NUMBER)
    jumlah = ft.TextField(label="Qty", border_radius=8, border_color=ft.colors.BLACK, keyboard_type=ft.KeyboardType.NUMBER)
    diskon_persen = ft.TextField(label="Discount %", value="0", border_radius=8, border_color=ft.colors.BLACK, keyboard_type=ft.KeyboardType.NUMBER)

    cart_list = ft.ListView(expand=False, height=200, spacing=5, auto_scroll=True)
    total_text = ft.Text("TOTAL: Rp 0", size=22, weight=ft.FontWeight.BOLD)
    error_text = ft.Text("", color=ft.colors.RED_500)

    struk_container = ft.Container(visible=False)

    # FOOTER
    footer = ft.Container(
        content=ft.Column([
            ft.Text("©2026 Developed By:", size=11, color=ft.colors.GREY_500),
            ft.Text("Agil", size=11, color=ft.colors.GREY_500, weight=ft.FontWeight.BOLD),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2),
        padding=ft.padding.only(top=20, bottom=10),
        alignment=ft.alignment.bottom_center
    )

    def show_error(msg):
        error_text.value = msg
        page.update()

    def input_angka(value_str):
        if not value_str.strip().isdigit():
            return None, "Error! Hanya angka"
        angka = int(value_str.strip())
        if angka <= 0:
            return None, "Error! Angka harus lebih dari 0"
        return angka, ""

    def update_cart():
        cart_list.controls.clear()
        total_belanja = 0

        if not keranjang:
            cart_list.controls.append(ft.Text("Keranjang masih kosong", italic=True, color=ft.colors.GREY))
        else:
            for idx, item in enumerate(keranjang):
                total_belanja += item["subtotal"]
                cart_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{idx+1}. {item['nama']}", expand=2),
                            ft.Text(f"{item['jumlah']}x", expand=1),
                            ft.Text(f"Rp {item['subtotal']:,}", expand=2, text_align=ft.TextAlign.RIGHT),
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                icon_color=ft.colors.RED_400,
                                icon_size=18,
                                tooltip="Hapus",
                                on_click=lambda e, i=idx: hapus_item(i)
                            )
                        ]),
                        padding=5,
                        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_200))
                    )
                )

        # HITUNG DISKON
        total_akhir, diskon_rp, persen_diskon = hitung_diskon(total_belanja)
        total_text.value = f"TOTAL: Rp {int(total_akhir):,}"
        page.update()
        return total_belanja, total_akhir, diskon_rp, persen_diskon

    def hitung_diskon(total_belanja):
        disc_str = diskon_persen.value.strip()
        if not disc_str.isdigit():
            return total_belanja, 0, 0

        persen_diskon = int(disc_str)
        if persen_diskon < 0 or persen_diskon >= 100:
            return total_belanja, 0, 0

        if total_belanja > BATAS_DISKON and persen_diskon > 0:
            jumlah_diskon = total_belanja * (persen_diskon / 100)
            total_akhir = total_belanja - jumlah_diskon
            return total_akhir, jumlah_diskon, persen_diskon
        else:
            return total_belanja, 0, 0

    def add_item_click(e):
        error_text.value = ""

        # VALIDASI NAMA
        nama = nama_barang.value.strip().title()
        if not nama:
            show_error("Error! Nama barang kosong")
            return
        if not nama.replace(" ", "").isalnum():
            show_error("Error! Isi nama yang sesuai")
            return

        # VALIDASI ANGKA
        harga_val, err1 = input_angka(harga.value)
        if err1:
            show_error(f"Harga: {err1}")
            return

        jumlah_val, err2 = input_angka(jumlah.value)
        if err2:
            show_error(f"Jumlah: {err2}")
            return

        # MASUKIN KE KERANJANG
        subtotal = harga_val * jumlah_val
        keranjang.append({
            "nama": nama,
            "harga": harga_val,
            "jumlah": jumlah_val,
            "subtotal": subtotal
        })

        # CLEAR FIELD
        nama_barang.value = ""
        harga.value = ""
        jumlah.value = ""
        nama_barang.focus()
        struk_container.visible = False
        update_cart()

    def hapus_item(index):
        barang_terakhir_dihapus[0] = keranjang.pop(index)
        struk_container.visible = False
        update_cart()
        page.show_snack_bar(ft.SnackBar(ft.Text(f"Barang '{barang_terakhir_dihapus[0]['nama']}' dihapus"), open=True))

    def undo_click(e):
        if barang_terakhir_dihapus[0]:
            keranjang.append(barang_terakhir_dihapus[0])
            page.show_snack_bar(ft.SnackBar(ft.Text(f"UNDO: '{barang_terakhir_dihapus[0]['nama']}' balik lagi"), open=True))
            barang_terakhir_dihapus[0] = None
            struk_container.visible = False
            update_cart()
        else:
            show_error("Error! Gak ada yang bisa di-undo")

    def calculate_click(e):
        error_text.value = ""
        disc_str = diskon_persen.value.strip()

        if disc_str and not disc_str.isdigit():
            show_error("Error! Diskon hanya angka")
            return

        disc = int(disc_str) if disc_str else 0
        if disc < 0:
            show_error("Error! Diskon tidak bisa minus")
            return
        if disc >= 100:
            show_error("Diskon terlalu besar!")
            return

        total_belanja, total_akhir, diskon_rp, persen_diskon = update_cart()

        # BIKIN STRUK
        struk_content = [
            ft.Text("="*38, font_family="monospace"),
            ft.Text("STRUK BELANJA V14".center(38), font_family="monospace", weight=ft.FontWeight.BOLD),
            ft.Text("="*38, font_family="monospace"),
        ]

        for item in keranjang:
            nama = item["nama"][:15]
            struk_content.append(
                ft.Text(f"{nama:<18} {item['jumlah']:>2} : Rp {item['subtotal']:>9,.0f}", font_family="monospace")
            )

        struk_content.append(ft.Text("-"*38, font_family="monospace"))
        struk_content.append(ft.Text(f"{'Subtotal':<25}: Rp {total_belanja:>9,.0f}", font_family="monospace"))

        if diskon_rp > 0:
            struk_content.append(ft.Text(f"{'Diskon ' + str(persen_diskon) + '%':<23}:-Rp {diskon_rp:>8,.0f}", font_family="monospace"))
            struk_content.append(ft.Text("-"*38, font_family="monospace"))

        struk_content.extend([
            ft.Text(f"{'TOTAL BAYAR':<19}: Rp {total_akhir:>9,.0f}", font_family="monospace", weight=ft.FontWeight.BOLD),
            ft.Text("="*38, font_family="monospace"),
            ft.Text("TERIMAKASIH!".center(38), font_family="monospace"),
        ])

        struk_container.content = ft.Container(
            content=ft.Column(struk_content, spacing=2),
            bgcolor=ft.colors.GREY_100,
            padding=15,
            border_radius=8,
            border=ft.border.all(1, ft.colors.BLACK)
        )
        struk_container.visible = True
        page.update()

    def clear_all_click(e):
        keranjang.clear()
        barang_terakhir_dihapus[0] = None
        diskon_persen.value = "0"
        struk_container.visible = False
        error_text.value = ""
        update_cart()

    # LAYOUT
    page.add(
        ft.Column([
            ft.Text("Kasir", size=32, weight=ft.FontWeight.W_500),
            ft.Container(height=10),

            nama_barang,
            ft.Container(height=10),
            price,
            ft.Container(height=10),
            qty,
            ft.Container(height=5),
            error_text,
            ft.Container(height=10),

            ft.FilledButton(
                content=ft.Row([ft.Icon(ft.icons.ADD), ft.Text("Add Item")], alignment=ft.MainAxisAlignment.CENTER),
                on_click=add_item_click,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_50, color=ft.colors.BLUE, shape=ft.RoundedRectangleBorder(radius=20)),
                width=400, height=45
            ),

            ft.Divider(height=30),
            ft.Row([
                ft.Text("Cart:", size=16, weight=ft.FontWeight.W_500),
                ft.ElevatedButton("UNDO", icon=ft.icons.UNDO, on_click=undo_click, height=30)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Container(
                content=cart_list,
                border=ft.border.all(1, ft.colors.BLACK),
                border_radius=8,
                padding=10,
            ),

            ft.Divider(height=20),
            ft.Text("Diskon hanya berlaku jika total > Rp 100,000", size=11, color=ft.colors.GREY, italic=True),
            ft.Container(height=5),
            discount,
            ft.Container(height=15),

            ft.FilledButton(
                content=ft.Row([ft.Icon(ft.icons.CALCULATE), ft.Text("Calculate")], alignment=ft.MainAxisAlignment.CENTER),
                on_click=calculate_click,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_50, color=ft.colors.BLUE_700, shape=ft.RoundedRectangleBorder(radius=20)),
                width=400, height=45
            ),

            ft.Container(height=15),
            total_text,
            ft.Container(height=15),

            ft.FilledButton(
                content=ft.Row([ft.Icon(ft.icons.DELETE_SWEEP), ft.Text("Clear All")], alignment=ft.MainAxisAlignment.CENTER),
                on_click=clear_all_click,
                style=ft.ButtonStyle(bgcolor=ft.colors.RED_500, color=ft.colors.WHITE, shape=ft.RoundedRectangleBorder(radius=20)),
                width=400, height=45
            ),

            ft.Container(height=20),
            struk_container,
            footer
        ])
    )

    update_cart()

ft.app(target=main)
