import logging
import time
from cryptoconditions import crypto
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.exceptions import TransportError
import bdb_config
import pymysql
import file_IO

# from bigchaindb_driver.exceptions import BigchaindbException

logging.basicConfig(level=logging.DEBUG)

bdb = BigchainDB(bdb_config.host)
delay = 1.0


# Actual Voting function with duplicate checker implemented
# Input: (str)Current voter ID/(str)current voter private key
#       /(str)candidate public key/(list)List of past verified transfer ID list
# Output: (str)Validated block id or (None)None
def transfer_ballot(voter_private_key, candidate_public_key, voter_ids):
    voter_public_key = crypto.Ed25519SigningKey(voter_private_key).get_verifying_key().encode().decode()
    for voter_id in voter_ids:
        retrieve_block = bdb.transactions.retrieve(voter_id)  # call by txid
        if retrieve_block['transaction']['fulfillments'][0]['owners_before'][0] == voter_public_key:
            # if not poll_id_check(retrieve_block, candidate_dict):
            #     # voter is trying to vote to a candidate in different poll
            #     logging.warning('Vote to different Poll Committed')
            #     return None

            # if not candidate_check(candidate_public_key, candidate_list):
            #     # Candidate is not in the list of candidates of the poll.
            #     logging.warning('Candidate is not in the poll')
            #     return None

            # if not duplicate_check(retrieve_block, verified_transfer_ids) :
            #    logging.warning('Duplicate Vote Committed')  # Duplicate vote error logging
            #    return None
            try:
                transfer_block = bdb.transactions.transfer(
                    retrieve_block,  # txid called block
                    candidate_public_key,  # asset endpoint
                    asset=retrieve_block['transaction']['asset'],  # txid called asset
                    signing_key=voter_private_key  # voter login key
                )
            except TransportError as Error:
                logging.warning('Duplicate Vote Committed')  # Duplicate vote error logging
                return None
            # log vote success
            logging.info("Transaction ID : " + transfer_block['id'] + " Voter (" +
                         retrieve_block['transaction']['fulfillments'][0]['owners_before'][0] + ")"
                         + " transferred ballot to Candidate (" + str(candidate_public_key) + ")")
            time.sleep(delay)

            return [transfer_block['id'], voter_public_key]  # return only the transfer_block_id
    logging.warning("There's no voter data on DB")
    return None


def send_ballot_to_server(lst, string):
    try:
        db = pymysql.connect("cleanvote.ciw1fnz2m9zw.ap-northeast-2.rds.amazonaws.com",
                             "cleanvote", "1234asdf", "cleanvote")
        cursor = db.cursor()
        sql = """ insert into ballot (id, voter, candidate)
                      VALUES (%s, %s, %s)"""
        try:
            cursor.execute(sql, (lst[0], lst[1], string))
            db.commit()
            db.close()
            return 1
        except Exception:
            logging.warning('dbcommit failed')
            return 0
    except Exception:
        logging.warning('dbconnect failed')
        return 0


def all_in_one(voter_private_key, candidate_public_key, voter_ids):
    id_voter = transfer_ballot(voter_private_key, candidate_public_key, voter_ids)
    if id_voter is not None:
        file_IO.lst_to_file("log.txt", [str(send_ballot_to_server(id_voter, candidate_public_key))])
    else:
        file_IO.lst_to_file("log.txt", ['0'])

# Poll Id checker
# Input: (Block)Current voter_block/(dictionary) dictionary of candidates in that poll
# Output: (boolean)TRUE: Voter is trying to vote to a candidate in sound poll.
#                  False: Voter is trying to vote to a candidate in different poll.
# def poll_id_check(voter_block, candidate_dict):
#     if voter_block['transaction']['asset']['data']['vote']['poll_id'] == candidate_dict['poll_id']:
#         return True
#     else:
#         return False


# Candidate checker
# Input: (str)Current candidate_public_key/(dictionary) dictionary of candidates in that poll
# Output: (boolean)TRUE: Candidate IS in the list of candidates of the poll.
#                  False: Candidate is NOT in the list of candidates of the poll.
# def candidate_check(candidate_public_key, candidate_list):
#    for currId in candidate_list:
#        if candidate_public_key == currId:
#            return True
#        else:
#            continue
#    return False

# Duplicate checker
# Input: (Block)Current voter_block/(list)Verified Transfer ID List
# Output: (boolean)TRUE:No Duplicate
#                  False:Duplicate found in Verified ID List
# def duplicate_check(voter_block, verified_transfer_ids):
#     if len(verified_transfer_ids) == 0:
#         return True
#     for i in range(0, len(verified_transfer_ids)):
#         transfer_block = bdb.transactions.retrieve(verified_transfer_ids[i])
#         if (transfer_block['transaction']['fulfillments'][0]['owners_before'][0]
#                 == voter_block['transaction']['fulfillments'][0]['owners_before'][0]):
#             return False
#         else:
#             continue
#     return True

# Exception Handling Not Implemented
# def transfer_ballot(voter_id, voter_private_key, candidate_public_key):
#     try:
#         retrieve_block = bdb.transactions.retrieve(voter_id)
#         transfer_block = bdb.transactions.transfer(
#             retrieve_block,
#             candidate_public_key,
#             retrieve_block['transaction']['asset'],
#             voter_private_key
#         )
#     except BigchaindbException as e:
#         print(e)
#         return None
#
#     return transfer_block['id']

##################################################################
# Version 0.1 Created by 박종훈

# import sys
# import time
# import logging
# from bigchaindb_driver import BigchainDB
# from bigchaindb.common.exceptions import KeypairMismatchException
#
# bdb = BigchainDB('http://localhost:9984/api/v1')
# logging.basicConfig(level=logging.DEBUG)
# vote = {
#     'data': {
#         'vote': {
#             'poll_id': 'abcd1234',
#         },
#     },
# }
#
# sign_key = sys.argv[1]  # 'm9DJRc7PF5aJ62fuN7kdqrD34P42cLRbDfjqB5z7cYH'
# vote_to = sys.argv[2]  # '2H33a8XNH7VXMwVNbqCWsM9dfAPrGkcNQGNvTHrA8K1p'
#
# verifying_keys = ['AMrzzErJCTEGkWuGgDGLyMdLypLJ2cdS6rK1wGUg4EfS', 'Hzsdai8iBSzWVFSpFwLGuiFapfHvtVvVENsvnKu44qpm']
#
# logging.info('Testing verifying key')
# for verifying_key in verifying_keys:
#     try:
#         creation_tx = bdb.transactions.create(verifying_key=verifying_key,
#                                               signing_key=sign_key,
#                                               asset=vote)
#         logging.info('correct verifying key')
#         time.sleep(2)
#         transfer_tx = bdb.transactions.transfer(
#             creation_tx,
#             vote_to,
#             asset=creation_tx['transaction']['asset'],
#             signing_key=sign_key,
#         )
#         logging.info('Voting complete')
#         break
#     except KeypairMismatchException as e:
#         continue
