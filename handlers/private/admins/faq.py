from database.models import CategoryModel, QuestionModel
from . import *
from .general import get_menu_reply_keyboard

# __router__ !DO NOT DELETE!
faq_router = Router()


# __states__ !DO NOT DELETE!
class UpdateStates(StatesGroup):
    get_category = State()  # отлавливает категорию
    get_question = State()
    get_content = State()


class CategoryStates(StatesGroup):
    get_category = State()
    get_content = State()


class QuestionStates(StatesGroup):
    get_category = State()
    get_question = State()
    get_content = State()


# __buttons__ !DO NOT DELETE!
async def get_categories_menu_inline_keyboard(
    lang: str, is_admin: bool = False
    ) -> InlineKeyboardMarkup:
    button_list = []

    categories = await db.categories.get_all()
    if categories:
        for category in categories:
            category_id = category.id
            category_name = category.name
            button_list.append(
                [InlineKeyboardButton(
                    text=str(category_name),
                    callback_data=f'category {category_id} {int(is_admin)}'
                    )]
            )

    if is_admin:
        button_list.append(
            [InlineKeyboardButton(
                text=strs(lang=lang).add_category_btn,
                callback_data='add_category_btn'
                )]
        )

    @faq_router.callback_query(F.data.startswith('add_category_btn'))
    async def handle_add_category_button_callback(
        callback: CallbackQuery,
        state: FSMContext):
        bot_logger.info(
            f'Handling category add button callback from user {callback.message.chat.id}'
            )
        from . import get_decline_reply_keyboard

        await callback.message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
                ).faq_ask_category,
            reply_markup=await get_decline_reply_keyboard(
                lang=(await state.get_data())['lang']
                )
        )

        await state.set_state(CategoryStates.get_category)
        await callback.message.delete()
        await callback.answer()

    @faq_router.message(CategoryStates.get_category)
    async def handle_add_category_name(
        message: Message,
        state: FSMContext):
        bot_logger.info(
            f'Handling states CategoryStates.get_category_name from user {message.chat.id}'
            )
        category_name = message.text.strip()

        # Проверка наличия категории в базе
        existing_category = await db.categories.get_by_name(category_name)
        if existing_category:
            await message.answer(
                text=strs(
                    lang=(await state.get_data())['lang']
                    ).faq_category_exist
                )
            return

        # Сохранение имени категории в состоянии
        await state.update_data(category_name=category_name)
        await message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
                ).faq_ask_content
            )
        await state.set_state(CategoryStates.get_content)

    @faq_router.message(CategoryStates.get_content)
    async def handle_add_category_content(
        message: Message,
        state: FSMContext):
        bot_logger.info(
            f'Handling states UpdateStates.get_question from user {message.chat.id}'
            )
        category_content = message.text

        # Сохранение описания категории в состоянии
        await state.update_data(category_content=category_content)
        data = await state.get_data()
        category_name = data['category_name']
        category_content = data['category_content']
        new_category = CategoryModel(
            name=str(category_name),
            description=str(category_content),
        )
        await db.categories.insert(new_category)

        # from .general import get_menu_reply_keyboard
        await message.answer(
            text=strs(lang=(await state.get_data())['lang']).data_update,
            reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
        )
        await state.clear()

    @faq_router.callback_query(F.data.startswith('category'))
    async def handle_category_button_callback(
        callback: CallbackQuery,
        state: FSMContext
        ):
        bot_logger.info(
            f'Handling category button callback from user {callback.message.chat.id}'
            )
        data = callback.data.split()

        await callback.answer()

        category_id, is_admin = int(data[1]), bool(int(data[2]))

        category = await db.categories.get_by_id(category_id)

        if category:
            description = category.description
            await callback.message.delete()
            await callback.message.answer(
                str(description),
                reply_markup=await get_questions_menu_inline_keyboard(
                    lang=(await state.get_data())['lang'],
                    category_id=category_id,
                    is_admin=is_admin
                    )
                )
            await callback.answer()
        else:
            await callback.answer(
                'Категория не найдена. Перезапустите бота',
                show_alert=True,
            )

    return InlineKeyboardMarkup(inline_keyboard=button_list)


async def get_questions_menu_inline_keyboard(
        lang: str, category_id: int,
        is_admin: bool = False
    ) -> InlineKeyboardMarkup:

    button_list = []
    questions = await db.questions.get_all_by_id(category_id)
    if questions:
        for question in questions:
            question_id = question.id
            question_name = question.name
            button_list.append(
                [InlineKeyboardButton(
                    text=str(question_name),
                    callback_data=f'question {question_id} {int(is_admin)} {category_id}'
                )]
            )
    if is_admin:
        button_list.append(
            [InlineKeyboardButton(
                text=strs(lang=lang).add_question_btn,
                callback_data=f'add_question_btn {category_id}'
                )]
        )

    @faq_router.callback_query(F.data.startswith('question'))
    async def handle_question_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(f'Handling question button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        question_id = int(data[1])

        question = await db.questions.get_by_id(question_id)
        if question:
            await callback.message.delete()
            answer = question.answer
            await callback.message.answer(str(answer))
            await callback.answer()
        else:
            await callback.answer(
                'Вопрос не найден. Попробуйте еще раз',
                show_alert=True,
            )

    @faq_router.callback_query(F.data.startswith('add_question_btn'))
    async def handle_add_question_button_callback(
        callback: CallbackQuery,
        state: FSMContext):
        bot_logger.info(
            f'Handling question add button callback from user {callback.message.chat.id}'
        )

        # todo fix import
        from . import get_decline_reply_keyboard

        data = callback.data.split()
        category_id = int(data[1])

        await callback.message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
                ).faq_ask_question,
            reply_markup=await get_decline_reply_keyboard(
                lang=(await state.get_data())['lang']
                )
        )
        await state.update_data(category_id=category_id)
        await state.set_state(QuestionStates.get_question)
        await callback.message.delete()
        await callback.answer()

    @faq_router.message(QuestionStates.get_question)
    async def handle_add_question_name(
        message: Message,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling states QuestionStates.get_question_name from user {message.chat.id}'
            )
        question_name = message.text

        await state.update_data(question_name=question_name)
        await message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
                ).faq_ask_content
            )
        await state.set_state(QuestionStates.get_content)

    @faq_router.message(QuestionStates.get_content)
    async def handle_add_question_answer(
        message: Message,
        state: FSMContext,
    ):
        bot_logger.info(
            f'Handling states UpdateStates.get_question from user {message.chat.id}'
        )
        question_content = message.text

        await state.update_data(question_content=question_content)
        data = await state.get_data()

        question_name = data['question_name']
        question_content = data['question_content']
        category_id = data['category_id']

        new_question = QuestionModel(
            category_id=int(category_id),
            name=str(question_name),
            answer=str(question_content),
        )
        await db.questions.insert(new_question)

        # from .general import get_menu_reply_keyboard
        await message.answer(
            text=strs(lang=(await state.get_data())['lang']).data_update,
            reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
        )
        await state.clear()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


# async def get_category_details_inline_keyboard(
#     lang: str, category_id: str, is_admin: bool
#     ) -> InlineKeyboardMarkup:
#     button_list = []
#     if is_admin:
#         button_list.append(
#             [InlineKeyboardButton(text=strs(lang=lang).update_btn_category, callback_data=f'update_btn category {category_id}'),
#              InlineKeyboardButton(text=strs(lang=lang).update_btn_category_description, callback_data=f'update_btn content {category_id}')],
#         )
#         button_list.append(
#             [InlineKeyboardButton(text=strs(lang=lang).remove_btn, callback_data=f'remove_btn {category_id} {int(is_admin)}'),
#              InlineKeyboardButton(text=strs(lang=lang).update_btn, callback_data=f'question_update {category_id} {int(is_admin)}')]
#         )
#     button_list.append(
#         [InlineKeyboardButton(text=strs(lang=lang).back_btn, callback_data=f'back_btn {int(is_admin)}')],
#     )
#
#     @faq_router.callback_query(F.data.startswith('question_update'))
#     async def handle_question_update_button_callback(callback: CallbackQuery, state: FSMContext):
#         bot_logger.info(f'Handling faq_details question update button callback from user {callback.message.chat.id}')
#         data = callback.data.split()
#         question_id, is_admin = data[1], bool(int(data[2]))
#
#         faq = await db.preferences.get_by_key(key='faq')
#         questions = faq.value.get('questions')
#         question = [question for question in questions if question['question_id'] == question_id][0]
#
#         await callback.message.delete()
#         message = Message(**question['content'])
#         await message.send_copy(
#             chat_id=callback.message.chat.id,
#             reply_markup=await get_faq_details_inline_keyboard(
#                 lang=(await state.get_data())['lang'], question_id=question_id, is_admin=is_admin
#             )
#         ).as_(callback.bot)
#
#         await callback.answer()
#
#     @faq_router.callback_query(F.data.startswith('update_btn'))
#     async def handle_update_button_callback(callback: CallbackQuery, state: FSMContext):
#         bot_logger.info(f'Handling faq_details update button callback from user {callback.message.chat.id}')
#         data = callback.data.split()
#         action, question_id = data[1], data[2]
#
#         await state.update_data({'question_id': question_id})
#         if action == 'question':
#             await callback.message.answer(text=strs(lang=(await state.get_data())['lang']).faq_ask_question)
#             await state.set_state(UpdateStates.get_question.state)
#         elif action == 'content':
#             await callback.message.answer(text=strs(lang=(await state.get_data())['lang']).faq_ask_content)
#             await state.set_state(UpdateStates.get_content.state)
#
#         await callback.answer()
#
#     @faq_router.callback_query(F.data.startswith('remove_btn'))
#     async def handle_remove_button_callback(callback: CallbackQuery, state: FSMContext):
#         bot_logger.info(f'Handling faq_details remove button callback from user {callback.message.chat.id}')
#         data = callback.data.split()
#         question_id, is_admin = data[1], bool(int(data[2]))
#
#         faq = await db.preferences.get_by_key(key='faq')
#         questions = faq.value.get('questions')
#         remove_idx = -1
#         for idx, question in enumerate(questions):
#             if question.get('question_id') == question_id:
#                 remove_idx = idx
#         if remove_idx >= 0:
#             del questions[remove_idx]
#
#         faq.value['questions'] = questions
#         await db.preferences.update(preference=faq)
#
#         await callback.message.delete()
#         await callback.message.answer(
#             text=strs(lang=(await state.get_data())['lang']).faq_questions,
#             reply_markup=await get_faq_menu_inline_keyboard(lang=(await state.get_data())['lang'], is_admin=is_admin)
#         )
#         await callback.answer()
#
#     @faq_router.callback_query(F.data.startswith('back_btn'))
#     async def handle_back_button_callback(callback: CallbackQuery, state: FSMContext):
#         bot_logger.info(f'Handling faq_details back button callback from user {callback.message.chat.id}')
#         data = callback.data.split()
#         is_admin = bool(int(data[1]))
#
#         await callback.message.delete()
#         await callback.message.answer(
#             text=strs(lang=(await state.get_data())['lang']).faq_questions,
#             reply_markup=await get_faq_menu_inline_keyboard(lang=(await state.get_data())['lang'], is_admin=is_admin)
#         )
#         await callback.answer()
#
#     return InlineKeyboardMarkup(inline_keyboard=button_list)


# async def get_faq_menu_inline_keyboard(lang: str, is_admin: bool = False) -> InlineKeyboardMarkup:
#     button_list = []

#     faqs = await db.preferences.get_by_key(key='faq')
#     questions = faqs.value.get('questions')
#     if questions:
#         for question in questions:
#             question_id = question.get('question_id')
#             question_text = question.get('question')
#             button_list.append(
#                 [InlineKeyboardButton(text=question_text, callback_data=f'faq {question_id} {int(is_admin)}')]
#             )

#     if is_admin:
#         button_list.append(
#             [InlineKeyboardButton(text=strs(lang=lang).add_btn, callback_data='add_btn')]
#         )

# 1. Нарисовать список категорий
# 2. В категории что отправляет (ID?)
# 3. Нарисовать еще клавиатуру который показывает список вопросов по ID категории
# 4. [InlineKeyboardButton(text=question_text, callback_data=f'faq {question_id} {int(is_admin)}')]
# 5. Найти где создавайть вопрос и добавить туда возможность категории
    # @faq_router.callback_query(F.data.startswith('faq'))
    # async def handle_faq_button_callback(callback: CallbackQuery, state: FSMContext):
    #     bot_logger.info(f'Handling question faq button callback from user {callback.message.chat.id}')
    #     data = callback.data.split()
    #     category_id, is_admin = data[1], bool(int(data[2]))

    #     categories = await db.categories.get_by_id('category_id')
    #     categories = faq.value['questions']
    #     question = [question for question in questions if question['question_id'] == question_id][0]
    #     content = question.get('content', 'Отсутствует')

    #     await callback.message.delete()
    #     message = Message(**content)
    #     await message.send_copy(
    #         chat_id=callback.message.chat.id,
    #         reply_markup=await get_faq_details_inline_keyboard(
    #             lang=(await state.get_data())['lang'], question_id=question_id, is_admin=is_admin
    #         )
    #     ).as_(callback.bot)
    #     await callback.answer()

# __chat__ !DO NOT DELETE!
@general_router.message(
    filters.Private(),
    ((F.text == '/change_faq') | (F.text.in_(change_faq_btn)) |
     (F.text.in_(faq_btn)) | (F.text == '/faq'))
)
async def handle_faq_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /faq from user {message.chat.id}')
    user = await db.users.get_by_id(user_id=message.chat.id)
    is_admin = user.status == 'admin'
    lang = (await state.get_data())['lang']
    await message.answer(
        text=strs(lang=lang).faq_category,
        reply_markup=await get_categories_menu_inline_keyboard(
            lang=lang,
            is_admin=is_admin
            )
        )


# """ПОУЧЕНИЯ КАТЕГОРИИ"""
# @faq_router.message(CategoryStates.get_category)
# async def handle_get_category_state(message: Message, state: FSMContext):
#     bot_logger.info(f'Handling states CategoryStates.get_category from user {message.chat.id}')
#     category_name = message.text

#     if category_name:
#         await state.update_data({'category_name': category_name})
#         lang = (await state.get_data())['lang']
#         await message.answer(
#             text=strs(lang=lang).faq_ask_content,
#             reply_markup=types.ReplyKeyboardRemove()
#         )
#         await CategoryStates.get_content.set()
#     else:
#         await message.answer(
#             text=strs(lang=lang).faq_ask_category_error
#         )


# """ПОЛУЧЕНИЕ КОНТЕНТА ВОПРОСА"""
# @faq_router.message(FaqStates.get_content)
# async def handle_get_content_state(message: Message, state: FSMContext):
#     bot_logger.info(f'Handling states FaqStates.get_content from user {message.chat.id}')
#     question_id = str(uuid4())[:10]

#     message_info = loads(dumps(message.model_dump(), cls=CustomJSONEncoder))
#     data = await state.get_data()
#     question = data['question']

#     faq = await db.preferences.get_by_key('faq')
#     faq.value.get('questions').append({
#         'question_id': question_id,
#         'question': question,
#         'content': message_info
#     })
#     await db.preferences.update(preference=faq)

#     from .general import get_menu_reply_keyboard

#     await message.answer(
#         text=strs(lang=(await state.get_data())['lang']).faq_added,
#         reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
#     )
#     await state.clear()


# """ОБНОВЛЕНИЕ НАЗВАНИЯ ВОПРОСА"""
# @faq_router.message(UpdateStates.get_question)
# async def handle_get_update_question_state(message: Message, state: FSMContext):
#     bot_logger.info(f'Handling states UpdateStates.get_question from user {message.chat.id}')
#     data = await state.get_data()
#     question_id = data['question_id']

#     question_text = message.text
#     if question_text:
#         faq = await db.preferences.get_by_key('faq')
#         for idx, question in enumerate(faq.value['questions']):
#             q_id = question.get('question_id')
#             if q_id == question_id:
#                 faq.value['questions'][idx] = {
#                     'question_id': question_id,
#                     'question': question_text,
#                     'content': question.get('content')
#                 }
#                 await db.preferences.update(preference=faq)
#                 break

#         from .general import get_menu_reply_keyboard
#         await message.answer(
#             text=strs(lang=(await state.get_data())['lang']).data_update,
#             reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
#         )
#         await state.clear()
#     else:
#         await message.answer(text=strs(lang=(await state.get_data())['lang']).faq_ask_question_error)


# """ ОБНОВЛЕНИЕ СОДЕРЖАНИЯ ВОПРОСА"""
# @faq_router.message(UpdateStates.get_content)
# async def handle_get_update_content_state(message: Message, state: FSMContext):
#     bot_logger.info(f'Handling states UpdateStates.get_content from user {message.chat.id}')
#     data = await state.get_data()
#     question_id = data['question_id']

#     message_info = loads(dumps(message.model_dump(), cls=CustomJSONEncoder))
#     faq = await db.preferences.get_by_key('faq')
#     for idx, question in enumerate(faq.value['questions']):
#         q_id = question.get('question_id')
#         if q_id == question_id:
#             faq.value['questions'][idx] = {
#                 'question_id': question_id,
#                 'question': question.get('question'),
#                 'content': message_info
#             }
#             await db.preferences.update(preference=faq)
#             break

#     from .general import get_menu_reply_keyboard
#     await message.answer(
#         text=strs(lang=(await state.get_data())['lang']).data_update,
#         reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
#     )
#     await state.clear()
