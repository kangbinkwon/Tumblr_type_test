from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from data_qna import qna_data, result_data


@app.route('/')
def get_main_page():
    return render_template('index.html')


@app.route('/question')
def get_question_page():
    return render_template('question.html')


@app.route('/result')
def get_result_page():
    answers = list(request.args.get('answers'))
    result_type = calc_result(answers)
    result = result_data[result_type]
    return render_template('result.html', result=result)


#유형 결과 계산
def calc_result(answers):
    all_qna = qna_data
    score_dict = dict()

    for i in range(8):
        score_dict['type'+str(i+1)] = 0

    for i in range(len(answers)):
        answer = int(answers[i])
        qna = all_qna[i]
        score = qna['a'][answer][1]

        for s in score:
            key = s
            val = score[s]
            score_dict[key] += val

    result = max(score_dict, key=score_dict.get)
    return result


# data_qna.py 데이터 가져와서 question1.html에 보여주는 api 만들기
@app.route('/qnas', methods=['GET'])
def show_qna():
    qnas = qna_data
    return jsonify({'result':'success','qna':qnas})


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000)