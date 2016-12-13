import pymysql
import user
import file_IO
import logging
import bdb_config

voter_num = 9
candidate_num = 3
poll_id = 'kutest01'

voters = user.make_voter(voter_num, poll_id)  # create voter
candidates = user.make_candidate(candidate_num, poll_id)  # create candidate

voter_ids = user.list_voter_ids(voters)  # (list)voter_transaction_ids
voter_private_keys = user.list_voter_private_keys(voters)  # (list)voter_signing_keys
voter_public_keys = user.list_voter_public_keys(voter_private_keys)
candidate_public_keys = user.list_candidate_public_keys(candidates)  # (list)candidate_public_keys

print("voter_public_keys\n" + str(voter_public_keys))
file_IO.lst_to_file("key.txt", voter_private_keys)
file_IO.lst_to_file("public.txt", voter_public_keys)
del voter_private_keys
for i in range(len(voter_ids)):
    try:
        db = pymysql.connect(bdb_config.mysql_host, bdb_config.mysql_user,
                             bdb_config.mysql_pw, bdb_config.mysql_bdname)
        cursor = db.cursor()
        sql = """ insert into voter (id)
                  VALUES (%s)"""
        try:
            cursor.execute(sql, voter_ids[i])
            db.commit()
            db.close()
        except Exception:
            logging.warning('dbcommit failed')

    except Exception:
        logging.warning('dbconnect failed')

for i in range(len(candidate_public_keys)):
    try:
        db = pymysql.connect(bdb_config.mysql_host, bdb_config.mysql_user,
                             bdb_config.mysql_pw, bdb_config.mysql_bdname)
        cursor = db.cursor()
        sql = """ insert into candidate (public_key)
                  VALUES (%s)"""
        try:
            cursor.execute(sql, candidate_public_keys[i])
            db.commit()
            db.close()
        except Exception:
            logging.warning('dbcommit failed')

    except Exception:
        logging.warning('dbconnect failed')
