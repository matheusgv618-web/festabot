import os
from groq import Groq


class IAService:

    def __init__(self):

        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )

        self.model = "llama-3.3-70b-versatile"
        self.historico = []

    def enviar_mensagem(self, mensagem_usuario: str, system_prompt: str) -> str:

        # Adiciona system prompt apenas uma vez
        if not self.historico:
            self.historico.append({
                "role": "system",
                "content": system_prompt
            })

        # Adiciona mensagem do usuário
        self.historico.append({
            "role": "user",
            "content": mensagem_usuario
        })

        try:

            chat_completion = self.client.chat.completions.create(
                messages=self.historico,
                model=self.model,
                max_tokens=1024,
            )

            # 🔥 RESPOSTA LIMPA (SEM HTML)
            resposta_ia = chat_completion.choices[0].message.content

            resposta_ia = (
                resposta_ia
                .replace("<br>", "\n")
                .replace("<br/>", "\n")
                .replace("<br />", "\n")
            )

            # Salva no histórico já limpo
            self.historico.append({
                "role": "assistant",
                "content": resposta_ia
            })

            return resposta_ia

        except Exception as e:

            print(f"Erro na API da Groq: {e}")

            if "invalid_api_key" in str(e).lower():
                return "Erro de autenticação: verifique sua GROQ_API_KEY."

            elif "rate_limit" in str(e).lower():
                return "Limite de requisições atingido."

            else:
                return "Erro ao processar solicitação."


if __name__ == "__main__":

    ia_service = IAService()

    prompt_mestre_exemplo = (
        "Você é um assistente pessoal que responde de forma simples."
    )

    print("Enviando mensagem de teste para a IA...")

    resposta = ia_service.enviar_mensagem(
        "O que é uma variável em Python?",
        prompt_mestre_exemplo
    )

    print("\nResposta da IA:")
    print(resposta)