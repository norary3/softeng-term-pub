def read_txt_file(file_name):
    lst = []

    f = open(file_name, 'r')
    for row in f:
        row = row.replace("\n", "")
        lst.append(row)
    f.close()

    return lst


# 생성할 file이름과 list를 넣으면 list 내용을 txt 파일로 저장합니다.
def lst_to_file(file_name, lst):
    with open(file_name, mode='w') as myfile:
        myfile.write('')
    for text in lst:
        with open(file_name, mode='a') as myfile:
            myfile.write(''.join(text))
            myfile.write('\n')

    return None


# file이름과 내용을 입력하면 해당 파일의 아래에 내용이 추가됩니다.
def append_str_to_file(file_name, text):
    with open(file_name, mode='a') as myfile:
        myfile.write(''.join(text))
        myfile.write('\n')

    return None
