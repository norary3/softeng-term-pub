import user
import vote
import dashboard

voter_num = 5
candidate_num = 2
poll_id = 'kutest01'

voters = user.make_voter(voter_num, poll_id)  # create voter
candidates = user.make_candidate(candidate_num, poll_id)  # create candidate
verified_transfers = []  # empty list for handling valid transaction_id MYSQL implementation needed

# MySQL Parsing Function Implementation Needed
voter_ids = user.list_voter_ids(voters)  # (list)voter_transaction_ids
voter_private_keys = user.list_voter_private_keys(voters)  # (list)voter_signing_keys
candidate_ids = user.list_candidate_ids(candidates)  # (list)candidate_transaction_ids
candidate_public_keys = user.list_candidate_public_keys(candidates)  # (list)candidate_public_keys

# Console Print
print("voters\n" + str(voters))
print("candidates\n" + str(candidates))
print("voter_private_keys\n" + str(voter_private_keys))
print("voter_ids\n" + str(voter_ids))
print("candidate_public_keys\n" + str(candidate_public_keys))
print("candidate_ids\n" + str(candidate_ids))


# # add invalide voter and candidate for test
# poll_id2 = 'kutest02'
# voters2 = user.make_voter(1, poll_id2)  # create invalid voter
# candidates2 = user.make_candidate(1, poll_id2)  # create invalid candidate
# voter_ids.append(user.list_voter_ids(voters2)[0])  # (list)voter_transaction_ids
# voter_private_keys.append(user.list_voter_private_keys(voters2)[0])  # (list)voter_signing_keys
# candidate_ids.append(user.list_candidate_ids(candidates2)[0])  # (list)candidate_transaction_ids
# candidate_public_keys.append(user.list_candidate_public_keys(candidates2)[0])  # (list)candidate_public_keys


# Usage : Temporary vote function from index to index made just for testing purposes
# Input: (int)voter_index/(int)candidate_index/(list)verified_transfers
# Output: void
def temp_transfer_ballot(voter_index, candidate_index):
    temp = vote.transfer_ballot(voter_private_keys[voter_index],
                                candidate_public_keys[candidate_index],
                                voter_ids)
    if temp is not None:  # If Valid vote
        print("Voter #" + str(voter_index) + " transferred ballot to Candidate #" + str(candidate_index))
        verified_transfers.append(temp)
        return True
    return False  # if not Valid vote


#####################################################################
# Console Testing Area
temp_transfer_ballot(0, 0)  # Valid
temp_transfer_ballot(0, 1)  # Double Voting both sides
temp_transfer_ballot(1, 0)  # Valid
temp_transfer_ballot(1, 0)  # Double Voting
temp_transfer_ballot(1, 0)  # Double Voting
temp_transfer_ballot(1, 0)  # Double Voting
temp_transfer_ballot(2, 1)  # Valid
temp_transfer_ballot(2, 0)  # Double Voting both sides
temp_transfer_ballot(3, 1)  # Valid
temp_transfer_ballot(3, 1)  # Double Voting
# temp_transfer_ballot(4, 2)  # InValid Candidate
temp_transfer_ballot(4, 1)  # Valid
# temp_transfer_ballot(5, 0)  # Invalid Voter

#####################################################################

print(verified_transfers)  # List of verified transfers
stat = dashboard.make_statistics(verified_transfers, candidate_public_keys)  # Vote counter call
dashboard.print_statistics(stat)
