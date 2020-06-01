let questionContainer = document.getElementsByClassName('question_container')[0],
        answerCount = document.getElementsByClassName('answer_count'),
        questionCount = document.getElementById('question_count'),
        flexRow = document.getElementById('flex_row'),
        answerList = document.getElementsByClassName('answer_list'),
        listItemAnswer = document.getElementsByClassName('li_answer')[0],
        questionNumber = document.getElementsByClassName('question_number');
        
        questionCount.addEventListener('input', function () {
            let questions = document.getElementsByClassName('question_container');
            
            if (questions.length < questionCount.value) {             
                for (let i = questions.length; i < questionCount.value; i++) {
                    createQuestion(i);
                }
            } else{
                if (questions.length > questionCount.value) {
                    for (let i = questions.length; i > questionCount.value; i--) {
                        flexRow.removeChild(flexRow.lastElementChild);
                    }
                }
            }
        });

        function initQuestions() {
            flexRow.removeChild(flexRow.lastElementChild);
            createQuestion(0);
        }
        
        initQuestions();
        
        function createQuestion(index) {
            let newQuestion = questionContainer.cloneNode(true);
            newQuestion.children[1].firstChild.name = 'question' + (index+1);
            newQuestion.getElementsByClassName('answer')[0].name = 'answer'+ (index+1) + '_1';
            newQuestion.getElementsByClassName('answer_value')[0].name = 'answer_value'+ (index+1) + '_1';
            newQuestion.getElementsByClassName('answer_count')[0].name = 'answer_count' + (index+1);
            flexRow.appendChild(newQuestion);
            createAnswer(index);
        }

        function createAnswer(index) {
            let answersInput = answerCount[index],
                answers = answerList[index],
                number = index + 1;

            questionNumber[index].innerHTML = 'Вопрос ' + number;
            answersInput.addEventListener('input', function () {
                if (answerList[index].children.length < answersInput.value) {
                    for (let i =answers.children.length; i < answersInput.value; i++) {
                        let newAnswer = listItemAnswer.cloneNode(true);
                        newAnswer.getElementsByClassName('answer')[0].name = 'answer' + number + '_' + (i+1);
                        newAnswer.getElementsByClassName('answer_value')[0].name = 'answer_value' + number + '_' + (i+1);
                        answers.appendChild(newAnswer);
                    }
                } else{
                    if (answerList[index].children.length > answersInput.value) {
                        for (let i =answers.children.length; i > answersInput.value; i--) {
                           answers.removeChild(answerList[index].lastChild);
                        }
                    }
                }
            });
        }