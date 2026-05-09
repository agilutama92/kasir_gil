import flet as ft

def main(page: ft.Page):
    page.title = "Kasir Gil V15"
    page.window_width = 400
    page.bgcolor = ft.Colors.BLUE_50
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    page.add(
        ft.Icon(ft.icons.LOCAL_CAFE, size=80, color=ft.Colors.BROWN),
        ft.Text("KASIR GIL READY 🔥", size=28, weight="bold"),
        ft.Text("Build by Github Action", size=14)
    )

ft.app(target=main)
