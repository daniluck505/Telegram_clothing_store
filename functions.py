import asyncio
from aiogram import types
from middlewares import ThrottlingMiddleware
from loader import *
import Markup


async def start_bot(dp):
    try:
        await bot.send_message(str(config.admin_id), 'Бот запущен')
    except:
        pass
    await setup(dp)

    scheduler.add_job(make_dump, 'cron',
                      day_of_week='mon-sun',
                      hour=config.hour_scheduler,
                      minute=config.minute_scheduler + 6)
    # https://telegra.ph/Zapusk-funkcij-v-bote-po-tajmeru-11-28
    scheduler.start()


async def stop_bot(dp):
    """ Выключение бота """
    DB.close()
    await bot.send_message(str(config.admin_id), 'Бот выключен')


async def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())


async def admins_test(message):
    """ Проверка id на админа  """
    if message.from_user.id in config.admins_list:
        return True
    else:
        return False


async def make_dump():
    mess = DB.backup()
    if mess:
        with open('backup.db', "rb") as f:
            await bot.send_document(config.DUMP_ID, f)
    else:
        bot.send_message(config.DUMP_ID, f"Ошибка при резервном копировании: \n {mess}")

#
# async def give_profile_desider_text(user_id, chanel=False):
#     user_dict, list_sub = DB.get_user_info(user_id)
#     sub_text = ', '.join(['#'+x for x in list_sub])
#
#     text = f'<b>{user_dict["name"]}</b>\n' \
#            f'ВУЗ - {user_dict["univer"]}\n' \
#            f'Предметы:\n{sub_text}\n'
#     return text

