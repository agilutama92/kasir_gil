import flet as ft

def main(page: ft.Page):
    page.title = "Kasir"
    page.window_width = 400
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    users = {
        "admin": "admin123",
        "kasir": "kasir123"
    }

    current_user = [""] # list biar mutable

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

    username_field = ft.TextField(
        label="Username",
        width=300,
        autofocus=True,
        prefix_icon=ft.icons.PERSON
    )
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=300,
        prefix_icon=ft.icons.LOCK,
        on_submit=lambda e: login_click(e)
    )
    error_text = ft.Text("", color=ft.colors.RED_500)

    def logout_click(e):
        current_user[0] = "" # ubah index 0
        page.go("/")

    def halaman_dashboard():
        return ft.View(
            "/dashboard",
            [
                ft.AppBar(title=ft.Text("Menu Input Barang"), bgcolor=ft.colors.BLUE_600),
                ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.icons.INVENTORY_2, size=60, color=ft.colors.BLUE_600),
                            ft.Text(f"Halo, {current_user[0].upper()}", size=24, weight=ft.FontWeight.BOLD), # pake [0]
                            ft.Divider(),
                            ft.Text("Fitur Input Barang", size=18),
                            ft.ElevatedButton("Tambah Barang Baru", icon=ft.icons.ADD_BOX, width=300, height=45),
                            ft.ElevatedButton("Lihat Stok Barang", icon=ft.icons.LIST_ALT, width=300, height=45),
                            ft.ElevatedButton(
                                "Logout",
                                icon=ft.icons.LOGOUT,
                                on_click=logout_click,
                                bgcolor=ft.colors.RED_400,
                                color=ft.colors.WHITE,
                                width=300,
                                height=45
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15),
                        padding=20,
                        expand=True
                    ),
                    footer
                ], expand=True)
            ],
            padding=0
        )

    def halaman_login():
        return ft.View(
            "/",
            [
                ft.Column([
                    ft.Container(expand=True),
                    ft.Icon(ft.icons.POINT_OF_SALE, size=80, color=ft.colors.BLUE_600),
                    ft.Text("Kasir", size=32, weight=ft.FontWeight.BOLD),
                    ft.Container(height=20),
                    username_field,
                    password_field,
                    error_text,
                    ft.ElevatedButton(
                        "Masuk",
                        icon=ft.icons.LOGIN,
                        on_click=login_click,
                        width=300,
                        height=50,
                    ),
                    ft.Container(expand=True),
                    footer
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True)
            ],
            padding=20
        )

    def login_click(e):
        user = username_field.value.strip()
        pw = password_field.value.strip()

        # FIX 1: Bandingin users sama pw
        if user in users and users == pw:
            current_user[0] = user # FIX 2: assign ke index 0
            error_text.value = ""
            page.go("/dashboard")
            username_field.value = ""
            password_field.value = ""
        else:
            error_text.value = "Username atau password salah"
            password_field.value = ""
        page.update()

    def route_change(route):
        page.views.clear()
        if page.route == "/dashboard":
            page.views.append(halaman_dashboard())
        else:
            page.views.append(halaman_login())
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
