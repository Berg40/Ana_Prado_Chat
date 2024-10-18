import requests
import json
import flet as ft
import os
from dotenv import load_dotenv

load_dotenv(override=True)

chave = os.getenv("API_KEY")
print(chave)


def gpt(pergunta, display_result, pergunta_input):
    headers = {
        "Authorization": f"Bearer {chave}",
        "Content-Type": "application/json"
    }

    # Link da API
    link1 = "https://api.openai.com/v1/chat/completions"
    id_modelo = "gpt-3.5-turbo"

    # Construir o corpo da mensagem
    body_mensagem = {
        "model": id_modelo,
        "messages": [{"role": "user", "content": pergunta}]
    }

    # Converter para JSON
    body_mensagem = json.dumps(body_mensagem)

    # Fazer a requisição POST para obter a resposta do modelo
    requisicao2 = requests.post(link1, headers=headers, data=body_mensagem)

    # Processar a resposta
    if requisicao2.status_code == 200:
        resposta = requisicao2.json()

        mensagem = resposta["choices"][0]["message"]["content"]

        display_result.value += f"\nVocê: {pergunta}\nAna Prado : {mensagem}\n"
    else:
        display_result.value += f"\nErro ao obter a resposta para a pergunta: {pergunta}\n"

    # Limpar o campo de pergunta
    pergunta_input.value = ""
    pergunta_input.update()

    display_result.update()


def main(page: ft.Page):
    page.window_always_on_top = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.PINK_100
    page.padding = 0


    page.title = "Ana Prado Chat"

    def toglle_theme(e):
        page.theme_mode= ft.ThemeMode.DARK  if page.theme_mode == page.theme_mode.LIGHT else page.theme_mode.LIGHT
        page.update()

    # Criar campo para pergunta
    pergunta_input = ft.TextField(label="Digite sua pergunta:", width=400)

    # Texto para exibir a resposta (histórico da conversa)
    resposta_text = ft.Text(value="", width=400, selectable=True, weight=ft.FontWeight.BOLD)

    # Botão para enviar a pergunta
    enviar_button = ft.ElevatedButton(
        text="Enviar",
        on_click=lambda _: gpt(pergunta_input.value, resposta_text, pergunta_input)
    )

    # Container para organizar os elementos
    container = ft.Container(

        height=900,
        width=400,
        padding=10,
        bgcolor=ft.colors.PINK_100,
        image_src='images/fotoprincipal.jpg',
        image_fit=ft.ImageFit.COVER,
        image_opacity=0.3,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.icons.BRIGHTNESS_6,
                    on_click=toglle_theme
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                    value="Ana Prado a sua Personal Trainer virtual.",
                    size=20

                ),
                pergunta_input,
                enviar_button,

                ft.Container(
                    height=350,
                    width=400,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            resposta_text
                        ]
                    )
                ),
                ft.Container(

                    margin=0,
                    height=80,
                    width=200,
                    image_src='images/logo.png',
                    image_fit=ft.ImageFit.COVER

                )

            ]
        )
    )

    # Adicionar os elementos à página
    page.add(container)


# Rodar a aplicação Flet
if __name__ == "__main__":
    ft.app(target=main)

