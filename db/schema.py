# -*- coding: utf-8 -*-
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, \
Numeric, SmallInteger, String, Text, text, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Index
from sqlalchemy.pool import NullPool


Base = declarative_base()
metadata = Base.metadata


class Db():

    def __init__(self, host, db, username, password, socket=None, port=None):
        self.host = host
        self.db = db
        self.username = username
        self.password = password
        self.port = port
        self.socket = socket
        self.db_uri = self.get_connection_uri()
        self.engine = self.get_engine()
        self.db_session = self.get_db_session()
        '''
        virtuals db configs
        '''
        self.host_vt = host
        self.db_vt = db
        self.username_vt = username
        self.password_vt = password
        self.db_vt_uri = self.get_vt_connection_uri()
        self.engine_vt = self.get_vt_engine()
        self.db_vt_session = self.get_vt_db_session()
        

    def get_connection_uri(self):
        return "mysql+pymysql://{username}:{password}@{host}/{db}?charset=utf8&use_unicode=0".format(
                username = self.username,
                password = self.password,
                host = self.host,
                db = self.db,
                #socket=self.socket
            )

    def get_engine(self):
        return create_engine(self.db_uri, poolclass=NullPool)

    def get_db_session(self):
        return scoped_session(
                sessionmaker(autocommit=False,
                    autoflush=True,
                    bind=self.engine)
            )

    def get_session(self):
        return self.db_session

    def close(self):
        try:
            self.db_session.remove()
            self.engine.dispose()
        except:
            pass
        
    '''
    virtuals db uri
    '''
        
    def get_vt_connection_uri(self):
        return "mysql+pymysql://{username_vt}:{password_vt}@{host_vt}/{db_vt}?charset=utf8&use_unicode=0".format(
                username_vt = self.username_vt,
                password_vt = self.password_vt,
                host_vt = self.host_vt,
                db_vt = self.db_vt,
                #socket=self.socket
            )

    def get_vt_engine(self):
        return create_engine(self.db_vt_uri, poolclass=NullPool)

    def get_vt_db_session(self):
        return scoped_session(
                sessionmaker(autocommit=False,
                    autoflush=True,
                    bind=self.engine_vt)
            )

    def get_vt_session(self):
        return self.db_vt_session

    def close_vt(self):
        try:
            self.db_vt_session.remove()
            self.engine_vt.dispose()
        except:
            pass
        
metadata = Base.metadata


class AccountFreeze(Base):
    __tablename__ = 'account_freeze'
    __table_args__ = (
        Index('msisdn_status', 'msisdn', 'status', unique=True),
    )

    account_freeze_id = Column(BigInteger, primary_key=True)
    msisdn = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Bb(Base):
    __tablename__ = 'bb'

    bet_id = Column(Integer, primary_key=True)
    profile_id = Column(BigInteger, nullable=False, index=True)
    bet_message = Column(String(200), nullable=False)
    total_odd = Column(Numeric(10, 2), nullable=False)
    bet_amount = Column(Numeric(10, 2), nullable=False)
    possible_win = Column(Numeric(10, 2), nullable=False)
    status = Column(SmallInteger, nullable=False)
    win = Column(Integer, nullable=False, server_default=text("'0'"))
    reference = Column(String(70), nullable=False, index=True)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)


class Bet(Base):
    __tablename__ = 'bet'

    bet_id = Column(Integer, primary_key=True)
    profile_id = Column(ForeignKey(u'profile.profile_id'), nullable=False, index=True)
    bet_message = Column(String(200), nullable=False)
    total_odd = Column(Numeric(10, 2), nullable=False)
    bet_amount = Column(Numeric(10, 2), nullable=False)
    possible_win = Column(Numeric(10, 2), nullable=False)
    status = Column(SmallInteger, nullable=False)
    win = Column(Integer, nullable=False, server_default=text("'0'"))
    reference = Column(String(70), nullable=False, index=True)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, nullable=False)

    profile = relationship(u'Profile')


class BetDiscount(Base):
    __tablename__ = 'bet_discount'

    bet_discount_id = Column(BigInteger, primary_key=True)
    bet_id = Column(BigInteger, nullable=False, unique=True)
    discount_amount = Column(Numeric(10, 2), nullable=False)
    ratio = Column(Numeric(10, 2), nullable=False)
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class BetSlip(Base):
    __tablename__ = 'bet_slip'

    bet_slip_id = Column(Integer, primary_key=True)
    parent_match_id = Column(ForeignKey(u'match.parent_match_id'), nullable=False, index=True)
    bet_id = Column(ForeignKey(u'bet.bet_id'), nullable=False, index=True)
    bet_pick = Column(String(20), nullable=False, index=True)
    special_bet_value = Column(String(20), nullable=False, server_default=text("''"))
    total_games = Column(Integer, nullable=False)
    odd_value = Column(Numeric(10, 2), nullable=False)
    win = Column(Integer, nullable=False)
    live_bet = Column(SmallInteger, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer, nullable=False)
    sub_type_id = Column(Integer, nullable=False)
    outcome_id = Column(String(200), nullable=False, server_default=text("'-1'"))

    bet = relationship(u'Bet')
    parent_match = relationship(u'Match')


class BetSlipTemp(Base):
    __tablename__ = 'bet_slip_temp'

    bet_slip_id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, nullable=False)
    bet_pick = Column(String(20), nullable=False)
    reference_id = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    sub_type_id = Column(Integer)
    special_bet_value = Column(String(20), nullable=False, server_default=text("''"))


class BonusBet(Base):
    __tablename__ = 'bonus_bet'

    bonus_bet_id = Column(Integer, primary_key=True)
    bet_id = Column(ForeignKey(u'bet.bet_id'), nullable=False, index=True)
    bet_amount = Column(Numeric(10, 2), nullable=False)
    possible_win = Column(Numeric(10, 2), nullable=False)
    profile_bonus_id = Column(ForeignKey(u'profile_bonus.profile_bonus_id'), nullable=False, index=True)
    won = Column(Integer, nullable=False, server_default=text("'0'"))
    ratio = Column(Numeric(10, 2), nullable=False)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    bet = relationship(u'Bet')
    profile_bonus = relationship(u'ProfileBonu')


class BonusBetCount(Base):
    __tablename__ = 'bonus_bet_count'

    bonus_bet_count_id = Column(Integer, primary_key=True)
    profile_bonus_id = Column(ForeignKey(u'profile_bonus.profile_bonus_id'), nullable=False, index=True)
    profile_id = Column(ForeignKey(u'profile.profile_id'), nullable=False, index=True)
    num_bets = Column(Integer, nullable=False)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    profile_bonus = relationship(u'ProfileBonu')
    profile = relationship(u'Profile')


class BonusTrx(Base):
    __tablename__ = 'bonus_trx'
    __table_args__ = (
        Index('profile_id_reference_iscredit', 'profile_id', 'reference', 'iscredit', unique=True),
    )

    id = Column(Integer, primary_key=True)
    profile_id = Column(BigInteger, nullable=False, index=True)
    profile_bonus_id = Column(Integer, nullable=False)
    account = Column(String(50), nullable=False)
    iscredit = Column(SmallInteger, nullable=False)
    reference = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 0), nullable=False)
    created_by = Column(String(60), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Competition(Base):
    __tablename__ = 'competition'
    __table_args__ = (
        Index('competition_name_category_sport_id', 'competition_name', 'category', 'sport_id', unique=True),
    )

    competition_id = Column(Integer, primary_key=True)
    competition_name = Column(String(120), nullable=False)
    category = Column(String(120), nullable=False)
    status = Column(SmallInteger, nullable=False)
    sport_id = Column(ForeignKey(u'sport.sport_id'), nullable=False, index=True)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    priority = Column(Integer, server_default=text("'0'"))
    max_stake = Column(Numeric(10, 2))

    sport = relationship(u'Sport')


class DeliveryReport(Base):
    __tablename__ = 'delivery_report'
    __table_args__ = (
        Index('correlator_msisdn', 'correlator', 'msisdn', unique=True),
    )

    delivery_report_id = Column(BigInteger, primary_key=True)
    msisdn = Column(String(50), nullable=False)
    correlator = Column(String(70), nullable=False)
    no_of_retry = Column(Integer, nullable=False, server_default=text("'0'"))
    status = Column(String(200), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Event(Base):
    __tablename__ = 'event'

    match_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, nullable=False, unique=True)
    home_team = Column(String(50), nullable=False)
    away_team = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    game_id = Column(String(6), nullable=False, unique=True)
    competition_id = Column(Integer, nullable=False, index=True)
    status = Column(Integer, nullable=False)
    bet_closure = Column(DateTime, nullable=False)
    created_by = Column(String(60), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    result = Column(String(45))
    ht_score = Column(String(5))
    ft_score = Column(String(5))
    completed = Column(Integer, server_default=text("'0'"))
    priority = Column(Integer, server_default=text("'50'"))


class EventOdd(Base):
    __tablename__ = 'event_odd'
    __table_args__ = (
        Index('parent_match_id_sub_type_id_odd_key', 'parent_match_id', 'sub_type_id', 'odd_key', 'special_bet_value', unique=True),
    )

    event_odd_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, index=True)
    sub_type_id = Column(Integer, index=True)
    max_bet = Column(Numeric(10, 0), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    odd_key = Column(String(20), nullable=False)
    odd_value = Column(String(20))
    odd_alias = Column(String(20))
    special_bet_value = Column(String(20), nullable=False, server_default=text("''"))


class EventOddO(Base):
    __tablename__ = 'event_odd_o'

    event_odd_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, index=True)
    sub_type_id = Column(Integer, index=True)
    max_bet = Column(Numeric(10, 0), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    odd_key = Column(String(20), nullable=False)
    odd_value = Column(String(20))
    odd_alias = Column(String(20))
    special_bet_value = Column(String(20), nullable=False, server_default=text("'-1'"))


class EventOddOld(Base):
    __tablename__ = 'event_odd_old'

    event_odd_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, index=True)
    sub_type_id = Column(Integer, index=True)
    max_bet = Column(Numeric(10, 0), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    odd_key = Column(String(20), nullable=False)
    odd_value = Column(String(20))
    odd_alias = Column(String(20))


class GameRequest(Base):
    __tablename__ = 'game_request'

    request_id = Column(Integer, primary_key=True)
    match_id = Column(Integer, nullable=False)
    profile_id = Column(Integer, nullable=False)
    offset = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Inbox(Base):
    __tablename__ = 'inbox'

    inbox_id = Column(Integer, primary_key=True)
    network = Column(String(50))
    shortcode = Column(Integer)
    msisdn = Column(String(20))
    message = Column(String(300))
    linkid = Column(String(100))
    created = Column(DateTime)
    modified = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created_by = Column(String(45))

class JackpotBet(Base):
    __tablename__ = 'jackpot_bet'

    jackpot_bet_id = Column(BigInteger, primary_key=True)
    bet_id = Column(ForeignKey(u'bet.bet_id'), nullable=False, index=True)
    jackpot_event_id = Column(ForeignKey(u'jackpot_event.jackpot_event_id'), nullable=False, index=True)
    status = Column(Enum(u'ACTIVE', u'CANCELLED', u'FINISHED'), nullable=False, server_default=text("'ACTIVE'"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    bet = relationship(u'Bet')
    jackpot_event = relationship(u'JackpotEvent')


class JackpotEvent(Base):
    __tablename__ = 'jackpot_event'

    jackpot_event_id = Column(BigInteger, primary_key=True)
    jackpot_type = Column(ForeignKey(u'jackpot_type.jackpot_type_id'), nullable=False, index=True)
    jackpot_name = Column(String(250), nullable=False, unique=True)
    jp_key = Column(String(10), nullable=False)
    created_by = Column(String(70), nullable=False)
    status = Column(Enum(u'CANCELLED', u'ACTIVE', u'INACTIVE', u'SUSPENDED', u'FINISHED', u'OTHER'), server_default=text("'INACTIVE'"))
    bet_amount = Column(Numeric(10, 2), nullable=False)
    jackpot_amount = Column(Numeric(10, 2), nullable=False)
    total_games = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    jackpot_type1 = relationship(u'JackpotType')


class JackpotMatch(Base):
    __tablename__ = 'jackpot_match'

    jackpot_match_id = Column(BigInteger, primary_key=True)
    parent_match_id = Column(BigInteger, nullable=False, unique=True)
    jackpot_event_id = Column(Integer, nullable=False)
    game_order = Column(Integer, nullable=False)
    status = Column(Enum(u'CANCELLED', u'POSTPONED', u'ACTIVE'), nullable=False, server_default=text("'ACTIVE'"))
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class JackpotTrx(Base):
    __tablename__ = 'jackpot_trx'

    jackpot_trx_id = Column(BigInteger, primary_key=True)
    trx_id = Column(ForeignKey(u'transaction.id'), nullable=False, index=True)
    jackpot_event_id = Column(ForeignKey(u'jackpot_event.jackpot_event_id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    jackpot_event = relationship(u'JackpotEvent')
    trx = relationship(u'Transaction')


class JackpotType(Base):
    __tablename__ = 'jackpot_type'

    jackpot_type_id = Column(BigInteger, primary_key=True)
    sub_type_id = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False, unique=True)


class JackpotWinner(Base):
    __tablename__ = 'jackpot_winner'

    jackpot_winner_id = Column(BigInteger, primary_key=True)
    win_amount = Column(Integer, nullable=False)
    bet_id = Column(ForeignKey(u'bet.bet_id'), nullable=False, index=True)
    jackpot_event_id = Column(ForeignKey(u'jackpot_event.jackpot_event_id'), nullable=False, index=True)
    total_games_correct = Column(Integer, nullable=False)
    created_by = Column(String(70), nullable=False)
    status = Column(Integer, server_default=text("'1'"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    bet = relationship(u'Bet')
    jackpot_event = relationship(u'JackpotEvent')


class JackpotRedeem(Base):
    __tablename__ = 'jackpot_redeem'

    jackpot_redeem_id = Column(BigInteger, primary_key=True)
    bet_id = Column(Integer, nullable=False)
    jackpot_bet_id = Column(Integer, nullable=False)
    jackpot_event_id = Column(Integer, nullable=False)
    redeem_code = Column(String(30), nullable=False, unique=True)
    created_by = Column(String(120), nullable=False)
    msisdn = Column(String(30))
    profile_id = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class JackpotRedeemTrx(Base):
    __tablename__ = 'jackpot_redeem_trx'
    __table_args__ = (
        Index('reference_profile_id', 'reference', 'profile_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    transaction_id = Column(BigInteger, nullable=False, index=True)
    profile_id = Column(Integer, nullable=False)
    msisdn = Column(String(30))
    jackpot_redeem_id = Column(ForeignKey(u'jackpot_redeem.jackpot_redeem_id'), nullable=False, index=True)
    reference = Column(String(200), nullable=False, unique=True)
    created_by = Column(String(120), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    jackpot_redeem = relationship(u'JackpotRedeem')


class LiveOddsChange(Base):
    __tablename__ = 'live_odds_change'
    __table_args__ = (
        Index('parent_match_id_subtype_key', 'parent_match_id', 'subtype', 'key', unique=True),
    )

    live_odds_change_id = Column(BigInteger, primary_key=True)
    parent_match_id = Column(BigInteger, nullable=False, index=True)
    subtype = Column(String, nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    match_time = Column(String, nullable=False)
    score = Column(String, nullable=False)
    bet_status = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class LiveMatch(Base):
    __tablename__ = 'live_match'

    match_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, nullable=False, unique=True)
    home_team = Column(String(50), nullable=False)
    away_team = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    game_id = Column(String(20), nullable=False, unique=True)
    competition_id = Column(Integer, nullable=False, index=True)
    status = Column(Integer, nullable=False)
    instance_id = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    bet_closure = Column(DateTime, nullable=False)
    created_by = Column(String(60), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    result = Column(String(45))
    ht_score = Column(String(5))
    ft_score = Column(String(5))
    completed = Column(Integer, server_default=text("'0'"))
    priority = Column(Integer, server_default=text("'50'"))


class LiveOdds(Base):
    __tablename__ = 'live_odds'
    __table_args__ = (
        Index('sub_type_ids', 'parent_match_id', 'sub_type_id', 'odd_key', 'special_bet_value', unique=True),
    )

    live_odds_change_id = Column(BigInteger, primary_key=True)
    parent_match_id = Column(BigInteger, nullable=False, index=True)
    sub_type_id = Column(Integer, nullable=False, index=True)
    odd_key = Column(String(20), nullable=False, index=True)
    odd_value = Column(String(20), nullable=False)
    special_bet_value = Column(String(20))
    match_time = Column(String, nullable=False)
    score = Column(String, nullable=False)
    bet_status = Column(String, nullable=False)
    active = Column(Integer, nullable=False, server_default=text("'0'"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    sequence_no = Column(BigInteger, nullable=False, server_default=text("'0'"))
    betradar_timestamp = Column(DateTime, nullable=False)


class LiveOddsMeta(Base):
    __tablename__ = 'live_odds_meta'

    live_odds_meta_id = Column(BigInteger, primary_key=True)
    parent_match_id = Column(BigInteger, nullable=False, unique=True)
    match_time = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    score = Column(String(60))
    bet_status = Column(String(60), index=True)
    match_status = Column(String(20))
    event_status = Column(String(60), index=True)
    active = Column(Integer, nullable=False, server_default=text("'0'"))
    sequence_no = Column(BigInteger, nullable=False, index=True, server_default=text("'0'"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    betradar_timestamp = Column(DateTime, nullable=False, index=True)


class Match(Base):
    __tablename__ = 'match'

    match_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, nullable=False, unique=True)
    home_team = Column(String(50), nullable=False)
    away_team = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    game_id = Column(String(6), nullable=False, unique=True)
    competition_id = Column(ForeignKey(u'competition.competition_id'), nullable=False, index=True)
    status = Column(Integer, nullable=False)
    bet_closure = Column(DateTime, nullable=False)
    created_by = Column(String(60), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    result = Column(String(45))
    ht_score = Column(String(5))
    ft_score = Column(String(5))
    completed = Column(Integer, server_default=text("'0'"))
    priority = Column(Integer, server_default=text("'50'"))

    competition = relationship(u'Competition')


class UofMatch(Base):
    __tablename__ = 'uof_match'

    match_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, nullable=False, unique=True)
    home_team = Column(String(50), nullable=False)
    away_team = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    game_id = Column(String(20), nullable=False, unique=True)
    competition_id = Column(ForeignKey(u'competition.competition_id'), nullable=False, index=True)
    status = Column(Integer, nullable=False)
    instance_id = Column(Integer, nullable=False)
    bet_closure = Column(DateTime, nullable=False)
    created_by = Column(String(60), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    result = Column(String(45))
    ht_score = Column(String(10))
    ft_score = Column(String(10))
    completed = Column(Integer, server_default=text("'0'"))
    priority = Column(Integer, nullable=True, server_default=text("'50'"))
    ussd_priority = Column(Integer, nullable=True)

    competition = relationship(u'Competition')


class MpesaRate(Base):
    __tablename__ = 'mpesa_rate'

    id = Column(BigInteger, primary_key=True)
    min_amount = Column(Float, nullable=False)
    max_amount = Column(Float, nullable=False)
    charge = Column(Float, nullable=False)
    created = Column(DateTime)
    updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class MpesaTransaction(Base):
    __tablename__ = 'mpesa_transaction'

    mpesa_transaction_id = Column(BigInteger, primary_key=True)
    msisdn = Column(BigInteger, nullable=False)
    transaction_time = Column(DateTime, nullable=False)
    message = Column(String(300), nullable=False)
    mpesa_customer_id = Column(String(50), nullable=False)
    account_no = Column(String(100), nullable=False)
    mpesa_code = Column(String(100), nullable=False, unique=True)
    mpesa_amt = Column(Numeric(53, 2), nullable=False)
    mpesa_sender = Column(String(100), nullable=False)
    business_number = Column(Integer, nullable=False)
    enc_params = Column(String(250))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class MtsTicketSubmit(Base):
    __tablename__ = 'mts_ticket_submit'

    mts_ticket_submit_id = Column(BigInteger, primary_key=True)
    bet_id = Column(BigInteger, nullable=False)
    mts_ticket = Column(String(200), nullable=False)
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    response = Column(String(200), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class OddHistory(Base):
    __tablename__ = 'odd_history'

    odd_history_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer)
    sub_type_id = Column(Integer)
    odd_key = Column(String(20), nullable=False)
    odd_value = Column(String(20))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class OddKeyAlia(Base):
    __tablename__ = 'odd_key_alias'

    odd_key_alias_id = Column(Integer, primary_key=True)
    sub_type_id = Column(ForeignKey(u'odd_type.sub_type_id'), nullable=False, index=True)
    odd_key = Column(String(10), nullable=False)
    odd_key_alias = Column(String(10), nullable=False)
    special_bet_value = Column(String(10), nullable=False)

    sub_type = relationship(u'OddType')


class OddType(Base):
    __tablename__ = 'odd_type'

    bet_type_id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    sub_type_id = Column(Integer, nullable=False, unique=True)
    short_name = Column(String(10), nullable=False)
    priority = Column(Integer, nullable=False, server_default=text("'0'"))


class OddsSubtype(Base):
    __tablename__ = 'odds_subtype'

    odds_subtype_id = Column(BigInteger, primary_key=True)
    sub_type_id = Column(Integer, nullable=False, unique=True, server_default=text("'0'"))
    freetext = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Outbox(Base):
    __tablename__ = 'outbox'

    outbox_id = Column(BigInteger, primary_key=True)
    shortcode = Column(Integer)
    network = Column(String(50))
    profile_id = Column(ForeignKey(u'profile.profile_id'), index=True)
    linkid = Column(String(100))
    date_created = Column(DateTime, index=True)
    date_sent = Column(DateTime)
    retry_status = Column(Integer, server_default=text("'0'"))
    modified = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    text = Column(Text)
    msisdn = Column(String(25))
    sdp_id = Column(String(100))

    profile = relationship(u'Profile')


class Outcome(Base):
    __tablename__ = 'outcome'
    __table_args__ = (
        Index('parent_match_id_sub_type_id_winning_outcome', 'parent_match_id', 'sub_type_id', 'winning_outcome', 'special_bet_value', unique=True),
    )

    match_result_id = Column(Integer, primary_key=True)
    sub_type_id = Column(Integer, nullable=False, index=True)
    parent_match_id = Column(Integer, nullable=False, index=True)
    special_bet_value = Column(String(20), nullable=False, server_default=text("''"))
    live_bet = Column(Integer, server_default=text("'0'"))
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer, server_default=text("'0'"))
    winning_outcome = Column(String(20), nullable=False, index=True)


class OutcomeO(Base):
    __tablename__ = 'outcome_o'

    match_result_id = Column(Integer, primary_key=True)
    sub_type_id = Column(Integer, nullable=False, index=True)
    parent_match_id = Column(Integer, nullable=False, index=True)
    special_bet_value = Column(String(20))
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer, server_default=text("'0'"))
    winning_outcome = Column(String(20), nullable=False, index=True)


class OutcomeOld(Base):
    __tablename__ = 'outcome_old'

    match_result_id = Column(Integer, primary_key=True)
    sub_type_id = Column(Integer, nullable=False, index=True)
    parent_match_id = Column(Integer, nullable=False, index=True)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer, server_default=text("'0'"))
    winning_outcome = Column(String(20), nullable=False)


class Profile(Base):
    __tablename__ = 'profile'

    profile_id = Column(BigInteger, primary_key=True)
    msisdn = Column(String(45), unique=True)
    created = Column(DateTime)
    status = Column(SmallInteger)
    modified = Column(DateTime)
    created_by = Column(String(45))
    network = Column(String(50))


class ProfileBalance(Base):
    __tablename__ = 'profile_balance'

    profile_balance_id = Column(Integer, primary_key=True)
    profile_id = Column(ForeignKey(u'profile.profile_id'), nullable=False, unique=True)
    balance = Column(Numeric(10, 2), nullable=False)
    transaction_id = Column(BigInteger, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    bonus_balance = Column(Numeric(10, 2), server_default=text("'0.00'"))

    profile = relationship(u'Profile')


class ProfileBalanceOld(Base):
    __tablename__ = 'profile_balance_old'

    profile_balance_id = Column(Integer, primary_key=True)
    profile_id = Column(BigInteger, nullable=False, unique=True)
    balance = Column(Numeric(10, 2), nullable=False)
    transaction_id = Column(BigInteger, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    bonus_balance = Column(Numeric(10, 2), server_default=text("'0.00'"))


class ProfileBonu(Base):
    __tablename__ = 'profile_bonus'

    profile_bonus_id = Column(Integer, primary_key=True)
    profile_id = Column(ForeignKey(u'profile.profile_id'), nullable=False, index=True)
    referred_msisdn = Column(String(25), nullable=False)
    bonus_amount = Column(Numeric(10, 2), nullable=False, server_default=text("'0.00'"))
    status = Column(Enum(u'NEW', u'CLAIMED', u'EXPIRED', u'CANCELLED'), nullable=False, server_default=text("'NEW'"))
    bet_on_status = Column(SmallInteger, nullable=True)
    expiry_date = Column(DateTime, nullable=False)
    date_created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(String(45), nullable=True)
    profile = relationship(u'Profile')


class ProfileSetting(Base):
    __tablename__ = 'profile_setting'

    profile_setting_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, nullable=False, unique=True)
    balance = Column(Numeric(10, 2), nullable=False)
    status = Column(Integer, nullable=False)
    verification_code = Column(Integer)
    name = Column(String(255))
    reference_id = Column(String(20))
    created = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    password = Column(Text, nullable=False)


class ProfileSettings(Base):
    __tablename__ = 'profile_settings'

    profile_setting_id = Column(BigInteger, primary_key=True)
    profile_id = Column(BigInteger, unique=True)
    balance = Column(BigInteger, server_default=text("'0'"))
    status = Column(SmallInteger, server_default=text("'0'"))
    verification_code = Column(Integer)
    name = Column(String(250))
    reference_id = Column(String(20))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    password = Column(Text, nullable=False)
    max_stake = Column(Numeric(10, 2))


class RunningBalance(Base):
    __tablename__ = 'running_balance'

    id = Column(Integer, primary_key=True)
    profile_id = Column(BigInteger, nullable=False, index=True)
    account = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 0), nullable=False)
    running_balance = Column(Numeric(10, 0), nullable=False)
    created_by = Column(String(60), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Sport(Base):
    __tablename__ = 'sport'

    sport_id = Column(Integer, primary_key=True)
    sport_name = Column(String(50), nullable=False)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Transaction(Base):
    __tablename__ = 'transaction'
    __table_args__ = (
        Index('profile_id_reference_iscredit', 'profile_id', 'reference', 'iscredit', unique=True),
    )

    id = Column(Integer, primary_key=True)
    profile_id = Column(ForeignKey(u'profile.profile_id'), nullable=False, index=True)
    account = Column(String(50), nullable=False)
    iscredit = Column(SmallInteger, nullable=False)
    reference = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 0), nullable=False)
    running_balance = Column(Numeric(10, 2))
    created_by = Column(String(60), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    profile = relationship(u'Profile')


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(20), nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    auth_key = Column(Text, nullable=False)
    password_reset_token = Column(Text, nullable=False)
    status = Column(String(5), nullable=False)
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)


class VoidBetSlip(Base):
    __tablename__ = 'void_bet_slip'

    bet_slip_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, nullable=False, index=True)
    bet_id = Column(Integer, nullable=False, index=True)
    bet_pick = Column(String(20), nullable=False, index=True)
    special_bet_value = Column(String(20), nullable=False, server_default=text("''"))
    total_games = Column(Integer, nullable=False)
    odd_value = Column(Numeric(10, 2), nullable=False)
    win = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer, nullable=False)
    sub_type_id = Column(Integer, nullable=False)


class Winner(Base):
    __tablename__ = 'winner'

    winner_id = Column(Integer, primary_key=True)
    bet_id = Column(ForeignKey(u'bet.bet_id'), nullable=False, index=True)
    bet_amount = Column(Numeric(10, 0), nullable=False)
    win_amount = Column(Numeric(10, 0), nullable=False)
    profile_id = Column(ForeignKey(u'profile.profile_id'), nullable=False, index=True)
    credit_status = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    bet = relationship(u'Bet')
    profile = relationship(u'Profile')


class Withdrawal(Base):
    __tablename__ = 'withdrawal'

    withdrawal_id = Column(Integer, primary_key=True)
    inbox_id = Column(ForeignKey(u'inbox.inbox_id'), index=True)
    msisdn = Column(String(25), nullable=False, index=True)
    raw_text = Column(String(200), nullable=False)
    amount = Column(Numeric(64, 2), nullable=False)
    reference = Column(String(50), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created_by = Column(String(45), nullable=False)
    status = Column(Enum(u'PROCESSING', u'QUEUED', u'SUCCESS', u'FAILED', u'TRX_SUCCESS', u'CANCELLED'))
    provider_reference = Column(String(250))
    number_of_sends = Column(Integer, nullable=False, server_default=text("'0'"))
    charge = Column(Float, nullable=False, server_default=text("'30'"))
    max_withdraw = Column(Float, nullable=False, server_default=text("'10000'"))
    network = Column(String(200))

    inbox = relationship(u'Inbox')


class BetikaPoint(Base):
    __tablename__ = 'betika_point'

    betika_point_id = Column(BigInteger, primary_key=True)
    profile_id = Column(BigInteger, nullable=False, unique=True)
    points = Column(Numeric(20, 2), nullable=False)
    redeemed_amount = Column(Numeric(20, 2), nullable=False)
    created_by = Column(String(200), nullable=False)
    status = Column(Enum(u'ACTIVE', u'INACTIVE', u'SUSPENDED'), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class BetikaPointBet(Base):
    __tablename__ = 'betika_point_bet'
    __table_args__ = (
        Index('bet_id_betika_point_trx_id', 'bet_id', 'betika_point_trx_id', unique=True),
    )

    betika_point_bet_id = Column(BigInteger, primary_key=True)
    bet_id = Column(BigInteger, nullable=False, unique=True)
    betika_point_trx_id = Column(ForeignKey(u'betika_point_trx.betika_point_trx_id'), nullable=False, index=True)
    points = Column(Numeric(20, 2), nullable=False)
    amount = Column(Numeric(20, 2), nullable=False)
    created_by = Column(String(200), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    betika_point_trx = relationship(u'BetikaPointTrx')


class BetikaPointTrx(Base):
    __tablename__ = 'betika_point_trx'

    betika_point_trx_id = Column(BigInteger, primary_key=True)
    trx_id = Column(BigInteger, nullable=False, unique=True)
    points = Column(Numeric(20, 2), nullable=False)
    trx_type = Column(Enum(u'CREDIT', u'DEBIT'), nullable=False)
    status = Column(Enum(u'REDEEM', u'GAIN', u'TRANSFER', u'CANCELLED'), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class ProfileMap(Base):
    __tablename__ = 'profile_map'

    profile_map_id = Column(BigInteger, primary_key=True)
    betika_profile_id = Column(BigInteger, nullable=False, unique=True)
    status = Column(SmallInteger)
    created = Column(DateTime)
    modified = Column(DateTime)
    created_by = Column(String(45))


class TransactionMap(Base):
    __tablename__ = 'transaction_map'

    transaction_map_id = Column(Integer, primary_key=True)
    betika_transaction_id = Column(Integer, nullable=False, unique=True)
    iscredit = Column(SmallInteger, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created_by = Column(String(60), nullable=False)


class SevenAggregatorRequest(Base):
    __tablename__ = 'seven_aggregator_request'

    id = Column(BigInteger, primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)
    request_name = Column(String(200), nullable=False)
    amount_small = Column(Integer, nullable=False)
    currency = Column(String(50), nullable=False)
    user = Column(String(100), nullable=False)
    payment_strategy = Column(Enum(u'strictSingle', u'flexibleMultiple'))
    transactionType = Column(Enum(u'reserveFunds', u'credit'))
    payment_id = Column(String(200), nullable=False, index=True)
    transaction_id = Column(String(200), index=True)
    source_id = Column(String(250), nullable=False)
    reference_id = Column(String(250), nullable=False)
    tp_token = Column(Text, nullable=False)
    ticket_info = Column(Text)
    security_hash = Column(String(250), nullable=False)
    club_uuid = Column(String(250), nullable=False)
    status = Column(Integer, server_default=text("'0'"))
    created_by = Column(String(200), nullable=False)
    date_created = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class CashBet(Base):
    __tablename__ = 'cash_bet'

    cash_bet_id = Column(Integer, primary_key=True)
    profile_id = Column(Integer)
    bet_id = Column(BigInteger, nullable=False)
    bet_message = Column(String, nullable=False)
    total_odd = Column(Float(10, True), nullable=False)
    bet_amount = Column(Float(10, True), nullable=False)
    possible_win = Column(Float(10, True), nullable=False)
    status = Column(SmallInteger, nullable=False, index=True, server_default=text("'1'"))
    win = Column(Integer, nullable=False)
    reference = Column(String(250))
    created_by = Column(String(250), nullable=False, index=True)
    created = Column(DateTime, nullable=False, index=True)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class CashBetSlip(Base):
    __tablename__ = 'cash_bet_slip'

    cash_bet_slip_id = Column(Integer, primary_key=True)
    parent_match_id = Column(Integer, nullable=False, index=True)
    cash_bet_id = Column(ForeignKey(u'cash_bet.cash_bet_id'), nullable=False, index=True)
    bet_pick = Column(Integer, nullable=False, index=True)
    special_bet_value = Column(String(30), nullable=False)
    total_games = Column(Integer, nullable=False)
    odd_value = Column(Float(10, True), nullable=False)
    win = Column(Integer, nullable=False)
    live_bet = Column(Integer, nullable=False, server_default=text("'0'"))
    sub_type_id = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    cash_bet = relationship(u'CashBet')


class AffiliateType(Base):
    __tablename__ = 'affiliate_type'

    affiliate_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(120), nullable=False)


class AffiliateProfile(Base):
    __tablename__ = 'affiliate_profile'

    affiliate_profile_id = Column(BigInteger, primary_key=True)
    affiliate_id = Column(String(70), nullable=False, unique=True)
    affiliate_name = Column(String(120), nullable=False)
    affiliate_type = Column(ForeignKey(u'affiliate_type.affiliate_type_id'), nullable=False, index=True)
    created_by = Column(String(120), nullable=False)
    status = Column(Integer, nullable=False)
    active = Column(SmallInteger, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    affiliate_type1 = relationship(u'AffiliateType')


class AffiliateTx(Base):
    __tablename__ = 'affiliate_tx'
    __table_args__ = (
        Index('reference_profile_id', 'reference', 'profile_id', unique=True),
    )

    affiliate_tx_id = Column(BigInteger, primary_key=True)
    affiliate_profile_id = Column(ForeignKey(u'affiliate_profile.affiliate_profile_id'), nullable=False, index=True)
    affiliate_id = Column(String(120), nullable=False)
    profile_id = Column(Integer, nullable=False)
    transaction_id = Column(BigInteger, nullable=False)
    reference = Column(String(70), nullable=False)
    transaction_type = Column(String(120), nullable=False, index=True)
    created_by = Column(String(120), nullable=False)
    affiliate_tag = Column(String(500), nullable=False, server_default=text("''''''"))
    status = Column(SmallInteger, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    affiliate_profile = relationship(u'AffiliateProfile')


class BetProfileMap(Base):
    __tablename__ = 'bet_profile_map'

    bet_profile_map_id = Column(BigInteger, primary_key=True)
    bet_id = Column(ForeignKey(u'bet.bet_id', onupdate=u'CASCADE'), nullable=False, unique=True)
    profile_id = Column(BigInteger, nullable=False, index=True)
    short_bet_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_by = Column(String(70), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    archive_status = Column(Integer, nullable=False, server_default=text("'0'"))

    bet = relationship(u'Bet')


class BetTax(Base):
    __tablename__ = 'bet_tax'

    bet_tax_id = Column(BigInteger, primary_key=True)
    bet_id = Column(ForeignKey(u'bet.bet_id'), nullable=False, unique=True)
    taxable_amount = Column(Numeric(10, 2), nullable=False)
    withheld_amount = Column(Numeric(10, 2))
    tax_rate = Column(ForeignKey(u'tax_matrix.tax_matrix_id'), nullable=False, index=True)
    new_possible_win = Column(Numeric(10, 2))
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    created_by = Column(String(200), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    archive_status = Column(Integer, nullable=False, server_default=text("'0'"))

    bet = relationship(u'Bet')
    tax_matrix = relationship(u'TaxMatrix')


class TaxMatrix(Base):
    __tablename__ = 'tax_matrix'
    __table_args__ = (
        Index('minimum_maximum', 'minimum', 'maximum', unique=True),
    )

    tax_matrix_id = Column(BigInteger, primary_key=True)
    rate = Column(Numeric(5, 2), nullable=False)
    minimum = Column(Numeric(10, 2), nullable=False)
    maximum = Column(Numeric(10, 2), nullable=False)
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    created_by = Column(String(200), nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    archive_status = Column(Integer, nullable=False, server_default=text("'0'"))


class LuckySixTax(Base):
    __tablename__ = 'lucky_six_tax'

    id = Column(Integer, primary_key=True)
    profile_id = Column(BigInteger, nullable=False)
    aggregator_id = Column(Integer, nullable=False)
    payment_id = Column(String(50), nullable=False)
    reference_id = Column(String(50), nullable=False)
    request_message = Column(Text, nullable=False)
    tax_matrix_id = Column(ForeignKey(u'tax_matrix.tax_matrix_id'), nullable=False, index=True)
    tax_amount = Column(Float(20, True), nullable=False)
    tax_rate = Column(Numeric(10, 4), nullable=False)
    status = Column(Integer, nullable=False, server_default=text("'1'"))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    tax_matrix = relationship(u'TaxMatrix')
