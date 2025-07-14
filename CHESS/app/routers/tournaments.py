import random
from fastapi import APIRouter,Depends,HTTPException,status
from pymysql import IntegrityError
from .. import database,auth,oauth2,schemas,models
from sqlalchemy.orm import Session
from typing import List
from . import user
router = APIRouter(
    prefix='/tournament',
    tags=['Tournaments']
)


@router.post('/', dependencies=[Depends(user.admin_only)])
def create_tournament(
    tournament: schemas.CreateTour, 
    db: Session = Depends(database.get_db), 
):
    num_participants = len(tournament.participant)
    if num_participants % 2 != 0:
        raise HTTPException(status_code=400, detail="The number players should be even")
    
    if tournament.rounds > num_participants - 1:
        raise HTTPException(status_code=400, detail="The number of rounds cannot be more than players")
    

    new_tour = models.Tournament(
        tournament_name=tournament.tournament_name,
        rounds=tournament.rounds,
        current_round=0
    )
    db.add(new_tour)
    db.commit()
    db.refresh(new_tour)

    participants = []
    leaderboard = []
    for participant_id in tournament.participant:
        participant = models.Participant(user_id=participant_id, tournament_id=new_tour.tournament_id)
        db.add(participant)
        db.commit() 
        db.refresh(participant)
        participants.append(participant)
        
        # Создание записей в таблице LeaderBoard с начальными значениями очков равными нулю
        new_leaderboard_entry = models.LeaderBoard(
            tournament_id=new_tour.tournament_id,
            participant_id=participant.id,
            points=0
        )
        db.add(new_leaderboard_entry)
        db.commit()
        db.refresh(new_leaderboard_entry)
        leaderboard.append(new_leaderboard_entry)

    # Создание пар
    pairings = []
    for i in range(0, len(participants), 2):
        pairing = models.Pairings(
            tournament_id=new_tour.tournament_id,
            first_participant=participants[i].id,
            second_participant=participants[i + 1].id  
        ) 
        db.add(pairing)
        pairings.append(pairing)
    db.commit()

    response = {
        'tournament_id': new_tour.tournament_id,
        'tournament_name': new_tour.tournament_name,
        'participants': [{'participant_id': p.id, 'user_id': p.user_id} for p in participants],
        'pairings': [{'first_participant': p.first_participant, 'second_participant': p.second_participant} for p in pairings],
        'rounds': new_tour.rounds,
        'current_round': 1,
        'leaderboard': [{'participant_id': l.participant_id, 'points': l.points} for l in leaderboard]
    }
    return response


@router.get('/',dependencies=[Depends(user.admin_only)])
def get_tour(db:Session=Depends(database.get_db)):
    tournament = db.query(models.Tournament).all()
    response = []
    for tour in tournament:
        participants = db.query(models.Participant).filter(models.Participant.tournament_id == tour.tournament_id)
        participant_details = []
        for participant in participants:
            user = db.query(models.Users).filter(models.Users.id == participant.user_id).first()
            user_response = schemas.UserResponse(
                id=user.id,
                name=user.name,
                country=user.country,
                age=user.age,
                rating=user.rating,
                role=user.role
            )
            participant_response = schemas.ParticipantResponse(user=user_response)
            participant_details.append(participant_response)
        tournament_response = schemas.TournamentResponseGet(
            tournament_id=tour.tournament_id,
            tournament_name=tour.tournament_name,
            participants=participant_details,
            rounds=tour.rounds,
            current_round=tour.current_round
        )
        response.append(tournament_response)
    return response




# import random
# @router.put('/play/{id}')
# def play(id: int, db: Session = Depends(database.get_db)):

#     tournament = db.query(models.Tournament).filter(models.Tournament.tournament_id == id).first()
#     if not tournament:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tournament with id {id} was not found')
    
#     if tournament.current_round >= tournament.rounds:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Rounds are over')
    
#     tournament.current_round += 1
#     db.commit()


#     participants = db.query(models.Participant).filter(models.Participant.tournament_id == id).all()

#     participant_points = {}
#     for participant in participants:
#         leaderboard_entry = db.query(models.LeaderBoard).filter(
#             models.LeaderBoard.participant_id == participant.id,
#             models.LeaderBoard.tournament_id == id
#         ).first()

#         if leaderboard_entry:
#             points = leaderboard_entry.points
#         else:
#             points = 0

#         participant_points[participant.id] = points


#     sorted_participants = sorted(participant_points.items(), key=lambda item: item[1])


#     pairings = []
#     for i in range(0, len(sorted_participants), 2):
#         first_participant_id = sorted_participants[i][0]
#         second_participant_id = sorted_participants[i + 1][0] if i + 1 < len(sorted_participants) else None

#         if second_participant_id:
#             pairing = models.Pairings(
#                 tournament_id=id,
#                 first_participant=first_participant_id,
#                 second_participant=second_participant_id
#             )
#             db.add(pairing)
#             pairings.append(pairing)


#         winner_id = random.choice([first_participant_id, second_participant_id])
#         leaderboard_entry = db.query(models.LeaderBoard).filter(
#             models.LeaderBoard.participant_id == winner_id,
#             models.LeaderBoard.tournament_id == id
#         ).first()

#         if leaderboard_entry:
#             leaderboard_entry.points += 1
#         else:
#             new_leaderboard = models.LeaderBoard(
#                 tournament_id=id,
#                 participant_id=winner_id,
#                 points=1
#             )
#             db.add(new_leaderboard)
    
#     db.commit()


#     tournament_response = schemas.TournamentResponse.model_validate(tournament)
#     tournament_response.pairings = [
#         schemas.PairingResponse(
#             first_participant=p.first_participant,
#             second_participant=p.second_participant
#         ) for p in pairings
#     ]

#     leaderboard_response = db.query(models.LeaderBoard).filter(
#         models.LeaderBoard.tournament_id == id
#     ).order_by(models.LeaderBoard.points.desc()).all()

#     tournament_response.leaderboard = [
#         schemas.LeaderBoardResponse(
#             participant_id=l.participant_id,
#             points=l.points
#         ) for l in leaderboard_response
#     ]

#     return tournament_response.model_dump()




# import random
# @router.put('/play/{id}')

# def play(id:int,db:Session=Depends(database.get_db)):
#     tournament = db.query(models.Tournament).filter(models.Tournament.tournament_id == id).first()

#     if not tournament:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Tournament with id {id} was not found')
#     if tournament.current_round >= tournament.rounds:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='rounds are over')
    
#     tournament.current_round += 1
#     db.commit()

#     participants = db.query(models.Participant).filter(models.Participant.tournament_id == id).all()

#     participant_points = {}

#     for participant in participants:
#         leaderboard_entry = db.query(models.LeaderBoard).filter(
#             models.LeaderBoard.participant_id == participant.id,
#             models.LeaderBoard.tournament_id == id).first()
#         if leaderboard_entry:
#             points = leaderboard_entry.points
#         else:
#             points = 0
#         participant_points[participant.id] = points

#     sorted_participants = sorted(participant_points.items(),key=lambda item: item[1])

#     pairing_history = set((min(p.first_participant,p.second_participant),max(p.first_participant,p.second_participant))
#                         for p in db.query(models.PairingHistory).filter(models.PairingHistory.tournament_id == id))
    
#     pairings = []
    
#     num_participants = len(sorted_participants)

#     for i in range(0,num_participants,2):
#         if i + 1 < num_participants:
#             first_participant_id = sorted_participants[i][0]
#             second_participant_id = sorted_participants[i+1][0]
#             pair = (min(first_participant_id,second_participant_id),max(first_participant_id,second_participant_id))
#         if pair not in pairing_history:
#             pairing = models.Pairings(
#                 tournament_id = id,
#                 first_participant = first_participant_id,
#                 second_participant = second_participant_id
#             )
#             db.add(pairing)
#             pairings.append(pairing)
#             new_history = models.PairingHistory(
#                 tournament_id = id,
#                 first_participant = first_participant_id,
#                 second_participant = second_participant_id
#             )
#             db.add(new_history)
    
#             winner_id = random.choice([first_participant_id,second_participant_id])

#             leaderboard_entry = db.query(models.LeaderBoard).filter(
#                 models.LeaderBoard.tournament_id == id,
#                 models.LeaderBoard.participant_id == winner_id).first()
#             if leaderboard_entry:
#                 leaderboard_entry.points += 1
#             else:
#                 new_leaderboard = models.LeaderBoard(
#                     tournament_id = id,
#                     participant_id = winner_id,
#                     points = 1
#                 )
#                 db.add(new_leaderboard)
            
#     db.commit()

#     tournament_response = schemas.TournamentResponse.model_validate(tournament)

#     tournament_response.pairings = [
#         schemas.PairingResponse(first_participant=p.first_participant,second_participant=p.second_participant)
#         for p in pairings
#     ]

#     leaderboard_order = db.query(models.LeaderBoard).filter(models.LeaderBoard.tournament_id == id).order_by(models.LeaderBoard.points.desc()).all()

#     tournament_response.leaderboard = [
#         schemas.LeaderBoardResponse(participant_id=l.participant_id,points=l.points)
#         for l in leaderboard_order
#     ]

#     return tournament_response.model_dump()


import random
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

@router.put('/play/{id}')
def play(id: int, db: Session = Depends(database.get_db)):
    # Получение турнира
    tournament = db.query(models.Tournament).filter(models.Tournament.tournament_id == id).first()

    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tournament with id {id} was not found')
    if tournament.current_round >= tournament.rounds:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Rounds are over')
    
    # Переход к следующему раунду
    tournament.current_round += 1
    db.commit()

    # Получение участников и их очков
    participants = db.query(models.Participant).filter(models.Participant.tournament_id == id).all()

    participant_points = {}
    for participant in participants:
        leaderboard_entry = db.query(models.LeaderBoard).filter(
            models.LeaderBoard.participant_id == participant.id,
            models.LeaderBoard.tournament_id == id).first()
        points = leaderboard_entry.points if leaderboard_entry else 0
        participant_points[participant.id] = points

    sorted_participants = sorted(participant_points.items(), key=lambda item: item[1], reverse=True)

    # Получение истории пар
    pairing_history = set((min(p.first_participant, p.second_participant), max(p.first_participant, p.second_participant))
                          for p in db.query(models.PairingHistory).filter(models.PairingHistory.tournament_id == id))

    # Генерация новых пар
    pairings = []
    available_participants = [p[0] for p in sorted_participants]

    # Создание новых пар
    for i in range(0, len(available_participants) - 1, 2):
        first_participant_id = available_participants[i]
        second_participant_id = available_participants[i + 1]
        pair = (min(first_participant_id, second_participant_id), max(first_participant_id, second_participant_id))
        
        # Проверяем, что пара не была использована в предыдущих раундах
        if pair not in pairing_history:
            pairing = models.Pairings(
                tournament_id=id,
                first_participant=first_participant_id,
                second_participant=second_participant_id
            )
            db.add(pairing)
            pairings.append(pairing)
            
            # Добавление пары в историю
            new_history = models.PairingHistory(
                tournament_id=id,
                first_participant=first_participant_id,
                second_participant=second_participant_id
            )
            db.add(new_history)
            
            # Выбор победителя и обновление очков
            winner_id = random.choice([first_participant_id, second_participant_id])
            leaderboard_entry = db.query(models.LeaderBoard).filter(
                models.LeaderBoard.tournament_id == id,
                models.LeaderBoard.participant_id == winner_id).first()
            if leaderboard_entry:
                leaderboard_entry.points += 1
            else:
                new_leaderboard = models.LeaderBoard(
                    tournament_id=id,
                    participant_id=winner_id,
                    points=1
                )
                db.add(new_leaderboard)
    
    # Обработка случая, когда количество участников нечетное
    if len(available_participants) % 2 != 0:
        # Допустим, последний участник может играть в следующем раунде
        remaining_participant = available_participants[-1]
        # Можно создать временную пару или назначить как "ожидающего"

    db.commit()

    # Подготовка ответа
    tournament_response = schemas.TournamentResponse.model_validate(tournament)
    tournament_response.pairings = [
        schemas.PairingResponse(first_participant=p.first_participant, second_participant=p.second_participant)
        for p in pairings
    ]

    leaderboard_order = db.query(models.LeaderBoard).filter(models.LeaderBoard.tournament_id == id).order_by(models.LeaderBoard.points.desc()).all()
    tournament_response.leaderboard = [
        schemas.LeaderBoardResponse(participant_id=l.participant_id, points=l.points)
        for l in leaderboard_order
    ]

    return tournament_response.model_dump()
    





@router.get('/pairing')

def pairing(db:Session=Depends(database.get_db)):
    pairing = db.query(models.PairingHistory).all()
    return pairing


    
        

    

       



        

        



     

    



    

    




