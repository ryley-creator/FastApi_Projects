from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, String,Integer,ForeignKey,Column,Float,Table
from .database import Base
from sqlalchemy.sql.sqltypes import DATE,TIMESTAMP
from datetime import datetime,timezone

    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(45), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    country = Column(String(45), nullable=False)
    password = Column(String(10000), nullable=False)
    role = Column(String(10), nullable=False)
    participants = relationship('Participant', back_populates='user')

class Tournament(Base):
    __tablename__ = 'tournaments'
    tournament_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tournament_name = Column(String(45), nullable=False, unique=True)
    rounds = Column(Integer,nullable=False)
    current_round = Column(Integer,nullable=False)
    participants = relationship('Participant', back_populates='tournament')
    pairings = relationship('Pairings', back_populates='tournament')
    
    

class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.tournament_id', ondelete='CASCADE'))
    tournament = relationship('Tournament', back_populates='participants')
    user = relationship('User', back_populates='participants')


class Pairings(Base):
    __tablename__ = 'pairings'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.tournament_id', ondelete='CASCADE'))
    first_participant = Column(Integer, ForeignKey('participant.id', ondelete='CASCADE'), nullable=False)
    second_participant = Column(Integer, ForeignKey('participant.id', ondelete='CASCADE'), nullable=False)
    tournament = relationship('Tournament', back_populates='pairings')     



class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.tournament_id'), nullable=False)
    first_participant = Column(Integer, ForeignKey('participant.id'), nullable=False)
    second_participant = Column(Integer, ForeignKey('participant.id'), nullable=False)
    winner_id = Column(Integer, ForeignKey('participant.id'), nullable=True)
    score = Column(String(10), nullable=False)
    date = Column(DateTime, nullable=False)
    # first_participant = relationship("Participant", foreign_keys=[first_participant])
    # second_participant = relationship("Participant", foreign_keys=[second_participant])
    winner = relationship("Participant", foreign_keys=[winner_id])


class LeaderBoard(Base):
    __tablename__ = 'leaderboard'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.tournament_id', ondelete='CASCADE'))
    participant_id = Column(Integer, ForeignKey('participant.id'), nullable=False)
    points = Column(Integer,nullable=False)

class PairingHistory(Base):
    __tablename__ = 'pairing_history'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.tournament_id', ondelete='CASCADE'))
    first_participant = Column(Integer, ForeignKey('participant.id'), nullable=False)
    second_participant = Column(Integer, ForeignKey('participant.id'), nullable=False)
    




    







 

    