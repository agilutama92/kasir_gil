import flet as ft

def main(page: ft.Page):
    page.title = "Kasir"
    page.theme_mode = ft.ThemeMode.LIGHT

    users = {
        "admin": {"password": "admin123", "role": "admin"},
        "kasir": {"password": "kasir123", "role": "kasir"}
    }
    current_user = {"role": None}

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    def show_snack(msg):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def logout(e):
        current_user["role"] = None
        page.clean()
        login_view()

    def admin_view():
        page.appbar = ft.AppBar(
            title=ft.Text("Dashboard Admin"),
            bgcolor=ft.colors.BLUE,
            actions=[
                ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=toggle_theme),
                ft.IconButton(ft.icons.LOGOUT, on_click=logout)
            ]
        )
        page.add(
            ft.Column([
                ft.Text("Login sebagai: Admin", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Kelola Produk", icon=ft.icons.INVENTORY),
                ft.ElevatedButton("Laporan Penjualan", icon=ft.icons.BAR_CHART),
                ft.ElevatedButton("Kelola User", icon=ft.icons.PEOPLE),
            ], spacing=20)
        )
        page.update()

    def kasir_view():
        page.appbar = ft.AppBar(
            title=ft.Text("Kasir"),
            bgcolor=ft.colors.GREEN,
            actions=[
                ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=toggle_theme),
                ft.IconButton(ft.icons.LOGOUT, on_click=logout)
            ]
        )
        page.add(
            ft.Column([
                ft.Text("Login sebagai: Kasir", size=20, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Transaksi Baru", icon=ft.icons.ADD_SHOPPING_CART),
                ft.ElevatedButton("Riwayat Transaksi", icon=ft.icons.HISTORY),
            ], spacing=20)
        )
        page.update()

    def login(e):
        user = username.value
        pwd = password.value
        # INI YG BENER: users[user]["password"]
        if user in users and users[user]["password"] == pwd:
            current_user["role"] = users[user]["role"]
            page.clean()
            if current_user["role"] == "admin":
                admin_view()
            else:
                kasir_view()
        else:
            show_snack("Username / Password salah!")

    username = ft.TextField(label="Username", autofocus=True)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, on_submit=login)

    def login_view():
        page.appbar = ft.AppBar(title=ft.Text("Login Kasir"), bgcolor=ft.colors.BLUE_GREY)
        page.add(
            ft.Column([
                ft.Icon(ft.icons.STORE, size=80, color=ft.colors.BLUE),
                ft.Text("Aplikasi Kasir", size=32, weight=ft.FontWeight.BOLD),
                username,
                password,
                ft.ElevatedButton("Login", icon=ft.icons.LOGIN, on_click=login, width=300),
                ft.Text("admin/admin123 | kasir/kasir123", size=10, color=ft.colors.GREY)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        )
        page.update()

    login_view()

ft.app(target=main)
