mport discord, asyncio
from discord.ext import commands
import random
import os 

# --------------------
# 기본 설정
# --------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------
# 임시 이미지 (이미지 없을 때 사용)
# --------------------
DEFAULT_IMAGE = "https://i.namu.wiki/i/example.png"

# --------------------
# 생존자 데이터
# image 없으면 None 가능
# --------------------
SURVIVORS = [
    {"name": "행운아", "image": None},
    {"name": "의사", "image": None},
    {"name": "변호사", "image": None},
    {"name": "도둑", "image": None},
    {"name": "정원사", "image": None},
    {"name": "마술사", "image": None},
    {"name": "모험가", "image": None},
    {"name": "용병", "image": None},
    {"name": "공군", "image": None},
    {"name": "기계공", "image": None},
    {"name": "포워드", "image": None},
    {"name": "맹인", "image": None},
    {"name": "조향사", "image": None},
    {"name": "카우보이", "image": None},
    {"name": "무희", "image": None},
    {"name": "선지자", "image": None},
    {"name": "납관사", "image": None},
    {"name": "탐사원", "image": None},
    {"name": "주술사", "image": None},
    {"name": "야만인", "image": None},
    {"name": "곡예사", "image": None},
    {"name": "항해사", "image": None},
    {"name": "바텐더", "image": None},
    {"name": "우편 배달부", "image": None},
    {"name": "묘지기", "image": None},
    {"name": "죄수", "image": None},
    {"name": "곤충학자", "image": None},
    {"name": "화가", "image": None},
    {"name": "타자", "image": None},
    {"name": "장난감 상인", "image": None},
    {"name": "심리학자", "image": None},
    {"name": "환자", "image": None},
    {"name": "소설가", "image": None},
    {"name": "여자아이", "image": None},
    {"name": "우는 광대", "image": None},
    {"name": "교수", "image": None},
    {"name": "골동품 상인", "image": None},
    {"name": "작곡가", "image": None},
    {"name": "기자", "image": None},
    {"name": "항공 전문가", "image": None},
    {"name": "치어리더", "image": None},
    {"name": "인형사", "image": None},
    {"name": "화재조사관", "image": None},
    {"name": "파로 부인", "image": None},
    {"name": "기사", "image": None},
    {"name": "기상학자", "image": None},
    {"name": "궁수", "image": None},
    {"name": "탈출 마스터", "image": None},
    {"name": "환등사", "image": None},
]

HUNTERS = [
    {"name": "공장장", "image": None},
    {"name": "광대", "image": None},
    {"name": "사냥터지기", "image": None},
    {"name": "리퍼", "image": None},
    {"name": "거미", "image": None},
    {"name": "붉은 나비", "image": None},
    {"name": "노란 옷의 왕", "image": None},
    {"name": "우산의 영혼", "image": None},
    {"name": "사진사", "image": None},
    {"name": "광기의 눈", "image": None},
    {"name": "꿈의 마녀", "image": None},
    {"name": "울보", "image": None},
    {"name": "재앙의 도마뱀", "image": None},
    {"name": "블러디 퀸", "image": None},
    {"name": "수위 26호", "image": None},
    {"name": "사도", "image": None},
    {"name": "바이올리니스트", "image": None},
    {"name": "조각가", "image": None},
    {"name": "박사", "image": None},
    {"name": "파멸의 바퀴", "image": None},
    {"name": "나이아스", "image": None},
    {"name": "밀랍인형사", "image": None},
    {"name": "악몽", "image": None},
    {"name": "서기관", "image": None},
    {"name": "은둔자", "image": None},
    {"name": "나이트 워치", "image": None},
    {"name": "오페라 가수", "image": None},
    {"name": "파이라이트", "image": None},
    {"name": "시공의 그림자", "image": None},
    {"name": "절름발이 판", "image": None},
    {"name": "훌라발루", "image": None},
    {"name": "잡화상", "image": None},
    {"name": "당구 선수", "image": None},
    {"name": "여왕벌", "image": None},
]

PERSONA = ["3시", "6시", "9시", "12시"]

# --------------------
# 임베드 함수
# --------------------
def single_embed(title, char, color):
    embed = discord.Embed(
        title=title,
        description=f"**{char['name']}**",
        color=color
    )
    embed.set_image(url=char["image"] or DEFAULT_IMAGE)
    return embed


def four_embed(chars):
    names = " / ".join(c["name"] for c in chars)
    embed = discord.Embed(
        title="👥 4인 생존자 추천",
        description=f"**{names}**",
        color=0x57F287
    )
    embed.set_image(url=chars[0]["image"] or DEFAULT_IMAGE)
    return embed


def persona_embed(picks):
    embed = discord.Embed(
        title="⭐ 추천 인격",
        description=f"**{picks[0]} / {picks[1]}**",
        color=0x5865F2
    )
    embed.set_footer(text="3·6·9·12시 중 랜덤 2개")
    return embed

# --------------------
# 다시 추천 버튼
# --------------------
class RerollView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔁 다시 추천", style=discord.ButtonStyle.primary)
    async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
        picks = random.sample(SURVIVORS, 4)
        await interaction.response.edit_message(
            embed=four_embed(picks),
            view=self
        )
# --------------------
# 슬래시 명령어
# --------------------
@bot.tree.command(
    name="생존자",
    description="생존자 캐릭터 1명 랜덤 추천"
)
async def survivor(interaction: discord.Interaction):
    char = random.choice(SURVIVORS)
    await interaction.response.send_message(
        embed=single_embed("🎲 생존자 추천", char, 0x4CAF50)
    )


@bot.tree.command(
    name="감시자",
    description="감시자 캐릭터 1명 랜덤 추천"
)
async def hunter(interaction: discord.Interaction):
    char = random.choice(HUNTERS)
    await interaction.response.send_message(
        embed=single_embed("🔪 감시자 추천", char, 0xE53935)
    )


@bot.tree.command(
    name="파티",
    description="생존자 4인 파티 추천"
)
async def party(interaction: discord.Interaction):
    picks = random.sample(SURVIVORS, 4)
    await interaction.response.send_message(
        embed=four_embed(picks),
        view=RerollView()
    )


@bot.tree.command(
    name="인격",
    description="인격 2개 랜덤 추천"
)
async def persona(interaction: discord.Interaction):
    picks = random.sample(PERSONA, 2)
    picks.sort(key=lambda x: int(x.replace("시", "")))
    await interaction.response.send_message(
        embed=persona_embed(picks)
    )


@bot.tree.command(
    name="추천",
    description="생존자 + 인격 종합 추천"
)
async def recommend(interaction: discord.Interaction):
    char = random.choice(SURVIVORS)
    persona = random.sample(PERSONA, 2)
    persona.sort(key=lambda x: int(x.replace("시", "")))

    embed = discord.Embed(
        title="🎯 오늘의 추천",
        color=0x57F287
    )
    embed.add_field(name="👤 생존자", value=f"**{char['name']}**", inline=False)
    embed.add_field(name="⭐ 인격", value=f"**{persona[0]} / {persona[1]}**", inline=False)
    embed.set_image(url=char["image"] or DEFAULT_IMAGE)

    await interaction.response.send_message(embed=embed)

# --------------------
# 봇 준비
# --------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("제5인격 캐릭터 추천")
    )
    print(f"봇 로그인 완료: {bot.user}")

# --------------------
# 실행
# --------------------
bot.run(os.environ["DISCORD_TOKEN"])
