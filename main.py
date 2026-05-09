import flet as ft

def main(page: ft.Page):
    page.title = "Aplikasi Kasir"
    page.window_width = 400
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # DATABASE USER LU
    users = {
        "admin": "admin123",
        "kasir": "kasir123"
    }

    # KOMPONEN LOGIN
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
        prefix_icon=ft.icons.LOCK
    )
    error_text = ft.Text("", color=ft.colors.RED_500)

    def masuk_dashboard(user):
        page.clean()
        page.add(
            ft.Column([
                ft.Icon(ft.icons.CHECK_CIRCLE, size=100, color=ft.colors.GREEN),
                ft.Text(f"Selamat Datang, {user.upper()}!", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Aplikasi Kasir by Agil", size=16, color=ft.colors.BLUE_700),
                ft.ElevatedButton(
                    "Logout",
                    icon=ft.icons.LOGOUT,
                    on_click=lambda e: page.go("/"),
                    bgcolor=ft.colors.RED_400,
                    color=ft.colors.WHITE
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30)
        )
        page.update()

    def login_click(e):
        user = username_field.value.strip()
        pw = password_field.value.strip()

        if user in users and users[user] == pw:
            masuk_dashboard(user)
        else:
            error_text.value = "Username atau password salah!"
            page.update()

    # TAMPILAN LOGIN
    login_view = ft.Column([
        ft.Icon(ft.icons.STORE, size=80, color=ft.colors.BLUE_600),
        ft.Text("Aplikasi Kasir", size=32, weight=ft.FontWeight.BOLD),
        username_field,
        password_field,
        error_text,
        ft.ElevatedButton(
            "Login",
            icon=ft.icons.LOGIN,
            on_click=login_click,
            width=300,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE
            )
        ),
        ft.Text("Lisensi by Agil yg Keren 🔥", size=12, color=ft.colors.GREY_500)
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=20)

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View("/", [login_view])
        )
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
