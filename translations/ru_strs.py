class RuTranslation:
    # Buttons
    decline_btn = 'Отмена ❌'
    month_btn_1 = 'От 1️⃣ месяца'
    month_btn_3 = 'От 3️⃣ месяцев'
    month_btn_6 = 'От 6️⃣ месяцев'
    month_btn_12 = 'От года 🗓️'
    notification_btn_on = 'Включить уведомления 🔊'
    notification_btn_off = 'Выключить уведомления 🔇'
    update_btn_category = 'Обновить категорию'
    update_btn_question = 'Обновить вопрос ❓'
    update_btn_category_description = 'Обновить описание 📝'
    update_btn_content = 'Обновить контент 📝'
    remove_btn = 'Удалить 🗑️'
    update_btn = 'Обновить 🔄'
    back_btn = 'Назад 🔙'
    delete_btn = 'Закрыть 🚫'
    delete_tickets_btn = 'Удалить тикеты 🗑️'
    add_category_btn = 'Добавить ➕'
    add_question_btn = 'Добавить ❓'
    change_faq_btn = 'Изменить FAQ ❓'
    faq_btn = 'FAQ ❓'
    change_subscription_channel_btn = 'Изменить канал подписки 🌐'
    find_user_btn = 'Найти пользователя 🔎'
    my_tickets_btn = 'Мои тикеты 📂'
    user_tickets_btn = 'Тикеты пользователя 📂'
    send_mailing_btn = 'Отправить рассылку 📬'
    send_mailing_message_btn = 'Отправить 📨'
    mailing_add_link_btn = 'Добавить ссылку 🌐'
    mailing_delete_btn = 'Убрать меню ❌'
    start_msg_btn = 'Стартовое сообщение 💬'
    change_close_release_btn = 'Изменить время авто осовобождения/закрытия 🕒'
    manager_mode_btn = 'Режим менеджера 💼'
    admin_mode_btn = 'Режим администратора 😎'
    change_channel_info_btn = 'Изменить данные канала 🔄'
    change_channel_button_name_btn = 'Изменить название кнопки пользователей 🖲️'
    make_subscription_necessary_btn = 'Сделать подписку обязательной 🔔'
    make_subscription_unnecessary_btn = 'Сделать подписку необязательной 🔕'
    remove_menu_btn = 'Убрать меню 🚫'
    opened_tickets_btn = 'Открытые беседы 💬'
    create_ticket_btn = 'Создать тикет 💬'
    press_update_btn = ' Нажмите на кнопку "Обновить 🔄"'
    change_ticket_description_btn = 'Изменить описание 📝'
    change_ticket_title_btn = 'Изменить тему беседы 🏷️'
    mute_btn = 'Ограничить 🤐'
    history_btn = 'История 💬'
    commentary_btn = 'Комментарий ✍'
    ticket_data_btn = 'Данные беседы 🔄'
    release_ticket_btn = 'Освободить 🙅🏻‍♂️'
    archive_btn = 'Архив 🗄️'
    user_info_btn = 'Информация о пользователе ℹ️'
    accept_btn = 'Принять ✅'
    hide_btn = 'Спрятать 🗂️'
    ban_btn = 'Забанить ⛔'
    unban_btn = 'Разбанить 🟢'
    make_ordinary_btn = 'Сделать обычным пользователем 👤'
    make_manager_btn = 'Сделать менеджером 👨🏻‍💻'
    check_subscription_btn = 'Проверить подписку 🔔'
    choose_lang_btn = 'Язык 🌎'

    reply_buttons = [
        decline_btn, delete_tickets_btn, change_faq_btn, faq_btn, change_subscription_channel_btn,
        find_user_btn, my_tickets_btn, send_mailing_btn, start_msg_btn, change_close_release_btn,
        manager_mode_btn, admin_mode_btn, opened_tickets_btn, create_ticket_btn, choose_lang_btn
    ]

    # Composite
    release_composite = '<b>Беседа освобождается от менеджера</b>, если последние действие было более {} ч. назад \n\n'
    close_composite = '<b>Беседа закрывается</b>, если последние действие было более {} ч. назад\n\n'
    ticket_data_composition = '<b>Тикет:</b> {}\n\n<b>Создан:</b> {} по МСК\n\n<b>Закрыт:</b> {} по МСК\n\n<b>Имя пользователя:</b> {}\n\n<b>Тема беседы:</b> {}\n\n<b>Описание беседы:</b> {}\n\n<b>Комментарий:</b> {}'
    manager_released_ticket_composition = '<b>Менеджер освободил тикет!</b>\n\n'
    user_found = '<b>Пользователь найден!</b>'
    current_ticket_comment_composition = '<b>Текущий тикет:</b>\n\n{}\n\n<b>Комментарий: </b>{}'
    current_ticket_composition = '<b>Текущий тикет:</b>\n\n{}'

    tickets_info = lambda is_extended: ''.join(('<b>Беседа:</b> {}\n',
                                        '<b>Создан:</b> {} по МСК\n',
                                        '<b>Закрыт:</b> {} по МСК\n',
                                        '<b>Имя пользователя:</b> {}\n',
                                        '<b>Ссылка пользователя:</b> @{}\n',
                                        '<b>Имя ТГ:</b> {}\n',
                                        '<b>Тема беседы:</b> {}\n',
                                        '<b>Описание беседы:</b> {}\n',
                                        '<b>Комментарий:</b> {}\n' if is_extended else '',
'____________________________________\n\n'))
    user_info = ''.join(('<b>ТГ имя:</b> {}\n\n',
                '<b>ТГ ID:</b> {}\n\n',
                '<b>Ссылка:</b> @{}\n\n',
                '<b>Статус:</b> {}\n\n',
                '<b>Кол-во бесед (как пользователь):</b> {}\n\n',
                '<b>Кол-во бесед (как менеджер):</b> {}\n\n',
    ))
    user_is_banned = lambda is_banned: f'<b>Забанен ли:</b> {"✔️" if is_banned else "✖️"}\n\n'
    user_restricted = '<b>Запрет на беседы до:</b> {}\n\n'
    conversations = lambda upper, len_tickets: f'<b>Беседы |{upper}/{len_tickets}|</b>\n\n'
    history_ticket = lambda ticket_id, upper, len_content: f'<i>История: Тикет {ticket_id}</i> <b>|{upper}/{len_content}|</b>\n\n'
    manager_extended = lambda manager_id, message_id, media_group_text: f'<b>🗣️ Менеджер: ({manager_id})</b>\nID сообщения: {message_id}\nМедиа-группа {media_group_text}\n\n'
    user_extended = lambda user_id, message_id, media_group_text: f'<b>👤 Пользователь: ({user_id})</b>\nID сообщения: {message_id}\nМедиа-группа {media_group_text}\n\n'
    manager_usual = lambda message_id, media_group_text: f'<b>🗣️ Менеджер:</b>\nID сообщения: {message_id}\nМедиа-группа {media_group_text}\n\n'
    user_usual = lambda message_id, media_group_text: f'<b>👤 Пользователь:</b>\nID сообщения: {message_id}\nМедиа-группа {media_group_text}\n\n'
    media_files_in_msg = '<i>В данном сообщении присутствует медиафайл!</i>\n\n'
    msg_caption = lambda message_id, media_group_text: f'<b>ID сообщения:</b> {message_id}\n<b>Медиа-группа:</b> {media_group_text}\n\n'
    status_usual = 'обычный пользователь'
    status_manager = 'менеджер'
    status_admin = 'администратор'
    ticket = 'Тикет'
    # ----------------------------------------------------------------------------------------

    # Middleware
    middle_check_channel = f'Вы не можете писать в службу заботы, так как <b>не подписаны</b> на канал!\n\nВы можете воспользоваться кнопкой и проверить подписку'

    # Users channel
    channel_subscribed = '<b>Вы подписаны на канал!</b>\n\nВоспользуйтесь командой <i>/help</i> и воспользуйтесь кнопками меню!'
    channel_unsubscribed = f'<b>Вы не подписаны на канал!</b>\n\nЧтобы пользоваться функционалом чат-бота, Вы должны подписаться на канал'

    # Button
    decline_msg = '<b>Состояние команды сброшено!</b>\n\nВоспользуйтесь командой <i>/help</i> для дальнейших действий'
    use_help = 'Воспользуйтесь командой <i>/help</i>, чтобы продолжить'

    # Users General
    general_start = '<b>Вас приветствует служба заботы Legends Group ❤️‍🩹</b>\n\n Заявки принимаем <b>24/7</b> 🗳\n\n Отвечаем на вопросы с <b>6:00</b> до <b>18:00</b> UTC 🌐\n\n Воспользуйтесь кнопками ниже ⬇️'
    general_help = ('<b>Список команд:</b> 📃\n\n'
                    '<b>/create_ticket</b> - <i>создать беседу</i>\n'
                    '<b>/my_tickets</b> - <i>показать собственные беседы</i>\n'
                    '<b>/faq</b> - <i>посмотреть часто задаваемые вопросы</i>\n'
                    '<b>/lang</b> - <i>изменить язык</i>')
    general_lang = '<b>Выберите язык!</b>'
    language_updated = 'Язык обновлен!'

    # Users Tickets
    ticket_opened_already = '<b>У Вас уже есть открытая беседа!</b>\n\nВоспользуйтесь командой <i>/my_tickets</i>, чтобы посмотреть информацию'

    ticket_ask_name = '<b>Как к Вам можно обращаться?</b> <i>(до 50 символов)</i>'
    ticket_ask_name_error = '<b>Я вас не понял 🤪</b>\n\nУбедитесь, правильно ли вы ввели данные? Пожалуйста попробуйте отправить свое имя еще раз'

    ticket_ask_title = 'Пожалуйста, введите <b>название</b> темы беседы! <i>(до 50 символов)</i>\n\n<i>Например:</i> Венчур, нода, автодроп и т.д.'
    ticket_ask_title_error = '<b>Я вас не понял 🤪</b>\n\nУбедитесь, правильно ли вы ввели данные? Пожалуйста попробуйте отправить название беседы еще раз'

    ticket_ask_description = 'Пожалуйста, напишите коротко <b>вопрос</b> для большей ясности! <i>(до 100 символов)</i>\n\n<i>Например:</i> не получается зайти в кабинет, не приходит код при регистрации и т.д.'
    ticket_ask_description_error = '<b>Я вас не понял 🤪</b>\n\nУбедитесь, правильно ли вы ввели данные? Пожалуйста попробуйте отправить короткое описание беседы еще раз'

    ticket_info = lambda id_, tg_name, name, title, description: f'Пользователь <b>{name}</b> открыл беседу!\n<b>ID:</b> {int(id_)}\n<b>TG имя:</b> {tg_name}\n\n<b>Название:</b> {title}\n\n<b>Описание:</b> {description}'
    ticket_no_opened = '<b>У Вас нет открытой беседы!</b>\n\nВоспользуйтесь командой <i>/create_ticket</i>, чтобы создать беседу'
    ticket_no_opened_manager = '<b>У Вас нет открытой беседы!</b>\n\nВоспользуйтесь командой <i>/opened_tickets</i>, чтобы увидеть открытые беседы'
    ticket_opened = '<b>Вы открыли беседу!</b>\n\nПодождите, пока наш менеджер подключится к Вам\n\nЧтобы закрыть беседу, воспользуйтесь командой <i>/my_tickets</i>'

    ticket_user_close = '<b>Вы закрыли беседу!</b>\n\nИсторию просмотреть можно воспользовавшись командой <i>/my_tickets</i>'
    ticket_closed_by_user = lambda name, title, description: f'<b>Беседа закрыта пользователем!</b>\n\n<b>Информация:</b>\n<b>Пользователь:</b> {name}\n\n<b>Название беседы:</b> {title}\n\n<b>Описание беседы:</b> {description}\n\nВоспользуйтесь командой <i>/my_tickets</i> для просмотра истории бесед'
    ticket_closed_by_manager = lambda name, title, description: f'<b>Беседа закрыта менеджером!</b>\n\n<b>Информация:</b>\n<b>Пользователь:</b> {name}\n\n<b>Название беседы:</b> {title}\n\n<b>Описание беседы:</b> {description}\n\nВоспользуйтесь командой <i>/my_tickets</i> для просмотра истории бесед'

    ticket_no_manager = '<b>К Вашей беседе еще никто не присоединился!</b>\n\nПожалуйста, подождите'
    ticket_no_history = '<b>У беседы нет истории!</b>'

    ticket_no_media_on_page = 'У данных сообщений нет медиафайлов!'
    tickets_no_archive = 'У Вас нет закрытых бесед!'
    ticket_empty = 'Нет закрытых бесед!'

    ticket_released = 'Вы освободили беседу!'
    ticket_manager_released = '<b>Менеджер отсоединился от беседы!</b>\n\nПожалуйста подождите пока другой менеджер присоединится к Вам или закройте текущую беседу <i>/my_tickets</i>!'
    ticket_accepted_manager = '<b>Менеджер присоединился к беседе!</b>'
    ticket_already_have_current = 'Вы уже участвуете в беседе!'
    ticket_already_closed = 'Беседа уже закрыта!'

    # Managers Tickets
    ticket_accepted = '<b>Вы приняли беседу!</b>\n\nОтправляйте сообщения и они перенаправятся пользователю\n\nЧтобы закрыть беседу воспользуйтесь командой <i>/my_tickets</i>'
    ticket_no_opened_tickets = '<b>Нет открытых бесед!</b>'

    ticket_get_mute = 'Пожалуйста, введите сколько <b>минут</b> пользователь не сможет открывать беседы или их открывать!\n\n<i>Например:</i> 5, 15, 90 и т.д. Либо введите 0, чтобы снять ограничения'
    ticket_get_mute_error = '<b>Я вас не понял 🤪</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить кол-во минут еще раз'

    # Managers Restrictions
    restriction_before = lambda date: f'Менеджер запретил Вам создавать или писать в беседы до {date} по UTC. Если у Вас была открытая беседа, то она закрылась!'
    restriction_unmuted = '<b>Ограничения сняты!</b>\n\nВы опять можете создавать или писать в беседы'
    restirction_get_muted = lambda mins: f'Менеджер запретил Вам создавать или писать в беседы на {mins} мин. Если у Вас была открытая беседа, то она закрылась!'
    restriction_succesfully = lambda mins: f'<b>Вы запретили писать/создавать беседы пользователю на {mins} мин. Беседа у пользователя закрылась, если она была открыта!</b>'
    restriction_unmuted_succesfully = '<b>Вы сняли ограничения с пользователя!</b>'
    restriction_banned_forever = '<b>Вы навсегда забанены!</b>'
    restriction_unbanned = '<b>Вы разбанены!</b>'
    restriction_banned_successfully = 'Пользователь забанен!'
    restriction_unbanned_successfully = 'Пользователь разбанен!'

    # Manager General
    manager_general_status_updated = '<b>Вы переключились в режим администратора!</b>'
    manager_general_status_updated_error = '<b>Вы не записаны как администратор!</b>'
    manager_general_help = ('<b>Список команд:</b> 📃\n\n'
                            '<b>/opened_tickets</b> - <i>посмотреть открытые беседы</i>\n'
                            '<b>/my_tickets</b> - <i>показать собственные беседы</i>\n'
                            '<b>/search</b> - <i>найти пользователя по имени/ID</i>\n'
                            '<b>/to_admin</b> - <i>перейти в режим администратора</i>\n'
                            '<b>/faq</b> - <i>посмотреть часто задаваемые вопросы</i>\n'
                            '<b>/lang</b> - <i>изменить язык</i>')

    # Managers Ticket Data
    data_update = 'Данные обновлены!'

    data_ask_comment = 'Пожалуйста, введите <b>комментарий</b> к беседе <i>(до 100 символов)</i>'
    data_ask_comment_error = '<b>Я вас не понял 🤪</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить комментарий еще раз'

    data_title_changed = lambda title: f'Менеджер изменил <b>название</b> беседы на: <b>{title}</b>'
    data_description_changed = lambda description: f'Менеджер изменил <b>описание</b> беседы на: <b>{description}</b>'

    # Managers User Search
    search_ask_info = 'Пожалуйста, введите <b>телеграмм имя/ID/ссылку</b> пользователя\n\nНапример: <i>765432125</i> или <i>Иван Иванович</i> или <i>@url_user_name</i>'
    search_ask_info_error = '<b>Я вас не понял 🤪</b>\n\nУбедитесь, правильно ли вы ввели данные? Внимательно посмотрите на пример и попробуйте отправить данные еще раз!'

    search_manager_now = '<b>Вы теперь менеджер!</b>\n\nВоспользуйтесь командой <i>/help</i>, чтобы узнать о новых командах'
    search_user_now = '<b>Вы теперь обычный пользователь!</b>\n\nВоспользуйтесь командой <i>/help</i>, чтобы увидеть доступные команды'

    search_not_found = f'Пользователь не найден!'

    # Admin General
    admin_general_now_manager = '<b>Вы теперь менеджер!</b>\n\nЧтобы вернуть статус админа воспользуйтесь командой <i>/to_admin</i>'
    admin_general_ask_faq = 'Пожалуйста, введите сообщение <b>FAQ</b>'
    admin_general_ask_faq_error = '<b>Некорректный ввод!</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить сообщение FAQ еще раз'

    # Admin channel
    admin_channel_ask_channel_url = 'Пожалуйста, введите <b>ссылку</b> на канал!\n\n<b>Обязательно сделайте чат-бота администратором канала, иначе он не сможет проверять подписку пользователей!</b>'
    admin_channel_ask_channel_url_error = '<b>Некорректный ввод!</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить ссылку еще раз'

    admin_channel_ask_channel_id = 'Пожалуйста, перешлите <b>сообщение с канала</b>!\n\n<b>Не забывайте: обязательно сделайте чат-бота администратором канала, иначе он не сможет проверять подписку пользователей!</b>'
    admin_channel_ask_channel_id_error = 'Пожалуйста, <b>переотправьте сообщение с канала!</b>'

    admin_channel_ask_button_name = 'Пожалуйста, отправьте <b>название кнопки</b>, которое отображается в меню, отправляющеяся пользователям, если они не подписаны на канал!'
    admin_channel_ask_button_name_error = '<b>Некорректный ввод!</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить название кнопки еще раз'
    admin_channel_button_name_updated = '<b>Вы обновили название кнопки!</b>'

    admin_channel_channel_updated_info = lambda \
        url: f'<b>Канал обязательной подписки изменен!</b>\n\nЧтобы продолжить пользоваться функционалом, подпишитесь {url}'
    admin_channel_channel_info = lambda id_, url, button_name: f'<b>Текущий канал:</b> {url}\n<b>ID канала:</b> {int(id_)}\n\n<i>Название кнопки для пользователей:</i> {button_name}'

    admin_channel_menu = '<b>Меню изменения подписки</b>'
    admin_channel_on = 'Вы сделали подписку обязательной'
    admin_channel_off = 'Вы сделали подписку необязательной'

    # Admin Mailing
    mailing_what_to_do = '<b>Что сделайте с сообщением?</b>'
    admin_general_ask_mailing_msg = 'Пожалуйста, отправьте <b>сообщение</b>, которое хотите отправить всем пользователям!'
    admin_general_mailing_successful = '<b>Рассылка отправлена пользователям!</b>'
    admin_general_no_users = '<b>Некому отправлять сообщение!</b>'
    admin_mailing_add_link = 'Отправьте <b>название кнопки и ссылку</b>, которая будет находится под сообщением\n\nНапример: Супер поисковик google.com'
    admin_mailing_add_link_error = '<b>Некорректный ввод!</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить ссылку еще раз'

    admin_general_help = ('<b>Список команд:</b> 📃\n\n'
                          '<b>/change_faq</b> - <i>изменить часто заваемые вопросы</i>\n'
                          '<b>/change_channel</b> - <i>изменить канал подписки</i>\n'
                          '<b>/search</b> - <i>найти пользователя по имени/ID</i>\n'
                          '<b>/my_tickets</b> - <i>показать собственные беседы</i>\n'
                          '<b>/mailing</b> - <i>отправить рассылку всем пользователям</i>\n'
                          '<b>/start_msg</b> - <i>изменить стартовое сообщение</i>\n'
                          '<b>/change_release_close_time</b> - <i>изменить время авто закрытия/освобождения бесед</i>\n'
                          '<b>/delete_tickets</b> - <i>удалить тикеты по промежутку времени (месяцы)</i>\n'
                          '<b>/to_manager</b> - <i>перейти в режим менеджера</i>\n'
                          '<b>/lang</b> - <i>изменить язык</i>')

    # Admin FAQ
    faq_category_exist = 'Такая категория уже есть, введите другое название'
    faq_ask_category = 'Пожалуйста, введите <b>категорию</b> для отображения в inline режиме. Желательно коротко.'
    faq_ask_question = 'Пожалуйста, введите <b>вопрос</b> для отображения в inline режиме. Желательно коротко.'
    faq_ask_question_error = '<b>Некорректный ввод!</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить  еще раз'

    faq_ask_content = '<b>Отправьте сообщение</b>, которое будет отображаться при выборе данного пункта'
    faq_ask_content_error = '<b>Некорректный ввод!</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить текст еще раз'

    faq_added = '<b>Вопрос добавлен!</b>\n\nВоспользуйтесь <i>/faq</i>, чтобы увидеть изменения'

    faq_questions = '<b>Выберете вопрос</b>'
    faq_category = '<b>Выберете категорию</b>'

    # Admin Start Msg
    admin_start_current = '<b>Текущее стартовое сообщение:</b>'
    admin_start_ask_msg = 'Пожалуйста, отправьте <b>стартовое сообщение</b>, которое будут видеть пользователи!'
    admin_start_updated = '<b>Стартовое сообщение обновлено!</b>\n\nМожете воспользоваться командой <i>/start</i>, чтобы увидеть изменения'

    # Admin Release Close
    admin_release_close_ask_time = 'Пожалуйста, отправьте <b>кол-во часов</b>, через которое происходит действие\n\nНапример: <i>Закрытие 48</i> или <i>Освобождение 2</i> '
    admin_release_close_ask_time_error = '<b>Некорректный ввод!</b>\n\nУбедитесь, правильно ли вы ввели данные? Попробуйте отправить действие и кол-во часов еще раз'
    admin_close_updated = '<b>Вы обновили время закрытия беседы!</b>'
    admin_release_updated = '<b>Вы обновили время освобождения беседы!</b>'

    # Admin Delete Tickets
    admin_delete = '<b>Выберите соответствующее время для удаления устаревших бесед</b>\n\nТакже Вы можете отключить/включить уведомления, которые приходят каждый месяц, как напоминание об очистке'
    admin_delete_sure = '<b>Вы уверены, что хотите удалить беседы?</b> Найдено: {}'
    admin_delete_tickets = lambda count: f'Кол-во удаленных записей: {count}'
    admin_delete_notification_on = 'Вы включили уведомления!'
    admin_delete_notification_off = 'Вы отключили уведомления!'
    admin_delete_notification = '<b>Рассмотрите вариант удаления бесед!</b>\n\nОчистите беседу командой <i>/delete_tickets</i>'

    # Background
    last_modified_outdated = lambda \
        time: f'<b>Беседа закрыласть, так как прошло более {time} ч. с последнего изменения!</b>\n\nИсторию можно посмотреть, используя команду <i>/my_tickets</i>'
    last_modified_manager_disconnected = lambda \
        time: f'<b>Вы были отключены от беседы, так как бездействовали более {time} ч.!</b>'
    ticket_not_updating_msg = '<b>Беседа не обновляется более часа! Перенаправление свободным менеджерам</b>\n\n'
