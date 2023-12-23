
from pyrogram import *
import requests as re
from config import Config
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import wget
import os 

buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('انشاء بريد', callback_data='generate'),
            InlineKeyboardButton('اعادة تحميل', callback_data='refresh'),
            InlineKeyboardButton('اغلاق', callback_data='close')
                   ] 
                             ])

msg_buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('عرض الرساله', callback_data='view_msg'),
            InlineKeyboardButton('اغلاق', callback_data='close')
                   ] 
                             ])


app=Client('Temp-Mail Bot',
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

email=''
@app.on_message(filters.command('start'))
async def start_msg(client,message):
    await message.reply("**مرحبا يا "+message.from_user.first_name+" !!**\n @GMAIL_Imag_BOT  isهي خدمة مجانية تسمح بإنشاء واستقبال رسائل البريد الإلكتروني في عنوان مؤقت تم تدميره ذاتيًا بعد انقضاء وقت معين.\n\n**__ هل هو آمن??**__\n- يتيح لك استخدام البريد المؤقت حماية صندوق بريدك الحقيقي تمامًا مقابل فقدان المعلومات الشخصية. عنوان البريد الإلكتروني المؤقت الخاص بك مجهول تمامًا. التفاصيل الخاصة بك: معلومات عن شخصك ومستخدميك الذين تتواصل معهم ، و عنوان الايبي ، وعنوان البريد الإلكتروني محمي وسرية تمامًا.\n\nلمعرفة المزيد. @UY_30  ")
    await message.reply("**قم ب انشاء بريد وهمي الان❕**",
                        reply_markup=buttons)
@app.on_callback_query()
async def mailbox(client,message):
    response=message.data
    if response=='generate':
       global email
       email = re.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
       await message.edit_message_text('__**هذا هو بريدك الوهمي: **__`'+str(email)+'`',
                                       reply_markup=buttons)
       print(email)
    elif response=='refresh':
        print(email)
        try:
            if email=='':
                await message.edit_message_text('انشاء بريد وهمي',reply_markup=buttons)
            else: 
                getmsg_endp =  "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:]
                print(getmsg_endp)
                ref_response = re.get(getmsg_endp).json()
                global idnum
                idnum=str(ref_response[0]['id'])
                from_msg=ref_response[0]['from']
                subject=ref_response[0]['subject']
                refreshrply='You a message from '+from_msg+'\n\nSubject : '+subject
                await message.edit_message_text(refreshrply,
                                                reply_markup=msg_buttons)
        except:
            await message.answer('لم يتم استلام اي رساله..\nفي صندوق بريدك '+email)
    elif response=='view_msg':
        msg =re.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum).json()
        print(msg)
        from_mail=msg['from']
        date=msg['date']
        subjectt=msg['subject']
        try:
          attachments=msg['attachments'][0]
        except:
            pass
        body=msg['body']
        mailbox_view='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body
        await message.edit_message_text(mailbox_view,reply_markup=buttons)
        mailbox_view='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body
        if attachments == "[]":
            await message.edit_message_text(mailbox_view,reply_markup=buttons)
            await message.answer("No Messages Were Recieved..", show_alert=True)
        else:
            dlattach=attachments['filename']
            attc="https://www.1secmail.com/api/v1/?action=download&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum+"&file="+dlattach
            print(attc)
            mailbox_vieww='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body+'\n\n'+'[Download]('+attc+') Attachments'
            filedl=wget.download(attc)
            await message.edit_message_text(mailbox_vieww,reply_markup=buttons)
            os.remove(dlattach)
    elif response=='close':
        await message.edit_message_text('تم الاغلاق بنجاح✅')
app.run()


