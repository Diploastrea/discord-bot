from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Member(Base):
    __tablename__ = "members"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
        "comment": "Nihilum guild applications archive"
    }

    def __init__(self, discord_name, ingame_name, comment=None):
        self.discord_name = discord_name
        self.ingame_name = ingame_name
        self.comment = comment

    discord_name = Column(String(255), primary_key=True, nullable=False, comment="Applicant's discord name")
    ingame_name = Column(String(255), nullable=False, comment="Applicant's in-game name", index=True)
    comment = Column(Text, nullable=True, comment="Optional comment")
