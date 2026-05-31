import discord
from groq import Groq

# 1. MASUKKAN KUNCI AKSES KAMU DI SINI
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DISCORD_TOKEN = "MTUwODM0MzUwNDYyMTc5NzQ1Ng.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Inisialisasi API Groq
groq_client = Groq(api_key=GROQ_API_KEY)

# Atur izin khusus untuk Bot Discord
intents = discord.Intents.default()
intents.message_content = True  
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    # Menandakan jika bot sudah berhasil menyala
    print(f'Mantap! {bot.user} sekarang sudah online dan siap bekerja!')

@bot.event
async def on_message(message):
    # Agar bot tidak membalas pesannya sendiri
    if message.author == bot.user:
        return

    # Bot HANYA akan merespons jika namanya di-mention (@bot) oleh pengguna
    if bot.user.mentioned_in(message):
        # Menghapus tag @mention dari teks agar tidak ikut diproses AI
        clean_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        if not clean_text:
            await message.reply("Ya? Ada yang bisa saya bantu? Tag saya lalu ketik pertanyaannya, ya!")
            return

        # Membuat efek tulisan "Bot is typing..." di Discord biar estetik
        async with message.channel.typing():
            try:
                # Memanggil model Llama 3.3 70b dari Groq
                completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        # Di sini kamu bisa mengatur sifat/kepribadian bot-mu
                        {"role": "system", "content": "Kamu adalah asisten Discord yang sangat pintar, ramah, keren, dan membantu."},
                        {"role": "user", "content": clean_text}
                    ]
                )
                
                # Mengambil hasil jawaban dari Groq
                response_ai = completion.choices[0].message.content
                
                # Mengirimkan balasan ke Discord
                await message.reply(response_ai)
                
            except Exception as e:
                await message.reply(f"Waduh, maaf ada kendala teknis: {e}")

# Menjalankan bot
bot.run(DISCORD_TOKEN)
