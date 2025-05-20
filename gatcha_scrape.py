from telethon import *
import sqlite3, subprocess
import requests, os, math, time
from datetime import timedelta
import asyncio
import psycopg2
import psycopg2.extras

def get_db():
	conn = psycopg2.connect(
        dbname='roziwjcvreixmcpolwqn',
        user='ffzshaglnugrharolzpe',
        password='kenfbuxfqgqyrjsksjpeautigbgsih',
        host='9qasp5v56q8ckkf5dc.leapcellpool.com',
		port=6438
    )
	return conn

conn = get_db()
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS limiting (
    uid BIGINT PRIMARY KEY,
    counted INTEGER NOT NULL DEFAULT 0
)
""")
conn.commit()
cur.close()
conn.close()
#ENV
TOKEN=os.getenv("TOKEN")
SESSION="22332316"
TOPIC_ID=3282669
bot = TelegramClient(SESSION,"6","eb06d4abfb49dc3eeb1aeb98ae0f581e").start(bot_token=TOKEN)

@bot.on(events.NewMessage(pattern=r"(?:.r|/r)$"))
async def resetting(event):
	uid = await event.get_sender()
	if uid.id == 1810081802:
		conn = get_db()
		cur = conn.cursor()
		cur.execute("DROP TABLE IF EXISTS limiting")
		sc = f"""
CREATE TABLE limiting (
		uid INTEGER,
		counted INTEGER NOT NULL DEFAULT 0
		);
"""
		cur.execute(sc)
		conn.commit()
		cur.close()
		conn.close()
		await event.reply("Reset complete")

@bot.on(events.NewMessage)
async def starts(event):
	conn = get_db()
	cur = conn.cursor()
	if event.reply_to != None and event.reply_to.reply_to_msg_id == TOPIC_ID:
		print('detected')
		uid = await event.get_sender()
		await asyncio.sleep(1)
		permissions = await bot.get_permissions(event.chat_id, uid.id)
		print(permissions.is_admin)
		if '#WTB' in event.message.message.upper() or '#WTS' in event.message.message.upper():
			if permissions.is_admin == False:
				print('this guy is not an admin!')
				getAllUid = cur.execute('SELECT uid FROM limiting').fetchall()
				a = [v[0] for v in getAllUid]
				if uid.id not in a:
					cur.execute('INSERT INTO limiting (uid, counted) VALUES (?,?)', (uid.id, 1,))
					cur.commit()
					cur.close()
					conn.close()
				else:
					counted = cur.execute('SELECT counted FROM limiting WHERE uid = ?', (uid.id,)).fetchone()[0]
					if int(counted) >= 2:
						msg = f'User {uid.first_name} kamu sudah mengirim lebih dari 2 pesan. Kamu bisa mengirim pesan lagi dalam 24jam.'
						await bot.edit_permissions(event.chat_id, uid.id, timedelta(minutes=1440),
            	                  send_messages=False)
						await asyncio.sleep(1)
						await bot.send_message(event.chat_id, msg, reply_to=TOPIC_ID)
						await asyncio.sleep(1)
						await bot.delete_messages(event.chat_id, event.message.id)
						
					else:
						cur.execute('UPDATE limiting SET counted = ?', (counted+1,))
						cur.commit()
						cur.close()
						conn.close()
			else:
				pass
		elif permissions.is_admin == False:
			await asyncio.sleep(1)
			await event.delete()
	else:
		pass
'''
	a = event.pattern_match.group(1)
	a = a.split("/")
	print(a)
	message = await bot.get_messages(GROUP_ID, ids=int(a[-1]))
	print(message.text)
	await event.reply(message.text)
'''
if __name__ == "__main__":
	bot.run_until_disconnected()
