import vote
import pymysql
import file_IO
import bdb_config


def web_vote():
    db = pymysql.connect(bdb_config.mysql_host, bdb_config.mysql_user,
                         bdb_config.mysql_pw, bdb_config.mysql_bdname)
    cursor = db.cursor()
    cursor.execute("""select * from voter""")
    voter_ids = [b for a, b in cursor.fetchall()]
    ballot = file_IO.read_txt_file("ballot.txt")
    vote.all_in_one(ballot[0], ballot[1], voter_ids)
    db.close()


web_vote()
