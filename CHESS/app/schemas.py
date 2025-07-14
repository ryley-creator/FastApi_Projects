from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional
from . import models

class UserResponse(BaseModel):
    id: int
    name: str
    country: str
    age: int
    rating: float
    role: str

    class Config:
        from_attributes = True

class Tournament(BaseModel):
    tournament_id: int
    tournament_name: str
    participants: List[UserResponse]

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id: int

class CreateUser(BaseModel):
    name: str
    password: str
    country: str
    age: int
    rating: float
    role: str

# class CreateTour(BaseModel):
#     tournament_name: str
#     participant: List[int]
#     rounds: int
#     current_round: Optional[int] = 0

class CreateTour(BaseModel):
    tournament_name: str
    participant: List[int]
    rounds: int
    current_round: Optional[int] = 0

class UpdateUser(BaseModel):
    name: str
    country: str
    age: int
    rating: float

class Pairings(BaseModel):
    # id:int
    first_participant:int
    second_participant:int

class MatchResults(BaseModel):
    first_participant_id: int
    second_participant_id: int
    winner_id: Optional[int] = None
    score: str
    date: datetime

class MatchResultUpdate(BaseModel):
    tournament_id: int
    first_participant_id: int
    second_participant_id: int
    winner_id: int
    score: str
    date: datetime

# class CreateMatch(BaseModel):
#     tournament_id:int
#     first_participant:int
#     second_participant:int
#     score:Optional[str] = '0-0'
#     winner_id:int

class CreateMatch(BaseModel):
    tournament_id: int
    first_participant: int
    second_participant: int
    # winner_id: Optional[int]
    score: str
    date: datetime

    class Config:
        from_attributes = True

class CreateLeaderBoard(BaseModel):
    player_name:str
    points:float
    rank:int
    wins:int
    draws:int
    losses:int
class UpdateLeaderBoard(CreateLeaderBoard):
    pass

class CreatePlay(BaseModel):
    current_round: int


class PairingResponse(BaseModel):
    first_participant: int
    second_participant: int

    class Config:
        from_attributes = True

class LeaderBoardResponse(BaseModel):
    participant_id: int
    points: int

    class Config:
        from_attributes = True

class TournamentResponse(BaseModel):
    tournament_id: int
    tournament_name: str
    current_round: int
    pairings: List[PairingResponse]
    leaderboard: List[LeaderBoardResponse] = []
    

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    country: str
    age: int
    rating: float
    role: str

class ParticipantResponse(BaseModel):
    user: UserResponse

class TournamentResponseGet(BaseModel):
    tournament_id: int
    tournament_name: str
    participants: List[ParticipantResponse]
    rounds: int
    current_round: int




    






