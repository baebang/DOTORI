from flask import Blueprint, g, render_template

ranking_service = Blueprint("ranking_service", __name__)

###########################################
#
#
# 랭킹 조회 기능 구현 : 이현지
#
#
###########################################
@ranking_service.route('/ranking', methods=['GET'])
def ranking():
    # db에 저장된 명단을 가져온다
    # point 높은 순으로 정렬한다
    userslist = list(g.db.users.find({}, {'_id':False}).sort('point', -1))
    
    return render_template("ranking.html", userslist = userslist)