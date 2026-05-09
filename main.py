import flet as ft

def main(page: ft.Page):
    page.title = "Kasir Gil V15"
    page.bgcolor = ft.Colors.BLUE_50
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.add(
        ft.Column(
            [
                ft.Icon(name=ft.Icons.LOCAL_CAFE, size=100, color=ft.Colors.BROWN_400),
                ft.Text("KASIR GIL READY 🔥", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                ft.Text("Build by Github Action", size=16, color=ft.Colors.GREY_700),
                ft.Text("Version 0.1", size=12, color=ft.Colors.GREY_500)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )
    page.update()  # ← INI YG KURANG KEMARIN

ft.app(target=main)
