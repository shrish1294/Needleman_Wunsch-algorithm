import numpy as np


def create_matrix(sequence1 , sequence2):
    score_matrix = np.zeros((len(sequence1)+1,len(sequence2)+1))
    match_check_matrix = np.zeros((len(sequence1),len(sequence2)))
    return score_matrix , match_check_matrix


def fill_match_check_matrix(match_check_matrix , reward , mismatch_penalty ,sequence1 , sequence2):
    for i in range(len(sequence1)):
        for j in range(len(sequence2)):
            if sequence1[i] == sequence2[j]:
                match_check_matrix[i][j]= reward
            else:
                match_check_matrix[i][j]= mismatch_penalty
    return match_check_matrix

def fill_score_matrix(score_matrix ,match_check_matrix , gap_penalty , sequence1 , sequence2):
    for i in range(len(sequence1)+1):
        score_matrix[i][0] = i*gap_penalty
    for j in range(len(sequence2)+1):
        score_matrix[0][j] = j * gap_penalty

    for i in range(1,len(sequence1)+1):
        for j in range(1,len(sequence2)+1):
            score_matrix[i][j] = max(score_matrix[i-1][j-1]+match_check_matrix[i-1][j-1],
                                    score_matrix[i-1][j]+gap_penalty,
                                    score_matrix[i][j-1]+ gap_penalty)

    return score_matrix

def traceback(sequence1 ,sequence2, score_matrix,match_check_matrix , gap_penalty):
    aligned_1 = ""
    aligned_2 = ""

    i = len(sequence1)
    j = len(sequence2)

    while(i >0 or j >0):
        # print(i, j)
        if (i >0 and j > 0 and score_matrix[i][j] == (score_matrix[i-1][j-1]+match_check_matrix[i-1][j-1])):

            aligned_1 = sequence1[i-1] + aligned_1
            aligned_2 = sequence2[j-1] + aligned_2

            i = i - 1
            j = j - 1

        elif(i > 0 and score_matrix[i][j] == score_matrix[i-1][j] + gap_penalty):
            aligned_1 = sequence1[i-1] + aligned_1
            aligned_2 = "-" + aligned_2

            i = i -1
        else:
            aligned_1 = "-" + aligned_1
            aligned_2 = sequence2[j-1] + aligned_2
            j = j - 1


    return aligned_1 ,aligned_2

def sequence_matching(sequence1 , sequence2 , reward = 1 , mismatch_penalty = -1 , gap_penalty = -1):
    score_matrix , match_check_matrix = create_matrix(sequence1, sequence2)
    match_check_matrix = fill_match_check_matrix(match_check_matrix ,reward , mismatch_penalty , sequence1 , sequence2)
    # print('yes' , match_check_matrix)
    score_matrix = fill_score_matrix(score_matrix , match_check_matrix, gap_penalty , sequence1 , sequence2)
    aligned_1, aligned_2= traceback(sequence1 , sequence2 , score_matrix, match_check_matrix, gap_penalty)

    print(aligned_1)
    print(aligned_2)




sequence_matching('GCATGCU' , 'GATTACA')
