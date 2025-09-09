#-----------------------------------------#
#                                         #
#                                         #
#-----------------------------------------#
#333333333333333333333333333333333333333
#3333333333333333333333333333333333333333

import flet as ft


def main(page: ft.Page):
    page.title = "Текстовый редактор"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.window.width = 500
    page.window.height = 600
    page.window.resizable = True

    current_file_path = None

    def pick_result(e: ft.FilePickerResultEvent):
        nonlocal current_file_path
        if e.files:
            current_file_path = e.files[0].path
            selected_files.value = f"Выбран: {e.files[0].name}"

            try:
                with open(current_file_path, 'r', encoding='utf-8') as file:
                    file_content.value = file.read()
                    page.open(ft.SnackBar(ft.Text('Файл загружен!'), action = "OK"))
            except Exception as ex:
                file_content.value = f"Ошибка чтения: {ex}"
                page.open = ft.SnackBar(ft.Text(f"Ошибка: {ex}"), action="OK")
        else:
            selected_files.value = "Файл не выбран"

        page.update()

    def save_file(e):
        if current_file_path and file_content.value:
            try:
                with open(current_file_path, 'w', encoding='utf-8') as file:
                    file.write(file_content.value)
                page.open = ft.SnackBar(ft.Text("Файл сохранен!"), action="OK")

                page.update()
            except Exception as ex:
                page.open = ft.SnackBar(ft.Text(f"Ошибка сохранения: {ex}"), action="OK")

                page.update()

    def save_file_as_result(e: ft.FilePickerResultEvent):
        nonlocal current_file_path
        if e.path:
            try:
                with open(e.path, 'w', encoding='utf-8') as file:
                    file.write(file_content.value)
                current_file_path = e.path
                selected_files.value = f"Сохранен как: {e.path.split('/')[-1]}"
                page.snack_bar = ft.SnackBar(ft.Text("Файл сохранен!"), action="OK")
                page.snack_bar.open = True
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка сохранения: {ex}"), action="OK")
                page.snack_bar.open = True
                page.update()

    def save_file_as(e):
        # Открываем диалог сохранения файла
        save_dialog.save_file(
            file_name="новый_файл.txt",
            allowed_extensions=["txt", "py", "html", "css", "js", "json", "xml"]
        )

    def new_file(e):
        nonlocal current_file_path
        current_file_path = None
        selected_files.value = "Новый файл"
        file_content.value = ""
        page.update()


    pick_dialog = ft.FilePicker(on_result=pick_result)


    save_dialog = ft.FilePicker(on_result=save_file_as_result)


    page.overlay.extend([pick_dialog, save_dialog])

    selected_files = ft.Text("Файл не выбран", size=16)
    file_content = ft.TextField(
        multiline=True,
        expand=True,
        border_color=ft.Colors.GREY_600,
        text_size=14
    )

    page.add(
        ft.Column(
            [
                ft.Text('Текстовый редактор', size=25, weight=ft.FontWeight.BOLD),

                ft.Row([
                    ft.ElevatedButton(
                        'Новый',
                        icon=ft.Icons.CREATE,
                        on_click=new_file
                    ),
                    ft.ElevatedButton(
                        'Открыть',
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda _: pick_dialog.pick_files(
                            allow_multiple=False,
                            file_type=ft.FilePickerFileType.CUSTOM,
                            allowed_extensions=["txt", "py", "html", "css", "js", "json", "xml"]
                        )
                    ),
                    ft.ElevatedButton(
                        "Сохранить",
                        icon=ft.Icons.SAVE,

                        on_click=save_file,
                        tooltip="Сохранить текущий файл (Ctrl+S)"
                    ),
                    ft.ElevatedButton(
                        "Сохранить как",
                        icon=ft.Icons.SAVE_AS,
                        on_click=save_file_as,
                        tooltip="Сохранить файл под новым именем"
                    )
                ], spacing=10),

                selected_files,

                ft.Container(
                    file_content,
                    border=ft.border.all(1, ft.Colors.GREY_600),
                    border_radius=5,
                    padding=10,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True
        )
    )


ft.app(target=main)
