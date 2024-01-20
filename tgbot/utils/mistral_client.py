from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage

spam_texts = "\n".join(
    [
        """Есть новая Тема
Возьмем 1 человечка 
От 200-300+ долларов  в  день
Работа со своим капиталом 
1-2 часа занятость 
Интересно?: Пишите + в ЛС""",
        """ИЩУ ЛЮДEЙ В КOМAНДУ НA НOВЫЙ ПPOEKT 21+
ТЕСТUРОВЩUК CETU МOНET 💥

🟢Бесплатное обученuе noлнoстью с нyля;
📌nотенцuал дoxoдa: 2000 $ в неделю

напuшu мне""",
        """Ecть yдaлeнка на пocтояннoй oснoвe! Дoxoд oт 85$ в дeнь и вышe. Пиши + в лс и yзнaвaй пoдpoбнocти.
18+""",
        """Есть удалённая работа для вас
Работа в сфере общения 
Зарплата от 200$ за неделю
Пишите всё обсудим""",
        """"Реальная Тема
270+ Баксов в день 
(  С телефона или ПК )
2 часа в день занятость 
Пиши + в ЛС за подробностями""",
        """Pocceльxoзбaнк дарит 6000 рублей каждому клиенту.
 
Получить - https://link...""",
        """Привет! Новая сфера, удаленный заработок прямо с дома! 
Для работы нужен только телефон или пк! 
Занятость 1-2 часа в день! 
Заработок от 9000 руб. в день! 
Пишите в лс 🔥""",
    ]
)


async def check_spam(mistral_client: MistralAsyncClient, text: str) -> bool:
    chat_response = await mistral_client.chat(
        model="mistral-tiny",
        messages=[
            ChatMessage(
                role="user",
                content=f"""You're a professional spam detector, you have to detect if the following text is spam or not. Answer ONLY with Y/N, NOTHING ELSE. 
You have to detect only similar spam texts like these ones:
{spam_texts}
Here's the text to analyze: {text}""",
            )
        ],
        max_tokens=1,
    )
    # Assuming the response is just 'Y' or 'N'
    return chat_response.choices[0].message.content == "Y"
