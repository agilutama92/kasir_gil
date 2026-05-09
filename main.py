import flet as ft

def main(page: ft.Page):
    page.title = "Kasir"
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = ft.padding.symmetric(horizontal=15, vertical=10)
    page.scroll = ft.ScrollMode.AUTO

    # STATE
    cart_items = []
    
    # KOMPONEN INPUT
    item_name = ft.TextField(label="Item Name", border_radius=8, border_color=ft.colors.BLACK)
    price = ft.TextField(label="Price", border_radius=8, border_color=ft.colors.BLACK, keyboard_type=ft.KeyboardType.NUMBER)
    qty = ft.TextField(label="Qty", border_radius=8, border_color=ft.colors.BLACK, keyboard_type=ft.KeyboardType.NUMBER)
    discount = ft.TextField(label="Discount %", value="0", border_radius=8, border_color=ft.colors.BLACK, keyboard_type=ft.KeyboardType.NUMBER)
    
    cart_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)
    total_text = ft.Text("TOTAL: Rp 0", size=20, weight=ft.FontWeight.BOLD)

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

    def update_cart():
        cart_list.controls.clear()
        total = 0
        for item in cart_items:
            subtotal = item = 0
            cart_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{item}", expand=True),
                        ft.Text(f"{item} x Rp {item:,}"),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE, 
                            icon_color=ft.colors.RED_400,
                            on_click=lambda e, i=item: remove_item(i)
                        )
                    ]),
                    padding=5,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_200))
                )
            )
            total += subtotal
        
        disc = float(discount.value) if discount.value else 0
        total_setelah_disc = total - (total * disc / 100)
        total_text.value = f"TOTAL: Rp {int(total_setelah_disc):,}"
        page.update()

    def add_item_click(e):
        if item_name.value and price.value and qty.value:
            try:
                name = item_name.value
                harga = float(price.value)
                jumlah = int(qty.value)
                cart_items.append({"name": name, "price": harga, "qty": jumlah})
                item_name.value = ""
                price.value = ""
                qty.value = ""
                item_name.focus()
                update_cart()
            except ValueError:
                page.show_snack_bar(ft.SnackBar(ft.Text("Price & Qty harus angka"), open=True))
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text("Lengkapi semua field"), open=True))
        page.update()

    def remove_item(item):
        cart_items.remove(item)
        update_cart()

    def calculate_click(e):
        update_cart()
        page.show_snack_bar(ft.SnackBar(ft.Text("Total dihitung ulang"), open=True))

    def clear_all_click(e):
        cart_items.clear()
        discount.value = "0"
        update_cart()

    # LAYOUT UTAMA
    page.add(
        ft.Column([
            ft.Text("Kasir", size=32, weight=ft.FontWeight.W_500),
            ft.Container(height=10),
            
            item_name,
            ft.Container(height=10),
            price,
            ft.Container(height=10),
            qty,
            ft.Container(height=15),
            
            ft.FilledButton(
                content=ft.Row([
                    ft.Icon(ft.icons.ADD),
                    ft.Text("Add Item")
                ], alignment=ft.MainAxisAlignment.CENTER),
                on_click=add_item_click,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE_50,
                    color=ft.colors.BLUE,
                    shape=ft.RoundedRectangleBorder(radius=20)
                ),
                width=400,
                height=45
            ),
            
            ft.Divider(height=30),
            ft.Text("Cart:", size=16, weight=ft.FontWeight.W_500),
            ft.Container(
                content=cart_list,
                border=ft.border.all(1, ft.colors.BLACK),
                border_radius=8,
                padding=10,
                height=160
            ),
            
            ft.Divider(height=20),
            discount,
            ft.Container(height=15),
            
            ft.FilledButton(
                content=ft.Row([
                    ft.Icon(ft.icons.CALCULATE),
                    ft.Text("Calculate")
                ], alignment=ft.MainAxisAlignment.CENTER),
                on_click=calculate_click,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE_50,
                    color=ft.colors.BLUE_700,
                    shape=ft.RoundedRectangleBorder(radius=20)
                ),
                width=400,
                height=45
            ),
            
            ft.Container(height=15),
            total_text,
            ft.Container(height=15),
            
            ft.FilledButton(
                content=ft.Row([
                    ft.Icon(ft.icons.DELETE_SWEEP),
                    ft.Text("Clear All")
                ], alignment=ft.MainAxisAlignment.CENTER),
                on_click=clear_all_click,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.RED_500,
                    color=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=20)
                ),
                width=400,
                height=45
            ),
            
            footer  # ← FOOTER "Developed By: Agil" DI SINI
        ])
    )

ft.app(target=main)
