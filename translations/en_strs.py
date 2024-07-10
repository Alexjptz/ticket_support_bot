class EnTranslation:
    # Buttons
    decline_btn = 'Decline ❌'
    month_btn_1 = 'From 1️⃣ month'
    month_btn_3 = 'From 3️⃣ months'
    month_btn_6 = 'From 6️⃣ months'
    month_btn_12 = 'From the year 🗓️'
    notification_btn_on = 'Enable notifications 🔊'
    notification_btn_off = 'Turn off notifications 🔇'
    update_btn_question = 'Update the question ❓'
    update_btn_content = 'Update content 📝'
    remove_btn = 'Delete 🗑️'
    update_btn = 'Update 🔄'
    back_btn = 'Back 🔙 '
    delete_btn = 'Close 🚫'
    delete_tickets_btn = 'Delete tickets 🗑️'
    add_btn = 'Add ➕'
    change_faq_btn = 'Change the FAQ ❓'
    faq_btn = 'FAQ ❓'
    change_subscription_channel_btn = 'Change the subscription channel 🌐'
    find_user_btn = 'Find a user 🔎'
    my_tickets_btn = 'My tickets 📂'
    user_tickets_btn = 'User tickets 📂'
    send_mailing_btn = 'Send a mailing 📬'
    send_mailing_message_btn = 'Send 📨'
    mailing_add_link_btn = 'Add a link 🌐'
    mailing_delete_btn = 'Remove the menu ❌'
    start_msg_btn = 'Start message 💬'
    change_close_release_btn = 'Change the auto-release/closing time 🕒'
    manager_mode_btn = 'Manager mode 💼'
    admin_mode_btn = 'Admin mode 😎'
    change_channel_info_btn = 'Change channel data 🔄'
    change_channel_button_name_btn = 'Change the name of the user button 🖲️'
    make_subscription_necessary_btn = 'Make subscription mandatory 🔔'
    make_subscription_unnecessary_btn = 'Make subscription optional 🔕'
    remove_menu_btn = 'Remove the menu 🚫'
    opened_tickets_btn = 'Open conversations 💬'
    create_ticket_btn = 'Create a ticket 💬'
    press_update_btn = ' Click on the "Update 🔄" button'
    change_ticket_description_btn = 'Change the description 📝'
    change_ticket_title_btn = 'Change the topic of the conversation 🏷️'
    mute_btn = 'Restrict 🤐'
    history_btn = 'History 💬'
    commentary_btn = 'Comment ✍'
    ticket_data_btn = 'Conversation data 🔄'
    release_ticket_btn = 'Release 🙅🏻 ️'
    archive_btn = 'Archive 🗄️️'
    user_info_btn = 'User information ℹ️'
    accept_btn = 'Accept ✅'
    hide_btn = 'Hide 🗂️'
    ban_btn = 'Ban ⛔'
    unban_btn = 'Unban 🟢'
    make_ordinary_btn = 'Make a regular user 👤'
    make_manager_btn = 'Make a manager 👨🏻 💻'
    check_subscription_btn = 'Check your subscription 🔔'
    choose_lang_btn = 'Language 🌎'

    reply_buttons = [
        decline_btn, delete_tickets_btn, change_faq_btn, faq_btn, change_subscription_channel_btn,
        find_user_btn, my_tickets_btn, send_mailing_btn, start_msg_btn, change_close_release_btn,
        manager_mode_btn, admin_mode_btn, opened_tickets_btn, create_ticket_btn, choose_lang_btn
    ]

    # Composite
    release_composite = '<b>The conversation is released from the manager</b> if the last action was more than {} hours ago \n\n'
    close_composite = '<b>The conversation is closed</b> if the last action was more than {} hours ago\n\n'
    ticket_data_composition = '<b>Ticket:</b> {}\n\n<b>Generated:</b> {} Moscow time\n\n<b>Closed:</b> {} Moscow time\n\n<b>Username:</b> {}\n\n<b>The topic of the conversation:</b> {}\n\n<b>Description of the conversation:</b> {}\n\n<b>Comment:</b> {}'
    manager_released_ticket_composition = '<b>The manager has released the ticket!</b>\n\n'
    user_found = '<b>The user has been found!</b>'
    current_ticket_comment_composition = '<b>Current ticket:</b>\n\n{}\n\n<b>Comment: </b>{}'
    current_ticket_composition = '<b>Current ticket:</b>\n\n{}'

    tickets_info = lambda is_extended: ''.join(('<b>Discussion:</b> {}\n',
                                        '<b>Generated:</b> {} Moscow time\n',
                                        '<b>Closed:</b> {} Moscow time\n',
                                        '<b>Username:</b> {}\n',
                                        '<b>Name of TG:</b> {}\n',
                                        '<b>User\'s link:</b> @{}\n',
                                        '<b>The topic of the conversation:</b> {}\n',
                                        '<b>Description of the conversation:</b> {}\n',
                                        '<b>Comment:</b> {}\n' if is_extended else '',
                                        '____________________________________\n\n'))
    user_info = ''.join(('<b>TG name:</b> {}\n\n',
                 '<b>TG ID:</b> {}\n\n',
                 '<b>Link:</b> @{}\n\n',
                 '<b>Status:</b> {}\n\n',
                 '<b>Number of conversations (as a user):</b> {}\n\n',
                 '<b>Number of conversations (as a manager):</b> {}\n\n',
                 ))
    user_is_banned = lambda is_banned: f'<b>Is user banned:</b> {" ✔️ " if is_banned else " ✖️ "}\n\n'
    user_restricted = '<b>User restriction time:</b> {}\n\n'
    conversations = lambda upper, len_tickets: f'<b>Conversations |{upper}/{len_tickets}|</b>\n\n'
    history_ticket = lambda ticket_id, upper, len_content: f'<i>History: Ticket {ticket_id}</i> <b>|{upper}/{len_content}|</b>\n\n'
    manager_extended = lambda manager_id, message_id, media_group_text: f'<b> 🗣️ Manager: ({manager_id})</b>\n<b>ID of the message:</b> {message_id}\n<b>Media group:</b> {media_group_text}\n\n'
    user_extended = lambda user_id, message_id, media_group_text: f'<b> 👤 User: ({user_id})</b>\n<b>Message ID:</b> {message_id}\n<b>Media group:</b> {media_group_text}\n\n'
    manager_usual = lambda message_id, media_group_text: f'<b> 🗣️ Manager:</b>\nID of the message: {message_id}\nMedia group {media_group_text}\n\n'
    user_usual = lambda message_id, media_group_text: f'<b> 👤 User:</b>\nID of the message: {message_id}\nMedia group {media_group_text}\n\n'
    media_files_in_msg = '<i>There is a media file in this message!</i>\n\n'
    msg_caption = lambda message_id, media_group_text: f'<b>Message ID:</b> {message_id}\n<b>Media Group:</b> {media_group_text}\n\n'
    status_usual = 'regular user'
    status_manager = 'manager'
    status_admin = 'administrator'
    ticket = 'Ticket'
    # ----------------------------------------------------------------------------------------

    # Middleware
    middle_check_channel = f'You cannot write to the customer service because <b>you are not subscribed</b> to the channel! You can use the button and check your subscription'

    # Users channel
    channel_subscribed = '<b>You are subscribed to the channel!</b>\n\n Use the <i>/help</i> command and use the menu buttons!'
    channel_unsubscribed = f'<b>You are not subscribed to the channel!</b>\n\n To use the chatbot functionality, you must subscribe to the channel'

    # Button
    decline_msg = '<b>The command status has been reset!</b>\n\n Use the <i>/help</i> command for further actions'
    use_help = 'Use the <i>/help</i> command to continue'

    # Users General
    general_start = '<b>Welcome to Legends Group Care Service ❤️‍🩹</b>\n\n We accept applications <b>24/7</b> 🗳\n\n Answering questions from <b>6:00</b> до <b>18:00</b> UTC 🌐\n\n Use the buttons below ⬇️'
    general_help = ('<b>List of commands:</b> 📃\n\n'
                    '<b>/create_ ticket</b> - <i>create a conversation</i>\n'
                    '<b>/my_tickets</b> - <i>show your own conversations</i>\n'
                    '<b>/FAQ</b> - <i>view frequently asked questions</i>\n'
                    '<b>/lang</b> - <i>change language</i>')
    general_lang = '<b>Choose language!</b>'
    language_updated = 'Language updated!'

    # Users Tickets
    ticket_opened_already = '<b>You already have an open conversation!</b>\n\n Use the <i>/my_tickets</i> command to view the information'

    ticket_ask_name = '<b>How can I contact you?</b> <i>(up to 50 characters)</i>'
    ticket_ask_name_error = '<b>I did not get it 🤪</b>\n\Make sure you entered the data correctly? Please try sending the name again'

    ticket_ask_title = 'Please enter the <b>name</b> of the topic of the conversation! <i>(up to 50 characters)</i>\n\n<i>For example:</i> Venture, node, airdrop, etc.'
    ticket_ask_title_error = '<b>I did not get it 🤪</b>\n\Make sure you entered the data correctly? Please try sending the conversation title again'

    ticket_ask_description = 'Please write a short <b>description</b> for more clarity! <i>(up to 100 characters)</i>\n\n<i>For example:</i> the product did not fit, I want to refund the money'
    ticket_ask_description_error = '<b>I did not get it 🤪</b>\n\Make sure you entered the data correctly? Please try sending a short description of the conversation again'

    ticket_info = lambda id_, tg_name, name, title, description: f'User <b>{name}</b> has opened a conversation!\n<b>ID:</b> {int(id_)}\n<b>TG name:</b> {tg_name}\n\n<b>Title:</b> {title}\n\n<b>Description:</b> {description}'
    ticket_no_opened = '<b>You don\'t have an open conversation!</b>\n\n Use the <i>/create_ ticket</i> command to create a conversation'
    ticket_no_opened_manager = '<b>You don\'t have an open conversation!</b>\n\n Use the <i>/opened_tickets</i> command to see open conversations'
    ticket_opened = '<b>You have opened a conversation!</b>\n\n Wait until our manager connects to you\n\n To close the conversation, use the command <i>/my_tickets</i>'

    ticket_user_close = '<b>You closed the conversation!</b>\n\pIstoria can be viewed using the command <i>/my_tickets</i>'
    ticket_closed_by_user = lambda name, title, description: f'<b>The conversation is closed by the user!</b>\n\n<b>Information:</b>\n<b>User:</b> {name}\n\n<b>The name of the conversation:</b> {title}\n\n<b>Description of the conversation:</b> {description}\n\n Use the <i>/my_tickets</i> command to view the conversation history'
    ticket_closed_by_manager = lambda name, title, description: f'<b>The conversation is closed by the manager!</b>\n\n<b>Information:</b>\n<b>User:</b> {name}\n\n<b>The name of the conversation:</b> {title}\n\n<b>Description of the conversation:</b> {description}\n\n Use the <i>/my_tickets</i> command to view the conversation history'

    ticket_no_manager = '<b>No one has joined your conversation yet!</b>\n\n Please wait'
    ticket_no_history = '<b>The conversation has no history!</b>'

    ticket_no_media_on_page = 'These messages do not have media files!'
    tickets_no_archive = 'You don\'t have closed conversations!'
    ticket_empty = 'There are no closed conversations!'

    ticket_released = 'You have released the conversation!'
    ticket_manager_released = '<b>The manager disconnected from the conversation!</b>\n\n Please wait for another manager to join you or close the current conversation <i>/my_tickets</i>!'
    ticket_accepted_manager = '<b>The manager joined the conversation!</b>'
    ticket_already_have_current = 'You are already participating in the conversation!'
    ticket_already_closed = 'The conversation is already closed!'

    # Managers Tickets
    ticket_accepted = '<b>You accepted the conversation!</b>\nSend messages and they will be redirected to the user\n\n To close the conversation, use the command <i>/my_tickets</i>'
    ticket_no_opened_tickets = '<b>There are no open conversations!</b>'

    ticket_get_mute = 'Please enter how many <b>minutes</b> the user will not be able to open conversations or open them!\n\n<i>For example:</i> 5, 15, 90, etc. Or enter 0 to remove the restrictions'
    ticket_get_mute_error = '<b>I did not get it 🤪</b>\n\Make sure you entered the data correctly? Try sending the number of minutes again'

    # Managers Restrictions
    restriction_before = lambda date: f' Manager forbade you to create or write to conversations before {date} UTC. If you had an open conversation, then it\'s closed!'
    restriction_unmuted = '<b>Restrictions are lifted!</b>\n\n yOu can create or write in conversations again'
    restirction_get_muted = lambda mins: f' Manager forbade you to create or write to conversations on {mins} min. If you had an open conversation, then it\'s closed!'
    restriction_succesfully = lambda mins: f'<b>You forbade me to write/create conversations for the user for {mins} min. The user\'s conversation was closed if it was open!</b>'
    restriction_unmuted_succesfully = '<b>You have removed the restrictions from the user!</b>'
    restriction_banned_forever = '<b>You are permanently banned!</b>'
    restriction_unbanned = '<b>You are banned!</b>'
    restriction_banned_successfully = 'The user is banned!'
    restriction_unbanned_successfully = 'The user is banned!'

    # Manager General
    manager_general_status_updated = '<b>You have switched to admin mode!</b>'
    manager_general_status_updated_error = '<b>You are not registered as an administrator!</b>'
    manager_general_help = ('<b>List of commands:</b> 📃\n\n'
                            '<b>/opened_tickets</b> - <i>view open conversations</i>\n'
                            '<b>/my_tickets</b> - <i>show your own conversations</i>\n'
                            '<b>/search</b> - <i>find a user by name/ID</i>\n'
                            '<b>/to_admin</b> - <i>switch to administrator mode</i>\n'
                            '<b>/FAQ</b> - <i>view frequently asked questions</i>\n'
                            '<b>/lang</b> - <i>change language</i>')

    # Managers Ticket Data
    data_update = 'The data has been updated!'

    data_ask_comment = 'Please enter a <b>comment</b> to the conversation <i>(up to 100 characters)</i>'
    data_ask_comment_error = '<b>I did not get it 🤪</b>\n\Make sure you entered the data correctly? Try to send a comment again'

    data_title_changed = lambda title: f' Manager changed the <b>title</b> of the conversation to: <b>{title}</b>'
    data_description_changed = lambda \
            description: f' Manager changed the <b>description</b> of the conversation to: <b>{description}</b>'

    # Managers User Search
    search_ask_info = 'Please enter <b>telegram name/ID/link</b> of the user\n\nexample: <i>765432125</i> or <i>Ivan Ivanovich</i> or <i>@url_user_name</i>'
    search_ask_info_error = '<b>I did not get it 🤪</b>\n\Make sure you entered the data correctly? Take a close look at the example and try to send the data again!'

    search_manager_now = '<b>You are the manager now!</b>\n\n Use the <i>/help</i> command to learn about new commands'
    search_user_now = '<b>You are now a regular user!</b>\n\n Use the <i>/help</i> command to see the available commands'

    search_not_found = f'The user has not been found!'

    # Admin General
    admin_general_now_manager = '<b>You are the manager now!</b>\n\n To return the admin status, use the command <i>/to_admin</i>'
    admin_general_ask_faq = 'Please enter the message <b>FAQ</b>'
    admin_general_ask_faq_error = '<b>Incorrect input!</b>\n\Make sure you entered the data correctly? Try sending the FAQ message again'

    # Admin channel
    admin_channel_ask_channel_url = 'Please enter the <b>link</b> to the channel!\n\n<b>Be sure to make the chatbot the channel administrator, otherwise it will not be able to check users</b>'
    admin_channel_ask_channel_url_error = '<b>Incorrect input!</b>\n\nMake sure you entered the data correctly? Try sending the link again'

    admin_channel_ask_channel_id = 'Please forward <b>the message from the channel</b>!\n\n<b>Don\'t forget: make sure to make the chatbot the channel administrator, otherwise it won \'t be able to check users</b>'
    admin_channel_ask_channel_id_error = 'Please <b>resend the message from the channel!</b>'

    admin_channel_ask_button_name = 'Please send <b>the name of the button</b> that is displayed in the menu that is sent to users if they are not subscribed to the channel!'
    admin_channel_ask_button_name_error = '<b>Incorrect input!</b>\n\nMake sure you entered the data correctly? Try sending the button name again'
    admin_channel_button_name_updated = '<b>You have updated the button name!</b>'

    admin_channel_channel_updated_info = lambda \
            url: f'<b>The mandatory subscription channel has been changed!</b>\n\n To continue using the functionality, subscribe {url}'
    admin_channel_channel_info = lambda id_, url, button_name: f'<b>Current Channel:</b> {url}\n<b>Channel ID:</b> {int(id_)}\n\n<i>The name of the button for users:</i> {button_name}'

    admin_channel_menu = '<b>Subscription change menu</b>'
    admin_channel_on = 'You have made the subscription mandatory'
    admin_channel_off = 'You have made the subscription optional'

    # Admin Mailing
    mailing_what_to_do = '<b>What should you do with the message?</b>'
    admin_general_ask_mailing_msg = 'Please send the <b>message</b> that you want to send to all users!'
    admin_general_mailing_successful = '<b>The mailing has been sent to users!</b>'
    admin_general_no_users = '<b>There is no one to send a message to!</b>'
    admin_mailing_add_link = 'Send <b>the name of the button and the link</b>, which will be located under the message\n\nexample: Super Search engine google.com '
    admin_mailing_add_link_error = '<b>Incorrect input!</b>\n\Make sure you entered the data correctly? Try sending the link again'

    admin_general_help = ('<b>List of commands:</b> 📃 \n\n'
                          '<b>/change_faq</b> - <i>change frequently asked questions</i>\n'
                          '<b>/change_channel</b> - <i>change the subscription channel</i>\n'
                          '<b>/search</b> - <i>find a user by name/ID</i>\n'
                          '<b>/my_tickets</b> - <i>show your own conversations</i>\n'
                          '<b>/mailing</b> - <i>send a mailing to all users</i>\n'
                          '<b>/start_msg</b> - <i>change the start message</i>\n'
                          '<b>/change_release_close_time</b> - <i>change the time of auto closing/releasing conversations</i>\n'
                          '<b>/delete_ticks</b> - <i>delete tickets by time interval (months)</i>\n'
                          '<b>/to_manager</b> - <i>switch to manager mode</i>\n'
                          '<b>/lang</b> - <i>change language</i>')

    # Admin FAQ
    faq_category_exist = 'Category name already exist. Please enter another name'
    faq_ask_category = 'Please enter a <b>category</b> to display inline. Preferably short.'
    faq_ask_question = 'Please enter the <b>question</b> to be displayed in inline mode. Preferably short.'
    faq_ask_question_error = '<b>Incorrect input!</b>\n\Make sure you entered the data correctly? Try submitting the question again'

    faq_ask_content = '<b>Send a message</b> that will be displayed when you select this option'
    faq_ask_content_error = '<b>Incorrect input!</b>\n\Make sure you entered the data correctly? Try sending the text again'

    faq_added = '<b>The question has been added!</b>\n\n Log in <i>/faq</i> to see the changes'

    faq_questions = '<b>Available questions</b>'
    faq_category = '<b>Available categories</b>'

    # Admin Start Msg
    admin_start_current = '<b>Current start message:</b>'
    admin_start_ask_msg = 'Please send a <b>start message</b> that users will see!'
    admin_start_updated = '<b>The start message has been updated!</b>\n\n You can use the <i>/start</i> command to see the changes'

    # Admin Release Close
    admin_release_close_ask_time = 'Please send <b>the number of hours</b> after which the action takes place\n\nexample: <i>Closing 48</i> or <i>Releasing 2</i> '
    admin_release_close_ask_time_error = '<b>Incorrect input!</b>\n\Make sure you entered the data correctly? Try sending the action and the number of hours again'
    admin_close_updated = '<b>You have updated the closing time of the conversation!</b>'
    admin_release_updated = '<b>You have updated the conversation release time!</b>'

    # Admin Delete Tickets
    admin_delete = '<b>Select the appropriate time to delete outdated conversations</b>\n\n You can also disable/enable notifications that come every month as a reminder to clean up'
    admin_delete_sure = '<b>Are you sure you want to delete conversations?</b> Found: {}'
    admin_delete_tickets = lambda count: f' Number of deleted records: {count}'
    admin_delete_notification_on = 'You have enabled notifications!'
    admin_delete_notification_off = 'You have disabled notifications!'
    admin_delete_notification = '<b>Consider deleting conversations!</b>\n\Clean up the conversation with the command <i>/delete_tickets</i>'

    # Background
    last_modified_outdated = lambda \
            time: f'<b>The conversation was closed because more than {time} hours have passed since the last change!</b>\n\pIstoria can be viewed using the command <i>/my_tickets</i>'
    last_modified_manager_disconnected = lambda \
            time: f'<b>You were disconnected from the conversation because you were inactive for more than {time} hours!</b>'
    ticket_not_updating_msg = '<b>The conversation has not been updated for more than an hour! Redirection to free managers</b>>\n\n'
