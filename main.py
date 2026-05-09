import flet as ft

def main(page: ft.Page):
    page.title = "Kasir Gil"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(ft.Text("AKHIRNYA NYALA GIL 🔥", size=30))
    page.update()

ft.app(target=main)
