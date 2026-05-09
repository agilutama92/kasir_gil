import flet as ft

def main(page: ft.Page):
    page.title = "Kasir"
    page.window_width = 400
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    # FOOTER GLOBAL
    footer = ft.Container(
        content=ft.Column([
            ft.Text("©2026 Developed By:", size=11, color=ft.colors.GREY_500),
            ft.Text("Agil", size=11, color=ft.colors.GREY_500, weight=ft.FontWeight.BOLD),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2),
        padding=ft.padding.only(bottom=15, top=10),
        alignment=ft.alignment.bottom_center
    )

    # LANGSUNG HALAMAN MENU INPUT BARANG
    page.add(
        ft.Column([
            ft.AppBar(title=ft.Text("Menu Input Barang"), bgcolor=ft.colors.BLUE_600),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.INVENTORY_2, size=60, color=ft.colors.BLUE_600),
                    ft.Text("KASIR", size=28, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Fitur Input Barang", size=18),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        "Tambah Barang Baru", 
                        icon=ft.icons.ADD_BOX,
                        width=300,
                        height=45
                    ),
                    ft.ElevatedButton(
                        "Lihat Stok Barang", 
                        icon=ft.icons.LIST_ALT,
                        width=300,
                        height=45
                    ),
                    ft.ElevatedButton(
                        "Laporan Penjualan", 
                        icon=ft.icons.BAR_CHART,
                        width=300,
                        height=45
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
                padding=20,
                expand=True
            ),
            footer  # ← FOOTER TETEP MUNCUL
        ], expand=True)
    )

ft.app(target=main)
