from zipfile import ZipFile
from sklearn.feature_extraction.text import TfidfVectorizer
from tika import parser
from pathlib import Path
import re
import os
import json


def build_class_file_list(files_path, i, encoding='utf8', vectorize=True):
    temp_folder = "temp"
    # Extraindo para um diretorio
    with ZipFile(files_path, 'r') as zipObj:
        zipObj.extractall('{}/extracted_{}'.format(temp_folder, i))

    files_together = []
    files_dir = os.listdir('{}/extracted_{}'.format(temp_folder, i))

    # Checando se existen sub pastas
    folder_name = "{}/extracted_{}".format(temp_folder, i)
    for fname in files_dir:
        path = os.path.join('{}/extracted_{}'.format(temp_folder, i), fname)
        if os.path.isdir(path):
            folder_name = "{}/extracted_{}/{}".format(temp_folder, i, fname)
            break

    for file in os.listdir(folder_name):
        file_ext = os.path.splitext(file)[1]

        if (file_ext == '.pdf'):
            raw = parser.from_file(r"{}/{}".format(folder_name, file))
            content = raw['content']
            files_together.append(content)
        else:
            print('ERRO: Extensao do arquivo nao suportada!')

    if vectorize:
        files_together = text_preprocessing(files_together)
        return files_together
    else:
        return folder_name


def text_preprocessing(content):
    for item in content:
        item = re.sub('http\S+\s*', ' ', item)  # remove URLs
        item = re.sub('RT|cc', ' ', item)  # remove RT and cc
        item = re.sub('#\S+', '', item)  # remove hashtags
        item = re.sub('@\S+', '  ', item)  # remove mentions
        item = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', item)  # remove punctuations
        item = re.sub(r'[^\x00-\x7f]', r' ', item)
        item = re.sub('\s+', ' ', item)  # remove extra whitespace

    requiredText = content

    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        stop_words='english',
        max_features=1500)

    #         requiredText = [requiredText]

    word_vectorizer.fit(requiredText)
    WordFeatures = word_vectorizer.transform(requiredText)
    # print("WordFeatures.shape: {}".format(WordFeatures.shape))
    return WordFeatures


# def resume_filter(predictions_result, keyword, id, extracted_folder):
#     filtered_resumes = []
#     for pred_json in predictions_result:
#         result = json.loads(pred_json)
#         if keyword == result['cargo']:
#             filtered_resumes.append(pred_json)
#
#     # Cria novo zip contendo apenas os curriculos filtrados
#     dir_name = Path(os.path.join("temp", "{}_filtered".format(id)))
#     dir_name.mkdir(parents=True, exist_ok=True)
#
#     file_path = os.path.join("temp", "{}_filtered".format(id), "filtered_resumes_{}.zip".format(id))
#
#     array_novo_de_corno = []
#     with ZipFile(file_path, 'w') as zipObj:
#         for result_json in filtered_resumes:
#             result = json.loads(result_json)
#
#             for file in os.listdir(extracted_folder):
#                 if file == result['curriculo']:
#                     # Parsing pdf file to string
#                     raw = parser.from_file(r"{}/{}".format(extracted_folder, file))
#
#                     # Getting the RAW pdf content
#                     content = raw['content']
#
#                     # Getting the NAME from raw text
#                     name = raw["metadata"].get("title", None) or raw["metadata"]["Author"]  or raw["content"].strip().split()[0]
#
#                     # Getting the EMAIL from raw text
#                     email_matches = re.findall(r'[\w\.-]+@[\w\.-]+', raw["content"].strip())
#                     for i in email_matches:
#                         email = i
#
#                     # Getting the PHONE number from raw text
#                     phone_matches = re.findall(r"\(?\d{2,}\)?[ -]?\d{4,}[\-\s]?\d{4}", raw["content"].strip())
#                     for i in phone_matches:
#                         phone = i
#
#                     result['candidato'].append({
#                         'nome' : name,
#                         'email' : email,
#                         'phone' : phone
#                     })
#
#                     # result['nome'] = name
#                     # result['email'] = email
#                     # result['telefone'] = phone
#
#                     file_path = os.path.join(extracted_folder, file)
#                     # print("{}/{}".format(extracted_folder, file))
#                     # with open("{}/{}".format(extracted_folder, file), 'rb') as file_content:
#                     #     zipped_file.write(file_content.read())
#                     zipObj.write(file_path)
#             result_json = json.dumps(result)
#             array_novo_de_corno.append(result_json)
#             print(f'array_novo_de_corno = {array_novo_de_corno}')
#
#     # return file_path, filtered_resumes
#     return file_path, array_novo_de_corno


def resume_filter_UPDATED(predictions_result, keyword, id, extracted_folder):
    filtered_resumes = []
    for pred_json in predictions_result:
        result = json.loads(pred_json)
        if keyword == result['cargo']:
            filtered_resumes.append(pred_json)

    # Cria novo zip contendo apenas os curriculos filtrados
    dir_name = Path(os.path.join("temp", "{}_filtered".format(id)))
    dir_name.mkdir(parents=True, exist_ok=True)

    file_path = os.path.join("temp", "{}_filtered".format(id), "filtered_resumes_{}.zip".format(id))

    with ZipFile(file_path, 'w') as zipObj:
        filtered_resumes_json = []
        candidats = []
        for result_json in filtered_resumes:
            result = json.loads(result_json)
            for file in os.listdir(extracted_folder):
                if file == result['curriculo']:
                    # Parsing pdf file to string
                    raw = parser.from_file(r"{}/{}".format(extracted_folder, file))

                    # Getting the NAME from raw text
                    name = raw["metadata"].get("title", None) or raw["metadata"]["Author"] or \
                           raw["content"].strip().split()[0]

                    # Getting the EMAIL from raw text
                    email_matches = re.findall(r'[\w\.-]+@[\w\.-]+', raw["content"].strip())
                    for i in email_matches:
                        email = i

                    # Getting the PHONE number from raw text
                    phone_matches = re.findall(r"\(?\d{2,}\)?[ -]?\d{4,}[\-\s]?\d{4}", raw["content"].strip())
                    for i in phone_matches:
                        phone = i

                    user_data = {
                        "cargo": result["cargo"],
                        "curriculo": result["curriculo"],
                        "nome": name,
                        "email": email,
                        "telefone": phone
                    }

                    file_path = os.path.join(extracted_folder, file)
                    zipObj.write(file_path)
            candidats.append(user_data)
            # print("candidats: {}".format(candidats))
            # result_json = json.loads(result)
        filtered_resumes_json = {
            "candidatos": candidats
        }
        print("filtered_resumes_json: {}".format(filtered_resumes_json))
    return file_path, filtered_resumes_json
