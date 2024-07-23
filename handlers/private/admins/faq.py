from database.models import CategoryModel, QuestionModel
from . import *
from .general import get_menu_reply_keyboard

# __router__ !DO NOT DELETE!
faq_router = Router()


# __states__ !DO NOT DELETE!
class UpdateStates(StatesGroup):
    get_category = State()
    get_question = State()
    get_content = State()


class CategoryUpdateStates(StatesGroup):
    get_category = State()
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
            button_list.append([
                InlineKeyboardButton(
                    text=str(question_name),
                    callback_data=f'question {question_id} {int(is_admin)} {category_id}'
                )
            ])
    if is_admin:
        button_list.append([
            InlineKeyboardButton(
                text=strs(lang=lang).add_question_btn,
                callback_data=f'add_question_btn {category_id}'
                ),
            InlineKeyboardButton(
                text=strs(lang=lang).edit_category_btn,
                callback_data=f'edit_category_btn {category_id} {int(is_admin)}'
                ),
            ])
    button_list.append([
        InlineKeyboardButton(
                text=strs(lang=lang).back_to_categories_btn,
                callback_data=f'back_to_categories_btn {category_id} {int(is_admin)}'
        ),
    ])

    @faq_router.callback_query(F.data.startswith('question'))
    async def handle_question_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(f'Handling question button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        question_id, is_admin, category_id = (
            int(data[1]),
            bool(int(data[2])),
            int(data[3])
        )

        question = await db.questions.get_by_id(question_id)
        if question:
            await callback.message.delete()
            answer = question.answer
            await callback.message.answer(
                str(answer),
                reply_markup=await get_question_details_inline_keyboard(
                    lang=(await state.get_data())['lang'],
                    question_id=question_id,
                    category_id=category_id,
                    is_admin=is_admin
                )
            )
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

    @faq_router.callback_query(F.data.startswith('back_to_categories_btn'))
    async def handle_back_to_categories_button_callback(
        callback: CallbackQuery,
        state: FSMContext):
        bot_logger.info(
            f'Handling back button callback from user {callback.message.chat.id}'
        )
        data = callback.data.split()
        is_admin = bool(int(data[2]))
        await callback.message.delete()
        await callback.message.answer(
            text=strs(lang=lang).faq_category,
            reply_markup=await get_categories_menu_inline_keyboard(
                lang=lang,
                is_admin=is_admin
            )
        )
        await callback.answer()

    @faq_router.callback_query(F.data.startswith('edit_category_btn'))
    async def handle_edit_category_button_callback(
        callback: CallbackQuery,
        state: FSMContext):
        bot_logger.info(
            f'Handling back button callback from user {callback.message.chat.id}'
        )
        data = callback.data.split()
        category_id, is_admin = int(data[1]), bool(int(data[2]))
        category = await db.categories.get_by_id(category_id)
        description = category.description

        await callback.message.delete()
        await callback.message.answer(
            text=str(description),
            reply_markup=await get_category_details_inline_keyboard(
                lang=lang,
                category_id=category_id,
                is_admin=is_admin
            )
        )
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

        await message.answer(
            text=strs(lang=(await state.get_data())['lang']).data_update,
            reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
        )
        await state.clear()

    return InlineKeyboardMarkup(inline_keyboard=button_list)

async def get_question_details_inline_keyboard(
    lang: str, question_id: int, category_id: int, is_admin: bool
    ) -> InlineKeyboardMarkup:
    button_list = []
    if is_admin:
        button_list.append([
            InlineKeyboardButton(
                text=strs(lang=lang).update_btn_question,
                callback_data=f'update_question_btn {question_id} {int(is_admin)} {category_id}'
            ),
            InlineKeyboardButton(
                text=strs(lang=lang).update_btn_content,
                callback_data=f'update_content_btn {question_id} {int(is_admin)} {category_id}'
            ),
        ],)
        button_list.append([
            InlineKeyboardButton(
                text=strs(lang=lang).remove_btn,
                callback_data=f'remove_btn {question_id} {int(is_admin)} {category_id}'
            ),
            InlineKeyboardButton(
                text=strs(lang=lang).update_btn,
                callback_data=f'q_update {question_id} {int(is_admin)} {category_id}'
            ),
        ],)
    button_list.append([
        InlineKeyboardButton(
            text=strs(lang=lang).back_btn,
            callback_data=f'back_btn {question_id} {int(is_admin)} {category_id}'
        )
    ],)

    @faq_router.callback_query(F.data.startswith('back_btn'))
    async def handle_back_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling faq_details back button callback from user {callback.message.chat.id}'
        )
        data = callback.data.split()
        is_admin, category_id = bool(int(data[2])), int(data[3])
        category = await db.categories.get_by_id(category_id)
        description = str(category.description)

        await callback.message.delete()
        await callback.message.answer(
            text=description,
            reply_markup=await get_questions_menu_inline_keyboard(
                lang=(await state.get_data())['lang'],
                category_id=category_id,
                is_admin=is_admin
            )
        )
        await callback.answer()

    @faq_router.callback_query(F.data.startswith('remove_btn'))
    async def handle_remove_question_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling question_details remove button callback from user {callback.message.chat.id}'
        )
        data = callback.data.split()
        question_id, is_admin, category_id = int(data[1]), bool(int(data[2])), int(data[3])
        question = await db.questions.get_by_id(question_id)
        category = await db.categories.get_by_id(category_id)
        description = str(category.description)

        await db.questions.delete(question)
        await callback.message.delete()
        await callback.message.answer(
            text=description,
            reply_markup=await get_questions_menu_inline_keyboard(
                lang=(await state.get_data())['lang'],
                category_id=category_id,
                is_admin=is_admin
            )
        )
        await callback.answer()

    @faq_router.callback_query(F.data.startswith('update_question_btn'))
    async def handle_update_question_name_button_callback(
        callback: CallbackQuery,
        state: FSMContext):
        bot_logger.info(
            f'Handling update question name button callback from user {callback.message.chat.id}'
            )
        from . import get_decline_reply_keyboard

        data = callback.data.split()
        question_id, is_admin, category_id = int(data[1]), bool(int(data[2])), int(data[3])

        await callback.message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).faq_ask_question,
            reply_markup=await get_decline_reply_keyboard(
                lang=(await state.get_data())['lang']
            )
        )
        await state.update_data(
            category_id=category_id,
            is_admin=is_admin,
        )
        await state.set_state(UpdateStates.get_question)
        await callback.message.delete()

    @faq_router.message(UpdateStates.get_question)
    async def handle_update_get_question_state(
        message: Message,
        state: FSMContext):
        bot_logger.info(
            f'Handling states UpdateStates.get_question_name from user {message.chat.id}'
        )
        question_name = message.text
        data = await state.get_data()
        is_admin = bool(int(data['is_admin']))

        await state.update_data(question_name=question_name)
        await message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).data_update,
            reply_markup=await get_question_details_inline_keyboard(
                lang=(await state.get_data())['lang'],
                question_id=question_id,
                category_id=category_id,
                is_admin=is_admin
            )
        )

    @faq_router.callback_query(F.data.startswith('update_content_btn'))
    async def handle_update_question_content_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling update content question button callback from user {callback.message.chat.id}'
            )
        from . import get_decline_reply_keyboard

        data = callback.data.split()
        question_id, is_admin, category_id = (
            int(data[1]),
            bool(int(data[2])),
            int(data[3])
        )
        await callback.message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).faq_ask_content,
            reply_markup=await get_decline_reply_keyboard(
                lang=(await state.get_data())['lang']
            )
        )
        await state.update_data(
            category_id=category_id,
            is_admin=is_admin,
        )
        await state.set_state(UpdateStates.get_content)

    @faq_router.message(UpdateStates.get_content)
    async def handle_update_get_question_content_state(
        message: Message,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling states UpdateStates.get_question_content from user {message.chat.id}'
            )
        question_content = message.text
        data = await state.get_data()
        is_admin = bool(int(data['is_admin']))

        await state.update_data(question_content=question_content)
        await message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).data_update,
            reply_markup=await get_question_details_inline_keyboard(
                lang=(await state.get_data())['lang'],
                question_id=question_id,
                category_id=category_id,
                is_admin=is_admin
            )
        )

    @faq_router.callback_query(F.data.startswith('q_update'))
    async def handle_question_update_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling update question from user {callback.message.chat.id}'
        )
        await callback.answer()
        state_data = await state.get_data()
        callback_data = callback.data.split()
        question_id = int(callback_data[1])

        question_name = state_data.get('question_name')
        question_answer = state_data.get('question_content')

        update_data = {}
        if question_name is not None:
            update_data['name'] = question_name
        if question_answer is not None:
            update_data['answer'] = question_answer

        if update_data:
            await db.questions.update(question_id, update_data)
            await callback.message.delete()
            await callback.message.answer(
                text=strs(
                    lang=(await state.get_data())['lang']
                ).data_update,
                reply_markup=await get_questions_menu_inline_keyboard(
                    lang=(await state.get_data())['lang'],
                    category_id=category_id,
                    is_admin=is_admin
                )
            )
            await state.clear()
        else:
            await callback.message.delete()
            await callback.message.answer(
                text=strs(
                    lang=(await state.get_data())['lang']
                ).data_update_empty,
                reply_markup=await get_question_details_inline_keyboard(
                    lang=(await state.get_data())['lang'],
                    question_id=question_id,
                    category_id=category_id,
                    is_admin=is_admin
                )
            )
            await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)

async def get_category_details_inline_keyboard(
    lang: str, category_id: int, is_admin: bool
    ) -> InlineKeyboardMarkup:
    button_list = []
    if is_admin:
        button_list.append([
            InlineKeyboardButton(
                text=strs(lang=lang).update_btn_category,
                callback_data=f'update_category_btn {category_id} {int(is_admin)}'
            ),
            InlineKeyboardButton(
                text=strs(lang=lang).update_btn_category_content,
                callback_data=f'update_category_content_btn {category_id} {int(is_admin)}'
            )
        ],)
        button_list.append([
            InlineKeyboardButton(
                text=strs(lang=lang).remove_btn,
                callback_data=f'remove_category_btn {category_id} {int(is_admin)}'
            ),
            InlineKeyboardButton(
                text=strs(lang=lang).update_btn,
                callback_data=f'c_update {category_id} {int(is_admin)}')
        ],)
    button_list.append([
        InlineKeyboardButton(
            text=strs(lang=lang).back_btn,
            callback_data=f'category {category_id} {int(is_admin)}'
        )
    ],)


    """МФункция работает не корректно"""
    @faq_router.callback_query(F.data.startswith('remove_category_btn'))
    async def handle_remove_category_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling category_details remove button callback from user {callback.message.chat.id}'
        )
        data = callback.data.split()
        category_id, is_admin = int(data[1]), bool(int(data[2]))

        await db.categories.delete(category_id)
        await callback.message.delete()
        await callback.message.answer(
            text=strs(lang=lang).faq_category,
            reply_markup=await get_categories_menu_inline_keyboard(
                lang=lang,
                is_admin=is_admin
            )
        )
        await callback.answer()

    @faq_router.callback_query(F.data.startswith('update_category_btn'))
    async def handle_update_category_name_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling update category name button callback from user {callback.message.chat.id}'
            )
        from . import get_decline_reply_keyboard

        data = callback.data.split()
        category_id, is_admin = int(data[1]), bool(int(data[2]))

        await callback.message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).faq_ask_category,
            reply_markup=await get_decline_reply_keyboard(
                lang=(await state.get_data())['lang']
            )
        )
        await state.update_data(
            category_id=category_id,
            is_admin=is_admin,
        )
        await state.set_state(CategoryUpdateStates.get_category)
        await callback.message.delete()

    @faq_router.message(CategoryUpdateStates.get_category)
    async def handle_update_get_category_state(
        message: Message,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling states CategoryUpdateStates.get_category from user {message.chat.id}'
        )
        category_name = message.text
        data = await state.get_data()
        is_admin = bool(int(data['is_admin']))

        await state.update_data(category_name=category_name)
        await message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).data_update,
            reply_markup=await get_category_details_inline_keyboard(
                lang=(await state.get_data())['lang'],
                category_id=category_id,
                is_admin=is_admin
            )
        )

    @faq_router.callback_query(F.data.startswith('update_category_content_btn'))
    async def handle_update_category_content_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling update category content button callback from user {callback.message.chat.id}'
            )
        from . import get_decline_reply_keyboard

        data = callback.data.split()
        category_id, is_admin = int(data[1]), bool(int(data[2]))
        await callback.message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).faq_ask_content,
            reply_markup=await get_decline_reply_keyboard(
                lang=(await state.get_data())['lang']
            )
        )
        await state.update_data(
            category_id=category_id,
            is_admin=is_admin,
        )
        await state.set_state(CategoryUpdateStates.get_content)

    @faq_router.message(CategoryUpdateStates.get_content)
    async def handle_update_get_content_state(
        message: Message,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling state CategoryUpdateStates.get_content from user {message.chat.id}'
            )
        category_content = message.text
        data = await state.get_data()
        is_admin = bool(int(data['is_admin']))

        await state.update_data(category_content=category_content)
        await message.answer(
            text=strs(
                lang=(await state.get_data())['lang']
            ).data_update,
            reply_markup=await get_category_details_inline_keyboard(
                lang=(await state.get_data())['lang'],
                category_id=category_id,
                is_admin=is_admin
            )
        )

    @faq_router.callback_query(F.data.startswith('c_update'))
    async def handle_category_update_button_callback(
        callback: CallbackQuery,
        state: FSMContext
    ):
        bot_logger.info(
            f'Handling update category from user {callback.message.chat.id}'
        )
        await callback.answer()
        state_data = await state.get_data()
        callback_data = callback.data.split()
        category_id = int(callback_data[1])

        category_name = state_data.get('category_name')
        category_description = state_data.get('category_content')

        update_data = {}
        if category_name is not None:
            update_data['name'] = category_name
        if category_description is not None:
            update_data['description'] = category_description

        if update_data:
            await db.categories.update(category_id, update_data)
            await callback.message.delete()
            await callback.message.answer(
                text=strs(
                    lang=(await state.get_data())['lang']
                ).data_update,
                reply_markup=await get_categories_menu_inline_keyboard(
                    lang=lang,
                    is_admin=is_admin
                )
            )
            await state.clear()
        else:
            await callback.message.delete()
            await callback.message.answer(
                text=strs(
                    lang=(await state.get_data())['lang']
                ).data_update_empty,
                reply_markup=await get_category_details_inline_keyboard(
                    lang=(await state.get_data())['lang'],
                    category_id=category_id,
                    is_admin=is_admin
                )
            )
            await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


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
